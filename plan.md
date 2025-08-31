# Development Plan - Words Learner Telegram Bot MVP

**Project:** Words Learner Telegram Bot  
**Version:** MVP v0.1  
**Timeline:** 6 weeks  
**Status:** Planning Phase

---

## 🎯 Project Overview

Building a Telegram bot for vocabulary learning with:
- Custom word list generation via AI
- Spaced repetition review system
- Support for English ↔ Dutch ↔ Russian
- Simple "Know/Don't Know" review interface

---

## 📋 Pre-Development Setup

### ✅ Environment Setup
- [ ] Set up development environment
- [ ] Install Node.js and npm
- [ ] Set up PostgreSQL database
- [ ] Create GitHub repository
- [ ] Set up project structure

### ✅ API Keys & Services
- [ ] Create Telegram Bot via @BotFather
- [ ] Get OpenAI API key for word generation
- [ ] Set up cloud hosting account (Heroku/AWS/DigitalOcean)
- [ ] Configure environment variables

### ✅ Setup Decisions Made
1. **Hosting Platform:** Railway (EU)
2. **Database:** PostgreSQL (managed)
3. **Environment:** Cursor (VS Code-like), Python 3.11 + FastAPI, uvicorn + rq
4. **Bot Name:** @wwwordlearner_bot
5. **Language Pairs:** EN ↔ NL, EN ↔ RU
6. **User Data:** Telegram ID, username, language pairs, timezone

---

## 🏗️ Week 1: Foundation & Bot Setup

### Milestone: Basic Bot Infrastructure
**Target:** Functional Telegram bot with basic commands

#### Tasks:
- [x] **Day 1-2: Project Structure**
  - [x] Initialize Python project with FastAPI
  - [x] Set up uvicorn server
  - [x] Install required dependencies (python-telegram-bot, fastapi, openai)
  - [x] Create basic folder structure

- [x] **Day 3-4: Telegram Bot Integration**
  - [x] Set up Telegram Bot API connection
  - [x] Implement basic command handlers (/start, /help)
  - [x] Create inline keyboard for language selection
  - [x] Test bot responsiveness

- [x] **Day 5-7: Database Setup**
  - [x] Design database schema (users, words, reviews)
  - [x] Set up SQLAlchemy models
  - [x] Create basic user registration structure
  - [x] Implement user state management

#### Deliverables:
- [x] Working Telegram bot that responds to /start
- [x] Language pair selection interface
- [x] User registration structure ready
- [x] Basic error handling

#### ✅ Week 1 Decisions Made
1. **Bot Name:** @wwwordlearner_bot ✅
2. **Language Pairs:** EN ↔ NL, EN ↔ RU ✅
3. **User Data:** Telegram ID, username, language pairs, timezone ✅

---

## 🤖 Week 2: User Management & Core Features

### Milestone: User Onboarding & Basic Commands
**Target:** Complete user onboarding flow

#### Tasks:
- [x] **Day 1-2: User Onboarding**
  - [x] Implement language pair selection flow
  - [x] Create user profile setup
  - [x] Add /profile command to view/update settings
  - [x] Implement /stats command for basic progress

- [x] **Day 3-4: Word Management**
  - [x] Create word storage system
  - [x] Implement AI word generation and storage
  - [x] Add word preview functionality
  - [x] Create word deletion functionality

- [x] **Day 5-7: Basic Review System**
  - [x] Implement simple review interface structure
  - [x] Create "Know/Don't Know" buttons (ready for Week 4)
  - [x] Add basic progress tracking
  - [x] Implement /review command structure

#### Deliverables:
- [x] Complete user onboarding flow
- [x] AI-powered word generation and management
- [x] Word preview and storage system
- [x] Progress tracking and statistics

#### ✅ Week 2 Decisions Made
1. **Review Interface:** One word per message with "знаю/не знаю" buttons ✅
2. **Word Display:** word → translation → examples (A1-A2 level) ✅
3. **Progress Metrics:** Total words, daily/weekly learned, review count, accuracy percentage ✅

---

## 🧠 Week 3: AI Integration & List Generation

### Milestone: Custom List Generation
**Target:** AI-powered word list creation

