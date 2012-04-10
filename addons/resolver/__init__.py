#!/usr/bin/env python

def chop_start(name, token):
    if lib.lower().startswith(token):
        lib = lib[len(token):]
    return name

def chop_end(name, token):
    if lib.lower().endswith(token):
        lib = lib[:len(token)]
    return name

def simplify_package_name(lib):
    lib = chop_start(lib,"lib")
    lib = chop_end(lib,"-dev")
    lib = chop_end(lib,"-devel")
    if len(lib) > 0:
        return lib
    return None

