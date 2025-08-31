from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Words Learner Bot", version="1.0.0")

# Initialize database (optional for testing)
try:
    from database.models import create_tables
    create_tables()
    logger.info("Database tables created successfully")
except Exception as e:
    logger.warning(f"Database initialization failed: {e}. Running in test mode.")

# Telegram bot setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
    raise ValueError("TELEGRAM_BOT_TOKEN is required")

telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

# Initialize the application
async def initialize_telegram():
    """Initialize Telegram application"""
    await telegram_app.initialize()
    await telegram_app.start()
    logger.info("Telegram application initialized successfully")

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Telegram app on FastAPI startup"""
    await initialize_telegram()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown Telegram app on FastAPI shutdown"""
    await telegram_app.stop()
    await telegram_app.shutdown()
    logger.info("Telegram application shutdown successfully")

# Basic command handlers
async def start_command(update: Update, context: CallbackContext) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    # Get or create user
    try:
        from services.user_service import user_service
        user_service.get_or_create_user(user.id, user.username)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
    
    welcome_message = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в Words Learner Bot! 

Этот бот поможет вам изучать слова с помощью:
• Генерации персональных списков слов
• Системы интервального повторения
• Простого интерфейса "Знаю/Не знаю"

Выберите языковую пару для начала:
"""
    
    # Create inline keyboard for language selection
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English ↔ 🇳🇱 Dutch", callback_data="lang_en_nl")],
        [InlineKeyboardButton("🇬🇧 English ↔ 🇷🇺 Russian", callback_data="lang_en_ru")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Handle /help command"""
    help_text = """
📚 Доступные команды:

/start - Начать работу с ботом
/help - Показать эту справку
/generate - Создать новый список слов
/learn - Изучить слова
/stats - Показать статистику
/profile - Настройки профиля

💡 Как использовать:
1. Выберите языковую пару
2. Опишите контекст (например, "поездка в Амстердам")
3. Получите персональный список слов
4. Регулярно изучайте слова
"""
    await update.message.reply_text(help_text)

async def generate_command(update: Update, context: CallbackContext) -> None:
    """Handle /generate command"""
    user = update.effective_user
    
    # Check if user is configured
    try:
        from services.user_service import user_service
        if not user_service.is_user_configured(user.id):
            await update.message.reply_text(
                "⚠️ Сначала выберите языковую пару!\n\n"
                "Используйте /start для настройки профиля."
            )
            return
    except Exception as e:
        logger.error(f"Error checking user configuration: {e}")
    
    await update.message.reply_text(
        "🎯 Опишите контекст для генерации слов.\n\n"
        "Например:\n"
        "• '2-дневная поездка в Барселону'\n"
        "• 'деловая встреча'\n"
        "• 'поход в ресторан'\n"
        "• 'заказ еды в ресторане'\n\n"
        "По умолчанию будет создано 20 слов.\n"
        "Можно указать количество: 'ресторан 15'"
    )

async def learn_command(update: Update, context: CallbackContext) -> None:
    """Handle /learn command"""
    user = update.effective_user
    
    try:
        from services.srs_service import SRSService
        srs_service = SRSService()
        
        # Get due words for review
        due_words = srs_service.get_due_words(user.id, limit=10)
        
        if not due_words:
            await update.message.reply_text(
                "🎉 Отлично! У вас нет слов для изучения.\n\n"
                "Все слова уже выучены или еще не готовы для повторения.\n"
                "Используйте /generate для добавления новых слов!"
            )
            return
        
        # Store words in context for this session
        context.user_data['review_words'] = due_words
        context.user_data['current_word_index'] = 0
        context.user_data['review_session_active'] = True
        
        # Show first word
        await show_next_review_word(update, context)
        
    except Exception as e:
        logger.error(f"Error starting learning session: {e}")
        await update.message.reply_text(
            "❌ Ошибка при запуске изучения.\n"
            "Попробуйте позже."
        )

