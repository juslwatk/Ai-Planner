import json
from personal_assistant.task import Task
from datetime import datetime, timedelta
import logging



class TaskList:
    
    def __init__(self):
        self.list = []
    
    def add_task(self, task: Task) -> None:
        self.list.append(task) 
        logging.info(
            "Added task: '%s' | priority=%s | due_date=%s",
            task.name, task.priority, task.due_date
    )
    
    def __str__(self):
            return "\n".join(str(task) for task in self.list)
        
    def review_tasks(self):
        for task in self.list:
            task.change_task_status()
            
    def filter_tasks(
        self,
        category: str = None,
        priority: str = None,
        status: str = None,
        max_duration: float = None
    ) -> list:
        filtered = self.list
        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
        if priority:
            filtered = [t for t in filtered if t.priority.lower() == priority.lower()]
        if status:
            filtered = [t for t in filtered if t.status.lower() == status.lower()]
        if max_duration is not None:
            filtered = [t for t in filtered if t.duration <= max_duration]
        return filtered
    
    def filter_by(self, **criteria):
        results = self.list
        for key, value in criteria.items():
            results = [task for task in results if getattr(task, key, None) == value]
        return results



    
    def save_to_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            json.dump([task.to_dict() for task in self.list], f, indent=2)
    @classmethod        
    def load_from_file(cls, filename: str) -> "TaskList":
        new_list = cls()
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for task_data in data:
                    task = Task.from_dict(task_data)
                    new_list.list.append(task)
        except FileNotFoundError:
            print(f"File {filename} could not be found. Try again.")
        return new_list



