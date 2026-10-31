class FilesystemGuard:
    def __init__(self):
        self.read_only = True

    def get_status(self):
        return {
            "read_only": self.read_only
        }
