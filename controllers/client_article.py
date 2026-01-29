#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' 
    SELECT id_jeux_video, nom_jeux_video AS nom, prix_jeux_video AS prix, photo_jeux_video AS photo, stock, libelle_console, libelle_type_jeux_video
    FROM jeux_video
    JOIN console ON jeux_video.console_id = console.id_console
    JOIN type_jeux_video ON jeux_video.type_jeux_video_id = type_jeux_video.id_type_jeux_video
    '''
    list_param = []
    condition_and = ""

    mycursor.execute(sql)
    articles = mycursor.fetchall()

    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''

    # pour le filtre
    sql = '''
    SELECT id_type_jeux_video AS id_type_article, libelle_type_jeux_video AS libelle
    FROM type_jeux_video
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = "SELECT id_console, libelle_console FROM console"
    mycursor.execute(sql)
    items_console = mycursor.fetchall()

    sql='''
    SELECT jeux_video.id_jeux_video, jeux_video.nom_jeux_video AS nom, jeux_video.prix_jeux_video AS prix, COUNT(ligne_panier.jeux_video_id) AS quantite, (jeux_video.prix_jeux_video * COUNT(ligne_panier.jeux_video_id)) as total_ligne
    FROM ligne_panier 
    JOIN jeux_video ON ligne_panier.jeux_video_id = jeux_video.id_jeux_video 
    WHERE ligne_panier.utilisateur_id = %s
    GROUP BY jeux_video.id_jeux_video, jeux_video.nom_jeux_video, jeux_video.prix_jeux_video;
    '''
    mycursor.execute(sql,(id_client,))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = '''
        SELECT SUM(jeux_video.prix_jeux_video) AS total
        FROM ligne_panier
        JOIN jeux_video ON ligne_panier.jeux_video_id = jeux_video.id_jeux_video
        WHERE ligne_panier.utilisateur_id = %s; '''
        mycursor.execute(sql, (id_client,))
        res = mycursor.fetchone()
        prix_total = res['total']
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           , items_console=items_console
                           )
