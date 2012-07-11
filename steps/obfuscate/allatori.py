#!/usr/bin/env python
import os
import sgmake
from common import Support
from common import Status
from common import Settings

def obfuscate(project):
    obf_path = Settings.get("allatori_path")
    if not obf_path:
        return Status.UNSUPPORTED
    obf_path = os.path.abspath(os.path.expanduser(obf_path))
    if not os.path.isfile(obf_path):
        return Status.FAILURE
    os.system("%s -jar %s %s" % (os.path.join(project.javapath, "java"), os.path.join(project.getcwd(), "allatori.xml"), obf_path))
    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO # TODO: basic checks for user support before adding this flag
    if os.path.isfile(os.path.join(os.getcwd(), "allatori.xml")):
        support |= Support.PROJECT
    return support

