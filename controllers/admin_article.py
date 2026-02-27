#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, flash
from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_jeux_video AS id_article, nom_jeux_video AS nom, prix_jeux_video AS prix, stock, photo_jeux_video AS image, libelle_type_jeux_video AS libelle, type_jeux_video_id AS type_article_id
    FROM jeux_video
    JOIN type_jeux_video ON jeux_video.type_jeux_video_id = type_jeux_video.id_type_jeux_video
    ORDER BY nom; 
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT id_type_jeux_video as id_type_article, libelle_type_jeux_video as libelleType FROM type_jeux_video;")
    types_article = mycursor.fetchall()
    mycursor.execute("SELECT id_console as id, libelle_console as libelle FROM console;")
    consoles = mycursor.fetchall()
    return render_template('admin/article/add_article.html', types_article=types_article, consoles=consoles)


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    nom = request.form.get('nom', '')
    type_id = request.form.get('type_article_id', '')
    console_id = request.form.get('console_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    photo = request.form.get('photo', '')

    message = 'Ajout d\'un article -- nom: ' + nom
    mycursor = get_db().cursor()
    tuple_param = (nom, description, prix, photo, stock, type_id, console_id)
    sql = '''
    INSERT INTO jeux_video (nom_jeux_video, description, prix_jeux_video, photo_jeux_video, stock, type_jeux_video_id, console_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s); 
    '''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete')
def delete_article():
    id_article = request.args.get('id', 0)
    mycursor = get_db().cursor()
    tuple_param = (id_article,)
    sql = '''DELETE FROM jeux_video WHERE id_jeux_video = %s;'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    flash('Suppression d\'un article -- id: ' + str(id_article), 'alert-warning')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article = request.args.get('id', 0)
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_jeux_video AS id_article, nom_jeux_video AS nom, description, prix_jeux_video AS prix,stock, photo_jeux_video AS image, type_jeux_video_id, console_id
    FROM jeux_video
    WHERE id_jeux_video = %s;
    '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()
    mycursor.execute("SELECT id_type_jeux_video as id, libelle_type_jeux_video as libelleType FROM type_jeux_video;")
    types_article = mycursor.fetchall()
    mycursor.execute("SELECT id_console as id, libelle_console as libelle FROM console;")
    consoles = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', article=article, types_article=types_article, consoles=consoles)


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    id_article = request.form.get('id')
    nom = request.form.get('nom', '')
    type_id = request.form.get('type_article_id', '')
    console_id = request.form.get('console_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    photo = request.form.get('photo', '')

    message = 'Modification d\'un article -- nom: ' + nom
    mycursor = get_db().cursor()
    tuple_param = (nom, description, prix, photo, stock, type_id, console_id, id_article)
    sql = '''
    UPDATE jeux_video
    SET nom_jeux_video  = %s, description = %s, prix_jeux_video = %s, photo_jeux_video = %s,stock = %s, type_jeux_video_id = %s, console_id = %s
    WHERE id_jeux_video = %s; 
    '''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/admin/article/show')

@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
