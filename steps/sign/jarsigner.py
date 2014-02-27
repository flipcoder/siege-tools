#!/usr/bin/env python2
import os
import sgmake
from common import Support
from common import Status
from common import Settings

def unsign(project):
    pass

def sign(project):
    try:
        project.signjars
    except:
        project.signjars = []

    try:
        project.output
    except:
        print "Nothing to sign."
        return
    if not project.output:
        print "Nothing to sign."
        return
    
    timestamp_flags = "-tsa http://tsa.starfieldtech.com"

    print "Signing %s..." % project.output
    cmd = "%s -storepass %s %s %s %s" % (
        os.path.join(project.javapath,"jarsigner"),
        Settings.get("keystore_pass"),
        timestamp_flags,
        project.output,
        Settings.get("keystore_name")
    )
    print cmd
    os.system(cmd)

    # sign libs too (TODO: make optional)
    for signjars in project.signjars:
        print "signjars dir: %s" % signjars
        if os.path.isdir(signjars):
            for fn in os.listdir(signjars):
                #if fn.lower().endswith(".%s" % project.bin_ext):
                if fn.lower().endswith(".jar"):
                    #print "Signing %s..." % fn
                    cmd = "%s -storepass %s %s %s %s" % (
                        os.path.join(project.javapath, "jarsigner"),
                        Settings.get("keystore_pass"),
                        timestamp_flags,
                        os.path.join(signjars,fn),
                        Settings.get("keystore_name")
                    )
                    print cmd                        
                    os.system(cmd)
        # TODO: if system call returns with error, then return Status.FAILURE, regardless of --strict
        #return Status.FAILURE if Args.option("strict") else Status.UNSUPPORTED

    return Status.SUCCESS


def set_defaults(project):
    try:
        project.signjars
    except:
        # default behavior is to recursively sign classpath (recursion isn't impl yet)
        project.signjars = project.classpath

def compatible(project):
    # always deny compatibility, step can be added only by registered by another other addon or user script
    support = Support.PROJECT | Support.ENVIRONMENT

    if(Settings.get("keystore_pass") and Settings.get("keystore_name")):
        support |= Support.USER
        
    return support

