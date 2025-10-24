# Vercel Deployment Guide - हिंदी में 🚀

## GitHub से Vercel पर Deploy करने की पूरी जानकारी

---

## चरण 1: Vercel पर Account बनाएं

1. अपने browser में जाएं: **https://vercel.com**
2. **"Sign Up"** बटन पर क्लिक करें
3. **"Continue with GitHub"** चुनें
4. अपने GitHub account से login करें
5. Vercel को अपने GitHub account access करने की permission दें

---

## चरण 2: अपना Project Import करें

1. Vercel dashboard में **"Add New..."** बटन पर क्लिक करें (ऊपर दाहिने कोने में)
2. **"Project"** option चुनें
3. आपको अपनी सभी GitHub repositories की list दिखेगी
4. **"newtmsignal"** repository को ढूंढें
5. उसके सामने **"Import"** बटन पर क्लिक करें

---

## चरण 3: Project Configure करें

Import करने के बाद आपको configuration page दिखेगा:

### Project Settings:
- **Project Name:** newtmsignal (या जो नाम चाहें)
- **Framework Preset:** Other (यही रहने दें)
- **Root Directory:** ./ (यही रहने दें)
- **Build Command:** (खाली छोड़ दें)
- **Output Directory:** (खाली छोड़ दें)

---

## चरण 4: Environment Variables जोड़ें (बहुत जरूरी! ⚠️)

यह सबसे महत्वपूर्ण step है:

1. **"Environment Variables"** section को खोलें
2. नीचे दिए गए हर variable को एक-एक करके add करें:

### Variable 1:
- **Name:** `APP_KEY`
- **Value:** `your_random_secret_key_12345` (कोई भी random string डालें)

### Variable 2:
- **Name:** `DATABASE_URL`
- **Value:** `sqlite:///db/algo.db`

### Variable 3:
- **Name:** `NGROK_ALLOW`
- **Value:** `FALSE`

### Variable 4:
- **Name:** `HOST_SERVER`
- **Value:** `https://your-app.vercel.app` (अभी के लिए यही लिखें, बाद में update करेंगे)

### Variable 5:
- **Name:** `LOGIN_RATE_LIMIT_MIN`
- **Value:** `5 per minute`

### Variable 6:
- **Name:** `LOGIN_RATE_LIMIT_HOUR`
- **Value:** `25 per hour`

### Variable 7:
- **Name:** `API_RATE_LIMIT`
- **Value:** `10 per second`

**नोट:** हर variable add करने के बाद **"Add"** बटन दबाएं

---

## चरण 5: Deploy करें

1. सभी environment variables add करने के बाद
2. नीचे **"Deploy"** बटन पर क्लिक करें
3. अब Vercel आपका app build करना शुरू करेगा
4. इसमें **2-5 मिनट** लग सकते हैं
5. Screen पर build logs दिखेंगे

### Build होने का इंतजार करें:
- ✅ Building... (हरा tick आने तक wait करें)
- ✅ Deploying...
- ✅ Ready!

---

## चरण 6: अपना Deployment URL कॉपी करें

1. Build complete होने के बाद **"Congratulations"** message दिखेगा
2. आपको एक URL मिलेगा जैसे: `https://newtmsignal.vercel.app`
3. इस URL को **copy** कर लें

---

## चरण 7: HOST_SERVER Update करें (जरूरी!)

अब हमें environment variable update करना है:

1. Vercel dashboard में अपने project पर जाएं
2. ऊपर **"Settings"** tab पर क्लिक करें
3. बाईं तरफ **"Environment Variables"** पर क्लिक करें
4. **HOST_SERVER** variable को ढूंढें
5. उसके सामने **"Edit"** (पेंसिल icon) पर क्लिक करें
6. Value में अपना actual Vercel URL डालें (जो step 6 में copy किया था)
   - Example: `https://newtmsignal.vercel.app`
7. **"Save"** बटन दबाएं

