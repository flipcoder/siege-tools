#!/usr/bin/env python
import os, sys

app_settings = {}
def settings_load(fn):
    try:
        with open("~"+os.sep+fn) as source:
            eval(compile(source.read(), fn, 'exec'), {}, app_settings)
        return True
    except IOError:
        return False
for fn in (".sgrc", "_sgrc"):
    if settings_load(fn):
        break
def settings():
    return app_settings

class Project:
    def __init__(self, fn):
        self.error = False

        self.filename = fn
        self.name = os.path.basename(fn)

        self.build_sys = None

        self.obfuscator = None
        self.signer = None
        self.packager = None

        self.sourcepath = None
        self.classpath = None
        self.manifest = None
        
        # Build system
        if not self.build_sys:
            for fn in os.listdir("."):
                if os.path.isfile(fn):
                    fn_lower = fn.lower();
                    if fn_lower.endswith(".mf"):
                        self.build_sys = "java"
                        self.manifest = fn
                        self.classpath = []
                        self.sourcepath = ["src"]
                    elif fn_lower=="makefile":
                        self.build_sys = "make"
                        self.build_script = fn;
                    elif fn_lower=="premake4.lua" or fn_lower=="premake.lua":
                        self.build_sys = "premake"
                        self.build_script = fn;
                    elif fn_lower=="cmakelists.txt":
                        self.build_sys = "cmake"
                        self.build_script = fn;

        # Project config
        for fn in os.listdir("."):
            if (fn.lower()=="sg.py" or fn.lower().endswith(".sg.py") and len(fn.lower())>len(".sg.py")) and os.path.isfile(os.path.join(os.getcwd(), fn)):
                with open(fn) as source:
                    eval(compile(source.read(), fn, 'exec'), {}, self.__dict__)

        if not self.build_sys:
            self.error = True
            return

        print("Found %s (%s)" % (self.name, self.build_sys))

    def configure(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "src")):
            return False

        for folder in ("bin","dist"):
            try:
                os.mkdir(os.path.join(os.getcwd(), folder))
            except OSError:
                pass

        # TODO: Add more languages
        if not self.build_sys == "java":
            return False

        return True

    def make(self):
        
        classpath = ".";
        
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
        

        #f = open("sg-cache"+os.sep+"classpath_file_list", "w");
        #f.write(classpath);
        #f.close()

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

        #f = open("sg-cache"+os.sep+"source_file_list", "w");
        #f.write(sourcepath);
        #f.close()

        #print(classpath_param)
        os.system("javac -Xlint:unchecked -source 1.6 -target 1.6 -d bin  %s -cp %s" % (sourcepath, classpath))
        os.system("jar cmf %s dist"%(self.manifest)+os.sep+"%s.jar -C bin ." % (self.name))

        return True

    def obfuscate(self):
        return True

    def sign(self):
        return True

    def package(self):
        return True

    def install(self):
        return True

    def complete(self):
        print("Configuring %s..." % self.name)
        if not self.configure():
            return False
        print("Configured %s." % self.name)

        print("Building %s..." % self.name)
        if not self.make():
            return False
        print("Built %s." % self.name)

        if self.obfuscator:
            print("Obfuscating %s..." % self.name)
            if not self.obfuscate():
                return False
            print("Obfuscated %s." % self.name)

        if self.signer:
            print("Signing %s..." % self.name)
            if not self.sign():
                return False
            print("Signed %s." % self.name)

        if self.packager:
            print("Packaging %s..." % self.name)
            if not self.package():
                return False
            print("Packaged %s." % self.name)

        print("Installing %s..." % self.name)
        if not self.install():
            return False
        print("Installed %s." % self.name)

        return True
       
def main():
    wdir = os.getcwd();
    built_count = 0
    failed_count = 0

    project = Project(wdir)
    if not project.error:
        if project.complete():
            built_count = built_count + 1
        else:
            failed_count = failed_count + 1

    # recurse once if no project
    if project.error:
        for fn in os.listdir("."):
            if fn.startswith("."):
                continue
            if not os.path.isdir(os.path.join(wdir, fn)):
                continue
            if os.path.islink(os.path.join(wdir, fn)):
                continue

            os.chdir(os.path.join(wdir, fn));
            project = Project(fn)
            if not project.error:
                if project.complete():
                    built_count = built_count + 1
                else:
                    failed_count = failed_count + 1
            os.chdir(wdir)

    if failed_count:
        print("%s project(s) failed." % failed_count)
    print("%s project(s) completed." % built_count)

if __name__ == "__main__":
    main()

