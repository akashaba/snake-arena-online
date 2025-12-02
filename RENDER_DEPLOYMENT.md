# 🚀 Deploy Snake Arena Online to Render

This guide will help you deploy your Snake Arena game to Render.com with a free PostgreSQL database.

## 📋 Prerequisites

1. **GitHub Account** - Your code should be pushed to GitHub
2. **Render Account** - Sign up at [render.com](https://render.com) (free)

## 🎯 Quick Deploy (Recommended)

### Option 1: Blueprint Deploy (Easiest)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push
   ```

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New" → "Blueprint"

3. **Connect Repository**
   - Select your `snake-arena-online` repository
   - Render will auto-detect `render.yaml`

4. **Click Deploy**
   - Render will create:
     - PostgreSQL database (free tier)
     - Web service with your app
   - Database URL is automatically configured

5. **Wait for Build** (~5-10 minutes)
   - Watch the build logs
   - First deploy takes longer

6. **Access Your App**
   - Click on your service URL (e.g., `https://snake-arena-app.onrender.com`)
   - Your app is live with HTTPS! 🎉

### Option 2: Manual Setup

If you prefer manual control:

#### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard → "New" → "PostgreSQL"
2. Configure:
   - **Name**: `snake-arena-db`
   - **Database**: `snake_arena`
   - **User**: `postgres`
   - **Region**: Choose closest to you
   - **Plan**: Free
3. Click "Create Database"
4. Copy the **Internal Database URL** (starts with `postgresql://`)

#### Step 2: Create Web Service

1. Go to "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `snake-arena-app`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`
   - **Plan**: Free

4. Add Environment Variables:
   ```
   DATABASE_URL = [paste Internal Database URL from Step 1]
   SECRET_KEY = [generate random 32+ character string]
   DATABASE_ECHO = false
   ACCESS_TOKEN_EXPIRE_MINUTES = 1440
   ALGORITHM = HS256
   DB_POOL_SIZE = 5
   DB_MAX_OVERFLOW = 10
   DB_POOL_TIMEOUT = 30
   DB_POOL_RECYCLE = 3600
   ```

5. Click "Create Web Service"

#### Step 3: Initialize Database

After first successful deploy:

1. Go to your web service → "Shell"
2. Run:
   ```bash
   python migrate_data.py
   ```

## 🔧 Configuration Details

### Database Connection

Render provides `DATABASE_URL` in this format:
```
postgresql://user:password@hostname:5432/database
```

Your backend (`backend/database.py`) should use:
```
postgresql+asyncpg://user:password@hostname:5432/database
```

If needed, update your database configuration to handle both formats.

### Environment Variables

All environment variables are set via Render dashboard:
- **Secrets**: Use Render's secret environment variables
- **Auto-generated**: `DATABASE_URL` is automatically provided
- **Custom**: Set `SECRET_KEY` to a strong random value

### Free Tier Limits

- **Web Service**: Spins down after 15 min inactivity (cold start ~30s)
- **Database**: 1GB storage, 97 hours/month uptime
- **Bandwidth**: 100GB/month

## 🧪 Testing

After deployment:

1. **Check Health**
   ```bash
   curl https://your-app.onrender.com/health
   ```

2. **Test API Docs**
   - Visit `https://your-app.onrender.com/docs`

3. **Test Login**
   - Email: `neon@example.com`
   - Password: `password123`

## 📊 Monitoring

### View Logs

1. Go to your service in Render Dashboard
2. Click "Logs" tab
3. Filter by:
   - `backend` - FastAPI logs
   - `nginx` - Web server logs

### Check Metrics

- Go to "Metrics" tab
- Monitor:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

## 🔄 Updates & Redeployment

### Auto Deploy (Recommended)

Enable auto-deploy for continuous deployment:

1. Go to service → "Settings"
2. Enable "Auto-Deploy"
3. Select branch (e.g., `main`)

Now every `git push` triggers a new deployment!

### Manual Deploy

1. Go to service → "Manual Deploy"
2. Click "Deploy latest commit"

### Rollback

1. Go to "Events" tab
2. Find previous successful deploy
3. Click "Rollback to this version"

## 🐛 Troubleshooting

### Build Fails

**Check build logs:**
- Look for Docker build errors
- Verify `Dockerfile` syntax
- Check all COPY paths are correct

**Common fixes:**
```bash
# Rebuild locally first
docker build -t test .
docker run -p 8080:80 test
```

### Database Connection Issues

**Check DATABASE_URL:**
1. Go to Database → "Connect"
2. Copy "Internal Database URL"
3. Verify it's set in web service environment variables

**Format should be:**
```
postgresql://user:pass@host/db
```

**Your app needs:**
```
postgresql+asyncpg://user:pass@host/db
```

### App Not Starting

**Check logs for:**
- Supervisor errors
- Nginx configuration issues
- Backend startup errors

**Verify health check:**
```bash
# Inside Render Shell
curl http://localhost/health
supervisorctl status
```

### Slow Response (Cold Starts)

Free tier spins down after 15 min inactivity:
- First request takes ~30 seconds
- Subsequent requests are fast
- Upgrade to paid tier ($7/month) for always-on

## 💰 Cost Optimization

### Stay on Free Tier
- Use free PostgreSQL (1GB limit)
- Use free web service
- Accept cold starts

### Upgrade Options
- **Starter Plan** ($7/month): Always-on, no cold starts
- **PostgreSQL** ($7/month): More storage & uptime
- **Combined**: ~$14/month for production-ready setup

## 🔒 Security Best Practices

1. **Set Strong SECRET_KEY**
   ```bash
   # Generate in PowerShell
   -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```

2. **Use Environment Variables**
   - Never commit secrets to Git
   - Use Render's secret environment variables

3. **Enable HTTPS** (automatic on Render)
   - All traffic is HTTPS by default
   - Free SSL certificates

4. **Database Security**
   - Use Internal Database URL (not external)
   - Database is in private network

## 📚 Resources

- [Render Documentation](https://render.com/docs)
- [Render Docker Guide](https://render.com/docs/docker)
- [PostgreSQL on Render](https://render.com/docs/databases)
- [Environment Variables](https://render.com/docs/environment-variables)

## 🎮 Next Steps

After successful deployment:

- [ ] Set up custom domain
- [ ] Configure email notifications
- [ ] Set up monitoring alerts
- [ ] Enable auto-deploy from GitHub
- [ ] Add more test users
- [ ] Monitor usage and costs
- [ ] Consider upgrading for production traffic

---

**Your app is now live!** 🎊

Share your game: `https://your-app-name.onrender.com`
