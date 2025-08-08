import argparse

def init_command(args):
    """Handle the init command"""
    print(f"Initializing plugin with name: {args.plugin_name}")

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