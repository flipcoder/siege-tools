#!/usr/bin/env python
import os
import sgmake
import multiprocessing
import subprocess
import tempfile
from common import Status
from common import Settings
from common import Support

def make(project):

    # relink a broken tmpfs-based obj dir
    if os.path.islink('obj') and not os.path.exists('obj'):
        os.unlink('obj')
        prefix = 'sg-' + os.getlogin() + '-' + project.name + '-'
        os.symlink(tempfile.mkdtemp(prefix=prefix), 'obj')
        
    try:
        project.makepath = os.path.abspath(os.path.expanduser(Settings.get('make_path')))
    except:
        project.makepath = ""

    try:
        project.makefile_params
    except:
        project.makefile_params = []

    cores = multiprocessing.cpu_count()
    project.makefile_params += ["-j" + str(int(cores * 1.5 + 0.5))]

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

