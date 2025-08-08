import argparse
import importlib.resources as resources


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

def main():
    parser = argparse.ArgumentParser(description="Basic Noxus CLI tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # "init" command
    init_parser = subparsers.add_parser('init', help='Initialize a new plugin')
    init_parser.add_argument('plugin_name', help='Name of the plugin to be created')
    init_parser.set_defaults(func=init_command)

    args = parser.parse_args()
    
    # Call the appropriate function based on the command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()