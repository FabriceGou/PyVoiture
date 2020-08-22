# -*- coding: utf-8 -*-
"""
Module d'initialisation  : 
    - des variables partagées dans l'application
    - du logger
    - de l'arborescence des répertoires
    - 
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def init():
    logger = __configurerLogger__()

    return logger
    

def __configurerLogger__():
    """
    Configuration du logger de l'application
    création de l'objet logger qui va nous servir à écrire dans les logs
    """
    msgConfLog = None
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    logFullPath = '/tmp/voiture.log'  # si pb avec oracle on espere avoir des traces

    file_handler = RotatingFileHandler(logFullPath, 'a', 1000000, 2)
    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] {%(pathname)s:%(lineno)d} %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logging.debug('Configuration des log terminée')
    if msgConfLog:
        logging.error(msgConfLog)

    return logger
