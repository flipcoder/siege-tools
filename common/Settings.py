#!/usr/bin/env python
import os

user_settings = {}

def settings_load(fn):
    try:
        fn = os.environ['HOME']+os.sep+fn
        with open(fn) as source:
            eval(compile(source.read(), fn, 'exec'), {}, user_settings)
        return True
    except IOError:
        return False

def settings():
    return settings

def get(fn):
    try:
        return user_settings[fn]
    except:
        pass
    return None

for fn in (".sgrc.py", "_sgrc.py"):
    if settings_load(fn):
        break