### Changes Apply करें:
1. ऊपर **"Deployments"** tab पर जाएं
2. सबसे ऊपर वाली deployment के सामने **"..."** (three dots) पर क्लिक करें
3. **"Redeploy"** चुनें
4. **"Redeploy"** confirm करें

---

## चरण 8: अपना App Test करें

Deployment complete होने के बाद:

1. अपने Vercel URL को browser में खोलें
2. Check करें:
   - ✅ Homepage खुल रहा है
   - ✅ Login page काम कर रहा है: `/login`
   - ✅ Register page काम कर रहा है: `/register`
   - ✅ About page काम कर रहा है: `/about`

---

## Important Notes (जरूर पढ़ें! ⚠️)

### Database के बारे में:
- ⚠️ **SQLite database Vercel पर temporary है**
- हर deployment पर database reset हो जाएगा
- Production के लिए **PostgreSQL** या **MySQL** use करें

### PostgreSQL कैसे add करें:
1. Vercel dashboard में **"Storage"** tab पर जाएं
2. **"Create Database"** → **"Postgres"** चुनें
3. Database बनने के बाद automatically `DATABASE_URL` update हो जाएगा
4. Project redeploy करें

### WebSocket के बारे में:
- ⚠️ Socket.IO features Vercel पर काम नहीं करेंगे
- Real-time features के लिए alternative solution चाहिए

---

## Troubleshooting (समस्या होने पर)

### अगर Build Fail हो जाए:
1. Vercel dashboard में **"Deployments"** tab खोलें
2. Failed deployment पर क्लिक करें
3. **"Build Logs"** देखें
4. Error message पढ़ें और fix करें

### अगर 500 Error आए:
1. **"Deployments"** → Failed deployment
2. **"Function Logs"** देखें
3. Check करें:
   - सभी environment variables सही हैं?
   - Database connection string सही है?

### अगर Static Files load न हों:
1. Browser cache clear करें (Ctrl + Shift + Delete)
2. Hard refresh करें (Ctrl + F5)
3. Vercel dashboard में redeploy करें

---

## Automatic Deployment (Bonus!)

अब जब भी आप code में changes करेंगे:

1. Code को GitHub पर push करें:
   ```bash
   git add .
   git commit -m "changes ka message"
   git push origin main
   ```

2. Vercel **automatically** deploy कर देगा
3. कुछ मिनटों में changes live हो जाएंगे
4. Email notification भी मिलेगा

---

## Quick Reference - Environment Variables

Copy-paste के लिए (values अपने अनुसार बदलें):

```
APP_KEY=your_secret_key_change_this_12345
DATABASE_URL=sqlite:///db/algo.db
NGROK_ALLOW=FALSE
HOST_SERVER=https://newtmsignal.vercel.app
LOGIN_RATE_LIMIT_MIN=5 per minute
LOGIN_RATE_LIMIT_HOUR=25 per hour
API_RATE_LIMIT=10 per second
```

---

## Help चाहिए?

- Vercel Documentation: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- YouTube पर "Vercel deployment tutorial" search करें

---

## Summary - संक्षेप में

1. ✅ Vercel.com पर GitHub से login करें
2. ✅ "Add New Project" → अपनी repository import करें
3. ✅ Environment variables add करें (7 variables)
4. ✅ "Deploy" button दबाएं
5. ✅ Deployment URL copy करें
6. ✅ HOST_SERVER variable update करें
7. ✅ Redeploy करें
8. ✅ अपना app test करें

**बस! आपका app अब live है! 🎉**

---

## Production के लिए सुझाव

1. **Database:** SQLite की जगह PostgreSQL use करें
2. **Security:** APP_KEY को strong random string बनाएं
3. **Domain:** Custom domain add करें (Settings → Domains)
4. **Monitoring:** Vercel Analytics enable करें
5. **Backup:** Regular database backups लें

---

**शुभकामनाएं! आपका deployment successful हो! 🚀**
