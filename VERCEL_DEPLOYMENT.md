# Vercel Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (sign up at https://vercel.com)
- Your code pushed to a GitHub repository

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
Make sure all your code is committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. Import Project to Vercel

1. Go to https://vercel.com and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Vercel will automatically detect it as a Python project

### 3. Configure Environment Variables

In the Vercel project settings, add these environment variables:

```
APP_KEY=your_secret_key_here_change_this
DATABASE_URL=sqlite:///db/algo.db
NGROK_ALLOW=FALSE
HOST_SERVER=https://your-app-name.vercel.app
LOGIN_RATE_LIMIT_MIN=5 per minute
LOGIN_RATE_LIMIT_HOUR=25 per hour
API_RATE_LIMIT=10 per second
```

**Important:** 
- Change `APP_KEY` to a secure random string
- Update `HOST_SERVER` with your actual Vercel URL after deployment

### 4. Deploy

Click "Deploy" and Vercel will:
- Install dependencies from `requirements.txt`
- Build your application
- Deploy it to a production URL

### 5. Post-Deployment

After deployment:
1. Copy your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Go to Settings → Environment Variables
3. Update `HOST_SERVER` with your actual Vercel URL
4. Redeploy the application

## Important Notes

### Database Considerations
- SQLite works on Vercel but the database is **ephemeral** (resets on each deployment)
- For production, consider using:
  - **PostgreSQL** (Vercel Postgres, Supabase, Neon)
  - **MySQL** (PlanetScale, Railway)
  - **MongoDB** (MongoDB Atlas)

To use PostgreSQL on Vercel:
1. Add Vercel Postgres from the Storage tab
2. Update `DATABASE_URL` environment variable
3. Install `psycopg2-binary` in requirements.txt

### WebSocket Limitations
- Vercel serverless functions don't support WebSockets
- Socket.IO features may not work
- Consider using Vercel's Edge Functions or alternative hosting for real-time features

### Static Files
- Static files in `/static` folder are automatically served
- Templates in `/templates` folder work as expected

## Troubleshooting

### Build Fails
- Check the build logs in Vercel dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt`

### Application Errors
- Check Function Logs in Vercel dashboard
- Verify all environment variables are set correctly
- Test locally first with `python app.py`

### Database Issues
- Remember: SQLite is ephemeral on Vercel
- Use external database for persistent data
- Check database connection string

## Alternative: Deploy with Vercel CLI (Optional)

If you prefer CLI:
```bash
npm i -g vercel
vercel login
vercel
```

Follow the prompts to deploy.

## Continuous Deployment

Once connected to GitHub:
- Every push to `main` branch automatically deploys to production
- Pull requests create preview deployments
- You can configure branch deployments in Vercel settings

## Support

For issues:
- Vercel Documentation: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
