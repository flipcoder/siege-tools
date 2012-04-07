#!/usr/bin/env python
import os
import sgmake
from common import Settings
from common import Args

class Project(sgmake.Project):
    def __init__(self):
        sgmake.Project.__init__(self)

        self.manifest = ""
        for fn in os.listdir("."):
            if os.path.isfile(fn):
                if fn.lower().endswith(".mf"):
                    self.manifest = fn

        self.name = os.path.basename(os.path.abspath(os.getcwd()))
        self.sourcepath = ["src"]
        self.classpath = ["lib","libs"]
        self.obfuscator = None
        self.output = None
        self.classdir = "bin"
        self.outputdir = "dist"
        self.language = "java"
        self.src_ext = ["java"]
        self.bin_ext = "jar"
        self.steps = ("clean","make","obfuscate","sign","package","install")
        self.javac_params = ["-Xlint:unchecked"]
        self.run_user_script()

        self.status = sgmake.Status.SUCCESS

    @staticmethod
    def compatible():
        for fn in os.listdir("."):
            if os.path.isfile(fn):
                if fn.lower().endswith(".mf"):
                    return True
        return False

    def clean(self):
        os.remove(os.path.join(self.outputdir, "%s%s%s" % (self.name, "." if self.bin_ext else "",self.bin_ext)))
        # TODO: try to delete class files in classdir
        return sgmake.Status.SUCCESS

    def make(self):
        for folder in self.sourcepath:
            if not os.path.isdir(os.path.join(os.getcwd(), folder)):
                return Status.FAILURE

        for folder in (self.classdir,self.outputdir):
            try:
                os.mkdir(os.path.join(os.getcwd(), folder))
            except OSError:
                pass

        classpath = ""
        #classpathlist = os.pathsep.join(self.classpath)

        for entry in self.classpath:
            if os.path.isfile(entry):
                if classpath:
                    classpath += os.pathsep + entry
                else:
                    classpath = entry
                continue
            for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
                for fn in files:
                    if fn.lower().endswith(".%s" % self.bin_ext):
                        rel_path = os.path.relpath(path,fn)
                        rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                        if classpath:
                            classpath = os.pathsep.join((classpath, os.path.join(rel_path,fn)))
                        else:
                            classpath = os.path.join(rel_path,fn)

        if classpath:
            classpath = os.pathsep.join((classpath, os.pathsep.join(self.classpath)))
        else:
            classpath = os.pathsep.join(self.classpath)

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
                    for ext in self.src_ext:
                        if fn.lower().endswith(".%s" % ext):
                            rel_path = os.path.relpath(path,fn)
                            rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                            if sourcepath:
                                sourcepath = "%s %s" % (sourcepath, os.path.join(rel_path,fn))
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
        # removed: -source 1.6 -target 1.6 
        misc_params = " ".join(self.javac_params)
        os.system("%sjavac %s -d %s %s -cp %s" % (self.javapath, misc_params, self.classdir, sourcepath, classpath))
        os.system("%sjar cmf %s %s -C %s ." % (self.javapath, self.manifest, self.output, self.classdir))
        # TODO wrap stdout from above commands and detect errors
        
        if not os.path.isfile(self.output):
            return sgmake.Status.FAILURE

        return sgmake.Status.SUCCESS

    def obfuscate(self):
        if self.obfuscator: # obfuscator used for project
            #try:
            obf_path = Settings.get("%s_path" % self.obfuscator)
            if not obf_path:
                return sgmake.Status.UNSUPPORTED
            obf_path = os.path.abspath(obf_path)
            if not os.path.isfile(obf_path):
                return sgmake.Status.FAILURE
            os.system(self.javapath + "java -jar " + obf_path + " " + self.obfuscator_params)
            #except:
            #    return sgmake.Status.UNSUPPORTED

            return sgmake.Status.SUCCESS

        return sgmake.Status.UNSUPPORTED

    def sign(self):
        #try:
        os.system("%sjarsigner -storepass %s %s %s" % (self.javapath, Settings.get("keystore_pass"), self.output, Settings.get("keystore_name")))
        
        # sign libs too (TODO: make optional)
        for classpath_dir in self.classpath:
            if os.path.isdir(classpath_dir):
                for fn in os.listdir(classpath_dir):
                    if fn.lower().endswith(".%s" % self.bin_ext):
                        os.system("%sjarsigner -storepass %s %s %s" % (self.javapath, Settings.get("keystore_pass"), os.path.join(classpath_dir,fn), Settings.get("keystore_name")))
                            
            # TODO: if system call returns with error, then return Status.FAILURE, regardless of --strict
        #except:
        #    return sgmake.Status.FAILURE
            #return sgmake.Status.FAILURE if Args.option("strict") else sgmake.Status.UNSUPPORTED

        return sgmake.Status.SUCCESS
    
    def package(self):
        return sgmake.Status.UNSUPPORTED
    def install(self):
        return sgmake.Status.UNSUPPORTED

