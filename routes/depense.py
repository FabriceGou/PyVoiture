
# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""
import datetime
import pandas as pd
from flask import render_template, jsonify, request, Blueprint

from modules.dal.plein import get_plein
from modules.db import engine
from modules.db.entities import Plein, Depense, Categorie
from modules.helper import ViewHelper, DateHelper
from startFlask import db
from modules.dal import plein as plein_dal

depense_page = Blueprint('depense_page', __name__, template_folder='templates')


@depense_page.route('/carburant')
def carburant():
    return render_template(
        'carburant.html',
        title='Carburant'
    )

@depense_page.route('/show_plein_form')
def show_plein_form():
    plein_id= request.values['plein_id']
    voiture_id = request.values['voiture_id']
    if plein_id != '-1':
        plein = db.session.query(Plein).get(int(plein_id))
    else:
        plein = Plein()
        plein.id = -1
        plein.voiture_id = int(voiture_id)
        plein.jour = datetime.date.today()

    return render_template(
        '_carburant_form.html',
        jour=DateHelper.date_to_str_web(plein.jour), plein=plein
    )


@depense_page.route('/list_carburant/<int:voiture_id>', methods=['POST'])
def list_carburant(voiture_id):
    df = get_plein(voiture_id)
    if df.empty:
        json_data='{}'
    else:
        json_data = df.to_json(orient='records')

    return jsonify(json_data)


@depense_page.route('/sauver_plein', methods=['POST'])
def sauver_plein():
    try:
        plein_id = request.form['plein_id']

        if plein_id != '-1':
            plein = db.session.query(Plein).get(int(plein_id))
        else:
            plein = Plein()
            voiture_id = request.form['voiture_id']
            plein.voiture_id = voiture_id

        jour = DateHelper.str_web_to_date(request.form['jour'])
        kilometrage = request.form['kilometrage']
        prix_litre = request.form['prix_litre']
        total = request.form['total']
        commentaire = request.form['commentaire']

        plein.jour = jour
        plein.kilometrage = kilometrage
        plein.prix_litre = prix_litre
        plein.total = total
        plein.description = commentaire

        if plein_id == '-1':
            plein_dal.create(plein)
        else:
            db.session.commit()

    except Exception as exc:
        return ViewHelper.notif_error("Erreur lors de l'enregistrement")

    return carburant()

@depense_page.route('/supprimer_plein/<int:id>', methods=['POST'])
def supprimer_plein(id):
    db.session.query(Plein).filter_by(id=id).delete()
    db.session.commit()
    return 'OK'

############# DEPENSES ###########################
@depense_page.route('/depense')
def depense():
    return render_template(
        'depenses.html',
        title='Dépenses'
    )


@depense_page.route('/list_depense/<int:voiture_id>', methods=['POST'])
def list_depense(voiture_id):
    query = db.session.query(Depense).filter_by(voiture_id=voiture_id).order_by(Depense.jour)
    df = pd.read_sql(query.statement, engine)
    if df.empty:
        json_data ='{}'
    else:
        df['jour'] = df['jour'].dt.strftime('%d/%m/%Y %H:%M')
        json_data = df.to_json(orient='records')

    return jsonify(json_data)


@depense_page.route('/show_depense_form')
def show_depense_form():
    depense_id = request.values['depense_id']

    if depense_id != '-1':
        depens = db.session.query(Depense).get(int(depense_id))
    else:
        depens = Depense()
        depens.depense_id = -1
        depens.jour = datetime.date.today()
    categories = db.session.query(Categorie).all()
    return render_template(
        '_depense_form.html', depense=depens, categories=categories
    )

@depense_page.route('/sauver_depense', methods=['POST'])
def sauver_depense():
    try:
        depense_id = request.values['depense_id']

        if depense_id != '-1':
            depense = db.session.query(Depense).get(int(depense_id))
        else:
            depense = Depense()
            depense.voiture_id = request.form['voiture_id']

        depense.cat_id = request.form['categorie_id']
        depense.jour = DateHelper.str_web_to_date(request.form['jour'])
        depense.total = request.form['total']
        depense.kilometrage = request.form['kilometrage']
        depense.description = request.form['description']

        if depense_id == '-1':
            db.session.add(depense)
        db.session.commit()

    except Exception as exc:
        return ViewHelper.notif_error("Erreur lors de l'enregistrement")

    return render_template('depenses.html', title='Dépenses')


@depense_page.route('/supprimer_depense/<int:id>', methods=['DELETE'])
def supprimer_depense(id):
    db.session.query(Depense).filter_by(depense_id=id).delete()
    db.session.commit()
    return 'OK'