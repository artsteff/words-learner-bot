from datetime import datetime, timedelta
from typing import List, Optional
import logging
from database.models import Word, Review, SessionLocal

logger = logging.getLogger(__name__)

class SRSService:
    """Spaced Repetition System service"""
    
    # SRS intervals in days
    INTERVALS = [1, 3, 7, 14, 30]
    
    def __init__(self):
        self.db = SessionLocal()
    
    def get_due_words(self, user_id: int, limit: int = 20) -> List[Word]:
        """Get words that are due for review"""
        try:
            due_words = self.db.query(Word).filter(
                Word.user_id == user_id,
                Word.next_review <= datetime.utcnow()
            ).limit(limit).all()
            
            logger.info(f"Found {len(due_words)} due words for user {user_id}")
            return due_words
            
        except Exception as e:
            logger.error(f"Error getting due words: {e}")
            return []
    
    def process_review(self, word_id: int, user_id: int, knew: bool) -> bool:
        """Process a word review and update SRS schedule"""
        try:
            word = self.db.query(Word).filter(
                Word.id == word_id,
                Word.user_id == user_id
            ).first()
            
            if not word:
                logger.error(f"Word {word_id} not found for user {user_id}")
                return False
            
            # Create review record
            review = Review(
                word_id=word_id,
                user_id=user_id,
                knew=knew,
                reviewed_at=datetime.utcnow()
            )
            self.db.add(review)
            
            # Update word schedule
            self._update_word_schedule(word, knew)
            
            self.db.commit()
            logger.info(f"Processed review for word {word_id}, knew={knew}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error processing review: {e}")
            return False
    
    def _update_word_schedule(self, word: Word, knew: bool):
        """Update word's next review date based on SRS algorithm"""
        current_interval = word.interval_days
        
        if knew:
            # Move to next interval
            current_index = self.INTERVALS.index(current_interval) if current_interval in self.INTERVALS else 0
            next_index = min(current_index + 1, len(self.INTERVALS) - 1)
            new_interval = self.INTERVALS[next_index]
        else:
            # Reset to first interval
            new_interval = self.INTERVALS[0]
        
        # Update word
        word.interval_days = new_interval
        word.next_review = datetime.utcnow() + timedelta(days=new_interval)
        word.difficulty = 1 if knew else 0  # Simple difficulty tracking
    
    def get_review_stats(self, user_id: int) -> dict:
        """Get review statistics for a user"""
        try:
            # Total words
            total_words = self.db.query(Word).filter(Word.user_id == user_id).count()
            
            # Due words
            due_words = self.db.query(Word).filter(
                Word.user_id == user_id,
                Word.next_review <= datetime.utcnow()
            ).count()
            
            # Today's reviews
            today = datetime.utcnow().date()
            today_reviews = self.db.query(Review).filter(
                Review.user_id == user_id,
                Review.reviewed_at >= today
            ).count()
            
            # Accuracy (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_reviews = self.db.query(Review).filter(
                Review.user_id == user_id,
                Review.reviewed_at >= thirty_days_ago
            ).all()
            
            if recent_reviews:
                accuracy = sum(1 for r in recent_reviews if r.knew) / len(recent_reviews) * 100
            else:
                accuracy = 0
            
            return {
                "total_words": total_words,
                "due_words": due_words,
                "today_reviews": today_reviews,
                "accuracy": round(accuracy, 1)
            }
            
        except Exception as e:
            logger.error(f"Error getting review stats: {e}")
            return {
                "total_words": 0,
                "due_words": 0,
                "today_reviews": 0,
                "accuracy": 0
            }
    
    def get_learning_streak(self, user_id: int) -> int:
        """Calculate user's learning streak (consecutive days with reviews)"""
        try:
            # Get all review dates for user
            reviews = self.db.query(Review.reviewed_at).filter(
                Review.user_id == user_id
            ).distinct().all()
            
            if not reviews:
                return 0
            
            # Convert to dates and sort
            review_dates = [r.reviewed_at.date() for r in reviews]
            review_dates.sort(reverse=True)
            
            # Calculate streak
            streak = 0
            current_date = datetime.utcnow().date()
            
            for i, review_date in enumerate(review_dates):
                if i == 0:
                    # Check if today or yesterday
                    if review_date == current_date or review_date == current_date - timedelta(days=1):
                        streak = 1
                    else:
                        break
                else:
                    # Check for consecutive days
                    expected_date = current_date - timedelta(days=i)
                    if review_date == expected_date:
                        streak += 1
                    else:
                        break
            
            return streak
            
        except Exception as e:
            logger.error(f"Error calculating learning streak: {e}")
            return 0

# Global instance
srs_service = SRSService()
