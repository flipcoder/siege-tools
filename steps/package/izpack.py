import os
import sgmake
from common import *


def package(project):
    wdir = os.getcwd()
    os.chdir(os.path.join(wdir, os.path.dirname(project.izpack_file)))

    try:
        os.system(
            "%s %s"
            % (
                os.path.join(project.izpack_dir, project.izpack_binary),
                os.path.basename(project.izpack_file),
            )
        )
    except:
        pass

    os.chdir(wdir)
    return Status.SUCCESS


def update(project):
    # project.clean_commands += ["install.jar"] # requires clean as a step
    pass


def compatible(project):
    support = Support.AUTO | Support.ENVIRONMENT

    for fn in ("izpack.xml", "izpack%sizpack.xml" % os.sep):
        if os.path.isfile(os.path.join(os.getcwd(), fn)):
            project.izpack_file = fn
            support |= Support.PROJECT
            break

    # only test for user compatibility if the project needs this plug-in
    if support & Support.PROJECT:
        project.izpack_dir = Settings.get("izpack_path")
        if project.izpack_dir:
            support |= Support.USER
        if os.name == "nt":
            project.izpack_binary = "compile.bat"
        else:
            project.izpack_binary = "compile"

    return support
