from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

Base = declarative_base()

class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime)
    priority = Column(Enum(Priority))
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    estimated_duration = Column(Float)  # in hours
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    study_blocks = relationship("StudyBlock", back_populates="task")

class StudyBlock(Base):
    __tablename__ = "study_blocks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    actual_duration = Column(Float)  # in hours
    productivity_score = Column(Integer)  # 1-10
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="study_blocks")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    preferred_study_hours = Column(String)  # JSON string of preferred hours
    break_duration = Column(Integer)  # in minutes
    study_block_duration = Column(Integer)  # in minutes
    productivity_peaks = Column(String)  # JSON string of peak hours
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user") 