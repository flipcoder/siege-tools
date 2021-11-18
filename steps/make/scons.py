#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Settings
from common import Support


def make(project):
    try:
        project.sconspath = os.path.abspath(
            os.path.expanduser(Settings.get("scons_path"))
        )
    except:
        project.sconspath = ""

    os.system(os.path.join(project.sconspath, "scons"))
    return Status.SUCCESS


def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("SConstruct") or os.path.isfile("scons/SConstruct"):
        support |= Support.PROJECT
    return support
