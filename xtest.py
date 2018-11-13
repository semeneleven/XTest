# -*- coding: utf-8 -*- 
import json
import os
import threading

import cherrypy
import webview

import util


class Base(object):

    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def stepcheck(self):
        module_name = cherrypy.request.json["module_name"]
        step = cherrypy.request.json["step"]
        data = cherrypy.request.json["data"]
        answer = cherrypy.request.json["answer"]

        return  {'result': util.get_method(step)[module_name](data, answer)}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def stepgenerators(self):
        module_name = cherrypy.request.json["module_name"]
        step = cherrypy.request.json["step"]
        generator = cherrypy.request.json["generator"]

        data = util.get_method(generator)[module_name]()

        return {'view': util.create_view(step, data),
                    'data': data}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def decoderesult(self):
        module_name = cherrypy.request.json["module_name"]
        data = cherrypy.request.json["data"]
        answer = cherrypy.request.json["answer"]

        return {'result': util.get_decodes_method(module_name)(data, answer)}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def decodedata(self):
        module_name = cherrypy.request.json["module_name"]
        data = util.get_gen_decode(module_name)()
        response = {'view': util.create_view(module_name, data),
                    'data': data}

        return response

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def encoderesult(self):
        module_name = cherrypy.request.json["module_name"]
        data = cherrypy.request.json["data"]
        answer = cherrypy.request.json["answer"]
        return {'result': util.get_encodes_method(module_name)(data, answer)}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def encodedata(self):
        module_name = cherrypy.request.json["module_name"]
        data = util.get_gen_encode(module_name)()
        response = {'view': util.create_view(module_name, data),
                    'data': data}

        return response



    @cherrypy.expose
    @cherrypy.tools.json_out()
    def cyclics(self):
        code_names = util.get_code_names('cyclics')

        return {'codes': code_names}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def others(self):
        code_names = util.get_code_names('others')

        return {'codes': code_names}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def nonbinary(self):
        code_names = util.get_code_names('nonbinary')

        return {'codes': code_names}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def systematics(self):
        code_names = util.get_code_names('systematics')

        return {'codes': code_names}



    @cherrypy.expose
    def index(self):
        return open('static/html/index.html')


def start_server():
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),

        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static',
        }
    }
    cherrypy.config.update({'log.screen': False,
                            'server.socket_port': 9090}
                           )
    cherrypy.quickstart(Base(), "/", conf)


start_server();
# t = threading.Thread(target=start_server)
#
# t.daemon = True
# t.start()
#
# webview.create_window("PyBrowse", "http://localhost:9090", width=600,
#                      height=550, resizable=True, fullscreen=False)
