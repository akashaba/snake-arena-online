# Setting up CI/CD Pipeline

This guide explains how to configure the GitHub Actions CI/CD pipeline for automatic testing and deployment to Render.

## 🎯 Pipeline Overview

The pipeline has 3 jobs that run on every push and pull request:

1. **Test Backend** - Runs Python tests with pytest
2. **Test Frontend** - Runs linter and builds frontend
3. **Deploy** - Triggers Render deployment (only on push to `main` after tests pass)

## 🔧 Setup Instructions

### Step 1: Get Render Deploy Hook

1. Go to your Render Dashboard: https://dashboard.render.com
2. Select your **snake-arena-app** web service
3. Go to **Settings** tab
4. Scroll to **Deploy Hook** section
5. Click **Create Deploy Hook**
6. Copy the webhook URL (looks like: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`)

### Step 2: Add GitHub Secret

1. Go to your GitHub repository: https://github.com/akashaba/snake-arena-online
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add secret:
   - **Name**: `RENDER_DEPLOY_HOOK_URL`
   - **Value**: Paste the deploy hook URL from Step 1
5. Click **Add secret**

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. If prompted, click **I understand my workflows, go ahead and enable them**

### Step 4: Test the Pipeline

Push a change to trigger the pipeline:

```bash
git add .
git commit -m "Test CI/CD pipeline"
git push
```

Watch the pipeline run at: https://github.com/akashaba/snake-arena-online/actions

## 📊 What Happens

### On Every Push/PR:
- ✅ Backend tests run (pytest)
- ✅ Frontend linter runs (eslint)
- ✅ Frontend build test runs

### On Push to `main` (after tests pass):
- 🚀 Render deployment is triggered automatically
- 📦 Render builds new Docker image
- 🔄 Render deploys updated app
- ✨ Your app is updated live!

## 🧪 Testing Locally

Before pushing, you can test locally:

### Backend Tests
```bash
cd backend
uv run pytest tests/ -v
```

### Frontend Lint
```bash
cd frontend
npm run lint
```

### Frontend Build
```bash
cd frontend
npm run build
```

## 🔍 Monitoring Pipeline

### View Pipeline Status
1. Go to **Actions** tab: https://github.com/akashaba/snake-arena-online/actions
2. Click on a workflow run to see details
3. View logs for each job

### Check Deployment Status
1. After pipeline triggers deployment, go to Render Dashboard
2. Click your service → **Events** tab
3. Watch the deployment progress
4. Logs show build and startup status

## 🚨 Troubleshooting

### Backend Tests Fail
- Check test logs in GitHub Actions
- Run tests locally: `cd backend && uv run pytest tests/ -v`
- Fix failing tests before pushing

### Frontend Build Fails
- Check build logs in GitHub Actions
- Run build locally: `cd frontend && npm run build`
- Fix TypeScript/build errors

### Deployment Not Triggered
- Check if tests passed (deploy only runs after tests pass)
- Verify `RENDER_DEPLOY_HOOK_URL` secret is set correctly
- Check Actions logs for curl errors

### Deployment Fails on Render
- Go to Render Dashboard → Service → Logs
- Check for Docker build errors
- Check for application startup errors
- Verify environment variables are set

## 🎨 Customizing the Pipeline

### Add More Tests

Edit `.github/workflows/ci-cd.yml`:

```yaml
- name: Run tests with coverage
  working-directory: ./backend
  run: uv run pytest tests/ --cov=app --cov-report=term
```

### Add Frontend Tests

Once you have frontend tests:

```yaml
- name: Run tests
  working-directory: ./frontend
  run: npm test -- --run
  # Remove continue-on-error when tests exist
```

### Deploy to Staging First

Add a staging environment:

```yaml
deploy-staging:
  needs: [test-backend, test-frontend]
  if: github.ref == 'refs/heads/develop'
  # ... deploy to staging

deploy-production:
  needs: [deploy-staging]
  if: github.ref == 'refs/heads/main'
  # ... deploy to production
```

## 🔐 Security Best Practices

1. **Never commit secrets** - Always use GitHub Secrets
2. **Limit secret access** - Only the deploy job needs the deploy hook
3. **Use branch protection** - Require PR reviews before merging to main
4. **Enable required checks** - Make tests required before merging

### Enable Branch Protection

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select: `Test Backend` and `Test Frontend`
4. Save changes

## 📈 Next Steps

- [ ] Add code coverage reporting
- [ ] Add integration tests
- [ ] Add E2E tests with Playwright
- [ ] Set up staging environment
- [ ] Add deployment notifications (Slack, Discord, etc.)
- [ ] Add database migration automation
- [ ] Implement rollback strategy

## 🎯 Pipeline Status Badge

Add to your README.md:

```markdown
[![CI/CD Pipeline](https://github.com/akashaba/snake-arena-online/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/akashaba/snake-arena-online/actions/workflows/ci-cd.yml)
```

This shows the current status of your CI/CD pipeline!

---

**Your CI/CD pipeline is now ready!** Every push to `main` will automatically test and deploy your app. 🎉
