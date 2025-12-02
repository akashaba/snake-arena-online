# Multi-stage Dockerfile combining Frontend and Backend

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --silent

# Copy frontend source
COPY frontend/ .

# Build frontend with API URL for nginx proxy
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# Stage 2: Build Backend Dependencies
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS backend-builder

WORKDIR /app

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Stage 3: Final Production Image
FROM python:3.13-slim

# Install nginx, supervisor, and PostgreSQL client
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend virtual environment from builder
COPY --from=backend-builder /app/.venv /app/.venv

# Copy backend application code
COPY backend/ /app/

# Copy built frontend from builder
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/sites-available/default

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor

COPY <<EOF /etc/supervisor/conf.d/supervisord.conf
[supervisord]
nodaemon=true
user=root

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/nginx.out.log
stderr_logfile=/var/log/supervisor/nginx.err.log

[program:backend]
command=/app/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
directory=/app
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/backend.out.log
stderr_logfile=/var/log/supervisor/backend.err.log
environment=PATH="/app/.venv/bin:%(ENV_PATH)s"
EOF

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port 80 (Render will map this to public HTTPS)
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start supervisor to manage both nginx and backend
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
