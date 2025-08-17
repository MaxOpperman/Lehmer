import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Get the port from the environment variable or default to 5050
    port = int(os.getenv("BACKEND_PORT", 5050))
    debug = bool(os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"))
    app.run(host="0.0.0.0", port=port, debug=debug)
