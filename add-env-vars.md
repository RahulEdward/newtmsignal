# Add Environment Variables to Vercel

## Option 1: Via Vercel Dashboard (Recommended)

1. Go to: https://vercel.com/rahuls-projects-4055f2e8/tmsignal/settings/environment-variables

2. Add these variables one by one:

```
Name: APP_KEY
Value: 335l52jlkj532fff67jk4354

Name: DATABASE_URL
Value: sqlite:///db/algo.db

Name: NGROK_ALLOW
Value: FALSE

Name: HOST_SERVER
Value: https://tmsignal-brq1j33jm-rahuls-projects-4055f2e8.vercel.app

Name: LOGIN_RATE_LIMIT_MIN
Value: 5 per minute

Name: LOGIN_RATE_LIMIT_HOUR
Value: 25 per hour

Name: API_RATE_LIMIT
Value: 10 per second
```

3. After adding all variables, redeploy:
   ```
   vercel --prod
   ```

## Option 2: Via CLI

Run these commands:

```bash
vercel env add APP_KEY
# Enter: 335l52jlkj532fff67jk4354
# Select: Production

vercel env add DATABASE_URL
# Enter: sqlite:///db/algo.db
# Select: Production

vercel env add NGROK_ALLOW
# Enter: FALSE
# Select: Production

vercel env add HOST_SERVER
# Enter: https://tmsignal-brq1j33jm-rahuls-projects-4055f2e8.vercel.app
# Select: Production

vercel env add LOGIN_RATE_LIMIT_MIN
# Enter: 5 per minute
# Select: Production

vercel env add LOGIN_RATE_LIMIT_HOUR
# Enter: 25 per hour
# Select: Production

vercel env add API_RATE_LIMIT
# Enter: 10 per second
# Select: Production
```

Then redeploy:
```bash
vercel --prod
```
