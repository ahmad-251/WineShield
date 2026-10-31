from security_profile import SecurityProfile
from filesystem_guard import FilesystemGuard
from firejail_backend import FirejailBackend


def main():
    profile = SecurityProfile()
    guard = FilesystemGuard()
    backend = FirejailBackend()

    print("Filesystem policy:", guard.get_status())

    result = backend.run(
        ["bash", "-c", "echo WineShield Sandbox is running!"],
        profile,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("Error:", result.stderr)


if __name__ == "__main__":
    main()
