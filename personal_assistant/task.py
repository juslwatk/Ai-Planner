from personal_assistant.sub_task import SubTask
from datetime import datetime
import logging

class Task:
    def __init__(
                self, name: str, duration: float, category: str = "general", 
                status: str = "pending", priority: str = None, subtasks = None,
                due_date: str = None
                 ):
        self.name = name
        self.duration = duration
        self.status = status
        self.category = category
        self.priority = priority
        self.subtasks = subtasks if subtasks is not None else []
        self.due_date = due_date
        
    def __str__(self):
            subtasks_str = "\n    - ".join(str(sub) for sub in self.subtasks) if self.subtasks else "None"
            date_str = f"Due: {self.due_date}" if self.due_date else "No due date"
            return (
                f"{self.name} ({self.category}, {self.priority}) for {self.duration}h - {self.status} | {date_str}\n"
                f"  Subtasks:\n    - {subtasks_str}"
            )

        
    @classmethod
    def from_user_input(cls) -> "Task":
        name = input("What is the task? ")
        priority = input("Task priority? ").lower()
        duration = float(input("What is the duration of this task? "))
        category = input("What category is this task? (e.g., work, personal, school)")
        
        # Validate date format
        due_date = None
        while True:
            date_input = input("Due date? (YYYY-MM-DD or leave blank): ").strip()
            if date_input == "":
                break
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                due_date = date_input
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")


        subtasks = []
        while True:
            add_sub = input("Add a subtask? (y/n): ").lower()
            if add_sub == 'y':
                sub = SubTask.from_user_input()
                subtasks.append(sub)
            elif add_sub == 'n':
                break

        return cls(name=name, priority=priority, duration=duration, category=category, subtasks=subtasks, due_date=due_date)


    
    def change_task_status(self) -> None:
        while True:
            result = input(f"Did you complete '{self.name}'? (done, missed, or reschedule) ")
            if result.lower() in ["done", "missed", "reschedule"]:
                self.status = result
                
                logging.info(
                    "Status changed for task '%s' → %s",
                    self.name, self.status
                )
                break

            print("Please type one of the following: done, missed, reschedule")

        for sub in self.subtasks:
            sub.change_status()

            
            
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "priority": self.priority,
            "category": self.category,
            "duration": self.duration,
            "status": self.status,
            "due_date": self.due_date,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks],
            
            
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        subtasks = [SubTask.from_dict(s) for s in data.get("subtasks", [])]
        return cls (
            name = data["name"],
            priority = data.get("priority", "medium"),
            category = data.get("category", "general"),
            duration = data["duration"],
            status = data.get("status", "pending"),
            due_date=data.get("due_date"),
            subtasks = subtasks
        )  
        