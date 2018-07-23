import os
import platform
import sgmake
import subprocess
from common import Status
from common import Settings
from common import Support
from common import call

def package(project):
    wine = False if platform.system() == "Windows" else True

    if wine:
        try:
            call(["makensis", project.nsi_file])
        except OSError:
            try:
                call(["wine",  "\"c:/Program Files (x86)/NSIS/makensis.exe\"", project.nsi_file])
            except OSError:
                return Status.UNSUPPORTED
            #except subprocess.CalledProcessError:
            #    return Status.FAILURE
        #except subprocess.CalledProcessError:
        #    return Status.FAILURE
    else:
        try:
            call(["makensis", project.nsi_file])
        except OSError:
            return Status.UNSUPPORTED

    return Status.SUCCESS

def update(project):
    # TODO: installer builder plugins should move step at the end of
    #  other packaging steps if necessary

    pass

def compatible(project):
    support = Support.USER | Support.ENVIRONMENT | Support.AUTO

    for fn in os.listdir("."):
        if os.path.isfile(os.path.join(os.getcwd(),fn)):
            if fn.lower().endswith(".nsi"):
                project.nsi_file = fn
                support |= Support.PROJECT

    return support

