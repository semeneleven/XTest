import inspect
import os
import pkgutil
import re

import codes


codes_dict = dict([]);


def get_codes_names(category):

    names = []

    path_info = get_path_info()
    for i in range(len(path_info[0])):

        path = []
        path.append(path_info[0][i])
        for importer, modname, ispkg in pkgutil.iter_modules(path, path_info[1][i]):
            print("Found submodule %s " % (modname))
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

def initialize_func_dict():

    path_info = get_path_info()



    print(path_info)

    for i in range(len(path_info[0])):

        path = []
        path.append(path_info[0][i])
        for importer, modname, ispkg in pkgutil.iter_modules(path, path_info[1][i]):
            print("Found submodule %s " % (modname))
            module = __import__(modname, fromlist="dummy");
            #print(modname[modname.rfind(".") + 1:])
            methods = inspect.getmembers(module, predicate=inspect.isfunction)
            if methods:
                codes_dict.update(
                    {modname[modname.rfind(".") + 1:]: methods[0][1]})

    return codes_dict


print(get_codes_names("systematic"))
print(get_codes_names("сyclics"))
print(get_codes_names("nonbinary"))
print(get_codes_names("others"))