"""
Noxus - A plugin and node framework
"""

__version__ = "0.1.0"

from .nodes import Node
from .plugins import Plugin

__all__ = ["Node", "Plugin"]
