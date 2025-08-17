from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class Priority(str, Enum):
    HIGH = "high"
    MED  = "med"
    LOW  = "low"

class TaskStatus(str, Enum):
    OPEN = "open"
    COMPLETED = "completed"

class Task(db.Model):
    __tablename__ = "tasks"
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False, unique=True)
    due_date  = db.Column(db.DateTime, nullable=False)
    priority  = db.Column(db.String(10), nullable=False, default=Priority.MED.value)
    category  = db.Column(db.String(100), nullable=True)
    status    = db.Column(db.String(20), nullable=False, default=TaskStatus.OPEN.value)

    def is_overdue(self, now: datetime | None = None) -> bool:
        now = now or datetime.now()
        return self.due_date < now and self.status == TaskStatus.OPEN.value

    def is_due_today(self, today: date | None = None) -> bool:
        today = today or date.today()
        return self.due_date.date() == today and self.status == TaskStatus.OPEN.value
