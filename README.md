# Evolving file for all parts of the challenge.

## Noxus CLI

A basic CLI tool for plugin management.

### Installation

For development, install in editable mode:

```bash
cd noxus-cli
pip install -e .
```

### Usage

```bash
# Initialize a new plugin
noxus init my-plugin-name

# Run locally (no container) 
noxus serve --plugin my-plugin-name/my-plugin-name.yaml

# Run locally (containerized) 
cd /my-plugin-name
docker-compose -f docker-compose.my-plugin-name.standalone.yml up --build




# Show help
python noxus.py --help
python noxus.py init --help
```
