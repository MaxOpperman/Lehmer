# Stage 1: Prepare the backend
FROM python:3.13-slim AS backend-build

WORKDIR /backend

COPY ./app /backend/app
COPY ./run.py /backend/run.py
COPY ./core /backend/core
COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir -r /backend/requirements.txt

EXPOSE $BACKEND_PORT
CMD ["python", "run.py"]

# Stage 2: Build the frontend
FROM node:22-slim AS frontend-build

WORKDIR /frontend

COPY ./frontend /frontend

RUN npm install && npm run build

EXPOSE $FRONTEND_PORT

CMD ["npx", "serve", "-s", "dist", "-l", "$FRONTEND_PORT"]