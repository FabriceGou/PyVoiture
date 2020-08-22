# -*- coding: utf-8 -*-
import time

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DATETIME, DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import relationship, column_property

from modules.db import engine, Base

@compiles(DATETIME, 'sqlite')

class Voiture(Base):
    __tablename__ = 'voiture'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, nullable=False)
    description = Column(String)
    pleins = relationship("Plein", backref="plein", lazy='joined')
    pleins = relationship("Depense", backref="depense", lazy='joined')


class Plein(Base):
    __tablename__ = 'plein'

    id = Column(Integer, primary_key=True, autoincrement=True)
    voiture_id = Column(Integer, ForeignKey('voiture.id'))
    prix_litre = Column(Numeric, nullable=False)
    total = Column(Numeric, nullable=False)
    kilometrage = Column(Integer, nullable=False)
    description = Column(String)
    jour = Column(DateTime, nullable=False)

    volume = column_property(total/prix_litre)

class Categorie(Base):
    __tablename__ = 'categorie'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, nullable=False)
    description = Column(String)


class Depense(Base):
    __tablename__ = 'depense'

    id = Column(Integer, primary_key=True, autoincrement=True)
    voiture_id = Column(Integer, ForeignKey('voiture.id'))
    categorie_id = Column(Integer, ForeignKey('categorie.id'))
    total = Column(Numeric, nullable=False)
    kilometrage = Column(Integer, nullable=False)
    description = Column(String)
    jour = Column(DateTime, nullable=False)

# creation des tables
Base.metadata.create_all(engine)

