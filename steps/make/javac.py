#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common.Plugin import Plugin
import sign.jarsigner

def make(project):

    for folder in (project.classdir,project.output_path):
        try:
            os.mkdir(os.path.join(os.getcwd(), folder))
        except OSError:
            pass

    classpath = ""
    #classpathlist = os.pathsep.join(project.classpath)

    for entry in project.classpath:
        if os.path.isfile(entry):
            if classpath:
                classpath += os.pathsep + entry
            else:
                classpath = entry
            continue
        for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
            for fn in files:
                if fn.lower().endswith(".jar"):
                    rel_path = os.path.relpath(path,fn)
                    rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                    if classpath:
                        classpath = os.pathsep.join((classpath, os.path.join(rel_path,fn)))
                    else:
                        classpath = os.path.join(rel_path,fn)

    if classpath:
        classpath = os.pathsep.join((classpath, os.pathsep.join(project.classpath)))
    else:
        classpath = os.pathsep.join(project.classpath)

    sourcepath = ""

    for entry in project.sourcepath:
        if os.path.isfile(entry):
            if sourcepath:
                sourcepath = sourcepath + os.linesep + os.path.join(rel_path,fn)
            else:
                sourcepath = os.path.join(rel_path,fn)
            continue
        for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
            for fn in files:
                for ext in project.src_ext:
                    if fn.lower().endswith(".%s" % ext):
                        rel_path = os.path.relpath(path,fn)
                        rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                        if sourcepath:
                            sourcepath = "%s %s" % (sourcepath, os.path.join(rel_path,fn))
                        else:
                            sourcepath = os.path.join(rel_path,fn)

    project.javapath = Settings.get('java_path')
    if project.javapath:
        project.javapath = os.path.abspath(project.javapath)
    else:
        project.javapath = ""

    #if project.javapath:
    #    if project.javapath[-1] != os.sep and os.altsep and Settings.get('java_path')[-1] != os.altsep:
    #        project.javapath += os.sep
    #else:
    #    project.javapath = ""

    project.output = os.path.join(project.output_path,project.name+".jar")

    # TODO: boostrap class path
    # removed: -source 1.6 -target 1.6 
    misc_params = " ".join(project.javac_params)
    os.system("%s %s -d %s %s -cp %s" % (os.path.join(project.javapath,"javac"), misc_params, project.classdir, sourcepath, classpath))
    os.system("%s cmf %s %s -C %s ." % (os.path.join(project.javapath,"jar"), project.manifest, project.output, project.classdir))
    # TODO wrap stdout from above commands and detect errors
    
    if not os.path.isfile(project.output):
        return Status.FAILURE

    return Status.SUCCESS

def set_defaults(project):
    if not project.sourcepath:
        project.sourcepath = ["src"]
    project.classpath = ["lib","libs"]
    project.obfuscator = None
    project.output = None
    # TODO: "classes" might be output dir, do that in local detect check
    project.classdir = "bin"
    try:
        project.output_path
    except:
        project.output_path = "dist"

    project.language = "java"
    project.src_ext = ["java"]
    # TODO if no manifest, auto-generate (?)
    #  note: first, make sure theres another entry path into this method
    #  (only one is by detecting a manifest)
    project.javac_params = ["-Xlint:unchecked"]

    # TODO list dirs to clean (so clean step can find them), and add clean step
    project.clean = []

def update(project):
    project.clean += ["%s/%s.jar" % (project.output_path, project.name) , "%s/**.class" % project.classdir]
    project.steps = [Plugin("steps","clean","clean")] + project.steps

    added = False

    # if signing is supported by the user, attempt it automatically
    if sign.jarsigner.compatible(project) & Support.USER:
        # if project needs to be obfuscated, add signing after that
        #  otherwise add it after compilation (this step)
        i = 0
        for s in project.steps:
            if s.type == "obfuscate":
                project.steps.insert(i+1, Plugin("steps", "sign", "jarsigner"))
                added = True
            i += 1

        i = 0
        if not added:
            if s.type == "make" and s.name == "javac":
                project.steps.insert(i+1, Plugin("steps", "sign", "jarsigner"))
                added = True
            i += 1

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    
    # TODO turn this into a detect
    for fn in os.listdir("."):
        if os.path.isfile(fn):
            if fn.lower().endswith(".mf"):
                project.manifest = fn    
                set_defaults(project)
                support |= Support.PROJECT
                break

    return support

