import importlib
import sys

class Plugin(object):
    def __init__(self, folder, type, name):
        self.folder = folder
        self.type = type
        self.name = name
        self.lib = importlib.import_module("%s.%s" % (self.type, self.name))
    def str(self):
        return self.name
    def len(self):
        return len(self.name)
    def call(self, method, *params):
        attr = None
        try:
            attr = getattr(self.lib, method)
        except:
            #print "Invalid attr: %s(%s)" % (self.lib,method)
            return

        try:
            return attr(*params)
        except:
            print "plug-in method %s(%s) threw exception" % (self.lib, method)
            print sys.exc_info()
            return Status.FAILURE

    def __eq__(self, other):
        return self.folder == other.folder and self.type == other.type and self.name == other.name