#### Tasks:
- [ ] **Day 1-2: OpenAI Integration**
  - [ ] Set up OpenAI API client
  - [ ] Create prompt templates for word generation
  - [ ] Implement error handling for API calls
  - [ ] Add rate limiting and cost monitoring

- [ ] **Day 3-4: List Generation Logic**
  - [ ] Implement /generate command
  - [ ] Create context parsing (e.g., "2-day trip to Barcelona")
  - [ ] Add clarifying questions for better relevance
  - [ ] Generate 10-20 words with translations and examples

- [ ] **Day 5-7: List Management**
  - [ ] Store generated lists in database
  - [ ] Add list naming/identification
  - [ ] Implement /lists command to view all lists
  - [ ] Add list deletion functionality

#### Deliverables:
- [ ] AI-powered word list generation
- [ ] Context-aware word selection
- [ ] List management system
- [ ] Cost-effective API usage

#### ✅ Week 3 Decisions Made
1. **AI Prompt Format:** Systematic prompt with language, level (A1/A2), context, JSON output ✅
2. **List Size:** Default 20 words, configurable up to 100 max ✅
3. **Context Examples:** User-defined context (e.g., "ordering food in restaurant") ✅
4. **API Budget:** $10/month limit with caching and optimization ✅

---

## 📅 Week 4: Spaced Repetition System

### Milestone: SRS Algorithm Implementation
**Target:** Automatic card scheduling

#### Tasks:
- [ ] **Day 1-2: SRS Algorithm**
  - [ ] Implement spaced repetition logic (1, 3, 7, 14, 30 days)
  - [ ] Create due date calculation
  - [ ] Add difficulty tracking per word
  - [ ] Implement interval adjustment based on performance

- [ ] **Day 3-4: Review Integration**
  - [ ] Connect SRS to review system
  - [ ] Implement due card prioritization
  - [ ] Add review session management
  - [ ] Create review completion tracking

- [ ] **Day 5-7: Scheduling System**
  - [ ] Implement automatic rescheduling
  - [ ] Add review reminders
  - [ ] Create daily due card notifications
  - [ ] Add review session limits

#### Deliverables:
- [ ] Working SRS algorithm
- [ ] Automatic card scheduling
- [ ] Review reminders
- [ ] Performance tracking

#### ❓ Open Questions - Week 4
1. **SRS Intervals:** Should we use the standard 1,3,7,14,30 days or customize based on language difficulty?
2. **Review Sessions:** How many cards should be reviewed per session? (all due cards or limit?)
3. **Reminders:** How often should we send review reminders? (daily, every 2 days?)
4. **Difficulty Levels:** Should we track difficulty per word or per user-word combination?

---

## 📊 Week 5: Progress Tracking & Analytics

### Milestone: User Analytics & Progress
**Target:** Comprehensive progress tracking

#### Tasks:
- [ ] **Day 1-2: Progress Metrics**
  - [ ] Implement word count tracking
  - [ ] Add review accuracy calculation
  - [ ] Create learning streak counter
  - [ ] Add time-based statistics

- [ ] **Day 3-4: Analytics Dashboard**
  - [ ] Create detailed /stats command
  - [ ] Add weekly/monthly progress reports
  - [ ] Implement performance graphs (text-based)
  - [ ] Add achievement tracking

- [ ] **Day 5-7: Data Management**
  - [ ] Add data export functionality
  - [ ] Implement backup system
  - [ ] Create data cleanup routines
  - [ ] Add performance optimization

#### Deliverables:
- [ ] Comprehensive progress tracking
- [ ] User analytics dashboard
- [ ] Data management tools
- [ ] Performance insights

#### ❓ Open Questions - Week 5
1. **Analytics Display:** How should we display statistics in Telegram? (text-based tables, charts?)
2. **Achievements:** What achievements should we implement? (first word, 7-day streak, etc.)
3. **Data Export:** What format should data export be in? (CSV, JSON, plain text?)
4. **Privacy:** How should we handle user data privacy and GDPR compliance?

---

## 🚀 Week 6: Testing & Launch Preparation

### Milestone: Production Ready Application
**Target:** Deployed and tested application

#### Tasks:
- [ ] **Day 1-2: Testing**
  - [ ] Unit testing for core functions
  - [ ] Integration testing for API calls
  - [ ] User acceptance testing
  - [ ] Performance testing

