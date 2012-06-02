#!/usr/bin/env python2
import os
import sgmake
from sgmake import Status
from common import Settings

def sign(project):
    os.system("%s -storepass %s %s %s" % (os.path.join(project.javapath,"jarsigner"), Settings.get("keystore_pass"), project.output, Settings.get("keystore_name")))
    
    # sign libs too (TODO: make optional)
    for classpath_dir in project.classpath:
        if os.path.isdir(classpath_dir):
            for fn in os.listdir(classpath_dir):
                #if fn.lower().endswith(".%s" % project.bin_ext):
                if fn.lower().endswith(".jar"):
                    print "Signing %s..." % fn
                    os.system("%s -storepass %s %s %s" % (os.path.join(project.javapath, "jarsigner"), Settings.get("keystore_pass"), os.path.join(classpath_dir,fn), Settings.get("keystore_name")))
                        
        # TODO: if system call returns with error, then return Status.FAILURE, regardless of --strict
        #return Status.FAILURE if Args.option("strict") else Status.UNSUPPORTED

    return Status.SUCCESS

def user_support():
    return Settings.get("keystore_pass") and Settings.get("keystore_name")

def compatible(project):
    # always deny compatibility, step can be added only by registered by another other addon or user script
    return False

