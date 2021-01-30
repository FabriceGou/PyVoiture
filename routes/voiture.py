
# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, jsonify, request, Blueprint

from modules.dal.voiture import create, delete
from modules.db import Session, AlchemyEncoder
from modules.db.entities import Voiture
from modules.helper import ViewHelper
from startFlask import db

voiture_page = Blueprint('voiture_page', __name__, template_folder='templates')


@voiture_page.route('/voiture')
def voiture():
    return render_template(
        'voiture.html',
        title='Gestion des voitures'
    )


@voiture_page.route('/list_voiture', methods=['POST'])
def list_voiture():
    res = Session().query(Voiture).all()
    json_data = AlchemyEncoder.to_json(res)
    return jsonify(json_data)


@voiture_page.route('/show_voiture_form')
def show_voiture_form():
    voiture_id = request.values['voiture_id']
    if voiture_id != '-1':
        voit = db.session.query(Voiture).get(int(voiture_id))
    else:
        voit = Voiture()
        voit.id = -1

    return render_template(
        '_voiture_form.html', voiture=voit
    )


@voiture_page.route('/sauver_voiture', methods=['POST'])
def sauver_voiture():
    try:
        voiture_id = request.form['voiture_id']
        if voiture_id != '-1':
            v = db.session.query(Voiture).get(int(voiture_id))
        else:
            v = Voiture()

        nom = request.form['nom']
        description = request.form['description']

        v.nom = nom
        v.description = description

        if voiture_id == '-1':
            create(v)
        else:
            db.session.commit()

    except Exception:
        return ViewHelper.notif_error("Erreur lors de l'enregistrement")

    return voiture()


@voiture_page.route('/supprimer_voiture/<voiture_id>', methods=['DELETE'])
def supprimer_voiture(voiture_id):
    delete(voiture_id)
    return 'OK'
