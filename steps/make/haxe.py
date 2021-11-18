#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common.Plugin import Plugin
import subprocess
from common import call


def make(project):

    cmd = ["haxe", "compile.hxml"]

    try:
        call(cmd)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS


def update(project):
    pass


def compatible(project):
    support = Support.MASK & (~Support.PROJECT)
    if os.path.isfile("compile.hxml"):
        support |= Support.PROJECT
    return support
