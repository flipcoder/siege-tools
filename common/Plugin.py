import importlib

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
        try:
            return getattr(self.lib, method)(*params)
        except:
            pass
    def __eq__(self, other):
        return self.folder == other.folder and self.type == other.type and self.name == other.name

