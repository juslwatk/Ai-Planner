class SubTask:
    def __init__(self, name: str, status: str = "pending"):
        self.name = name
        self.status = status

    def __str__(self):
        return f"{self.name} - {self.status}"

    @classmethod
    def from_user_input(cls) -> "SubTask":
        name = input("  → Subtask name: ")
        return cls(name)

    def change_status(self) -> None:
        while True:
            result = input(f"    Did you complete subtask '{self.name}'? (done, missed, or reschedule): ").lower()
            if result in ["done", "missed", "reschedule"]:
                self.status = result
                break
            print("    Please type one of the following: done, missed, reschedule")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SubTask":
        return cls(
            name=data["name"],
            status=data.get("status", "pending")
        )
