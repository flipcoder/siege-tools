#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common.Plugin import Plugin
import subprocess

def make(project):

    cmd = [
        'xbuild',
        project.solution
    ]
    
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS

def update(project):
    # TODO: add exe's in all bin/ folders to be cleaned
    pass
    
def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    # TODO: check env support: do we have xbuild on the system?
    
    # TODO turn this into a detect
    for fn in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(),fn)):
            if fn.lower().endswith(".sln"):
                sln = os.path.join(os.getcwd(), fn)
                f = open(sln, 'r')
                has_csharp = False
                for line in f:
                    if line.startswith('Project('):
                        if line.find(".csproj")!=-1:
                            has_csharp = True
                f.close()
                if has_csharp:
                    project.solution = sln
                    project.clean = []
                    support |= Support.PROJECT
                break

    return support

