#!/bin/bash

# Generate the runtime configuration file
echo "Generating runtime configuration..."
mkdir -p /dist/runtime-config
echo "window.RUNTIME_CONFIG = { VITE_API_URL: \"${VITE_API_URL}\" };" > /dist/runtime-config/env.js

# Start the frontend server using npx serve
echo "Starting the frontend server..."
exec npx serve -s /dist -l ${FRONTEND_PORT:-5173}