# -*- coding: utf-8 -*-

from modules.db import Session

def create(depense):
    session = Session()
    session.add(depense)
    session.commit()
