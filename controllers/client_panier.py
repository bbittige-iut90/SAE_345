#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))

    # Récupérer les informations de l'article, notamment le stock
    mycursor.execute("SELECT stock, nom_jeux_video FROM jeux_video WHERE id_jeux_video = %s", (id_article,))
    article_db = mycursor.fetchone()

    # Vérifier si l'article existe
    if article_db is None:
        flash("L'article que vous essayez d'ajouter n'existe pas.", "alert-danger")
        return redirect('/client/article/show')

    # Vérifier si le stock est suffisant
    if article_db['stock'] < quantite:
        flash(f"Le stock pour l'article '{article_db['nom_jeux_video']}' est insuffisant. Il ne reste que {article_db['stock']} exemplaire(s).", "alert-warning")
        return redirect('/client/article/show')
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    # id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # ... (code declinaison commenté car non supporté par le schéma actuel) ...

# ajout dans le panier d'un article
    sql = "SELECT * FROM ligne_panier WHERE jeux_video_id = %s AND utilisateur_id = %s;"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    mycursor.execute("UPDATE jeux_video SET stock = stock - %s WHERE id_jeux_video = %s", (quantite, id_article))

    if article_panier is not None:
        print("update quantite")
        mycursor.execute("UPDATE ligne_panier SET quantite = quantite + %s WHERE jeux_video_id = %s AND utilisateur_id = %s", (quantite, id_article, id_client))
    else:
        mycursor.execute("INSERT INTO ligne_panier (utilisateur_id, jeux_video_id, quantite, date_ajout) VALUES (%s, %s, %s, NOW())", (id_client, id_article, quantite))
    get_db().commit()
    flash(f"L'article '{article_db['nom_jeux_video']}' a bien été ajouté au panier.", "alert-success")

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = "SELECT * FROM ligne_panier WHERE jeux_video_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    if article_panier is not None and article_panier['quantite'] > 1:
        sql = "UPDATE ligne_panier SET quantite = quantite - 1 WHERE jeux_video_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (id_article, id_client))
        mycursor.execute("UPDATE jeux_video SET stock = stock + 1 WHERE id_jeux_video = %s", (id_article,))
    elif article_panier is not None:
        sql = "DELETE FROM ligne_panier WHERE jeux_video_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (id_article, id_client))
        mycursor.execute("UPDATE jeux_video SET stock = stock + 1 WHERE id_jeux_video = %s", (id_article,))

    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (client_id,))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = "DELETE FROM ligne_panier WHERE jeux_video_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (item['jeux_video_id'], client_id))
        sql2 = "UPDATE jeux_video SET stock = stock + %s WHERE id_jeux_video = %s"
        mycursor.execute(sql2, (item['quantite'], item['jeux_video_id']))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_article = request.form.get('id_declinaison_article')
    id_article = request.form.get('id_article')

    sql = "SELECT * FROM ligne_panier WHERE jeux_video_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))
    item_panier = mycursor.fetchone()

    if item_panier:
        sql = "DELETE FROM ligne_panier WHERE jeux_video_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (id_article, id_client))
        sql2 = "UPDATE jeux_video SET stock = stock + %s WHERE id_jeux_video = %s"
        mycursor.execute(sql2, (item_panier['quantite'], id_article))
        get_db().commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            session['filter_word'] = filter_word
        else:
            if 'filter_word' in session:
                session.pop('filter_word')
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isnumeric():
            session['filter_prix_min'] = filter_prix_min
        if filter_prix_max.isnumeric():
            session['filter_prix_max'] = filter_prix_max
    if filter_types:
        session['filter_types'] = filter_types
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    return redirect('/client/article/show')
