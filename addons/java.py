#!/usr/bin/env python
import os
from sgmake import *

class Java(Project):
    def __init__(self):
        Project.__init__(self)

        self.manifest = ""
        for fn in os.listdir("."):
            if os.path.isfile(fn):
                if fn.lower().endswith(".mf"):
                    self.manifest = fn

        self.name = os.path.basename(os.path.abspath(os.getcwd()))
        self.sourcepath = ["src"]
        self.classpath = []
        self.obfuscator = None
        self.output = None
        self.build_sys = "java"
        self.steps = ("clean","configure","make","obfuscate","sign","package","install")

        self.run_user_script()

        self.status = Status.SUCCESS

    @staticmethod
    def compatible():
        for fn in os.listdir("."):
            if os.path.isfile(fn):
                if fn.lower().endswith(".mf"):
                    return True
        return False

    def clean(self):
        try:
            os.remove("dist"+os.sep+self.name+".jar")
        except OSError:
            pass
        return Status.SUCCESS

    def configure(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "src")):
            return Status.FAILURE

        for folder in ("bin","dist"):
            try:
                os.mkdir(os.path.join(os.getcwd(), folder))
            except OSError:
                pass

        return Status.SUCCESS

    def make(self):
        classpath = "."
        
        classpathlist = []
        classpathlist += ("lib", "libs")
        if self.classpath:
            classpathlist += self.classpath

        for entry in classpathlist:
            if os.path.isfile(entry):
                if classpath:
                    classpath = classpath + os.pathsep + entry
                else:
                    classpath = entry
                continue
            for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
                for fn in files:
                    if fn.lower().endswith(".jar"):
                        rel_path = os.path.relpath(path,fn)
                        rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                        if classpath:
                            classpath = classpath + os.pathsep + os.path.join(rel_path,fn)
                        else:
                            classpath = os.path.join(rel_path,fn)

        if classpath:
            classpath = classpath + os.pathsep + os.pathsep.join(self.classpath)
        else:
            classpath = string.join(self.classpath,os.pathsep)

        sourcepath = ""

        for entry in self.sourcepath:
            if os.path.isfile(entry):
                if sourcepath:
                    sourcepath = sourcepath + os.linesep + os.path.join(rel_path,fn)
                else:
                    sourcepath = os.path.join(rel_path,fn)
                continue
            for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
                for fn in files:
                    if fn.lower().endswith(".java"):
                        rel_path = os.path.relpath(path,fn)
                        rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                        if sourcepath:
                            sourcepath = sourcepath + " " + os.path.join(rel_path,fn)
                        else:
                            sourcepath = os.path.join(rel_path,fn)

        self.javapath = Settings.get('java_path')
        if self.javapath:
            if self.javapath[-1] != os.sep and os.altsep and Settings.get('java_path')[-1] != os.altsep:
                self.javapath += os.sep
        else:
            self.javapath = ""

        self.output = "dist"+os.sep+self.name+".jar"

        # TODO: boostrap class path
        os.system("%sjavac -Xlint:unchecked -source 1.6 -target 1.6 -d bin %s -cp %s" % (self.javapath, sourcepath, classpath))
        os.system("%sjar cmf %s "%(self.javapath, self.manifest)+"%s -C bin ." % (self.output))
        
        if not os.path.isfile(self.output):
            return Status.FAILURE

        return Status.SUCCESS

    def obfuscate(self):
        if self.obfuscator: # obfuscator used for project
            #try:
            obf_path = Settings.get("%s_path" % self.obfuscator)
            obf_path = os.path.abspath(obf_path)
            print self.javapath + "java -jar " + obf_path
            if not os.path.isfile(obf_path):
                return Status.FAILURE
            os.system(self.javapath + "java -jar " + obf_path + " " + self.obfuscator_params)
            #except:
            #    return Status.UNSUPPORTED

            return Status.SUCCESS

        return Status.UNSUPPORTED

    def sign(self):
        try:
            os.system("%sjarsigner -storepass %s %s %s" % (self.javapath, Settings.get("keystore_pass"), self.output, Settings.get("keystore_name")))
            
            # sign libs too (TODO: make optional)
            for classpath_dir in self.classpath:
                for fn in os.listdir(classpath_dir):
                    if fn.lower().endswith(".jar"):
                        os.system("%sjarsigner -storepass %s %s %s" % (self.javapath, Settings.get("keystore_pass"), os.path.join(classpath_dir,fn), Settings.get("keystore_name")))
                            
                            
            # TODO: if system call returns with error, then return Status.FAILURE, regardless of --strict
        except:
            return Status.FAILURE if Args.options["strict"] else Status.UNSUPPORTED

        return Status.SUCCESS
    
    def package(self):
        return Status.UNSUPPORTED
    def install(self):
        return Status.UNSUPPORTED

overload = Java
