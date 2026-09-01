import subprocess


class Wine:
    def __init__(self, arguments=None):
        self.arguments = arguments or []

    def run(self):
        subprocess.run(
            ["wine"] + self.arguments
        )