from pathlib import Path

import yaml

from ..utils import get_template_content


def build_command(args):
    """Handle the build command"""
    current_dir = Path.cwd()

    # Look for YAML files in current directory
    yaml_files = list(current_dir.glob("*.yaml"))

    if not yaml_files:
        print("Error: No YAML configuration file found in current directory")
        print("Make sure you're in a plugin directory with a .yaml file")
        return

    # Use the first YAML file found
    yaml_file = yaml_files[0]

    try:
        # Load YAML configuration
        with open(yaml_file, "r") as f:
            config = yaml.safe_load(f)

        plugin_name = config.get("name")
        if not plugin_name:
            print(f"Error: No 'name' field found in {yaml_file}")
            return

        print(f"Building Docker files for plugin: {plugin_name}")

        # Get templates
        dockerfile_template = get_template_content("Dockerfile.template")
        compose_template = get_template_content("docker-compose.standalone.template")

        if not dockerfile_template or not compose_template:
            print("Error: Could not load Docker templates")
            return

        # Format templates with plugin info
        dockerfile_content = dockerfile_template.format(
            plugin_name=plugin_name, yaml_file=yaml_file.name
        )

        compose_content = compose_template.format(
            plugin_name=plugin_name, yaml_file=yaml_file.name
        )

        # Write Dockerfile
        dockerfile_path = current_dir / "Dockerfile"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)

        # Write docker-compose file
        compose_path = current_dir / f"docker-compose.{plugin_name}.standalone.yml"
        with open(compose_path, "w") as f:
            f.write(compose_content)

        print("Created Docker files:")
        print("  - Dockerfile")
        print(f"  - {compose_path.name}")
        print("\nTo build and run:")
        print(f"  docker-compose -f {compose_path.name} up --build")

    except Exception as e:
        print(f"Error building Docker files: {e}")
        return
