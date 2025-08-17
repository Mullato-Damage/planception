from typing import List
from models import Task
from repo import TaskRepository

class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def create_task(self, name: str, due_str: str, priority: str, category: str) -> bool:
        return self.repo.add(name, due_str, priority, category)

    def remove_task(self, name: str) -> bool:
        return self.repo.delete(name)

    def list_tasks(self) -> List[Task]:
        return self.repo.all_sorted()

    def list_overdue(self) -> List[Task]:
        return self.repo.overdue()

    def list_today(self) -> List[Task]:
        return self.repo.due_today()
