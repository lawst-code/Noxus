import importlib.util
import inspect
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from domain.plugins import Plugin


class PluginLoader:
    """
    Dynamically discovers and loads plugins from specified directories.
    """

    def __init__(self, plugin_directories: List[str] = None):
        """
        Initialize the plugin loader.

        Args:
            plugin_directories: List of directories to search for plugins.
                               Defaults to ['plugins/'] relative to current directory.
        """
        if plugin_directories is None:
            plugin_directories = ["plugins/"]

        self.plugin_directories = [Path(dir) for dir in plugin_directories]
        self.loaded_plugins: List[Plugin] = []

    def discover_plugins(self) -> List[str]:
        """
        Discover all plugin files in the plugin directories.

        Returns:
            List of plugin file paths
        """
        plugin_files = []

        for plugin_dir in self.plugin_directories:
            if not plugin_dir.exists():
                print(f"Warning: Plugin directory {plugin_dir} does not exist")
                continue

            # Look for plugin.py files in subdirectories
            for plugin_path in plugin_dir.rglob("plugin.py"):
                plugin_files.append(str(plugin_path))

            # Also look for any .py files directly in plugin directories
            for py_file in plugin_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    plugin_files.append(str(py_file))

        return plugin_files

    def load_plugin_from_file(self, file_path: str) -> List[Plugin]:
        """
        Load a plugin from a specific file.

        Args:
            file_path: Path to the plugin.py file

        Returns:
            List of plugin instances found in the file
        """
        plugins = []

        try:
            # Create module spec and load the module
            module_name = f"plugin_module_{hash(file_path)}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                print(f"Warning: Could not load spec for {file_path}")
                return plugins

            module = importlib.util.module_from_spec(spec)

            # Add the module's directory to sys.path temporarily for relative imports
            module_dir = os.path.dirname(file_path)
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
                remove_from_path = True
            else:
                remove_from_path = False

            try:
                spec.loader.exec_module(module)

                # Find all classes that inherit from Plugin
                for name in dir(module):
                    obj = getattr(module, name)

                    # Check if it's a class that inherits from Plugin (but isn't Plugin itself)
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, Plugin)
                        and obj is not Plugin
                    ):
                        try:
                            # Instantiate the plugin
                            plugin_instance = obj()
                            plugins.append(plugin_instance)
                            plugin_title = getattr(plugin_instance, "title", name)
                            print(f"Loaded plugin: {plugin_title}")
                        except Exception as e:
                            print(f"Could not instantiate plugin {name}: {e}")

            finally:
                # Clean up sys.path
                if remove_from_path and module_dir in sys.path:
                    sys.path.remove(module_dir)

        except Exception as e:
            print(f"Error loading plugin from {file_path}: {e}")

        return plugins

    def load_builtin_plugins(self) -> List[Plugin]:
        """
        Load plugins from the domain package itself.

        Returns:
            List of built-in plugin instances
        """
        plugins = []

        try:
            from domain.plugins import SentimentPlugin

            plugins.append(SentimentPlugin())
            print("Loaded built-in plugin: SentimentPlugin")
        except Exception as e:
            print(f"Error loading built-in plugins: {e}")

        return plugins

    def load_all_plugins(self) -> List[Plugin]:
        """
        Discover and load all plugins from configured directories + built-ins.

        Returns:
            List of all loaded plugin instances
        """
        self.loaded_plugins = []

        # Load built-in plugins first
        builtin_plugins = self.load_builtin_plugins()
        self.loaded_plugins.extend(builtin_plugins)

        # Discover and load external plugins
        plugin_files = self.discover_plugins()
        print(f"Discovered {len(plugin_files)} plugin files")

        for plugin_file in plugin_files:
            plugins = self.load_plugin_from_file(plugin_file)
            self.loaded_plugins.extend(plugins)

        print(f"Successfully loaded {len(self.loaded_plugins)} total plugins")
        return self.loaded_plugins

    def get_all_nodes(self) -> Dict[str, Any]:
        """
        Get all nodes from all loaded plugins, indexed by node name.

        Returns:
            Dictionary mapping node names to node instances
        """
        all_nodes = {}

        for plugin in self.loaded_plugins:
            try:
                nodes = plugin.nodes()
                for node in nodes:
                    node_name = getattr(node, "name", None)
                    if node_name:
                        if node_name in all_nodes:
                            print(f" Warning: Duplicate node name '{node_name}' found")
                        all_nodes[node_name] = node
                        print(f"Registered node: {node_name}")
            except Exception as e:
                plugin_name = getattr(plugin, "title", "Unknown")
                print(f"Error getting nodes from plugin {plugin_name}: {e}")

        return all_nodes

    def get_plugin_info(self) -> List[Dict]:
        """
        Get information about all loaded plugins.

        Returns:
            List of dictionaries containing plugin information
        """
        plugin_info = []

        for plugin in self.loaded_plugins:
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
