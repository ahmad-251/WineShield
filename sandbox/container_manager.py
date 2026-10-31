import docker


class ContainerManager:
    def __init__(self):
        self.client = docker.from_env()

    def test_connection(self):
        return self.client.ping()

    def create_container(self, profile, filesystem_guard):
        container = self.client.containers.run(
            "ubuntu:24.04",
            "echo WineShield Sandbox is running!",
            mem_limit=profile.memory_limit,
            read_only=filesystem_guard.read_only,
            detach=False,
            remove=True
        )

        return container.decode()
