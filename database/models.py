from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, BigInteger, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/wordslearner")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String(255))
    language_from = Column(String(10))
    language_to = Column(String(10))
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    words = relationship("Word", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    word = Column(String(255), nullable=False)
    translation = Column(String(255), nullable=False)
    example = Column(Text)
    context = Column(String(255))
    difficulty = Column(Integer, default=1)
    next_review = Column(DateTime, default=datetime.utcnow)
    interval_days = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="words")
    reviews = relationship("Review", back_populates="word")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    knew = Column(Boolean, nullable=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    word = relationship("Word", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
