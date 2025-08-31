#!/usr/bin/env python3
"""
Test script for Week 2 functionality
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_week2_features():
    """Test Week 2 features"""
    
    print("🧪 Testing Week 2 Features...\n")
    
    # Test 1: Environment variables
    print("1. Environment Variables:")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if telegram_token:
        print("   ✅ TELEGRAM_BOT_TOKEN found")
    else:
        print("   ❌ TELEGRAM_BOT_TOKEN missing")
    
    if openai_key:
        print("   ✅ OPENAI_API_KEY found")
    else:
        print("   ❌ OPENAI_API_KEY missing")
    
    # Test 2: Import services
    print("\n2. Service Imports:")
    try:
        from services.user_service import user_service
        print("   ✅ UserService imported")
    except Exception as e:
        print(f"   ❌ UserService import failed: {e}")
    
    try:
        from services.word_service import word_service
        print("   ✅ WordService imported")
    except Exception as e:
        print(f"   ❌ WordService import failed: {e}")
    
    try:
        from services.ai_service import ai_service
        print("   ✅ AIService imported")
    except Exception as e:
        print(f"   ❌ AIService import failed: {e}")
    
    try:
        from services.srs_service import srs_service
        print("   ✅ SRSService imported")
    except Exception as e:
        print(f"   ❌ SRSService import failed: {e}")
    
    # Test 3: Database models
    print("\n3. Database Models:")
    try:
        from database.models import User, Word, Review
        print("   ✅ Database models imported")
    except Exception as e:
        print(f"   ❌ Database models import failed: {e}")
    
    # Test 4: AI Service functionality
    print("\n4. AI Service Test:")
    try:
        from services.ai_service import ai_service
        
        # Test prompt generation
        prompt = ai_service._create_dutch_prompt("restaurant", 5)
        if "restaurant" in prompt and "A1-A2" in prompt:
            print("   ✅ AI prompt generation works")
        else:
            print("   ❌ AI prompt generation failed")
            
    except Exception as e:
        print(f"   ❌ AI service test failed: {e}")
    
    print("\n🎉 Week 2 Feature Tests Completed!")
    print("\nNext steps:")
    print("1. Set up PostgreSQL database")
    print("2. Test bot with /start command")
    print("3. Test word generation with context")
    print("4. Verify user management functionality")

if __name__ == "__main__":
    asyncio.run(test_week2_features())
