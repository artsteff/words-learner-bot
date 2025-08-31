from datetime import datetime
from typing import List, Dict, Optional
import logging
from database.models import Word, SessionLocal

logger = logging.getLogger(__name__)

class WordService:
    """Word management service"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def add_words_from_list(self, user_id: int, words_data: List[Dict], context: str = None) -> List[Word]:
        """Add multiple words from AI-generated list"""
        try:
            added_words = []
            
            for word_data in words_data:
                word = Word(
                    user_id=user_id,
                    word=word_data["word"],
                    translation=word_data["translation"],
                    example=word_data.get("example_sentence_L1", ""),  # Store L1 example
                    context=context,
                    difficulty=1,
                    next_review=datetime.utcnow(),  # Available for immediate review
                    interval_days=1,
                    created_at=datetime.utcnow()
                )
                self.db.add(word)
                added_words.append(word)
            
            self.db.commit()
            logger.info(f"Added {len(added_words)} words for user {user_id}")
            return added_words
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding words: {e}")
            return []
    
    def get_user_words(self, user_id: int, limit: int = 50) -> List[Word]:
        """Get all words for a user"""
        try:
            words = self.db.query(Word).filter(
                Word.user_id == user_id
            ).order_by(Word.created_at.desc()).limit(limit).all()
            
            return words
            
        except Exception as e:
            logger.error(f"Error getting user words: {e}")
            return []
    
    def get_word_by_id(self, word_id: int, user_id: int) -> Optional[Word]:
        """Get specific word by ID"""
        try:
            word = self.db.query(Word).filter(
                Word.id == word_id,
                Word.user_id == user_id
            ).first()
            
            return word
            
        except Exception as e:
            logger.error(f"Error getting word by ID: {e}")
            return None
    
    def delete_word(self, word_id: int, user_id: int) -> bool:
        """Delete a word"""
        try:
            word = self.db.query(Word).filter(
                Word.id == word_id,
                Word.user_id == user_id
            ).first()
            
            if not word:
                logger.error(f"Word {word_id} not found for user {user_id}")
                return False
            
            self.db.delete(word)
            self.db.commit()
            
            logger.info(f"Deleted word {word_id} for user {user_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting word: {e}")
            return False
    
    def get_words_by_context(self, user_id: int, context: str) -> List[Word]:
        """Get words by context"""
        try:
            words = self.db.query(Word).filter(
                Word.user_id == user_id,
                Word.context == context
            ).order_by(Word.created_at.desc()).all()
            
            return words
            
        except Exception as e:
            logger.error(f"Error getting words by context: {e}")
            return []
    
    def get_word_count_by_context(self, user_id: int) -> Dict[str, int]:
        """Get word count grouped by context"""
        try:
            from sqlalchemy import func
            
            result = self.db.query(
                Word.context,
                func.count(Word.id).label('count')
            ).filter(
                Word.user_id == user_id
            ).group_by(Word.context).all()
            
            return {row.context or "General": row.count for row in result}
            
        except Exception as e:
            logger.error(f"Error getting word count by context: {e}")
            return {}
    
    def format_word_for_display(self, word: Word) -> str:
        """Format word for Telegram display"""
        try:
            # Format: word → translation → example
            display = f"**{word.word}** → {word.translation}"
            
            if word.example:
                display += f"\n💡 {word.example}"
            
            return display
            
        except Exception as e:
            logger.error(f"Error formatting word: {e}")
            return f"{word.word} → {word.translation}"
    
    def get_word_stats(self, user_id: int) -> Dict[str, int]:
        """Get word statistics for user"""
        try:
            from sqlalchemy import func
            
            # Total words
            total_words = self.db.query(func.count(Word.id)).filter(
                Word.user_id == user_id
            ).scalar()
            
            # Words added today
            today = datetime.utcnow().date()
            today_words = self.db.query(func.count(Word.id)).filter(
                Word.user_id == user_id,
                func.date(Word.created_at) == today
            ).scalar()
            
            # Words due for review
            due_words = self.db.query(func.count(Word.id)).filter(
                Word.user_id == user_id,
                Word.next_review <= datetime.utcnow()
            ).scalar()
            
            return {
                "total_words": total_words or 0,
                "today_words": today_words or 0,
                "due_words": due_words or 0
            }
            
        except Exception as e:
            logger.error(f"Error getting word stats: {e}")
            return {
                "total_words": 0,
                "today_words": 0,
                "due_words": 0
            }

# Global instance
word_service = WordService()
