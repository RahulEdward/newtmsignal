# Vercel पर Database Setup करें - हिंदी में

## समस्या क्या है?

आपका app successfully deploy हो गया है! ✅ 

लेकिन SQLite database Vercel पर **temporary** है - हर deployment पर reset हो जाता है। इसलिए register किया हुआ user नहीं मिल रहा।

## समाधान: PostgreSQL Database Use करें

---

## Option 1: Vercel Postgres (सबसे आसान) ⭐

### Step 1: Vercel Postgres Create करें

1. अपने Vercel project में जाएं: https://vercel.com/rahuls-projects-4055f2e8/tmsignal
2. ऊपर **"Storage"** tab पर क्लिक करें
3. **"Create Database"** बटन दबाएं
4. **"Postgres"** चुनें
5. Database का नाम दें (जैसे: `tmsignal-db`)
6. **"Create"** बटन दबाएं

### Step 2: Database को Project से Connect करें

1. Database बनने के बाद **"Connect Project"** पर क्लिक करें
2. अपना project **"tmsignal"** select करें
3. Environment: **"Production"** चुनें
4. **"Connect"** बटन दबाएं

✅ Automatically `POSTGRES_URL` environment variable add हो जाएगा!

### Step 3: Requirements.txt Update करें

आपकी local machine पर:

```bash
# psycopg2 add करें requirements.txt में
```

मैं अभी update कर देता हूं...

---

## Option 2: Supabase (Free Alternative)

### Step 1: Supabase Account बनाएं

1. जाएं: https://supabase.com
2. **"Start your project"** पर क्लिक करें
3. GitHub से sign in करें

### Step 2: New Project बनाएं

1. **"New Project"** पर क्लिक करें
2. Project का नाम दें: `tmsignal`
3. Database Password set करें (याद रखें!)
4. Region चुनें: **"Mumbai"** (सबसे नजदीक)
5. **"Create new project"** दबाएं
6. 2-3 मिनट wait करें

### Step 3: Connection String Copy करें

1. Project dashboard में **"Settings"** पर जाएं
2. **"Database"** section खोलें
3. **"Connection string"** में **"URI"** tab चुनें
4. Connection string copy करें:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
5. `[YOUR-PASSWORD]` को अपने actual password से replace करें

### Step 4: Vercel में Environment Variable Add करें

1. Vercel dashboard: https://vercel.com/rahuls-projects-4055f2e8/tmsignal/settings/environment-variables
2. New variable add करें:
   - **Name:** `DATABASE_URL`
   - **Value:** (Supabase connection string paste करें)
   - Environment: **Production** select करें
3. **"Save"** दबाएं

---

## Option 3: Railway (भी Free है)

### Step 1: Railway Account

1. जाएं: https://railway.app
2. **"Login with GitHub"** करें

### Step 2: PostgreSQL Database बनाएं

1. **"New Project"** → **"Provision PostgreSQL"**
2. Database automatically बन जाएगा

### Step 3: Connection String Copy करें

1. PostgreSQL service पर क्लिक करें
2. **"Connect"** tab खोलें
3. **"Postgres Connection URL"** copy करें

### Step 4: Vercel में Add करें

Same as Supabase - Environment Variables में `DATABASE_URL` add करें

---

## Final Steps (सभी options के लिए)

### 1. Requirements.txt Update करें

Local machine पर ये command run करें:

```bash
# मैं अभी file update कर रहा हूं...
```

### 2. Code Push करें

```bash
git add requirements.txt
git commit -m "Add PostgreSQL support"
git push origin main
```

### 3. Vercel पर Redeploy करें

```bash
vercel --prod
```

या Vercel dashboard में जाकर **"Redeploy"** button दबाएं

---

## Test करें

1. अपने Vercel URL पर जाएं
2. **Register** page खोलें
3. नया user register करें
4. Login करें

अब database persist होगा! ✅

---

## Quick Comparison

| Database | Free Tier | Setup Time | Best For |
|----------|-----------|------------|----------|
| **Vercel Postgres** | 256 MB | 2 min | सबसे आसान |
| **Supabase** | 500 MB | 5 min | ज्यादा features |
| **Railway** | 500 MB | 3 min | Simple setup |

---

## मेरी सिफारिश

**Vercel Postgres use करें** - सबसे आसान है और automatically integrate हो जाता है!

---

## अभी क्या करें?

1. ऊपर दिए गए किसी एक option को follow करें
2. PostgreSQL database setup करें
3. `DATABASE_URL` environment variable update करें
4. Redeploy करें

**बस! आपका app production-ready हो जाएगा! 🚀**
