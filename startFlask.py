
# -*- coding: utf-8 -*-
"""
The flask application package.
"""
import os
import logging

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import Settings

app = Flask(__name__)
CORS(app)
app.name = 'Gestion voitures'
app.secret_key = b'mkmldskfkmlsdkkfmsdkkfmksdmkfmlkdskfmksdmkfmkdsmkfkmsdlkkflmksmldfkrozemlxcv'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voiture.db"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#crétion des objets partagés, logger, variables, etc...
logger = Settings.init()
app.logger = logger
logging.info('Démarrage du programme')
# Désactivation des warning pandas
#pour éviter les pb d'encodage avec la base
os.environ["NLS_LANG"] = "FRENCH_FRANCE.UTF8"


startUser = None
try:
    startUser = os.environ["LOGNAME"] #sur linux
except:
    startUser = None

import views
from routes.login import auth_bp
app.register_blueprint(auth_bp)
from routes.depense import depense_page
app.register_blueprint(depense_page)
from routes.voiture import voiture_page
app.register_blueprint(voiture_page)
from routes.categorie import categorie_page
app.register_blueprint(categorie_page)