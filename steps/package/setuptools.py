import os
import sgmake
from common import *


def package(project):
    wdir = os.getcwd()
    os.chdir(os.path.join(wdir, os.path.dirname(project.setuptools_file)))

    # val = os.system("python setup.py")
    # if val != 0:
    #     return Status.FAILURE

    os.chdir(wdir)
    return Status.SUCCESS


def update(project):
    project.setuptools_file = ""
    pass


def compatible(project):
    support = Support.AUTO | Support.ENVIRONMENT

    # if os.path.isfile(os.path.join(os.getcwd(), "setup.py")):
    #     support |= Support.PROJECT

    return support
