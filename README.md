# Words Learner Bot

A Telegram bot for vocabulary learning with AI-powered custom word lists and spaced repetition system.

## 🎯 Features

- **AI-Generated Word Lists**: Create custom vocabulary lists based on context
- **Spaced Repetition**: Scientifically-backed review scheduling
- **Simple Interface**: "Know/Don't Know" review system
- **Progress Tracking**: Monitor your learning progress
- **Multi-language Support**: English ↔ Dutch, English ↔ Russian

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key
- Telegram Bot token

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd words-learner-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

4. **Set up database**
   ```bash
   python -c "from database.models import create_tables; create_tables()"
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# Redis Configuration (for task queue)
REDIS_URL=redis://localhost:6379

# Application Configuration
TIMEZONE=UTC
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🏗️ Project Structure

```
words-learner-bot/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── database/
│   ├── __init__.py
│   └── models.py          # SQLAlchemy database models
├── services/
│   ├── __init__.py
│   ├── ai_service.py     # OpenAI integration for word generation
│   └── srs_service.py    # Spaced repetition system
├── PRD_Words_Learner.md   # Product Requirements Document
└── plan.md               # Development plan and milestones
```

## 🤖 Bot Commands

- `/start` - Initialize the bot and select language pair
- `/help` - Show available commands and usage guide
- `/generate` - Create a new custom word list
- `/review` - Start a review session
- `/stats` - View your learning statistics
- `/profile` - Manage your profile settings

## 🔧 Development

### Running in Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your values

# Run the application
python main.py
```

### Database Setup

The application uses PostgreSQL with the following schema:

- **users**: User profiles and preferences
- **words**: Vocabulary words with translations and examples
- **reviews**: Review history and SRS scheduling

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /webhook` - Telegram webhook handler

## 🚀 Deployment

### Railway Deployment

1. **Connect to Railway**
   ```bash
   railway login
   railway init
   ```

2. **Set environment variables in Railway dashboard**
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `DATABASE_URL`
   - `TIMEZONE`

3. **Deploy**
   ```bash
   railway up
   ```

4. **Set webhook URL**
   ```
   https://your-app.railway.app/webhook
   ```

## 📊 Monitoring

The application includes logging for:
- User interactions
- AI API calls
- Database operations
- Error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

---

**Version:** MVP v0.1  
**Status:** In Development  
**Last Updated:** December 2024
