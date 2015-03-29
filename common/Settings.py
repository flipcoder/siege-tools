#!/usr/bin/env python
import json
import os

user_settings = {}

def settings_load(fn):
    if fn.lower().endswith('.py'):
        try:
            fn = os.environ['HOME']+os.sep+fn
            with open(fn) as source:
                eval(compile(source.read(), fn, 'exec'), {}, user_settings)
            return True
        except IOError:
            return False
    #elif fn.lower().endswith('.json'):
        # not yet implemented
    else: # assume json
        return False

def settings():
    return settings

def get(fn):
    try:
        return user_settings[fn]
    except:
        pass
    return None

for fn in (".sgrc.py", "_sgrc.py", ".sgrc.json", "_sgrc.json"):
    if settings_load(fn):
        break

