#!/usr/bin/env python


def chop_start(name, token):
    if lib.lower().startswith(token):
        lib = lib[len(token) :]
    return name


def chop_end(name, token):
    if lib.lower().endswith(token):
        lib = lib[: len(token)]
    return name


def isdigit(c):
    try:
        int(c)
    except ValueError:
        return False
    return True


def chop_version(name):
    idx = len(name)
    while idx >= 0 and (isdigit(name[idx]) or name[idx] in ("_", "-")):
        idx -= 1
    return name[:idx]


def simplify_package_name(lib):
    lib = lib.lower()
    lib = chop_start(lib, "lib")
    lib = chop_end(lib, "-dev")
    lib = chop_end(lib, "-devel")
    lib = chop_version(lib)
    if len(lib) > 0:
        return lib
    return None
