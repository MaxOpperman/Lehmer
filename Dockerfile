# Stage 1: Prepare the backend
FROM python:3.13-slim AS backend-build

WORKDIR /backend

# Copy backend files
COPY ./app /backend/app
COPY ./run.py /backend/run.py
COPY ./core /backend/core
COPY ./requirements.txt /backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /backend/requirements.txt

# Expose the backend port (default to 5050)
EXPOSE ${FLASK_PORT:-5050}

# Use Gunicorn to serve the Flask app
CMD ["/bin/bash", "-c", "gunicorn run:app -w 4 -b 0.0.0.0:${FLASK_PORT:-5050}"]

# Stage 2: Build the frontend
FROM node:22-slim AS frontend-build

WORKDIR /frontend

# Copy frontend files
COPY ./frontend /frontend

# Install dependencies and build the frontend
RUN npm install && npm run build

# Expose the frontend port
EXPOSE ${FRONTEND_PORT:-5173}

# Use the custom entrypoint script
CMD ["/bin/bash", "-c", "npx serve -s dist -l ${FRONTEND_PORT:-5173}"]
