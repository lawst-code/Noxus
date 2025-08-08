# Noxus HTTP Server package
__version__ = "0.1.0"

from .server import app, start_server

__all__ = ["start_server", "app"]
