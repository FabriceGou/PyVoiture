# -*- coding: utf-8 -*-
import datetime
import logging
import calendar
from babel.dates import format_date

"""
Module d'aide pour manipuler les dates
"""

def to_str(dt, format_pattern, locale='fr_FR'):
    """
    Exemple de format :
    - 'EEE dd/MM/yy HH:mm:ss'   ==> jeudi 21/11/19
    """
    try:
       str = format_date(dt, format_pattern, locale=locale)
    except Exception:
        logging.exception('Erreur lors de la convertion de la date vers une string au format ' + format_pattern)
        raise
    return str


def now_to_str_sortable():
    """ Transforme une date en string au format yyyymmdd_HHMMSS_mili """
    try:
        d=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    except Exception:
        logging.exception('Erreur lors de la convertion de la date courante en string')
        raise
    return d


def date_to_str_web(dt):
    """ Transforme une date au format type web c'est à dire yyyy-MM-dd """
    try:
        d = to_str(dt, 'yyyy-MM-dd')
    except Exception:
        logging.exception(('Erreur lors de la convertion de la date {0} vers une chaine yyyy-MM-dd').format(dt))
        raise
    return d


def str_web_to_date(str):
    """ Transforme une string au format yyyy-mm-dd en date """
    try:
        d = datetime.datetime.strptime(str, '%Y-%m-%d')
    except Exception:
        logging.exception(('Erreur lors de la convertion de la chaine {0} vers une date').format(str))
        raise
    return d


def first_day_month(dt):
    """ Renvoie le premier jour du mois """
    try:
        d = datetime.date(dt.year, dt.month, 1)
    except Exception:
        logging.exception(('Erreur lors de la récupération du premier jour du mois pour la date {0}').format(dt))
        raise
    return d


def last_day_month(dt):
    """ Renvoie le dernier jour du mois """
    try:
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        d = datetime.date(dt.year, dt.month, last_day)

    except Exception:
        logging.exception(('Erreur lors de la récupération du dernier jour du mois pour la date {0}').format(dt))
        raise
    return d


def nb_jour_month(dt):
    """ Renvoie le nombre de jours dans le mois """
    try:
        nb = last_day_month(dt).day

    except Exception:
        logging.exception(('Erreur lors du calcul du nombre de jour dans le mois pour la date {0}').format(dt))
        raise
    return nb
