from http_server.server import start_server

from ..utils import load_plugin_from_yaml


def serve_command(args):
    """Handle the serve command"""

    # Load plugin from YAML file
    if hasattr(args, "plugin") and args.plugin:
        try:
            plugin = load_plugin_from_yaml(args.plugin)
            print(f"Loaded plugin: {plugin.title}")
        except Exception as e:
            print(f"Error loading plugin: {e}")
            return

    print(f"Starting Noxus API server on {args.host}:{args.port}")
    print("OpenAPI documentation available at:")
    print(f"  - Swagger UI: http://{args.host}:{args.port}/docs")
    print(f"  - ReDoc: http://{args.host}:{args.port}/redoc")

    if plugin:
        start_server(host=args.host, port=args.port, plugin=plugin)