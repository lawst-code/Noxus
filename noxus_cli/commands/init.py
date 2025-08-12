import importlib.resources as resources
from pathlib import Path


def get_template_content(template_name: str) -> str:
    """Get content from a template file in the noxus_cli package."""
    try:
        return (resources.files("noxus_cli") / "templates" / template_name).read_text()
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

    # Create YAML configuration file
    yaml_template = get_template_content("plugin_template.yaml")
    if yaml_template:
        yaml_content = yaml_template.format(**formats)
        yaml_file = plugin_dir / f"{plugin_name}.yaml"
        with open(yaml_file, "w") as f:
            f.write(yaml_content)

    # Create pyproject.toml for standalone deployment
    pyproject_template = get_template_content("pyproject.toml.template")
    if pyproject_template:
        pyproject_content = pyproject_template.format(**formats)
        pyproject_file = plugin_dir / "pyproject.toml"
        with open(pyproject_file, "w") as f:
            f.write(pyproject_content)

    print(f"Created plugin directory: {plugin_dir}")
    print("Created files:")
    print(f"  - {plugin_name}.py")
    print(f"  - {plugin_name}.yaml")
    print(f"  - pyproject.toml")
    print(
        f"Plugin ready! Run 'noxus serve --plugin {plugin_name}/{plugin_name}.yaml' to start a test server."
    )
