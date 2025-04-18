import logging
from collections import Counter
from personal_assistant.sub_task import SubTask  # if you need subtasks displayed
from personal_assistant.task import Task
from personal_assistant.task_list import TaskList

class CommandInterpreter:
    def __init__(self, task_list: TaskList):
        self.task_list = task_list

    def run(self):
        print("\nEntering Natural Language Command Mode. Type 'help' to see available commands. Type 'exit' to leave.")
        while True:
            command = input("\n> ").strip()
            if command.lower() == "report":
                self.generate_report()
                continue

            logging.info("User command: %s", command)

            if command.lower() == "exit":
                break
            elif command.startswith("delete"):
                self.handle_delete(command)
            elif command.startswith("modify"):
                self.handle_modify(command)
            elif command.startswith("list"):
                self.handle_list()
            elif command.startswith("filter"):
                self.filter_tasks(command[len("filter"):].strip())
            elif command.lower() == "help":
                self.show_help()
            else:
                print("\u2753 Unknown command. Try typing 'help'")

    def handle_delete(self, command: str):
        parts = command.split()
        if len(parts) < 2:
            print("Please provide the task number to delete. Example: delete 2")
            return
        try:
            task_index = int(parts[1]) - 1
            if 0 <= task_index < len(self.task_list.list):
                removed = self.task_list.list.pop(task_index)
                logging.info("Deleted task: '%s'", removed.name)
                print(f"\u274C Removed task: {removed.name}")
            else:
                print("Task number out of range.")
        except ValueError:
            print("Invalid task number. Use: delete <number>")

    def handle_modify(self, command: str):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            index = int(parts[1]) - 1
            if 0 <= index < len(self.task_list.list):
                task = self.task_list.list[index]
                print(f"\nModifying task: {task}\n")
                print("Fields you can modify: name, duration, category, priority, due_date")

                field = input("Which field do you want to modify? ").strip().lower()
                old_value = getattr(task, field, None)
                if field == "name":
                    task.name = input("Enter new task name: ")
                elif field == "duration":
                    task.duration = float(input("Enter new duration (in hours): "))
                elif field == "category":
                    task.category = input("Enter new category: ")
                elif field == "priority":
                    task.priority = input("Enter new priority (high, medium, low): ").lower()
                elif field == "due_date":
                    task.due_date = input("Enter new due date (YYYY-MM-DD or blank): ") or None
                else:
                    print("Invalid field. No changes made.")
                    return

                logging.info(
                    "Modified task '%s': %s changed from '%s' to '%s'",
                    task.name, field, old_value, getattr(task, field)
                )
                print("\u2705 Task updated.")
            else:
                print("Invalid task number.")
        else:
            print("Usage: modify <task_number>")

    def handle_list(self):
        if not self.task_list.list:
            print("No tasks to display.")
        else:
            print("\n\U0001F4CB Current Tasks:")
            for i, task in enumerate(self.task_list.list, start=1):
                print(f"{i}. {task}")

    def filter_tasks(self, args: str):
        filters = {}
        for pair in args.split():
            if "=" in pair:
                key, value = pair.split("=", 1)
                filters[key.strip()] = value.strip()

        results = self.task_list.filter_by(**filters)

        if results:
            print("\n\U0001F3AF Filtered Tasks:")
            for task in results:
                print(task)
        else:
            print("No tasks matched the given filters.")

    def show_help(self):
        print("""
Available Commands:
• add            – Add a new task with optional subtasks
• delete <n>     – Delete a task by its number
• modify <n>     – Modify a task's field (name, duration, category, priority, due_date)
• list           – View all current tasks and subtasks
• filter         – Filter tasks (e.g., filter category=work priority=high)
• report         – Show a summary of your assistant usage
• help           – Show this help menu
• exit           – Exit command mode
""")

    def generate_report(self):
        counts = Counter()
        try:
            with open("assistant_usage.log") as f:
                for line in f:
                    if "Added task:" in line:
                        counts["Tasks added"] += 1
                    elif "Status changed for task" in line:
                        counts["Status changes"] += 1
                    elif "Deleted task:" in line:
                        counts["Tasks deleted"] += 1
                    elif "Scheduled task" in line:
                        counts["Tasks scheduled"] += 1
                    elif "Scheduled break" in line:
                        counts["Breaks scheduled"] += 1
                    elif "Schedule exported" in line:
                        counts["Exports"] += 1
                    elif "Modified task" in line:
                        counts["Modifications"] += 1
        except FileNotFoundError:
            print("No usage log found.")
            return

        print("\n🗒️ Usage Report:")
        for label, num in counts.items():
            print(f" • {label}: {num}")
        print()
