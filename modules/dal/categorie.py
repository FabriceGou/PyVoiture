# -*- coding: utf-8 -*-

from modules.db import Session
from modules.db.entities import Categorie, Depense


def liste():
    li = Session().query(Categorie).all()
    return li


def create(cat):
    session = Session()
    session.add(cat)
    session.commit()


def delete(categorie_id):
    session = Session()
    depense = session.query(Depense).filter_by(cat_id=int(categorie_id)).first()
    if depense:
        return "La catégorie ne peut pas être supprimée car elle est utilisée par une dépence"
    session.query(Categorie).filter_by(categorie_id=int(categorie_id)).delete()
    session.commit()
    return None
