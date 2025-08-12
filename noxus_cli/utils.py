import importlib.resources as resources
import importlib.util
import sys
from pathlib import Path

import yaml


def get_template_content(template_name: str) -> str:
    """Get content from a template file in the noxus_cli package."""
    try:
        return (resources.files("noxus_cli") / "templates" / template_name).read_text()
    except Exception as e:
        print(f"Error reading template file {template_name}: {e}")
        return ""


def load_plugin_from_yaml(yaml_path: str):
    """
    Load a plugin from a YAML configuration file.

    Args:
        yaml_path: Path to the YAML configuration file

    Returns:
        Plugin instance
    """
    yaml_path = Path(yaml_path)

    if not yaml_path.exists():
        raise FileNotFoundError(f"Plugin configuration file not found: {yaml_path}")

    # Load YAML configuration
    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    # Get plugin file path (relative to YAML file location)
    plugin_file = config.get("plugin_file")
    if not plugin_file:
        raise ValueError(f"No 'plugin_file' specified in {yaml_path}")

    # Resolve plugin file path
    plugin_file_path = yaml_path.parent / plugin_file

    if not plugin_file_path.exists():
        raise FileNotFoundError(f"Plugin file not found: {plugin_file_path}")

    # Load the plugin module
    module_name = f"plugin_module_{plugin_file_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, plugin_file_path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load plugin module: {plugin_file_path}")

    module = importlib.util.module_from_spec(spec)

    # Add the plugin directory to sys.path for imports
    plugin_dir = plugin_file_path.parent
    if str(plugin_dir) not in sys.path:
        sys.path.insert(0, str(plugin_dir))

    try:
        spec.loader.exec_module(module)

        # Find the plugin class (should be the only class that inherits from Plugin)
        from domain.plugins import Plugin

        plugin_class = None
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(obj, "__bases__") and Plugin in obj.__bases__ and obj != Plugin:
                plugin_class = obj
                break

        if plugin_class is None:
            raise ImportError(f"No Plugin class found in {plugin_file_path}")

        # Instantiate and return the plugin
        return plugin_class()

    finally:
        # Clean up sys.path
        if str(plugin_dir) in sys.path:
            sys.path.remove(str(plugin_dir))
