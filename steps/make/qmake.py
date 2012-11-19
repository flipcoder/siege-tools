#!/usr/bin/env python
# TODO: detect *.pro files to verify
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common.Plugin import Plugin
import clean.clean

def make(project):
    os.system("% -o Makefile %s" % (os.path.join(project.qmakepath, "qmake"), project.qmake_pro_file))
    return Status.SUCCESS

def update(project):
    project.qmakepath= Settings.get('qmake_path')
    if project.qmakepath:
        project.qmakepath = os.path.abspath(project.qmakepath)
    else:
        project.qmakepath = ""

    make_step = Plugin("steps", "make", "make")
    project.clean_commands = ["%s clean" % os.path.join(project.makepath,"make")]
    clean_step = Plugin("steps", "clean", "clean")
    if make_step in project.steps:
        project.steps.remove(make_step)
    if clean_step in project.steps:
        project.steps.remove(clean_step)

    i = 0
    for s in project.steps:
        if s.type == "make" and s.name == "qmake":
            # TODO: check for user support (because of -r flag)
            if clean.clean.compatible(project) & Support.USER:
                project.steps.insert(i, clean_step)
                project.steps.insert(i+2, make_step)
            else:
                project.steps.insert(i+1, make_step)
            break
        i += 1

def compatible(project):
    support = Support.MASK & (~Support.PROJECT)
    for fn in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(),fn)):
            if fn.lower().endswith(".pro"):
                project.qmake_pro_file = os.path.join(os.getcwd(), fn)
                support |= Support.PROJECT
                break

    return support

