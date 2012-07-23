import os
import platform
import sgmake
from common import Status
from common import Settings
from common import Support

def package(project):
    wine = False if platform.system() == "Windows" else True

    if wine:
        os.system("wine \"c:/Program Files (x86)/NSIS/makensis.exe\" %s" % project.nsi_file)
    else:
        os.system("makensis %s" % project.nsi_file)

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

