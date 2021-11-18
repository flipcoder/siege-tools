#!/usr/bin/env python
import os
import sgmake
import subprocess
from common import Status
from common import Settings
from common import Support
from common.Plugin import Plugin
from common import call
import clean.clean


def make(project):
    try:
        call(["./autogen.sh"])
    except subprocess.CalledProcessError:
        return Status.FAILURE
    return Status.SUCCESS


def update(project):
    configure_step = Plugin("steps", "make", "configure")
    make_step = Plugin("steps", "make", "makefile")
    clean_step = Plugin("steps", "clean", "clean")
    remove_steps = [configure_step, make_step, clean_step]

    for s in remove_steps:
        if s in project.steps:
            project.steps.remove(s)

    i = 0

    for s in project.steps:
        if s.type == "make" and s.name == "autogen":
            if clean.clean.compatible(project) & Support.USER:
                project.steps.insert(i, clean_step)
                project.steps.insert(i + 2, configure_step)
                project.steps.insert(i + 4, make_step)
            else:
                project.steps.insert(i + 1, configure_step)
                project.steps.insert(i + 3, make_step)
        i += 1


def compatible(project):
    support = Support.MASK & (~Support.PROJECT)
    if os.path.isfile("autogen.sh"):
        support |= Support.PROJECT
    return support
