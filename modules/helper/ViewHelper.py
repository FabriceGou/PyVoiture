# -*- coding: utf-8 -*-

from flask import json, render_template
"""
Module contenant les fonctions partagées entre les views 
"""


def notif_success(msg, delay=5000):
    return json.dumps({'msg': msg, 'typeNotif': 'success', 'icon':'glyphicon glyphicon-ok', 'delay': delay})


def notif_error(msg, delay=3600000):
    return json.dumps({'msg': msg, 'typeNotif': 'danger', 'icon': 'glyphicon glyphicon-remove', 'delay': delay})


def notif_info(msg, delay=5000):
    return json.dumps({'msg': msg, 'typeNotif': 'info', 'icon': 'glyphicon glyphicon-info-sign', 'delay': delay})


def notif_warning(msg, delay=3600000):
    return json.dumps({'msg': msg, 'typeNotif': 'warning', 'icon': 'glyphicon glyphicon-warning-sign', 'delay': delay})