async def show_next_review_word(update: Update, context: CallbackContext, from_callback: bool = False) -> None:
    """Show next word for review"""
    try:
        words = context.user_data.get('review_words', [])
        current_index = context.user_data.get('current_word_index', 0)
        
        if current_index >= len(words):
            # Learning session complete
            completion_message = (
                "🎉 Изучение завершено!\n\n"
                f"Вы повторили {len(words)} слов.\n"
                "Используйте /stats для просмотра статистики."
            )
            
            if from_callback and update.callback_query:
                # We're in a callback query context
                await update.callback_query.message.reply_text(completion_message)
            elif update.message:
                # We're in a regular message context
                await update.message.reply_text(completion_message)
            else:
                logger.error("Cannot send message: neither callback_query nor message available")
            
            # Clear session data
            context.user_data.clear()
            return
        
        word = words[current_index]
        
        # Create inline keyboard for "Знаю/Не знаю" buttons
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Знаю", callback_data=f"review_knew_{word.id}"),
                InlineKeyboardButton("❌ Не знаю", callback_data=f"review_didnt_know_{word.id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Show word
        word_message = f"""
📖 Слово {current_index + 1} из {len(words)}:

**{word.word}** → {word.translation}

💡 Пример:
{word.example if word.example else 'Пример не доступен'}
"""
        
        if from_callback and update.callback_query:
            # We're in a callback query context
            await update.callback_query.message.reply_text(word_message, reply_markup=reply_markup)
        elif update.message:
            # We're in a regular message context
            await update.message.reply_text(word_message, reply_markup=reply_markup)
        else:
            logger.error("Cannot send word message: neither callback_query nor message available")
        
    except Exception as e:
        logger.error(f"Error showing review word: {e}")
        error_message = "❌ Ошибка при показе слова.\nПопробуйте /learn снова."
        
        if from_callback and update.callback_query:
            await update.callback_query.message.reply_text(error_message)
        elif update.message:
            await update.message.reply_text(error_message)
        else:
            logger.error("Cannot send error message: neither callback_query nor message available")

async def stats_command(update: Update, context: CallbackContext) -> None:
    """Handle /stats command"""
    user = update.effective_user
    
    try:
        from services.user_service import user_service
        user_stats = user_service.get_user_stats(user.id)
        
        stats = user_stats.get("stats", {})
        streak = user_stats.get("streak", 0)
        profile = user_stats.get("profile", {})
        
        stats_message = f"""
📊 Ваша статистика:

📚 Слова:
• Всего слов: {stats.get('total_words', 0)}
• Добавлено сегодня: {stats.get('today_reviews', 0)}
• Ожидают повторения: {stats.get('due_words', 0)}

🎯 Прогресс:
• Точность: {stats.get('accuracy', 0)}%
• Серия дней: {streak}

👤 Профиль:
• Языковая пара: {profile.get('language_from', 'Не выбрана')} → {profile.get('language_to', 'Не выбрана')}
• Часовой пояс: {profile.get('timezone', 'UTC')}
"""
        
        await update.message.reply_text(stats_message)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await update.message.reply_text(
            "📊 Ваша статистика:\n\n"
            "📚 Слова:\n"
            "• Всего слов: 0\n"
            "• Добавлено сегодня: 0\n"
            "• Ожидают повторения: 0\n\n"
            "🎯 Прогресс:\n"
            "• Точность: 0%\n"
            "• Серия дней: 0\n\n"
            "👤 Профиль:\n"
            "• Языковая пара: Не выбрана\n"
            "• Часовой пояс: UTC"
        )

async def profile_command(update: Update, context: CallbackContext) -> None:
    """Handle /profile command"""
    user = update.effective_user
    
    try:
        from services.user_service import user_service
        profile = user_service.get_user_profile(user.id)
        
        if profile:
            profile_message = f"""
👤 Ваш профиль:

📝 Основная информация:
• Имя: {user.first_name}
• Username: @{user.username or 'Не указан'}
• ID: {user.id}

🌍 Языки:
• Языковая пара: {profile.get('language_from', 'Не выбрана')} → {profile.get('language_to', 'Не выбрана')}
• Часовой пояс: {profile.get('timezone', 'UTC')}

📅 Активность:
• Дата регистрации: {profile.get('created_at', 'Неизвестно')}
• Последняя активность: {profile.get('last_active', 'Неизвестно')}

💡 Для изменения настроек используйте /start
"""
        else:
            profile_message = """
👤 Профиль не найден.

Используйте /start для создания профиля.
"""
        
        await update.message.reply_text(profile_message)
        
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        await update.message.reply_text(
            "❌ Ошибка при получении профиля.\n"
            "Попробуйте позже."
        )

async def handle_callback_query(update: Update, context: CallbackContext) -> None:
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data.startswith("lang_"):
            # Language selection
            _, lang_from, lang_to = query.data.split("_")
            
            from services.user_service import user_service
            user_service.update_user_languages(query.from_user.id, lang_from, lang_to)
            
            await query.edit_message_text(
                f"✅ Языковая пара установлена: {lang_from.upper()} → {lang_to.upper()}\n\n"
                "Теперь вы можете:\n"
                "• /generate - создать список слов\n"
                "• /learn - изучить слова\n"
                "• /stats - посмотреть статистику"
            )
        
        elif query.data.startswith("review_"):
            # Review session buttons
            user = query.from_user
            review_data = query.data.split("_")
            action = review_data[1]  # "knew" or "didnt_know"
            word_id = int(review_data[2])
            
            try:
                from services.srs_service import SRSService
                srs_service = SRSService()
                
                # Process the review
                knew = (action == "knew")
                success = srs_service.process_review(word_id, user.id, knew)
                
                if success:
                    # Move to next word
                    context.user_data['current_word_index'] = context.user_data.get('current_word_index', 0) + 1
                    
                    # Show feedback
                    feedback = "✅ Правильно!" if knew else "❌ Неправильно. Попробуйте еще раз!"
                    await query.edit_message_text(feedback)
                    
                    # Show next word after a short delay
                    await asyncio.sleep(1)
                    try:
                        await show_next_review_word(update, context, from_callback=True)
                    except Exception as e:
                        logger.error(f"Error showing next review word: {e}")
                        await query.edit_message_text(
                            "❌ Ошибка при показе следующего слова.\n"
                            "Попробуйте /learn снова."
                        )
                else:
                    await query.edit_message_text(
                        "❌ Ошибка при обработке ответа.\n"
                        "Попробуйте /learn снова."
                    )
            except Exception as e:
                logger.error(f"Error processing review: {e}")
                await query.edit_message_text(
                    "❌ Ошибка при обработке ответа.\n"
                    "Попробуйте /review снова."
                )
            
    except Exception as e:
        logger.error(f"Error handling callback query: {e}")
        await query.edit_message_text("❌ Произошла ошибка. Попробуйте снова.")

async def handle_text_message(update: Update, context: CallbackContext) -> None:
    """Handle text messages (context for word generation)"""
    user = update.effective_user
    text = update.message.text
    
    try:
        from services.user_service import user_service
        
        # Check if user is configured
        if not user_service.is_user_configured(user.id):
            await update.message.reply_text(
                "⚠️ Сначала выберите языковую пару!\n\n"
                "Используйте /start для настройки профиля."
            )
            return
        
        # Parse context and count
        parts = text.strip().split()
        
        # Check if the last part is a number
        if len(parts) >= 2:
            try:
                count = int(parts[-1])
                if count > 100:
                    count = 100
                    await update.message.reply_text("⚠️ Максимум 100 слов. Установлено 100.")
                # Remove the count from context
                context_text = " ".join(parts[:-1])
            except ValueError:
                # Last part is not a number, use default count
                context_text = text
                count = 20
        else:
            # Only one word or empty, use default count
            context_text = text
            count = 20
        
        # Get user's language pair
        profile = user_service.get_user_profile(user.id)
        lang_from = profile.get("language_from")
        lang_to = profile.get("language_to")
        
        # Show "generating" message
        generating_msg = await update.message.reply_text(
            f"🤖 Генерирую {count} слов для контекста: '{context_text}'...\n"
            "Это может занять несколько секунд."
        )
        
        # Generate words
        from services.ai_service import ai_service
        words = await ai_service.generate_word_list(context_text, lang_from, lang_to, count)
        
        if words:
            # Add words to database
            from services.word_service import word_service
            added_words = word_service.add_words_from_list(user.id, words, context_text)
            
            # Show results
            result_message = f"""
✅ Создан список из {len(added_words)} слов!

📝 Контекст: {context_text}
🌍 Языки: {lang_from.upper()} → {lang_to.upper()}
📊 Запрошено: {count} слов

📚 Слова добавлены в вашу коллекцию.
Используйте /learn для изучения!
"""
            
            await generating_msg.edit_text(result_message)
            
            # Show first few words as preview
            if len(words) > 0:
                preview = "📖 Предварительный просмотр:\n\n"
                for i, word in enumerate(words[:3]):  # Show first 3 words
                    preview += f"{i+1}. {word['word']} → {word['translation']}\n"
                    if word.get('example_sentence_L1'):
                        preview += f"   💡 {word['example_sentence_L1']}\n"
                    preview += "\n"
                
                if len(words) > 3:
                    preview += f"... и еще {len(words) - 3} слов"
                
                await update.message.reply_text(preview)
        else:
            await generating_msg.edit_text(
                "❌ Не удалось сгенерировать слова.\n"
                "Попробуйте другой контекст или попробуйте позже."
            )
            
    except Exception as e:
        logger.error(f"Error handling text message: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при генерации слов.\n"
            "Попробуйте позже."
        )

# Add command handlers
telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("generate", generate_command))
telegram_app.add_handler(CommandHandler("learn", learn_command))
telegram_app.add_handler(CommandHandler("stats", stats_command))
telegram_app.add_handler(CommandHandler("profile", profile_command))

# Add callback query handler for inline keyboards
from telegram.ext import CallbackQueryHandler
telegram_app.add_handler(CallbackQueryHandler(handle_callback_query))

# Add message handler for text input
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

# Webhook endpoint for Telegram
@app.post("/webhook")
async def webhook(request: Request):
    """Handle Telegram webhook"""
    try:
        data = await request.json()
        logger.info(f"Received webhook update: {data.get('update_id', 'unknown')}")
        
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        
        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        # Return 200 even on error to prevent Telegram from retrying
        return JSONResponse(content={"status": "error", "message": str(e)})

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "bot": "Words Learner Bot"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Words Learner Bot API", "version": "1.0.0"}

if __name__ == "__main__":
    try:
        logger.info("Starting Words Learner Bot...")
        logger.info(f"Telegram Token: {'SET' if TELEGRAM_TOKEN else 'MISSING'}")
        logger.info(f"OpenAI Key: {'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING'}")
        logger.info(f"Database URL: {'SET' if os.getenv('DATABASE_URL') else 'MISSING'}")
        
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
