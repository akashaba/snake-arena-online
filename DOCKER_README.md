#  Snake Arena Online - Docker Deployment

Run the complete Snake Arena Online application with Docker Compose using PostgreSQL, FastAPI backend, and nginx-served React frontend.

##  Architecture

```

                   Docker Network                          
                                                           
           
    Frontend          Backend         PostgreSQL  
     (Nginx)     (FastAPI)       16       
     Port 80         Port 8000        Port 5432   
           
                                                         

         
    Port 8080 (Host)
```

##  Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB free disk space

### 1. Setup

```bash
# The .env file is already created from .env.example
# Edit it to change SECRET_KEY and passwords
notepad .env  # or your preferred editor
```

### 2. Build and Start

```bash
# Build and start all services
docker compose up -d

# View logs
docker compose logs -f
```

### 3. Initialize Database

```bash
# Populate with test data (20 users, scores, etc.)
docker compose exec backend uv run python migrate_data.py
```

### 4. Access Application

- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

### 5. Test Login

```
Email: neon@example.com
Password: password123
```

##  Commands

### Service Management

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart a service
docker compose restart backend

# View logs
docker compose logs -f backend

# View all service status
docker compose ps
```

### Database Operations

```bash
# Access PostgreSQL CLI
docker compose exec db psql -U postgres -d snake_arena

# Backup database
docker compose exec db pg_dump -U postgres snake_arena > backup.sql

# Restore database
docker compose exec -T db psql -U postgres -d snake_arena < backup.sql
```

### Development

```bash
# Execute commands in backend
docker compose exec backend bash

# Run tests
docker compose exec backend pytest tests_integration/

# Check backend health
docker compose exec backend curl http://localhost:8000/health
```

### Cleanup

```bash
# Stop and remove containers
docker compose down

# Remove containers and volumes ( DATA LOSS!)
docker compose down -v

# Full cleanup including images
docker compose down -v --rmi all
```

##  Configuration

### Environment Variables (.env)

```bash
# Database
POSTGRES_DB=snake_arena
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password  #  Change this!

# Backend Security
SECRET_KEY=your-super-secret-key-min-32-chars  #  Change this!

# Optional
DATABASE_ECHO=false
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_PORT=8080
```

### Generate Secure Keys

```powershell
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

##  Services

### Database (PostgreSQL 16)
- **Image**: `postgres:16-alpine`
- **Port**: 5432 (exposed)
- **Volume**: `postgres_data` (persistent)
- **Health Check**: Every 10s

### Backend (FastAPI)
- **Build**: `./backend/Dockerfile` (uv-based)
- **Port**: 8000 (exposed)
- **Dependencies**: PostgreSQL
- **Health Check**: Every 30s

### Frontend (React + Nginx)
- **Build**: `./frontend/Dockerfile` (multi-stage)
- **Port**: 8080  80 (nginx)
- **Features**: Gzip, static caching, API proxy
- **Health Check**: Every 30s

##  Troubleshooting

### Port Already in Use

```powershell
# Check what's using port 8080
netstat -ano | findstr :8080

# Change port in .env
FRONTEND_PORT=8081
```

### Backend Can't Connect

```bash
# Check database health
docker compose ps db

# View logs
docker compose logs db
docker compose logs backend
```

### Rebuild After Changes

```bash
# Rebuild specific service
docker compose build backend
docker compose up -d backend

# Rebuild all
docker compose build --no-cache
docker compose up -d
```

##  Test Data

After running `migrate_data.py`:

| Username | Email | Password | Score |
|----------|-------|----------|-------|
| NeonMaster | neon@example.com | password123 | 1250 |
| SnakeKing | king@example.com | password123 | 1180 |
| SnakeWizard | wizard@example.com | password123 | 950 |

##  Production Deployment

### 1. Security

```bash
# Update .env with strong credentials
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
POSTGRES_PASSWORD=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 2. Remove Exposed Ports

Edit `docker-compose.yml`:

```yaml
backend:
  # Comment out ports for internal-only access
  # ports:
  #   - "8000:8000"
```

### 3. Enable HTTPS

Add SSL certificates to nginx configuration.

##  File Structure

```
snake-arena-online/
 docker-compose.yml          # Main compose file
 .env                        # Environment variables
 .env.example               # Template
 backend/
    Dockerfile             # Backend image (uv-based)
    .dockerignore          # Exclude files
    ...                    # FastAPI app
 frontend/
     Dockerfile             # Frontend multi-stage build
     .dockerignore          # Exclude files
     nginx.conf             # Reverse proxy config
     ...                    # React app
```

##  Next Steps

- [ ] Configure HTTPS with Let's Encrypt
- [ ] Set up automated backups
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Add Redis for caching
- [ ] Set up CI/CD pipeline

##  Additional Resources

- **Backend API**: http://localhost:8080/docs
- **OpenAPI Spec**: http://localhost:8080/openapi.json
- **PostgreSQL Logs**: `docker compose logs db`
- **Backend Logs**: `docker compose logs backend`

##  Support

Check logs for errors:
```bash
docker compose logs -f
```

Verify health:
```bash
docker compose ps
```

Test connectivity:
```bash
docker compose exec backend ping db
```
