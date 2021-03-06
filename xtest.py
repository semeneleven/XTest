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
    def exam(self):
        module_name = cherrypy.request.json["module_name"]
        amount_of_tasks = util.get_details(module_name)()['exam_tasks']
        data = {'count': [x for x in range(amount_of_tasks)]}
        return {'view': util.create_view('exam', data, 'exam'),
                'exam_tasks': amount_of_tasks}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def stepcheck(self):
        module_name = cherrypy.request.json["module_name"]
        step = cherrypy.request.json["step"]
        data = cherrypy.request.json["data"]
        answer = cherrypy.request.json["answer"]

        return {'result': util.get_method(step)[module_name](data, answer)}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def stepgenerators(self):
        module_name = cherrypy.request.json["module_name"]
        step = cherrypy.request.json["step"]
        generator = cherrypy.request.json["generator"]

        data = util.get_method(generator)[module_name]()

        return {'view': util.create_view(step, data,'encode'),
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
        response = {'view': util.create_view(module_name, data, 'decode'),
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
        response = {'view': util.create_view(module_name, data, 'encode'),
                    'data': data}

        return response

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def codedetails(self):
        # TODO
        module_name = cherrypy.request.json["module_name"]
        return {'name': module_name,
                'description': util.get_description(module_name),
                'details': util.get_details(module_name)()
                }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def cyclics(self):
        code_modules_names = util.get_code_names('cyclics')
        code_names = {}
        for code in code_modules_names:
            code_names.update({code: util.get_name(code)()})

        return {'codes': code_names}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def others(self):
        code_modules_names = util.get_code_names('others')
        code_names = {}
        for code in code_modules_names:
            code_names.update({code: util.get_name(code)()})

        return {'codes': code_names}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def nonbinary(self):
        code_modules_names = util.get_code_names('nonbinary')
        code_names = {}
        for code in code_modules_names:
            code_names.update({code: util.get_name(code)()})

        return {'codes': code_names}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def systematics(self):
        code_modules_names = util.get_code_names('systematics')
        code_names = {}
        for code in code_modules_names:
            code_names.update({code: util.get_name(code)()})

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


start_server()
# t = threading.Thread(target=start_server)
#
# t.daemon = True
# t.start()
#
# webview.create_window("PyBrowse", "http://localhost:9090", width=600,
#                      height=550, resizable=True, fullscreen=False)
