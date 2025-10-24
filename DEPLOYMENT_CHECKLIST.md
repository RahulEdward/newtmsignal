# Vercel Deployment Checklist ✅

## Before Deployment

- [ ] All code is committed to Git
- [ ] `.env` file is in `.gitignore` (already done ✓)
- [ ] `.env.example` is created with sample values (already done ✓)
- [ ] `requirements.txt` is up to date (already done ✓)
- [ ] `vercel.json` is configured (already done ✓)
- [ ] Code is pushed to GitHub

## GitHub Setup

1. **Create/Update GitHub Repository**
   - Go to https://github.com/new
   - Create a new repository or use existing one
   - Copy the repository URL

2. **Push Your Code** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

## Vercel Deployment Steps

### 1. Sign Up/Login to Vercel
- Go to https://vercel.com
- Click "Sign Up" or "Login"
- Choose "Continue with GitHub"
- Authorize Vercel to access your GitHub

### 2. Import Your Project
- Click "Add New..." button (top right)
- Select "Project"
- Find your GitHub repository in the list
- Click "Import"

### 3. Configure Project
- **Framework Preset:** Other
- **Root Directory:** ./
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)

### 4. Add Environment Variables
Click "Environment Variables" and add:

```
APP_KEY = your_random_secret_key_here
DATABASE_URL = sqlite:///db/algo.db
NGROK_ALLOW = FALSE
HOST_SERVER = https://your-app.vercel.app
LOGIN_RATE_LIMIT_MIN = 5 per minute
LOGIN_RATE_LIMIT_HOUR = 25 per hour
API_RATE_LIMIT = 10 per second
```

**Note:** You'll update `HOST_SERVER` after first deployment

### 5. Deploy
- Click "Deploy"
- Wait for build to complete (2-5 minutes)
- Copy your deployment URL

### 6. Update Environment Variables
- Go to Project Settings → Environment Variables
- Update `HOST_SERVER` with your actual Vercel URL
- Click "Redeploy" to apply changes

## Post-Deployment

- [ ] Test the homepage: `https://your-app.vercel.app`
- [ ] Test login page: `https://your-app.vercel.app/login`
- [ ] Test registration: `https://your-app.vercel.app/register`
- [ ] Check if static files load correctly
- [ ] Verify database connections work

## Important Notes

⚠️ **Database Warning:**
- SQLite on Vercel is ephemeral (resets on each deployment)
- For production, use PostgreSQL, MySQL, or MongoDB
- Consider Vercel Postgres, Supabase, or PlanetScale

⚠️ **WebSocket Warning:**
- Socket.IO may not work on Vercel serverless
- Real-time features might need alternative solutions

## Troubleshooting

### Build Fails
1. Check build logs in Vercel dashboard
2. Verify `requirements.txt` has all dependencies
3. Check Python version in `runtime.txt`

### 500 Internal Server Error
1. Check Function Logs in Vercel dashboard
2. Verify environment variables are set
3. Check database connection string

### Static Files Not Loading
1. Verify files are in `/static` folder
2. Check `vercel.json` routes configuration
3. Clear browser cache

## Continuous Deployment

✅ Automatic deployments are now enabled:
- Push to `main` branch → Production deployment
- Pull requests → Preview deployments
- All changes are automatically deployed

## Need Help?

- Read: `VERCEL_DEPLOYMENT.md` for detailed guide
- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support

---

**Ready to deploy?** Follow the steps above! 🚀
