# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from modules.db import Session
from modules.db.entities import Plein
from modules.db import engine
import pandas as pd
from startFlask import db


def create(plein):
    session = Session()
    session.add(plein)
    session.commit()

def get_plein(voiture_id, debut=None, fin=None):
    plein = db.session.query(Plein)
    if debut:
        plein = plein.filter(Plein.jour >= debut)
    if fin:
        plein = plein.filter(Plein.jour < (fin + timedelta(days=1)))
    plein = plein.filter(Plein.voiture_id==voiture_id)
    plein = plein.order_by(Plein.jour)
    # print(plein.statement)

    df = pd.read_sql(plein.statement, engine)
    if df.empty:
        return df
    else:
        df['jour'] = df['jour'].dt.strftime('%d/%m/%Y %H:%M')
        df['litre_100'] = 100 * df['anon_1'] / (df['kilometrage'] - df['kilometrage'].shift(1))
    return df