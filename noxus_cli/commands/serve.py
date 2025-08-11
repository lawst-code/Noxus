import os

from http_server.server import start_server


def serve_command(args):
    """Handle the serve command"""
    current_dir = os.getcwd()

    print(f"Starting Noxus API server on {args.host}:{args.port}")
    print("OpenAPI documentation available at:")
    print(f"  - Swagger UI: http://{args.host}:{args.port}/docs")
    print(f"  - ReDoc: http://{args.host}:{args.port}/redoc")

    start_server(host=args.host, port=args.port, plugins_dir=current_dir)
