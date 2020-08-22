# -*- coding: utf-8 -*-

from startFlask import app


def start():
    app.run('0.0.0.0', 8454, debug=True, use_reloader=True)


if __name__ == '__main__':
    start()
