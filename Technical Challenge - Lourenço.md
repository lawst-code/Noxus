# Technical Challenge (Zé team)

# Noxus Plugin System Technical Challenge

The platform at Noxus is extensible entirely using a complex plugin system. In this challenge you’ll replicate a simplified portion of the system based on a specification and prepare the infrastructure deployment of an implementation of a plugin.

The main goal is to build a plugin execution platform that enables developers to create, test, and deploy containerized plugins. Along the way you will implement:

- **A Local Development CLI** - A command-line tool for plugin development, testing, and local iteration
- **A Plugin Execution Server** - A containerized web service that loads and executes plugins via HTTP API
- **Cloud or Local Infrastructure** - Terraform configuration to deploy the server and sample plugin to a cloud provider

The final system will support a containerized HTTP server that serves installed plugins, both at the specification and execution level, with proper isolation, error handling, and monitoring.

---

## 2. Specification Overview

Plugins are defined by two main artifacts:

- A declaration of the plugin in yaml format. We separate the plugin definition in two sections:
  - A base section with core information about the plugin
  - An extensions section with support for advanced features
    - Base-Image to support the plugin dependencies
    - Permissions declaration that can be statically checked to ensure no operations happen outside that permission
    - An OAuth section to declare interactions with integrations that are authenticated through OAuth
- A class with a pre-defined structure implementing “Nodes” → each node represents an action that the plugin can execute

### Plugin.yaml Structure

```yaml
# base plugin.yaml
name: sentiment-analyze
version: 0.1.0
description: "Provides sentiment analysis nodes"
entrypoint: example.PluginExample
# extensions
image: ....
permissions:
  - network
  - env:OPENAI_API_KEY
oauth:
  provider: slack
  scopes: ["channels:read", "chat:write"]
```

### Plugin Code example

```python
from noxus.plugins import Plugin, Node

class SentimentNode(Node):
    title = "Sentiment Analysis"
    description = "Analyze text sentiment"

    def call(self, arg1: str, arg2: str) -> dict:
        # Plugin logic here
        return {"sentiment": "positive", "score": 0.8}

class SentimentPlugin(Plugin):
    def nodes(self):
        return [SentimentNode()]

```

- A Plugin can expose multiple nodes by including them in the nodes() method
- A Node must implement the call method that is then served in the HTTP server
- Nodes can receive any number of arguments and return any dictionary with valid string keys.

### Remote Plugin API

A plugin that is served exposes two endpoints to be used by the main platform:

- `GET /{node_name}/manifest` - Returns the plugin schema and the schema of each Node
- `POST /{node_name}/run` - Executes a specific node with provided inputs
  - Inputs are provided in the body with the structure
  ```python
  {
  	"inputs": {
  	  "arg1": "...",
  	  "arg2": "..."
  	}
  }
  ```

---

## 3. Detailed Objectives

### Objective 1: Noxus CLI for Local Development

As per the spec, a developed plugin must be served in a REST interface with the two provided endpoints.

The first task is to build a CLI tool that helps developers create, test, and serve plugins.

The main objective of the CLI is to serve created plugins, through the plugin.yaml, running a web server that creates the two necessary endpoints for each defined node in the plugin structure.

### Required Commands

```bash
# Plugin development workflow
noxus init <plugin-name>                     # Scaffold new plugin

# Plugin management
noxus plugin list                            # List plugins in current space
noxus plugin info <name>                     # Show plugin details

# Local development server
noxus serve [--port=8080] --plugin "path/to/plugin.yaml" # Serve the plugin

# Advanced
noxus validate                               # Validate plugin.yaml in curr. dir
noxus build                                  # Build plugin Docker image
```

Example request to run a node:

```python
# Plugin execution
POST /{node_name}/run
Content-Type: application/json

{
  "inputs": {
    "arg1": "Hello world",
    "arg2": "test"
  },
}

```

Example response:

```python
{
  "outputs": {
    "sentiment": "processed text",
    "score": 0.95
  },
  "execution_time": 1.23,
  "status": "success"
}

```

### Advanced Features

- **Validate**: Dynamically load the code and ensure that all the specifications defined in the plugin.yaml match the implemented code and nodes
- **Build**: Support building images based on any dependency management of your choice that can be used to serve the plugin
- **Hot Reload**: Watch for file changes and restart plugin automatically
- **Timeout Handling**: Kill long-running executions (30s default)
- **Health Checks**: `/health` endpoint and plugin status monitoring
- **Error Handling:** Define a structure for error handling and return errors correctly on the HTTP request
- **Logging**: Structured logs with request tracing

### Objective 3: Cloud Deployment with Terraform (6-8 hours)

Deploy the plugin execution server and sample plugin to a cloud provider.

### Infrastructure Requirements

Choose one cloud provider (AWS, GCP, or Azure) and implement:

1. **Container Service**: Deploy the image that serves the plugin using a container service of choice - you can go local and setup the deployment on Docker (ECS, Cloud Run, Container Apps) - let us know which one
2. **Load Balancer**: Deploy an HTTP load balancer or proxy, such as nginx - either locally or on cloud depending on 1.
3. **(Advanced) Secrets Management**: Store OAuth credentials and API keys securely
4. **(Advanced) Auto-scaling**: Scale based on CPU/memory usage (min 1, max 5 instances)

---

## 📝 Deliverables

**Focus on implementation of the core set of features, with extensions and advanced features as optional additional deliverables.**

1. **Noxus CLI** - Complete source code with installation instructions
2. **Sample Plugin** - Working plugin in both Docker and remote modes
3. **Terraform Infrastructure** - Complete cloud deployment configuration
4. **Documentation** - Setup guides, API docs, and architecture overview

## 🚀 Getting Started

1. Choose your technology stack
2. Start with CLI implementation and plugin scaffolding
3. Build and test the server locally
4. Create the sample plugin
5. Set up cloud infrastructure
6. Deploy and validate the complete system

**Success Criteria**: A developer should be able to create a new plugin with `noxus init`, test it locally with `noxus dev`, and deploy it to your cloud infrastructure.
