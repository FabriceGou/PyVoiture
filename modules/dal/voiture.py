# -*- coding: utf-8 -*-

from modules.db import Session
from modules.db.entities import Voiture


def liste():
    li = Session().query(Voiture).all()
    return li


def create(car):
    session = Session()
    session.add(car)
    session.commit()
