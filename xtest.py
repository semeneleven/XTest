# -*- coding: utf-8 -*- 
import inspect
import json
import os
import threading

import cherrypy
import webview


from codes.others import gray


class Home(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def check_code(self, data="", answer="", code=""):


        print(inspect.getmembers(dir("codes"), predicate=inspect.ismodule))
        codes={"gray": inspect.getmembers(gray, predicate=inspect.isfunction)[0][1]}
        print(data, answer, sep=" ~/~ ", end="!|")
        b = codes[code](data,answer)

        return  {"status":b}

    @cherrypy.expose
    def index(self):
        return open('public/html/index.html')


def start_server():

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public',
        }
    }
    cherrypy.config.update({'log.screen': False,
                            'server.socket_port': 9090}
                           )
    cherrypy.quickstart(Home(), "/", conf)

t = threading.Thread(target=start_server)


t.daemon = True
t.start()


webview.create_window("PyBrowse", "http://localhost:9090", width=800,
                      height=600, resizable=True, fullscreen=False)
