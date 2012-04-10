#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings
import addons

def make(project):
    
    project.makepath = Settings.get('make_path')
    if project.makepath:
        if project.makepath[-1] != os.sep and os.altsep and Settings.get('make_path')[-1] != os.altsep:
            project.makepath += os.sep
    else:
        project.makepath = ""

    os.system("%smake" % project.makepath)
    return Status.SUCCESS

def compatible(project):
    if os.path.isfile("Makefile"):
        return True
    return False

