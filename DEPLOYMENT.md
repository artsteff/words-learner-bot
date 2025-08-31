# Deployment Guide - Railway

## 🚀 Quick Deployment to Railway

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository with the bot code
- Telegram Bot token
- OpenAI API key

### Step 1: Prepare Your Code

1. **Ensure all files are committed to GitHub**
   ```bash
   git add .
   git commit -m "Week 1: Basic bot functionality complete"
   git push origin main
   ```

2. **Verify your project structure**
   ```
   words-learner-bot/
   ├── main.py
   ├── requirements.txt
   ├── .env (local only)
   ├── database/
   ├── services/
   └── README.md
   ```

### Step 2: Deploy to Railway

1. **Login to Railway**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**
   In Railway dashboard, add these variables:
   ```
   TELEGRAM_BOT_TOKEN=8228016705:AAGeaE-UYk2H6fWZPQ7UMEUwhUf4BMR7aLw
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://... (Railway will provide)
   TIMEZONE=UTC
   ENVIRONMENT=production
   ```

4. **Add PostgreSQL Database**
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically set DATABASE_URL

5. **Deploy**
   - Railway will automatically detect Python project
   - It will install dependencies from requirements.txt
   - Run `python main.py` as the start command

### Step 3: Configure Telegram Webhook

1. **Get your Railway URL**
   - After deployment, Railway provides a URL like: `https://your-app.railway.app`

2. **Set Telegram webhook**
   ```bash
   curl -X POST "https://api.telegram.org/bot8228016705:AAGeaE-UYk2H6fWZPQ7UMEUwhUf4BMR7aLw/setWebhook" \
   -H "Content-Type: application/json" \
   -d '{"url": "https://your-app.railway.app/webhook"}'
   ```

3. **Verify webhook**
   ```bash
   curl "https://api.telegram.org/bot8228016705:AAGeaE-UYk2H6fWZPQ7UMEUwhUf4BMR7aLw/getWebhookInfo"
   ```

### Step 4: Test Deployment

1. **Test health endpoint**
   ```bash
   curl https://your-app.railway.app/health
   ```

2. **Test bot in Telegram**
   - Send `/start` to @wwwordlearner_bot
   - Verify bot responds correctly

### Step 5: Monitor and Debug

1. **View logs in Railway**
   - Go to your project in Railway dashboard
   - Click on "Deployments" tab
   - View real-time logs

2. **Common issues and solutions**
   - **Bot not responding**: Check webhook URL and logs
   - **Database errors**: Verify DATABASE_URL is set correctly
   - **AI not working**: Check OpenAI API key and quota

## 🔧 Local Development vs Production

### Local Development
```bash
# Run locally
python3 main.py

# Test bot
python3 test_bot.py
```

### Production (Railway)
- Automatic deployment from GitHub
- Environment variables managed in Railway dashboard
- PostgreSQL database provided by Railway
- Automatic scaling and monitoring

## 📊 Monitoring

### Railway Metrics
- CPU usage
- Memory usage
- Request count
- Error rate

### Application Logs
- User interactions
- AI API calls
- Database operations
- Error tracking

## 🔄 Continuous Deployment

Railway automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "New feature"
git push origin main
# Railway will automatically deploy
```

## 🆘 Troubleshooting

### Bot Not Responding
1. Check Railway logs for errors
2. Verify webhook URL is correct
3. Test webhook endpoint manually

### Database Issues
1. Check DATABASE_URL in Railway environment
2. Verify PostgreSQL service is running
3. Check database connection in logs

### AI Generation Failing
1. Verify OpenAI API key is correct
2. Check OpenAI API quota/limits
3. Review AI service logs

---

**Last Updated:** December 2024  
**Status:** Ready for deployment
