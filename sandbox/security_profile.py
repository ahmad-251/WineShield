import os
class SecurityProfile:
    def __init__(self):
        self.memory_limit = "512m"
        self.cpu_limit = 1
        self.read_only = True
        self.pids_limit = 100
        self.network_disabled = True
        self.private_home = os.path.expanduser("~/wineshield/prefix_home")
        self.wine_prefix = ".wine"
