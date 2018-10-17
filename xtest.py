# -*- coding: utf-8 -*- 
import json
import os
import threading

import cherrypy
import webview

import util




class Base(object):

    def __init__(self,codes):
        self.codes_dict=codes

    @cherrypy.expose
    def check_code(self, data="", answer="", code=""):


        print(data, answer, sep=" ~/~ ", end="!|")
        b = self.codes_dict[code](data,answer)

        print(b)

        return  "<html><head></head><body><h1>"+b+"/h1></body></html>"

    @cherrypy.expose
    def index(self):
        return open('public/html/index.html')


def start_server():

    codes_dict=util.initialize_func_dict()

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
    cherrypy.quickstart(Base(codes_dict), "/", conf)


t = threading.Thread(target=start_server)


t.daemon = True
t.start()


webview.create_window("PyBrowse", "http://localhost:9090", width=800,
                      height=600, resizable=True, fullscreen=False)
