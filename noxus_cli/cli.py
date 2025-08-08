import argparse
import importlib.resources as resources

from http_server.server import start_server


def init_command(args):
    """Handle the init command"""
    plugin_name = args.plugin_name
    filename = f"{plugin_name}.yaml"
    
    try:
        template_content = (resources.files('noxus_cli') / 'plugin_template.yaml').read_text()
        yaml_content = template_content.format(plugin_name=plugin_name)
    except Exception as e:
        print(f"Error reading template file: {e}")
        return
    
    with open(filename, 'w') as f:
        f.write(yaml_content)
    
    print(f"Created {filename} in current directory")

def serve_command(args):
    """Handle the serve command"""
    print(f"Starting Noxus API server on {args.host}:{args.port}")
    print(f"OpenAPI documentation available at:")
    print(f"  - Swagger UI: http://{args.host}:{args.port}/docs")
    print(f"  - ReDoc: http://{args.host}:{args.port}/redoc")
    start_server(host=args.host, port=args.port)

def main():
    parser = argparse.ArgumentParser(description="Basic Noxus CLI tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # "init" command
    init_parser = subparsers.add_parser('init', help='Initialize a new plugin')
    init_parser.add_argument('plugin_name', help='Name of the plugin to be created')
    init_parser.set_defaults(func=init_command)
    
    # "serve" command
    serve_parser = subparsers.add_parser('serve', help='Start the API server')
    serve_parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    serve_parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    serve_parser.set_defaults(func=serve_command)

    args = parser.parse_args()
    
    # Call the appropriate function based on the command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()