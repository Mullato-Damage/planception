# Cleaned, testable task utilities with clearer names & structure

from dataclasses import dataclass
from datetime import datetime, date
from typing import List

DATE_FMT = "%m-%d-%Y"
VALID_PRIORITIES = ("low", "med", "high")

@dataclass
class Task:
    name: str
    due: datetime
    priority: str
    category: str

class TaskStore:
    """In-memory task store. Replaceable later with a DB or API."""
    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def add_task(self, name: str, due_str: str, priority: str, category: str) -> bool:
        """Add a task if valid and not a duplicate (case-insensitive by name)."""
        cleaned_name = name.strip()
        if not cleaned_name:
            print("Invalid task name")
            return False

        due = self._parse_date(due_str)
        if due is None:
            print("Invalid due date format (MM-DD-YYYY expected)")
            return False

        if priority not in VALID_PRIORITIES:
            print("Invalid priority")
            return False

        if self._name_exists(cleaned_name):
            print("Duplicate task name")
            return False

        self._tasks.append(Task(cleaned_name, due, priority, category))
        self._tasks.sort(key=lambda t: t.due)
        return True

    def remove_task(self, name: str) -> bool:
        """Remove task by name (case-insensitive). Returns True if removed."""
        idx = next((i for i, t in enumerate(self._tasks)
                    if t.name.lower() == name.lower()), -1)
        if idx == -1:
            print("Task not found")
            return False
        del self._tasks[idx]
        return True

    def get_overdue(self, now: datetime | None = None) -> List[Task]:
        """Return tasks due before 'now'."""
        now = now or datetime.now()
        return [t for t in self._tasks if t.due < now]

    def get_today(self, today: date | None = None) -> List[Task]:
        """Return tasks due today, ordered by priority (high → med → low)."""
        today = today or datetime.now().date()
        todays = [t for t in self._tasks if t.due.date() == today]
        priority_order = {"high": 0, "med": 1, "low": 2}
        return sorted(todays, key=lambda t: priority_order[t.priority])

    def filter_by_category(self, category: str) -> List[Task]:
        return [t for t in self._tasks if t.category == category]

    def all_tasks(self) -> List[Task]:
        return list(self._tasks)

    # ---------- internal helpers ----------

    def _name_exists(self, cleaned_name: str) -> bool:
        return any(t.name.lower() == cleaned_name.lower() for t in self._tasks)

    @staticmethod
    def _parse_date(due_str: str) -> datetime | None:
        try:
            return datetime.strptime(due_str, DATE_FMT)
        except ValueError:
            return None

# Demo 
if __name__ == "__main__":
    store = TaskStore()
    store.add_task("  Essay  ", "08-01-2025", "high", "School")
    store.add_task("groceries","08-09-2025","low","Life")
    store.add_task("groceries","08-09-2025","low","Life")  # Duplicate
    print([t.name for t in store.get_overdue()])
    print([t.name for t in store.get_today()])
    print([t.name for t in store.filter_by_category("Life")])
    store.remove_task("Essay")