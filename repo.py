"""
repo.py
Repository layer: directly interacts with the database.

Keeps raw SQLAlchemy operations separate from business logic,
so we can later swap persistence (different DB) or stub in tests.
"""

from typing import List
from datetime import datetime, date
from models import db, Task, Priority

class TaskRepository:
    """Encapsulates CRUD + query operations for Task entities."""
    
    def add(self, name: str, due_str: str, priority: str, category: str) -> bool:
        # Add a new task; return True if successful, False if invalid input.
        if not name or not name.strip():
            return False
        
        # Parse date string
        try:
            due_dt = datetime.strptime(due_str, "%Y-%m-%d")
        except ValueError:
            return False
        
        # Validate priority
        if priority not in (p.value for p in Priority):
            return False
        
        # Reject duplicate names (case-insensitive)
        if Task.query.filter(Task.name.ilike(name.strip())).first():
            return False
        
        # Persist new task
        t = Task(name=name.strip(), due_date=due_dt, priority=priority, category=category)
        db.session.add(t)
        db.session.commit()
        return True

    def delete(self, name: str) -> bool:
        # Delete task by name; return True if deleted, False if not found.
        t = Task.query.filter(Task.name.ilike(name.strip())).first()
        if not t: return False
        db.session.delete(t)
        db.session.commit()
        return True

    def all_sorted(self) -> List[Task]:
        # Return all tasks sorted by due date ascending
        return Task.query.order_by(Task.due_date.asc()).all()

    def by_category(self, category: str) -> List[Task]:
        # Return all tasks in the given category, sorted by due date
        return Task.query.filter_by(category=category).order_by(Task.due_date.asc()).all()

    def overdue(self, now: datetime | None = None) -> List[Task]:
        # Return all overdue tasks (due date before now and still open)
        now = now or datetime.now()
        return Task.query.filter(Task.due_date < now, Task.status == "open").all()

    def due_today(self, today: date | None = None) -> List[Task]:
        # Return all tasks due today (due date is today and still open)
        today = today or date.today()
        return [t for t in self.all_sorted() if t.is_due_today(today)]
