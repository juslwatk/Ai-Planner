import json
from datetime import datetime, timedelta

class Task:
    def __init__(self, name: str, duration: float, category: str = "general", status: str = "pending", priority: str = None):
        self.name = name
        self.duration = duration
        self.status = status
        self.category = category
        self.priority = priority
        
    def __str__(self):
        return f"{self.name} {self.category} {self.priority} for {self.duration} - {self.status}"
        
    @classmethod
    def from_user_input(cls) -> "Task":
        name = input("What is the task? ")
        priority = input("Task priority?").lower()
        duration = float(input("What is the duration of this task? "))
        category = input("What category is this task? (e.g., work, personal, school)")
        return cls(name=name,priority=priority, duration=duration, category=category)
    
    def change_task_status(self) -> None:
        while True:
            result = input(f"Did you complete '{self.name}'? (done, missed, or reschedule)")
            if result.lower() in ["done", "missed", "reschedule"]:
                self.status = result
                break
            print(f"Please type one of the following. (done, missed, reschedule)")
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "priority": self.priority,
            "category": self.category,
            "duration": self.duration,
            "status": self.status
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls (
            name = data["name"],
            priority = data.get("priority", "medium"),
            category = data.get("category", "general"),
            duration = data["duration"],
            status = data.get("status", "pending")
        )
        


class TaskList:
    
    def __init__(self):
        self.list = []
    
    def add_task(self, task: Task) -> None:
        self.list.append(task) 
    
    def __str__(self):
            return "\n".join(str(task) for task in self.list)
        
    def review_tasks(self):
        for task in self.list:
            task.change_task_status()
    
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
    
class Schedule:
    def __init__(self, tasks: list[Task], start: datetime, end: datetime):
        self.tasks = tasks
        self.start = start
        self.end = end
        self.slots = []
        
    def build(self):
        current = self.start
        time_since_break = timedelta(0)
        
        priority_order = {"high": 0, "medium": 1, "low": 2}
        self.tasks.sort(key=lambda task: priority_order.get(task.priority, 1))
        
        for task in self.tasks:
            duration = timedelta(hours=task.duration)
            
            if time_since_break >= timedelta(hours=2):
                break_duration = timedelta(minutes=15)
                break_end = current + break_duration
                
                self.slots.append((current, break_end, Task("Break", 0.25, "break", "scheduled")))
                current = break_end
                time_since_break = timedelta(0)
                
            end_time = current + duration
            
            if current + duration <= self.end:
                self.slots.append((current, current + duration, task))
                current += duration
                time_since_break += duration 
            else:
                print(f"Not enough time to fit {task.name}")
                
    def display(self): 
        print("\n Auto-Generated Schedule")
        print("-" * 40)
        for start, end, task in self.slots:
            print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} | {task.name} ({task.category})")
        

            
    def export(self, filename: str = "schedule.txt") -> None:
        with open(filename, "w") as f:
            f.write("Auto-Generated Schedule\n")
            f.write("-" * 40 + "\n")
            for start, end, task, in self.slots:
                line = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} | {task.name} ({task.category})\n"
                f.write(line)
            print(f"\n Schedule exported to '{filename}'")
            
    
        
def get_available_time_range() -> tuple[datetime, datetime]:
    print("\n📅 Let's set your available time for today.")
    
    start_str = input("Start time (e.g., 09:00): ")
    end_str = input("End time (e.g., 17:00): ")

    start = datetime.strptime(start_str, "%H:%M")
    end = datetime.strptime(end_str, "%H:%M")

    return start, end



if __name__ == "__main__":
    task_list = TaskList.load_from_file("tasks.json")

    while True:
        task = Task.from_user_input()
        task_list.add_task(task)
        print("Task added!\n")

        cont = input("Add another task? (y/n): ").lower()
        if cont != 'y':
            break

    task_list.review_tasks()

    print("\n✅ Final Task List with Status:")
    print(task_list)

    # 📅 Build and display the schedule
    start, end = get_available_time_range()
    planner = Schedule(task_list.list, start, end)
    planner.build()
    planner.display()
    planner.export()
    
    task_list.save_to_file("tasks.json")
    print("\n📁 Your tasks have been saved to 'tasks.json'.")
