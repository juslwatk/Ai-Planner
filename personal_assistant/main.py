from personal_assistant.task import Task
from personal_assistant.task_list import TaskList
from personal_assistant.schedule import Schedule
from personal_assistant.utils import get_available_time_range
from personal_assistant.command_interpreter import CommandInterpreter
from personal_assistant.suggestion_engine import SuggestionEngine
from personal_assistant.scoring_engine import ScoringEngine
import logging

logging.basicConfig(
    filename="assistant_usage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        
            # Run suggestion engine
    sugg_engine = SuggestionEngine(task_list)
    suggestions = sugg_engine.suggest()

    if suggestions:
        print("\nSuggestions:")
        for s in suggestions:
            print(f" - {s}")
    else:
        print("\nNo suggestions. Tasks look good!")


    print("\nFinal Task List with Status:")
    print(task_list)

    start, end = get_available_time_range()
    # Natural Language Command Mode
    command_mode = input("\nDo you want to use natural language mode? (y/n): ").strip().lower()
    if command_mode == "y":
        interpreter = CommandInterpreter(task_list)
        interpreter.run()
    
    scorer = ScoringEngine(task_list)
    scorer.score_tasks()

    planner = Schedule(task_list.list, start, end)
    planner.build()
    planner.display()
    planner.export()

    task_list.save_to_file("tasks.json")
    print("\n📁 Your tasks have been saved to 'tasks.json'.")
