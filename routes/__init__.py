# -*- coding: utf-8 -*-
from babel.dates import format_date
from jinja2 import Template
from startFlask import app

template = Template('')

def date_input_str(dt):
    """
    Transforme une date en str compatible avec les value des imput date
    :param dt: date
    :return: une str qui repesente la date au format yyyy-MM-dd
    """
    return format_date(dt, 'yyyy-MM-dd', locale='fr_FR')

# ajoute de la fonction aux fonctions appelables dans les templates Jinja
app.jinja_env.globals.update(date_input_str=date_input_str)

