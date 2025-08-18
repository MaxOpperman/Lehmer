import os

from dotenv import load_dotenv

from app import create_app

load_dotenv()
flask_cors = os.getenv("FLASK_CORS", "false").lower() in ("true", "1", "yes")
app = create_app(allow_cors=flask_cors)

if __name__ == "__main__":
    # Get the host and port from the environment variables or default to 127.0.0.1 and 5050
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5050))
    debug = bool(os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes"))
    app.run(host=host, port=port, debug=debug)
