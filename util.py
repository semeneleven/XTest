import inspect
import os
import pkgutil
import re

import pystache

import codes


def get_code_names(category):
    names = []
    path_info = get_path_info()
    for i in range(len(path_info[0])):

        path = []
        path.append(path_info[0][i])
        for importer, modname, ispkg in pkgutil.iter_modules(path, path_info[1][i]):
            if category in modname:
                names.append(modname[modname.rfind(".") + 1:])
    return names


def get_path_info():
    path_info = [[], []]
    prefix = codes.__name__ + '.'

    for path in [x[0] for x in os.walk(next(codes.__path__.__iter__()))]:
        if re.compile(r'^\/(\w*\/)*(codes)(\/\w*)(?!\/)$').match(path):
            path_info[0].append(path + '/')
            path_info[1].append(prefix + path[path.rfind("/") + 1:] + '.')

    return path_info


def get_method(method_name):
    codes_dict = dict([])
    path_info = get_path_info()

    for i in range(len(path_info[0])):

        path = []
        path.append(path_info[0][i])
        for importer, modname, ispkg in pkgutil.iter_modules(path, path_info[1][i]):

            module = __import__(modname, fromlist="dummy");
            methods = inspect.getmembers(module, predicate=inspect.isfunction)
            if methods:
                for method in methods:
                    if method_name in method:
                        codes_dict.update(
                            {modname[modname.rfind(".") + 1:]: method[1]})

    return codes_dict


def create_view(modname, data):
    tempalte = open('templates/' + modname + '.html', 'r')
    return pystache.render(tempalte.read(), data)


def get_encodes_method(modname):
    return get_method('assert_code')[modname]


def get_decodes_method(modname):
    return get_method('assert_decode')[modname]


def get_gen_encode(modname):
    return get_method('generate_for_encode')[modname]


def get_gen_decode(modname):
    return get_method('generate_for_decode')[modname]


def get_details(modname):
    return get_method('get_details')[modname]

def get_name(modname):
    return get_method('get_name')[modname]
