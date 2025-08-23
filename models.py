"""
models.py
Database schema + domain logic for Planception.
"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

# SQLAlchemy instance (bound to Flask app in app.py)
db = SQLAlchemy()

class Priority(str, Enum):
    """Enum of allowed task priorities."""
    HIGH = "high"
    MED  = "med"
    LOW  = "low"

class TaskStatus(str, Enum):
    """Enum for task lifecycle state."""
    OPEN = "open"
    COMPLETED = "completed"

class Task(db.Model):
    """
    ORM-mapped Task entity.

    Fields:
    - id: primary key
    - name: unique title of the task
    - due_date: deadline (date+time; we only compare date portion)
    - priority: one of {'high','med','low'}
    - category: optional grouping label
    - status: open/completed
    """
    __tablename__ = "tasks"
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False, unique=True)
    due_date  = db.Column(db.DateTime, nullable=False)
    priority  = db.Column(db.String(10), nullable=False, default=Priority.MED.value)
    category  = db.Column(db.String(100), nullable=True)
    status    = db.Column(db.String(20), nullable=False, default=TaskStatus.OPEN.value)

    def is_overdue(self, today: date | None = None) -> bool:
        # return True if task is overdue (due date before today and still open)
        today = today or date.today()
        return self.due_date.date() < today and self.status == TaskStatus.OPEN.value

    def is_due_today(self, today: date | None = None) -> bool:
        # return True if task is due today (due date is today and still open)
        today = today or date.today()
        return self.due_date.date() == today and self.status == TaskStatus.OPEN.value
