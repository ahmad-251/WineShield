from security_profile import SecurityProfile
from container_manager import ContainerManager
from filesystem_guard import FilesystemGuard


profile = SecurityProfile()
filesystem = FilesystemGuard()
manager = ContainerManager()

print("WineShield Sandbox Engine")
print("-------------------------")

result = manager.create_container(profile, filesystem)

print(result)
