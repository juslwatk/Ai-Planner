import json

class Task:
    def __init__(self, name: str, duration: float, status: str = "pending"):
        self.name = name
        self.duration = duration
        self.status = status
        
    def __str__(self):
        return f"{self.name} for {self.duration} - {self.status}"
        
    @classmethod
    def from_user_input(cls) -> "Task":
        name = input("What is the task? ")
        duration = float(input("What is the duration of this task "))
        return cls(name,duration)
    
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
            "duration": self.duration,
            "status": self.status
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls (
            name = data["name"],
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
                    new_list.append(task)
        except FileNotFoundError:
            print(f"File {filename} could not be found. Try again.")
        return new_list
            
    
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
    
    task_list.save_to_file("tasks.json")
    print("\n📁 Your tasks have been saved to 'tasks.json'.")
