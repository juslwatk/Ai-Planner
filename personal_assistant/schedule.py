from personal_assistant.task import Task
from datetime import datetime, timedelta
from personal_assistant.scoring_engine import ScoringEngine
import logging

# 1) Logging setup
logging.basicConfig(
    filename="assistant_usage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Schedule:
    # …

    def build(self):
        current = self.start
        time_since_break = timedelta(0)

        scorer = ScoringEngine()
        task_scores = [(scorer.score(task), task) for task in self.tasks]
        task_scores.sort(reverse=True, key=lambda x: x[0])
        self.tasks = [t for _, t in task_scores]

        for task in self.tasks:
            duration = timedelta(hours=task.duration)

            if time_since_break >= timedelta(hours=2):
                break_duration = timedelta(minutes=15)
                break_end = current + break_duration
                self.slots.append((current, break_end, Task("Break", 0.25, "break", "scheduled")))

                # 2) Log the break
                logging.info(
                    "Scheduled break from %s to %s",
                    current.strftime("%H:%M"),
                    break_end.strftime("%H:%M")
                )

                current = break_end
                time_since_break = timedelta(0)

            end_time = current + duration

            if end_time <= self.end:
                self.slots.append((current, end_time, task))

                # 3) Log the task
                logging.info(
                    "Scheduled task '%s' from %s to %s",
                    task.name,
                    current.strftime("%H:%M"),
                    end_time.strftime("%H:%M")
                )

                current += duration
                time_since_break += duration
            else:
                # 4) Log the overflow
                logging.warning("Not enough time to fit task '%s'", task.name)
                print(f"Not enough time to fit {task.name}")

    def export(self, filename: str = "schedule.txt") -> None:
        with open(filename, "w") as f:
            # … write lines …
            # 5) Log the export
            logging.info("Schedule exported to '%s'", filename)
            print(f"\n Schedule exported to '{filename}'")
