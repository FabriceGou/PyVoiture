
# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, jsonify, request, Blueprint

from modules.dal.categorie import create, delete
from modules.db import Session, AlchemyEncoder
from modules.db.entities import Categorie
from modules.helper import ViewHelper
from startFlask import db

categorie_page = Blueprint('categorie_page', __name__, template_folder='templates')


@categorie_page.route('/categorie')
def categorie():
    return render_template(
        'categorie.html',
        title='Gestion des catégories'
    )


@categorie_page.route('/list_categorie', methods=['POST'])
def list_categorie():
    res = Session().query(Categorie).all()
    json_data = AlchemyEncoder.to_json(res)
    return jsonify(json_data)


@categorie_page.route('/show_categorie_form')
def show_categorie_form():
    categorie_id = request.values['categorie_id']
    if categorie_id != '-1':
        c = db.session.query(Categorie).get(int(categorie_id))
    else:
        c = Categorie()
        c.categorie_id = -1

    return render_template('_categorie_form.html', categorie=c)


@categorie_page.route('/sauver_categorie', methods=['POST'])
def sauver_categorie():
    try:
        categorie_id = request.form['categorie_id']
        if categorie_id != '-1':
            c = db.session.query(Categorie).get(int(categorie_id))
        else:
            c = Categorie()

        nom = request.form['categorie']
        description = request.form['description']

        c.categorie = nom
        c.description = description

        if categorie_id == '-1':
            create(c)
        else:
            db.session.commit()

    except Exception:
        return ViewHelper.notif_error("Erreur lors de l'enregistrement")

    return categorie()


@categorie_page.route('/supprimer_categorie/<categorie_id>', methods=['DELETE'])
def supprimer_categorie(categorie_id):
    msg = delete(categorie_id)
    if msg:
        return ViewHelper.notif_warning(msg)
    else:
        return ViewHelper.notif_success("La catégorie à été supprimée")
