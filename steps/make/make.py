#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings

def make(project):
    project.makepath = Settings.get('make_path')
    if project.makepath:
        project.makepath = os.path.abspath(os.expanduser(Settings.get('make_path')))

    if project.makepath:
        if project.makepath[-1] != os.sep and os.altsep and Settings.get('make_path')[-1] != os.altsep:
            project.makepath += os.sep
    else:
        project.makepath = ""

    os.system(os.path.join(project.makepath,"make"))
    return Status.SUCCESS

def compatible(project):
    if os.path.isfile("Makefile"):
        return True
    return False

