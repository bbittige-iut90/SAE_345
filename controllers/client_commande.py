#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = """
    SELECT jv.nom_jeux_video AS nom,lp.quantite,jv.prix_jeux_video AS prix,(lp.quantite * jv.prix_jeux_video) as prix_ligne
    FROM ligne_panier AS lp
    JOIN jeux_video AS jv ON lp.jeux_video_id = jv.id_jeux_video
    WHERE lp.utilisateur_id = %s;
    """
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    if not articles_panier:
        flash("Votre panier est vide.", "alert-warning")
        return redirect('/client/article/show')

    sql_prix_total = """
    SELECT SUM(lp.quantite * jv.prix_jeux_video) as prix_total
    FROM ligne_panier AS lp
    JOIN jeux_video AS jv ON lp.jeux_video_id = jv.id_jeux_video
    WHERE lp.utilisateur_id = %s;
    """
    mycursor.execute(sql_prix_total, (id_client,))
    prix_total = mycursor.fetchone()['prix_total']

    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql_panier = """
    SELECT jv.id_jeux_video, jv.prix_jeux_video, lp.quantite
    FROM ligne_panier AS lp
    JOIN jeux_video AS jv ON lp.jeux_video_id = jv.id_jeux_video
    WHERE lp.utilisateur_id = %s;
    """
    mycursor.execute(sql_panier, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier:
        flash("Votre panier est vide.", "alert-warning")
        return redirect('/client/article/show')

    sql_create_commande = "INSERT INTO commande(date_commande, utilisateur_id, etat_id) VALUES (NOW(), %s, 1);"
    mycursor.execute(sql_create_commande, (id_client,))
    id_commande = mycursor.lastrowid

    for item in items_ligne_panier:
        sql_insert_ligne = "INSERT INTO ligne_commande(commande_id, jeux_video_id, prix, quantite) VALUES (%s, %s, %s, %s);"
        mycursor.execute(sql_insert_ligne, (id_commande, item['id_jeux_video'], item['prix_jeux_video'], item['quantite']))

    sql_vider_panier = "DELETE FROM ligne_panier WHERE utilisateur_id = %s;"
    mycursor.execute(sql_vider_panier, (id_client,))

    get_db().commit()
    flash(u'Votre commande a été enregistrée avec succès.', 'alert-success')
    return redirect('/client/commande/show')

@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = """
    SELECT c.id_commande, c.date_commande AS date_achat, SUM(lc.quantite) AS nbr_articles, SUM(lc.prix * lc.quantite) AS prix_total, e.libelle_etat AS etat, c.etat_id
    FROM commande AS c
    JOIN ligne_commande AS lc ON c.id_commande = lc.commande_id
    JOIN etat AS e ON c.etat_id = e.id_etat
    WHERE c.utilisateur_id = %s
    GROUP BY c.id_commande, date_achat, e.libelle_etat, c.etat_id
    ORDER BY c.etat_id, c.date_commande DESC;
    """
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande_show = request.args.get('id_commande', None)
    if id_commande_show:
        sql_articles = """
        SELECT jv.nom_jeux_video AS nom, lc.quantite, lc.prix, (lc.prix * lc.quantite) AS prix_ligne
        FROM ligne_commande AS lc
        JOIN jeux_video AS jv ON lc.jeux_video_id = jv.id_jeux_video
        WHERE lc.commande_id = %s;
        """
        mycursor.execute(sql_articles, (id_commande_show,))
        articles_commande = mycursor.fetchall()

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )