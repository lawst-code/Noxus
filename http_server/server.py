import inspect
from typing import Any, Dict, get_type_hints

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from noxus.plugins import SentimentPlugin


class NodeRunRequest(BaseModel):
    inputs: Dict[str, Any]


def get_required_params(node) -> set:
    """Get the required parameter names for a node's call method (excluding 'self')."""
    sig = inspect.signature(node.call)
    return {name for name, param in sig.parameters.items() if name != "self"}


def validate_node_inputs(node, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that inputs contain all required parameters for the node.
    Returns the validated inputs dict.
    """
    required_params = get_required_params(node)
    provided_params = set(inputs.keys())

    # Check for missing parameters
    missing_params = required_params - provided_params
    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    # Extract only the parameters needed for the call method
    validated_inputs = {param: inputs[param] for param in required_params}

    return validated_inputs


def get_node_inputs_json(node) -> str:
    """Display inputs as JSON schema format."""
    sig = inspect.signature(node.call)
    hints = get_type_hints(node.call)

    inputs = {}
    for name, param in sig.parameters.items():
        if name == "self":
            continue

        # Get type annotation
        param_type = hints.get(name, param.annotation)
        if param_type == inspect.Parameter.empty:
            type_str = "Any"
        else:
            type_str = (
                str(param_type)
                .replace("<class '", "")
                .replace("'>", "")
                .replace("typing.", "")
            )

        inputs[name] = type_str

    # Format as JSON
    if not inputs:
        return '{\n  "inputs": {}\n}'

    input_lines = []
    for name, type_str in inputs.items():
        input_lines.append(f'    "{name}": "{type_str}"')

    inputs_content = ",\n".join(input_lines)
    return f'{{\n  "inputs": {{\n{inputs_content}\n  }}\n}}'


mock_backend = SentimentPlugin()

# Initialize FastAPI app with OpenAPI documentation
app = FastAPI(
    title="Noxus API",
    description="A simple API server with OpenAPI documentation",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint - returns a simple HTML page with links to documentation
    """
    return """
    <html>
        <head>
            <title>Noxus API Server</title>
        </head>
        <body>
            <h1>Welcome to Noxus API Server</h1>
            <p>This is a simple API server with OpenAPI documentation.</p>
            <ul>
                <li><a href="/docs">Swagger UI Documentation</a></li>
                <li><a href="/redoc">ReDoc Documentation</a></li>
                <li><a href="/manifest">View Plugins (JSON)</a></li>
            </ul>
        </body>
    </html>
    """


@app.get("/manifest", response_class=HTMLResponse)
async def manifest():
    """Simple manifest endpoint"""
    nodes = mock_backend.nodes() if hasattr(mock_backend, "nodes") else []

    node_list = ""
    for node in nodes:
        title = getattr(node, "title", "Unknown")
        description = getattr(node, "description", "No description")
        inputs_json = get_node_inputs_json(node)
        node_list += (
            f"<li><strong>{title}</strong> - {description}<pre>{inputs_json}</pre></li>"
        )

    if not node_list:
        node_list = "<li>No nodes available</li>"

    plugin_title = getattr(mock_backend, "title", "Unknown Plugin")

    return f"""
    <html>
        <head>
            <title>Noxus Manifest</title>
        </head>
        <body>
            <h1>Plugin Manifest</h1>
            <h2>Plugin: {plugin_title}</h2>
            <h3>Nodes:</h3>
            <ul>{node_list}</ul>
            <a href="/">Back</a>
        </body>
    </html>
    """


@app.post("/{node_name}/run")
async def run_node(node_name: str, request_data: NodeRunRequest):
    """
    Execute a node by name with provided arguments
    """
    # Get all available nodes
    nodes = mock_backend.nodes() if hasattr(mock_backend, "nodes") else []

    # Find the node with matching name
    target_node = None
    for node in nodes:
        if getattr(node, "name", None) == node_name:
            target_node = node
            break

    if target_node is None:
        raise HTTPException(status_code=404, detail=f"Node '{node_name}' not found")

    try:
        # Validate that inputs contain all required parameters
        validated_inputs = validate_node_inputs(target_node, request_data.inputs)

        # Call the node with validated inputs
        result = target_node.call(**validated_inputs)

        return {"result": result, "status": "success"}

    except ValueError as e:
        # Parameter validation error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Execution error
        raise HTTPException(status_code=500, detail=str(e))


def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """
    Start the FastAPI server

    Args:
        host: Host to bind to
        port: Port to bind to
        reload: Enable auto-reload for development
    """
    uvicorn.run(
        "http_server.server:app", host=host, port=port, reload=reload, log_level="info"
    )


if __name__ == "__main__":
    start_server()
