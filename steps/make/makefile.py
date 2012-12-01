#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Settings
from common import Support

def make(project):
    try:
        project.makepath = os.path.abspath(os.path.expanduser(Settings.get('make_path')))
    except:
        project.makepath = ""

    os.system(os.path.join(project.makepath,"make"))
    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("Makefile"):
        support |= Support.PROJECT
    return support

