
# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""
import datetime
import json
import pandas as pd
import plotly
from flask import render_template, jsonify, request
from flask_login import login_required
from sqlalchemy.orm import joinedload

from modules.dal.plein import get_plein
from modules.db import AlchemyEncoder, Session, engine
from modules.db.entities import Voiture, Depense, Categorie
from modules.helper import DateHelper
from startFlask import app, db


@app.route('/')
@app.route('/home')
@login_required
def home():
    date_fin = datetime.datetime.today()
    date_debut = date_fin + datetime.timedelta(days=-366)

    return render_template(
        'accueil.html',
        title='Génération des voitures',
        date_debut= DateHelper.date_to_str_web(date_debut), 
        date_fin=DateHelper.date_to_str_web(date_fin)
    )

@app.route('/charger_graph_conso')
def charger_graph_conso():
    date_deb = request.args.get('date_deb', None)
    date_fin = request.args.get('date_fin', None)
    voiture_id = request.args.get('voiture_id', None)
    if date_deb:
        date_deb = DateHelper.str_web_to_date(date_deb)
    if date_fin:
        date_fin = DateHelper.str_web_to_date(date_fin)
    
    return make_graph(voiture_id, date_deb, date_fin)
    

def make_graph(voiture_id, date_deb, date_fin):
    df = get_plein(voiture_id, date_deb, date_fin, date_format='%Y-%m-%d %H')
    avg = df['litre_100'].mean()
    trace_point = dict(x=df['jour'], y=df['litre_100'], name="", mode="lines")
    layout = dict(
        title="Consommation {0} L/100 ".format(round(avg, 2)),
        xaxis=dict(title="Dates", tickformat="%d-%m-%Y", tickangle=0),
        yaxis_title="L/100",
        margin=dict(l=30, r=10, t=30, b=30),
        font=dict(
            family="Arial,Helvetica",
            size=11,
            color="black"
        ),
        plot_bgcolor='lightgrey',
        showlegend=False
    )

    data = [trace_point]
    fig = dict(data=data, layout=layout)

    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

# variable qui est utilisée dans chaque template
@app.context_processor
def list_voiture():
    voitures = Session().query(Voiture).all()
    return dict(voitures=voitures)

############# DEPENSES ###########################
@app.route('/depense')
def depense():
    return render_template(
        'depenses.html',
        title='Dépenses'
    )


@app.route('/list_depense/<int:voiture_id>', methods=['POST'])
def list_depense(voiture_id):
    query = db.session.query(Depense)\
        .options(joinedload(Depense.categorie).load_only(Categorie.categorie))\
        .filter_by(voiture_id=voiture_id).order_by(Depense.jour)
    df = pd.read_sql(query.statement, engine)
    if df.empty:
        json_data ='{}'
    else:
        df['jour'] = df['jour'].dt.strftime('%d/%m/%Y %H:%M')
        json_data = df.to_json(orient='records')

    return jsonify(json_data)
