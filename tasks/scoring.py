from datetime import date

class TaskScorer:
    def __init__(self):
        self.weights = {
            "urgency": 0.45,
            "importance": 0.35,
            "effort": 0.10,
            "dependency": 0.10
        }

    def urgency_score(self, due_date):
        days = (due_date - date.today()).days
        if days < 0:
            return 100
        elif days <= 2:
            return 90
        elif days <= 7:
            return 60
        else:
            return 20

    def effort_score(self, hours):
        if hours <= 1:
            return 90
        elif hours <= 3:
            return 60
        else:
            return 20

    def dependency_score(self, deps):
        if not deps:
            return 80
        return max(20, 80 - len(deps)*15)

    def calculate(self, task, strategy="default"):
        u = self.urgency_score(task.get("due_date", date.today()))
        i = task.get("importance", 5) * 10
        e = self.effort_score(task.get("estimated_hours", 1))
        d = self.dependency_score(task.get("dependencies", []))

        if strategy == "fastest":
            return 0.1*u + 0.1*i + 0.7*e + 0.1*d
        elif strategy == "important":
            return 0.2*u + 0.7*i + 0.05*e + 0.05*d
        elif strategy == "deadline":
            return 0.7*u + 0.1*i + 0.1*e + 0.1*d
        else:  # default Smart Balance
            return 0.45*u + 0.35*i + 0.1*e + 0.1*d
