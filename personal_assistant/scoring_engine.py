from datetime import datetime, timedelta

class ScoringEngine:
    def __init__(self, task_list):
        self.task_list = task_list

    def score_tasks(self):
        for task in self.task_list.list:
            task.score = self.calculate_score(task)

    def calculate_score(self, task):
        score = 0

        # 1. Priority weight
        if task.priority == "high":
            score += 30
        elif task.priority == "medium":
            score += 20
        elif task.priority == "low":
            score += 10

        # 2. Due date proximity
        if task.due_date:
            try:
                due = datetime.strptime(task.due_date, "%Y-%m-%d")
                days_left = (due - datetime.now()).days
                if days_left <= 1:
                    score += 30
                elif days_left <= 3:
                    score += 20
                elif days_left <= 7:
                    score += 10
            except:
                pass  # If date is invalid, ignore

        # 3. Duration (less is better to complete quickly)
        if task.duration <= 1:
            score += 15
        elif task.duration <= 2:
            score += 10
        elif task.duration <= 4:
            score += 5

        return score