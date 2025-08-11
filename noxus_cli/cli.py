import argparse
import importlib.resources as resources
import os
from pathlib import Path

from http_server.server import start_server


def get_template_content(template_name: str) -> str:
    """Get content from a template file in the noxus_cli package."""
    try:
        return (resources.files("noxus_cli") / template_name).read_text()
    except Exception as e:
        print(f"Error reading template file {template_name}: {e}")
        return ""


def format_plugin_name(plugin_name: str) -> dict:
    """Format plugin name for use in templates."""
    # Convert to title case and remove separators for class names
    class_name = plugin_name.title().replace("_", "").replace("-", "")

    return {
        "plugin_name": plugin_name,
        "plugin_name_lower": plugin_name.lower(),
        "plugin_class_name": class_name,
        "plugin_title": plugin_name.title().replace("_", " ").replace("-", " "),
    }


def init_command(args):
    """Handle the init command"""
    plugin_name = args.plugin_name
    formats = format_plugin_name(plugin_name)

    # Create plugin directory
    plugin_dir = Path(plugin_name)
    plugin_dir.mkdir(exist_ok=True)

    # Create plugin Python file
    plugin_template = get_template_content("plugin_template.py.txt")
    if plugin_template:
        plugin_py_content = plugin_template.format(**formats)
        plugin_py_file = plugin_dir / f"{plugin_name}.py"
        with open(plugin_py_file, "w") as f:
            f.write(plugin_py_content)

    # Create runner script
    runner_template = get_template_content("runner_template.py.txt")
    if runner_template:
        runner_content = runner_template.format(**formats)
        runner_file = plugin_dir / f"run_{plugin_name}.py"
        with open(runner_file, "w") as f:
            f.write(runner_content)

    # Create YAML configuration file
    yaml_template = get_template_content("plugin_template.yaml")
    if yaml_template:
        yaml_content = yaml_template.format(**formats)
        yaml_file = plugin_dir / f"{plugin_name}.yaml"
        with open(yaml_file, "w") as f:
            f.write(yaml_content)

    print(f"Created plugin directory: {plugin_dir}")
    print("Created files:")
    print(f"  - {plugin_name}.py")
    print(f"  - run_{plugin_name}.py")
    print(f"  - {plugin_name}.yaml")
    print(
        f"Plugin ready! Run 'noxus serve {plugin_name}/{plugin_name}.yaml' to start a test server."
    )


def serve_command(args):
    """Handle the serve command"""
    current_dir = os.getcwd()

    print(f"Starting Noxus API server on {args.host}:{args.port}")
    print("OpenAPI documentation available at:")
    print(f"  - Swagger UI: http://{args.host}:{args.port}/docs")
    print(f"  - ReDoc: http://{args.host}:{args.port}/redoc")

    start_server(host=args.host, port=args.port, plugins_dir=current_dir)


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
    serve_parser.set_defaults(func=serve_command)

    args = parser.parse_args()

    # Call the appropriate function based on the command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
