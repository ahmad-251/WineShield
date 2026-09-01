import json
import subprocess
from pathlib import Path


class AppRegistry:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "wineshield"
        self.apps_file = self.config_dir / "apps.json"

    def _query_registry(self, key):
        result = subprocess.run(
            [
                "wine",
                "reg",
                "query",
                key,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"Failed to query Wine registry: {key}")

            if result.stderr:
                print(result.stderr.strip())

            return None

        return result.stdout

    def update(self):
        uninstall_key = (
            r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall"
        )

        registry_output = self._query_registry(uninstall_key)

        if registry_output is None:
            return

        app_keys = []

        for line in registry_output.splitlines():
            line = line.strip()

            if line.startswith("HKEY_"):
                app_keys.append(line)

        apps_data = {}

        for app_key in app_keys:
            app_output = self._query_registry(app_key)

            if app_output is None:
                continue

            name = None
            version = None
            executable = None

            for line in app_output.splitlines():
                line = line.strip()

                if line.startswith("DisplayName"):
                    parts = line.split("REG_SZ", 1)

                    if len(parts) == 2:
                        name = parts[1].strip()

                elif line.startswith("DisplayVersion"):
                    parts = line.split("REG_SZ", 1)

                    if len(parts) == 2:
                        version = parts[1].strip()

                elif line.startswith("DisplayIcon"):
                    parts = line.split("REG_SZ", 1)

                    if len(parts) == 2:
                        executable = parts[1].strip()

            if name:
                apps_data[name] = {
                    "version": version,
                    "executable": executable,
                }

        self.config_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.apps_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                apps_data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        print(
            f"Application registry updated: {self.apps_file}"
        )

        print()

        self.print_apps()

    def load(self):
        if not self.apps_file.exists():
            return {}

        try:
            with self.apps_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except json.JSONDecodeError:
            print(
                f"Invalid application registry file: "
                f"{self.apps_file}"
            )
            return {}

        except OSError as error:
            print(
                f"Could not read application registry: {error}"
            )
            return {}

    def print_apps(self):
        apps_data = self.load()

        if not apps_data:
            print("No applications found.")
            return

        print(
            f"{'Name':<30} "
            f"{'Version':<15} "
            f"{'Executable'}"
        )

        print("-" * 100)

        for name, info in apps_data.items():
            version = info.get("version") or "-"
            executable = info.get("executable") or "-"

            print(
                f"{name:<30} "
                f"{version:<15} "
                f"{executable}"
            )

    def find(self, app_name):
        apps_data = self.load()

        search_name = app_name.lower()

        for name, info in apps_data.items():
            if search_name in name.lower():
                return {
                    "name": name,
                    "version": info.get("version"),
                    "executable": info.get("executable"),
                }

        return None