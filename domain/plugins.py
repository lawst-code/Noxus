from abc import ABC, abstractmethod
from typing import List, Dict

from .nodes import ExampleNode, Node, SentimentNode


class Plugin(ABC):
    @abstractmethod
    def nodes(self) -> List[Node]:
        pass


class SentimentPlugin(Plugin):
    title = "Sentiment Plugin"

    def nodes(self):
        return [SentimentNode(), ExampleNode()]


def get_plugin_info(plugin: Plugin) -> Dict:
    """
    Get information about plugin.

    Returns:
        Dictionary containing plugin information
    """
    plugin_info = []

    info = {
        "title": getattr(plugin, "title", "Unknown Plugin"),
        "description": getattr(plugin, "description", "No description"),
        "nodes": [],
    }

    try:
        nodes = plugin.nodes()
        for node in nodes:
            node_info = {
                "name": getattr(node, "name", "Unknown"),
                "title": getattr(node, "title", "Unknown Node"),
                "description": getattr(node, "description", "No description"),
            }
            info["nodes"].append(node_info)
    except Exception as e:
        print(f"Error getting node info for plugin: {e}")

    plugin_info.append(info)

    return plugin_info


def get_plugins_info(plugins: List[Plugin]) -> List[Dict]:
    """
    Get information about all loaded plugins.

    Returns:
        List of dictionaries containing plugin information
    """
    plugin_info = []

    for plugin in plugins:
        info = {
            "title": getattr(plugin, "title", "Unknown Plugin"),
            "description": getattr(plugin, "description", "No description"),
            "nodes": [],
        }

        try:
            nodes = plugin.nodes()
            for node in nodes:
                node_info = {
                    "name": getattr(node, "name", "Unknown"),
                    "title": getattr(node, "title", "Unknown Node"),
                    "description": getattr(node, "description", "No description"),
                }
                info["nodes"].append(node_info)
        except Exception as e:
            print(f"Error getting node info for plugin: {e}")

        plugin_info.append(info)

    return plugin_info
