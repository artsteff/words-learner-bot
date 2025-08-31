# Quick Deploy to Railway - Test Bot in Telegram

## 🚀 **5-Minute Deployment Guide**

### **Step 1: Create Railway Account**
1. Go to https://railway.app
2. Sign in with GitHub
3. Create new account (free tier available)

### **Step 2: Deploy from GitHub**
1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Week 2: Complete bot functionality"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/words-learner-bot.git
   git push -u origin main
   ```

2. **In Railway Dashboard:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python

### **Step 3: Add Environment Variables**
In Railway dashboard, add these variables:
```
TELEGRAM_BOT_TOKEN=8228016705:AAGeaE-UYk2H6fWZPQ7UMEUwhUf4BMR7aLw
OPENAI_API_KEY=your_openai_api_key_here
TIMEZONE=UTC
ENVIRONMENT=production
```

### **Step 4: Add PostgreSQL Database**
1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will auto-set DATABASE_URL

### **Step 5: Get Your Bot URL**
After deployment, Railway gives you a URL like:
```
https://your-app-name.railway.app
```

### **Step 6: Set Telegram Webhook**
```bash
curl -X POST "https://api.telegram.org/bot8228016705:AAGeaE-UYk2H6fWZPQ7UMEUwhUf4BMR7aLw/setWebhook" \
-H "Content-Type: application/json" \
-d '{"url": "https://your-app-name.railway.app/webhook"}'
```

### **Step 7: Test in Telegram**
1. Find @wwwordlearner_bot in Telegram
2. Send `/start`
3. Select language pair
4. Send `/generate`
5. Enter context (e.g., "restaurant")

## ✅ **Expected Results**

After deployment, you should see:
- Bot responds to `/start`
- Language selection works
- Word generation works
- Statistics work
- All commands functional

## 🔧 **Troubleshooting**

### **Bot Not Responding:**
1. Check Railway logs
2. Verify webhook URL is correct
3. Check environment variables

### **Database Errors:**
1. Verify PostgreSQL is added
2. Check DATABASE_URL is set
3. Restart deployment

### **AI Not Working:**
1. Check OpenAI API key
2. Verify API quota
3. Check logs for errors

## 📱 **Test Commands**

Once deployed, test these commands:
```
/start - Initialize bot
/generate - Generate words
restaurant - Generate restaurant words
restaurant 10 - Generate 10 restaurant words
/stats - View statistics
/profile - View profile
/help - Get help
```

---

**Time to Deploy:** ~5 minutes  
**Cost:** Free tier available  
**Result:** Fully functional bot in Telegram
