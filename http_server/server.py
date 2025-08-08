import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Initialize FastAPI app with OpenAPI documentation
app = FastAPI(
    title="Noxus API",
    description="A simple API server with OpenAPI documentation",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
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
                <li><a href="/plugins">View Plugins (JSON)</a></li>
            </ul>
        </body>
    </html>
    """

def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """
    Start the FastAPI server
    
    Args:
        host: Host to bind to
        port: Port to bind to
        reload: Enable auto-reload for development
    """
    uvicorn.run(
        "http_server.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()
