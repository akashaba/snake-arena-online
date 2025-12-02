#  Snake Arena Online - Single Container Deployment

Simplified Docker deployment with frontend and backend combined in one container.

##  Architecture

```

          Combined Container (Port 80)     
                                           
             
     Nginx        FastAPI        
   (Frontend)        (Backend)       
    Port 80          Port 8000       
             
                                        

                              
                              
     Port 8080           PostgreSQL
      (Host)             (Port 5432)
```

##  Benefits

-  **Single container** - Easier deployment and management
-  **Supervisor** - Manages nginx and uvicorn processes
-  **Less overhead** - No inter-container networking
-  **Simplified** - Only 2 services (app + db)

##  Quick Start

### 1. Build and Start

```bash
docker compose up -d
```

### 2. Initialize Database

```bash
docker compose exec app uv run python migrate_data.py
```

### 3. Access Application

- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Health**: http://localhost:8080/health

### 4. Test Login

```
Email: neon@example.com
Password: password123
```

##  Commands

```bash
# View logs
docker compose logs -f app

# View backend logs only
docker compose exec app tail -f /var/log/supervisor/backend.out.log

# View nginx logs only
docker compose exec app tail -f /var/log/supervisor/nginx.out.log

# Access app container shell
docker compose exec app bash

# Restart app
docker compose restart app

# Stop all services
docker compose down

# Rebuild and restart
docker compose up -d --build
```

##  Container Details

### Combined App Container
- **Nginx** - Serves static React frontend
- **Uvicorn** - Runs FastAPI backend on localhost:8000
- **Supervisor** - Process manager for both services
- **Port**: 8080  80

### Database
- **PostgreSQL 16** - Alpine Linux
- **Port**: 5432
- **Volume**: Persistent storage

##  Environment Variables

Edit `.env` file:

```bash
# Database
POSTGRES_DB=snake_arena
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Backend
SECRET_KEY=your-super-secret-key-min-32-chars

# App Port
APP_PORT=8080
```

##  Troubleshooting

### View Process Status

```bash
docker compose exec app supervisorctl status
```

### Restart Backend Only

```bash
docker compose exec app supervisorctl restart backend
```

### Restart Nginx Only

```bash
docker compose exec app supervisorctl restart nginx
```

### Check Health

```bash
curl http://localhost:8080/health
```

##  Logs

All logs are in `/var/log/supervisor/`:
- `backend.out.log` - Backend stdout
- `backend.err.log` - Backend stderr
- `nginx.out.log` - Nginx stdout
- `nginx.err.log` - Nginx stderr

##  Production Tips

1. **Remove database port** from docker-compose.yml
2. **Use strong passwords** in .env
3. **Enable HTTPS** with SSL certificates
4. **Set up log rotation** for supervisor logs
5. **Monitor** with health checks

##  Files

```
snake-arena-online/
 Dockerfile              # Multi-stage build (frontend + backend)
 docker-compose.yml      # 2 services: app + db
 .dockerignore          # Exclude unnecessary files
 .env                   # Environment variables
 frontend/
     nginx.conf         # Proxy to localhost:8000
```

##  Next Steps

- [ ] Set up automated backups
- [ ] Configure SSL/TLS
- [ ] Add monitoring
- [ ] Set up CI/CD pipeline
