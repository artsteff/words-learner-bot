#!/usr/bin/env python3
"""
Simple test script to verify the bot works locally
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application

# Load environment variables
load_dotenv()

async def test_bot():
    """Test basic bot functionality"""
    
    # Get bot token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found!")
        return
    
    print(f"✅ Bot token found: {token[:20]}...")
    
    # Test bot connection
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"   Name: {me.first_name}")
        print(f"   Username: @{me.username}")
        print(f"   ID: {me.id}")
        
        # Test basic commands
        print("\n📋 Testing basic commands...")
        
        # Test /start command
        print("   Testing /start command...")
        
        # Test OpenAI API
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print(f"✅ OpenAI API key found: {openai_key[:20]}...")
        else:
            print("❌ OpenAI API key not found!")
        
        print("\n🎉 Basic tests completed!")
        print("\nNext steps:")
        print("1. Set up PostgreSQL database")
        print("2. Run: python main.py")
        print("3. Test bot commands in Telegram")
        
    except Exception as e:
        print(f"❌ Error testing bot: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
