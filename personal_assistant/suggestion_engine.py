from datetime import datetime

class SuggestionEngine:
    def __init__(self, task_list):
        self.task_list = task_list

    def suggest(self) -> list[str]:
        suggestions = []

        for task in self.task_list.list:
            # Suggest a priority based on keywords
            suggestions.extend(self.suggest_priority(task))

            # Suggest breaking down long tasks
            if task.duration > 2 and not task.subtasks:
                suggestions.append(
                    f"Consider breaking '{task.name}' into subtasks — it's over 2h long."
                )

            # Flag overdue tasks
            if task.due_date:
                try:
                    due = datetime.strptime(task.due_date, "%Y-%m-%d")
                    if due < datetime.now() and task.status != "done":
                        suggestions.append(
                            f"Task '{task.name}' is overdue and still marked '{task.status}'."
                        )
                except ValueError:
                    suggestions.append(
                        f"Invalid due date format in '{task.name}'."
                    )

        return suggestions

    def suggest_priority(self, task) -> list[str]:
        keywords = {
            "urgent": "high",
            "important": "high",
            "email": "medium",
            "clean": "low",
        }

        found = []
        for word, level in keywords.items():
            if word in task.name.lower() and (task.priority is None or task.priority != level):
                found.append(
                    f"Suggest setting priority of '{task.name}' to '{level}'."
                )
        return found
