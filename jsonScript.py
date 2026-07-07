import json
import os, shutil, sys

# version = "1.0"
# Made by Qunalpha

class jsonFileManagment():
    def __init__(self, name, tuple_list, indent: int=4):
        """Make sure the (name) parameter is a string with .json as file type\n
        for example - 'file.json'"""

        self.name = name
        self.default = dict(tuple_list)
        self.indent = indent

    def load(self):
        if not os.path.exists(self.name):
                with open(self.name, "w") as file:
                    json.dump(self.default, file, indent=self.indent)
                return self.default
        with open(self.name, "r") as file:
            return json.load(file)
        
    def save(self, value):
        with open(self.ensure_writable_resource(self.name), "w") as file:
            json.dump(value, file, indent=4)

    def ensure_writable_resource(self, filename):
        user_path = os.path.join(os.getcwd(), filename)
        if not os.path.exists(user_path):
            bundled_path = self.resource_path(filename)
            shutil.copyfile(bundled_path, user_path)
        return user_path
    
    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)