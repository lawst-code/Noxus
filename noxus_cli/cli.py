import argparse

from .commands.build import build_command
from .commands.init import init_command
from .commands.serve import serve_command


def main():
    parser = argparse.ArgumentParser(description="Basic Noxus CLI tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # "init" command
    init_parser = subparsers.add_parser("init", help="Initialize a new plugin")
    init_parser.add_argument("plugin_name", help="Name of the plugin to be created")
    init_parser.set_defaults(func=init_command)

    # "serve" command
    serve_parser = subparsers.add_parser("serve", help="Start the API server")
    serve_parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to (default: 8000)"
    )
    serve_parser.add_argument("--plugin", help="Path to plugin YAML configuration file")
    serve_parser.set_defaults(func=serve_command)

    # "build" command
    build_parser = subparsers.add_parser(
        "build", help="Build Docker files for the current plugin"
    )
    build_parser.set_defaults(func=build_command)

    args = parser.parse_args()

    # Call the appropriate function based on the command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
