from typing import List
from datetime import datetime, date
from models import db, Task, Priority

class TaskRepository:
    def add(self, name: str, due_str: str, priority: str, category: str) -> bool:
        if not name or not name.strip():
            return False
        try:
            due_dt = datetime.strptime(due_str, "%Y-%m-%d")
        except ValueError:
            return False
        if priority not in (p.value for p in Priority):
            return False
        if Task.query.filter(Task.name.ilike(name.strip())).first():
            return False
        t = Task(name=name.strip(), due_date=due_dt, priority=priority, category=category)
        db.session.add(t)
        db.session.commit()
        return True

    def delete(self, name: str) -> bool:
        t = Task.query.filter(Task.name.ilike(name.strip())).first()
        if not t: return False
        db.session.delete(t)
        db.session.commit()
        return True

    def all_sorted(self) -> List[Task]:
        return Task.query.order_by(Task.due_date.asc()).all()

    def by_category(self, category: str) -> List[Task]:
        return Task.query.filter_by(category=category).order_by(Task.due_date.asc()).all()

    def overdue(self, now: datetime | None = None) -> List[Task]:
        now = now or datetime.now()
        return Task.query.filter(Task.due_date < now, Task.status == "open").all()

    def due_today(self, today: date | None = None) -> List[Task]:
        today = today or date.today()
        return [t for t in self.all_sorted() if t.is_due_today(today)]
