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
    sql = ''' selection des articles d'un panier 
    '''
    articles_panier = []
    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
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

    # choix de(s) (l')adresse(s)
    # 1. Récupérer les articles du panier de l'utilisateur
    sql = """
        SELECT jv.id_jeux_video, jv.prix_jeux_video, lp.quantite
        FROM ligne_panier AS lp
        JOIN jeux_video AS jv ON lp.jeux_video_id = jv.id_jeux_video
        WHERE lp.utilisateur_id = %s;
    """
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    id_client = session['id_user']
    sql = ''' selection du contenu du panier de l'utilisateur '''
    items_ligne_panier = []
    # if items_ligne_panier is None or len(items_ligne_panier) < 1:
    #     flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
    #     return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")
    # 2. Vérifier si le panier est vide
    if not items_ligne_panier:
        flash('Votre panier est vide, impossible de passer une commande.', 'alert-warning')
        return redirect('/client/article/show')

    sql = ''' creation de la commande '''
    # 3. Créer une nouvelle commande dans la table "commande"
    # On considère que l'état 1 correspond à "En cours de traitement"
    sql_create_commande = "INSERT INTO commande(date_commande, utilisateur_id, etat_id) VALUES (NOW(), %s, 1);"
    mycursor.execute(sql_create_commande, (id_client,))
    id_commande = mycursor.lastrowid

    sql = '''SELECT last_insert_id() as last_insert_id'''
    # numéro de la dernière commande
    # 4. Pour chaque article du panier, l'ajouter à "ligne_commande"
    for item in items_ligne_panier:
        sql = ''' suppression d'une ligne de panier '''
        sql = "  ajout d'une ligne de commande'"
        sql_insert_ligne = "INSERT INTO ligne_commande(commande_id, jeux_video_id, prix, quantite) VALUES (%s, %s, %s, %s);"
        mycursor.execute(sql_insert_ligne, (id_commande, item['id_jeux_video'], item['prix_jeux_video'], item['quantite']))

    # 5. Vider le panier de l'utilisateur
    sql_delete_panier = "DELETE FROM ligne_panier WHERE utilisateur_id = %s;"
    mycursor.execute(sql_delete_panier, (id_client,))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')
    flash('Votre commande a bien été enregistrée.', 'alert-success')
    return redirect('/client/commande/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  selection des commandes ordonnées par état puis par date d'achat descendant '''
    commandes = []

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