- [ ] **Day 3-4: Bug Fixes & Polish**
  - [ ] Fix identified issues
  - [ ] Improve error messages
  - [ ] Add input validation
  - [ ] Optimize performance

- [ ] **Day 5-7: Deployment & Launch**
  - [ ] Deploy to production environment
  - [ ] Set up monitoring and logging
  - [ ] Create user documentation
  - [ ] Plan launch strategy

#### Deliverables:
- [ ] Production-ready application
- [ ] Comprehensive testing
- [ ] Deployment documentation
- [ ] Launch strategy

#### ❓ Open Questions - Week 6
1. **Testing Strategy:** Who will be our beta testers? (friends, family, language learning communities?)
2. **Launch Marketing:** How should we promote the bot? (Reddit, Telegram groups, language learning forums?)
3. **Monitoring:** What metrics should we monitor in production? (API usage, error rates, user engagement?)
4. **Scaling:** What's our plan for handling increased user load?

---

## 📈 Post-Launch (Weeks 7-8)

### Milestone: User Feedback & Iteration
**Target:** User-driven improvements

#### Tasks:
- [ ] **Week 7: User Feedback Collection**
  - [ ] Implement feedback collection system
  - [ ] Monitor user behavior patterns
  - [ ] Collect user suggestions
  - [ ] Analyze usage data

- [ ] **Week 8: Iteration & Improvement**
  - [ ] Prioritize user feedback
  - [ ] Implement high-impact improvements
  - [ ] Fix critical bugs
  - [ ] Plan Phase 2 features

#### ❓ Open Questions - Post-Launch
1. **Feedback Channels:** How should users provide feedback? (in-bot command, external form, email?)
2. **Feature Prioritization:** What criteria should we use to prioritize new features?
3. **Monetization:** Should we consider monetization strategies for Phase 2?

---

## 🔧 Technical Architecture

### Database Schema (Draft)
```sql
-- Users table
users (
  telegram_id BIGINT PRIMARY KEY,
  username VARCHAR(255),
  language_from VARCHAR(10),
  language_to VARCHAR(10),
  timezone VARCHAR(50) DEFAULT 'UTC',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- Words table
words (
  id SERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(telegram_id),
  word VARCHAR(255),
  translation VARCHAR(255),
  example TEXT,
  context VARCHAR(255),
  difficulty INTEGER DEFAULT 1,
  next_review TIMESTAMP,
  interval_days INTEGER DEFAULT 1,
  created_at TIMESTAMP
)

-- Reviews table
reviews (
  id SERIAL PRIMARY KEY,
  word_id INTEGER REFERENCES words(id),
  user_id BIGINT REFERENCES users(telegram_id),
  knew BOOLEAN,
  reviewed_at TIMESTAMP
)
```

### API Endpoints (Draft)
- `POST /webhook` - Telegram webhook
- `GET /health` - Health check
- `POST /generate` - Generate word list (internal)

### Environment Variables Needed
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:pass@host:port/db
TIMEZONE=UTC
```

---

## 📝 Notes & Decisions Log

### Decisions Made:
- [ ] Telegram bot as primary interface
- [ ] AI-generated content vs pre-built database
- [ ] Binary review system (Know/Don't Know)
- [ ] Simple SRS intervals (1,3,7,14,30 days)

### Pending Decisions:
- [ ] Review interface design
- [ ] Analytics display format
- [ ] AI prompt format
- [ ] List size configuration

---

## 🎯 Success Criteria

### MVP Success Metrics:
- [ ] 100+ active users within 2 weeks of launch
- [ ] 70% user retention after 7 days
- [ ] Average 3+ word lists generated per user
- [ ] 80%+ review completion rate
- [ ] < 5% error rate in AI word generation

### Technical Success Criteria:
- [ ] Bot responds within 2 seconds
- [ ] 99% uptime
- [ ] < $50/month OpenAI API costs
- [ ] Database handles 1000+ users
- [ ] Zero data loss incidents

---

**Last Updated:** December 2024  
**Next Review:** Weekly during development  
**Status:** Week 2 Complete - Ready for Week 3 (SRS Implementation)
