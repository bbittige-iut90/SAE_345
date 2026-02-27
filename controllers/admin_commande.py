#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''
    SELECT id_commande, login, date_commande AS date_achat, SUM(quantite) AS nbr_articles, SUM(prix * quantite) AS prix_total, libelle_etat AS libelle, etat_id
    FROM commande
    JOIN utilisateur ON utilisateur_id = id_utilisateur
    JOIN etat ON etat_id = id_etat
    LEFT JOIN ligne_commande ON id_commande = commande_id
    GROUP BY id_commande
    ORDER BY etat_id;
    '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''
        SELECT nom_jeux_video AS nom, quantite, prix, (prix * quantite) AS prix_ligne,etat_id,id_commande AS id
        FROM ligne_commande
        JOIN jeux_video ON jeux_video_id = id_jeux_video
        JOIN commande ON commande_id = id_commande
        WHERE commande_id = %s;
        '''

        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s;'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
    return redirect('/admin/commande/show')
