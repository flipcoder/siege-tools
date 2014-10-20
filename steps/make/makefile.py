#!/usr/bin/env python
import os
import sgmake
import subprocess
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
        project.makefile_params = []

    # example makefile params (add in project sg file):
        # makefile_params="CXX=\'clang++\'"
        # makefile_params="CXX=\'gccfilter -c -a g++\'"

    cmdline = [os.path.join(project.makepath,"make")]
    if project.makefile_params:
        cmdline += project.makefile_params

    try:
        os.chdir(project.build_dir)
    except:
        pass
    
    try:
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError:
        try:
            if project.build_dir:
                os.chdir("..")
        except:
            pass
        return Status.FAILURE
    
    try:
        if project.build_dir:
            os.chdir("..")
    except:
        pass

    #os.system("%s%s" %
    #    (os.path.join(project.makepath,"make"),
    #        " %s" % project.makefile_params
    #    )
    #)
    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("Makefile"):
        support |= Support.PROJECT
    return support

