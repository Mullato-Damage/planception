"""
services.py
Application/business logic layer for Planception.

This layer coordinates higher-level operations on tasks without
knowing *how* data is persisted (that's the repository's job).
Keeping this thin and focused improves testability and separation of concerns.
"""

from typing import List
from models import Task
from repo import TaskRepository

class TaskService:
    """Service layer for task management operations."""
    
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo
    """Initialize with a repository instance."""
    
    def create_task(self, name: str, due_str: str, priority: str, category: str) -> bool:
        return self.repo.add(name, due_str, priority, category)
    """Create a new task with the given parameters."""
    
    def remove_task(self, name: str) -> bool:
        return self.repo.delete(name)
    """Remove a task by name."""
    
    def list_tasks(self) -> List[Task]:
        return self.repo.all_sorted()
    """List all tasks sorted by due date."""
    
    def list_overdue(self) -> List[Task]:
        return self.repo.overdue()
    """List all overdue tasks."""
    
    def list_today(self) -> List[Task]:
        return self.repo.due_today()
    """List all tasks due today."""