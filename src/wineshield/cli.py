import argparse
import sys

from .wine import Wine
from .app_registry import AppRegistry

VERSION = "0.1.0"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wineshield",
        description=(
            "WineShield is a command-line tool for managing and running "
            "Windows applications through Wine."
        ),
        epilog="""
Examples:
  wineshield list
      Show the Windows applications currently known to WineShield.

  wineshield update-appslist
      Scan the Wine registry and update WineShield's application list.

  wineshield run notepad++
      Find Notepad++ in the application list and run it through Wine.

  wineshield wine --version
      Pass '--version' directly to Wine.

  wineshield wine notepad++.exe
      Pass 'notepad++.exe' directly to Wine.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        metavar="{wine,run,list,update-appslist}",
    )

    # wine command
    subparsers.add_parser(
        "wine",
        help="Pass arguments directly to Wine.",
        description=(
            "Pass everything after 'wineshield wine' directly to Wine.\n\n"
            "Example:\n"
            "  wineshield wine --version\n\n"
            "This behaves approximately like:\n"
            "  wine --version"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a Windows application by name.",
        description=(
            "Run a Windows application using the application information "
            "stored by WineShield.\n\n"
            "Example:\n"
            "  wineshield run notepad++"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    run_parser.add_argument(
        "app_name",
        help="Name of the Windows application to run.",
    )

    # list command
    subparsers.add_parser(
        "list",
        help="Show Windows applications known to WineShield.",
        description=(
            "Display the applications currently stored in WineShield's "
            "application registry.\n\n"
            "This command does not rescan Wine automatically.\n"
            "Use 'wineshield update-appslist' to refresh the list."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # update-appslist command
    subparsers.add_parser(
        "update-appslist",
        help="Update the Windows application registry.",
        description=(
            "Scan the Wine registry for installed Windows applications and "
            "save the discovered applications to WineShield's local registry.\n\n"
            "Example:\n"
            "  wineshield update-appslist"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    return parser


def main() -> None:
    # The "wine" command is handled before argparse so every argument after
    # "wine" can be passed to Wine without WineShield interpreting it.
    if len(sys.argv) > 1 and sys.argv[1] == "wine":
        wine_args = sys.argv[2:]

        wine = Wine(wine_args)
        wine.run()

        return

    parser = create_parser()
    args = parser.parse_args()
    registry = AppRegistry()

    # Show help when WineShield is executed without a command.
    if args.command is None:
        parser.print_help()
        return


    if args.command == "run":
        app = registry.find(args.app_name)

        if app is None:
            print(f"Application not found: {args.app_name}")
            return

        executable = app["executable"]

        if not executable:
            print(f"Executable path not found for: {app['name']}")
            return

        runner = Wine([executable])
        runner.run()
        return

    if args.command == "list":
        registry.print_apps()
        return

    if args.command == "update-appslist":
        registry.update()
        return


if __name__ == "__main__":
    main()