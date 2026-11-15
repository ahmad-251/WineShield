class FilesystemGuard:
    def __init__(self):
        self.filesystem_isolation = True

    def get_status(self):
        return {
            "filesystem_isolation": self.filesystem_isolation
        }
