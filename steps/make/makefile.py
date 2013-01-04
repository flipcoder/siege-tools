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

    try:
        project.makefile_params
    except:
        project.makefile_params = ""

    # example makefile params (add in project sg file):
        # makefile_params="CXX=\'clang++\'"
        # makefile_params="CXX=\'gccfilter -c -a g++\'"

    os.system("%s%s" %
        (os.path.join(project.makepath,"make"),
            " %s" % project.makefile_params
        )
    )
    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("Makefile"):
        support |= Support.PROJECT
    return support

