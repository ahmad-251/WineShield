import os
import subprocess


def parse_memory(value):
    units = {"k": 1024, "m": 1024**2, "g": 1024**3}
    value = value.strip().lower()
    if value[-1] in units:
        return int(value[:-1]) * units[value[-1]]
    return int(value)


class FirejailBackend:
    def build_command(self, cmd, profile):
        prefix = []
        args = [
            "firejail",
            "--noprofile",
            "--noroot",
            "--caps.drop=all",
            "--nonewprivs",
        ]
        if profile is not None:
            prefix = [
                "systemd-run", "--user", "--scope", "--quiet",
                "-p", f"MemoryMax={profile.memory_limit.upper()}",
                "-p", f"CPUQuota={int(profile.cpu_limit * 100)}%",
                "-p", f"TasksMax={profile.pids_limit}",
            ]
            private_home = getattr(profile, "private_home", None)
            if private_home:
                os.makedirs(private_home, exist_ok=True)
                args.append(f"--private={private_home}")
            wine_prefix = getattr(profile, "wine_prefix", None)
            if wine_prefix:
                if not getattr(profile, "private_home", None):
                    raise RuntimeError("wine_prefix requires private_home")
                args.append(f"--env=WINEPREFIX={os.path.expanduser('~')}/{wine_prefix}")
            if getattr(profile, "read_only", False):
                args += [
                    "--private-tmp",
                    "--private-dev",
                    "--blacklist=/mnt",
                    "--blacklist=/media",
                    "--blacklist=/boot",
                    "--private-etc=alternatives,ld.so.cache,ld.so.conf,ld.so.conf.d,fonts,passwd,group,nsswitch.conf,localtime,ssl,ca-certificates,wine",
                ]
            if getattr(profile, "network_disabled", False):
                args.append("--net=none")
            if getattr(profile, "limit_virtual_memory", False):
                args.append(f"--rlimit-as={parse_memory(profile.memory_limit)}")
        return prefix + args + cmd

    def run(self, cmd, profile):
        args = self.build_command(cmd, profile)
        return subprocess.run(args, capture_output=True, text=True)
