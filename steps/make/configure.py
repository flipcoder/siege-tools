#!/usr/bin/env python
import os
import subprocess
import sgmake
from common import Status
from common import Settings
from common import Support
from common import call


def make(project):
    try:
        call(["./configure", "--prefix=/usr"])
    except subprocess.CalledProcessError:
        return Status.FAILURE
    return Status.SUCCESS


def update(project):
    pass


def compatible(project):
    support = Support.MASK & (~Support.PROJECT)
    if os.path.isfile("configure"):
        support |= Support.PROJECT
    return support
