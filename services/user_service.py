from datetime import datetime
from typing import Optional, Dict, Any
import logging
from database.models import User, SessionLocal

logger = logging.getLogger(__name__)

class UserService:
    """User management service"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def get_or_create_user(self, telegram_id: int, username: str = None) -> User:
        """Get existing user or create new one"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                # Create new user
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    created_at=datetime.utcnow(),
                    last_active=datetime.utcnow()
                )
                self.db.add(user)
                self.db.commit()
                logger.info(f"Created new user: {telegram_id}")
            else:
                # Update last active
                user.last_active = datetime.utcnow()
                if username and username != user.username:
                    user.username = username
                self.db.commit()
                logger.info(f"Updated user: {telegram_id}")
            
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error in get_or_create_user: {e}")
            raise
    
    def update_user_languages(self, telegram_id: int, language_from: str, language_to: str) -> bool:
        """Update user's language pair"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                logger.error(f"User {telegram_id} not found")
                return False
            
            user.language_from = language_from
            user.language_to = language_to
            user.last_active = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Updated languages for user {telegram_id}: {language_from} -> {language_to}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user languages: {e}")
            return False
    
    def update_user_timezone(self, telegram_id: int, timezone: str) -> bool:
        """Update user's timezone"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                logger.error(f"User {telegram_id} not found")
                return False
            
            user.timezone = timezone
            user.last_active = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Updated timezone for user {telegram_id}: {timezone}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user timezone: {e}")
            return False
    
    def get_user_profile(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile information"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return None
            
            return {
                "telegram_id": user.telegram_id,
                "username": user.username,
                "language_from": user.language_from,
                "language_to": user.language_to,
                "timezone": user.timezone,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_active": user.last_active.isoformat() if user.last_active else None
            }
            
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return None
    
    def is_user_configured(self, telegram_id: int) -> bool:
        """Check if user has completed initial setup"""
        try:
            user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return False
            
            return bool(user.language_from and user.language_to)
            
        except Exception as e:
            logger.error(f"Error checking user configuration: {e}")
            return False
    
    def get_user_stats(self, telegram_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            from services.srs_service import srs_service
            
            # Get basic stats from SRS service
            stats = srs_service.get_review_stats(telegram_id)
            streak = srs_service.get_learning_streak(telegram_id)
            
            # Get user profile
            profile = self.get_user_profile(telegram_id)
            
            return {
                "profile": profile,
                "stats": stats,
                "streak": streak
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {
                "profile": None,
                "stats": {"total_words": 0, "due_words": 0, "today_reviews": 0, "accuracy": 0},
                "streak": 0
            }

# Global instance
user_service = UserService()
