# -*- coding: utf-8 -*-

from modules.db import Session
from modules.db.entities import Voiture, Plein, Depense


def liste():
    li = Session().query(Voiture).all()
    return li


def create(car):
    session = Session()
    session.add(car)
    session.commit()


def delete(voiture_id):
    session = Session()
    session.query(Plein).filter_by(voiture_id=int(voiture_id)).delete()
    session.query(Depense).filter_by(voiture_id=int(voiture_id)).delete()
    session.query(Voiture).filter_by(id=int(voiture_id)).delete()
    session.commit()
