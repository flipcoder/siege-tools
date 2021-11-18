#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common.Plugin import Plugin
import clean.clean


def make(project):
    try:
        project.cmakepath = ""
    except:
        pass

    try:
        os.mkdir("build")
    except:
        pass
    os.chdir("build")

    try:
        os.system("%s .." % os.path.join(project.cmakepath, "cmake"))
    except:
        os.chdir("..")
        return Status.FAILURE
    project.build_dir_ = "build"
    return Status.SUCCESS


def update(project):
    try:
        project.makepath = os.path.abspath(
            os.path.expanduser(Settings.get("make_path"))
        )
    except:
        project.makepath = ""
    # make sure theres a make step after cmake

    make_step = Plugin("steps", "make", "makefile")
    conf_step = Plugin("steps", "make", "configure")
    project.clean_commands = ["%s clean" % os.path.join(project.makepath, "make")]
    clean_step = Plugin("steps", "clean", "clean")
    if make_step in project.steps:
        project.steps.remove(make_step)
    if clean_step in project.steps:
        project.steps.remove(clean_step)
    if conf_step in project.steps:
        project.steps.remove(conf_step)

    i = 0
    for s in project.steps:
        if s.type == "make" and s.name == "cmake":
            # TODO: check for user support (because of -r flag)
            if clean.clean.compatible(project) & Support.USER:
                project.steps.insert(i, clean_step)
                project.steps.insert(i + 2, make_step)
            else:
                project.steps.insert(i + 1, make_step)
            break
        i += 1


def compatible(project):
    support = Support.MASK & ~Support.PROJECT
    if os.path.isfile("CMakeLists.txt"):
        support |= Support.PROJECT
    return support
