#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings

def obfuscate(project):
    obf_path = Settings.get("allatori_path")
    if not obf_path:
        return Status.UNSUPPORTED
    obf_path = os.path.abspath(obf_path)
    if not os.path.isfile(obf_path):
        return Status.FAILURE
    os.system(project.javapath + "java -jar %s allatori.xml" % obf_path)
    return Status.SUCCESS

def compatible(project):
    if os.path.isfile("allatori.xml"):
        return True
    return False

