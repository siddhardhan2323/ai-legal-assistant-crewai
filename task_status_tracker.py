# task_status_tracker.py

import time
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class TaskStatus(Enum):
    """Enum for task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskInfo:
    """Information about a task"""
    name: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error: Optional[str] = None


class TaskStatusTracker:
    """Tracks the status of tasks in the legal assistant workflow"""
    
    def __init__(self):
        self.tasks: Dict[str, TaskInfo] = {}
        self.current_task: Optional[str] = None
        self.callbacks: List[callable] = []
        self._initialize_tasks()
    
    def _initialize_tasks(self):
        """Initialize all tasks with their information"""
        task_definitions = [
            ("case_intake", "📋 Analyzing your legal issue and extracting key information"),
            ("ipc_section", "📚 Finding relevant Indian Penal Code sections"),
            ("legal_precedent", "⚖️ Searching for relevant legal precedents"),
            ("legal_drafter", "📝 Drafting formal legal document")
        ]
        
        for task_id, description in task_definitions:
            self.tasks[task_id] = TaskInfo(
                name=task_id,
                description=description
            )
    
    def add_status_callback(self, callback: callable):
        """Add a callback function to be called when status changes"""
        self.callbacks.append(callback)
    
    def start_task(self, task_id: str):
        """Mark a task as started"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.IN_PROGRESS
            self.tasks[task_id].start_time = datetime.now()
            self.current_task = task_id
            self._notify_callbacks()
    
    def complete_task(self, task_id: str):
        """Mark a task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].end_time = datetime.now()
            if self.current_task == task_id:
                self.current_task = None
            self._notify_callbacks()
    
    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].end_time = datetime.now()
            self.tasks[task_id].error = error
            if self.current_task == task_id:
                self.current_task = None
            self._notify_callbacks()
    
    def get_status_summary(self) -> Dict:
        """Get a summary of all task statuses"""
        summary = {
            "tasks": [],
            "current_task": self.current_task,
            "total_tasks": len(self.tasks),
            "completed_tasks": sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED),
            "failed_tasks": sum(1 for task in self.tasks.values() if task.status == TaskStatus.FAILED)
        }
        
        for task_id, task_info in self.tasks.items():
            task_data = {
                "id": task_id,
                "name": task_info.name,
                "description": task_info.description,
                "status": task_info.status.value,
                "start_time": task_info.start_time.isoformat() if task_info.start_time else None,
                "end_time": task_info.end_time.isoformat() if task_info.end_time else None,
                "error": task_info.error
            }
            summary["tasks"].append(task_data)
        
        return summary
    
    def get_progress_percentage(self) -> float:
        """Get the overall progress percentage"""
        if not self.tasks:
            return 0.0
        
        completed = sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED)
        in_progress = sum(1 for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS)
        
        # Give partial credit for in-progress tasks
        progress = completed + (in_progress * 0.5)
        return (progress / len(self.tasks)) * 100
    
    def get_status_text(self) -> str:
        """Get a human-readable status text"""
        if self.current_task:
            current_task_info = self.tasks[self.current_task]
            return f"🔄 {current_task_info.description}"
        
        completed = sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED)
        failed = sum(1 for task in self.tasks.values() if task.status == TaskStatus.FAILED)
        
        if failed > 0:
            return f"❌ {failed} task(s) failed"
        elif completed == len(self.tasks):
            return "✅ All tasks completed successfully"
        else:
            return f"⏳ {completed}/{len(self.tasks)} tasks completed"
    
    def _notify_callbacks(self):
        """Notify all registered callbacks about status changes"""
        for callback in self.callbacks:
            try:
                callback(self.get_status_summary())
            except Exception as e:
                print(f"Error in status callback: {e}")
    
    def reset(self):
        """Reset all tasks to pending status"""
        for task_info in self.tasks.values():
            task_info.status = TaskStatus.PENDING
            task_info.start_time = None
            task_info.end_time = None
            task_info.error = None
        self.current_task = None
        self._notify_callbacks()


# Global instance for the application
task_tracker = TaskStatusTracker()