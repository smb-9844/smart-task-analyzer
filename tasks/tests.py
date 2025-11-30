from django.test import TestCase
from datetime import date, timedelta
from .scoring import TaskScorer

class TaskScorerTest(TestCase):

    def setUp(self):
        self.scorer = TaskScorer()

    def test_overdue_task(self):
        task = {"title": "Overdue", "due_date": date.today() - timedelta(days=1),
                "importance": 5, "estimated_hours": 2, "dependencies": []}
        score = self.scorer.calculate(task)
        self.assertTrue(score > 50)  # Overdue tasks get higher score

    def test_quick_win(self):
        task = {"title": "Quick Task", "due_date": date.today() + timedelta(days=10),
                "importance": 5, "estimated_hours": 1, "dependencies": []}
        score = self.scorer.calculate(task)
        self.assertTrue(score >= 0)

    def test_high_importance(self):
        task = {"title": "Important Task", "due_date": date.today() + timedelta(days=5),
                "importance": 10, "estimated_hours": 3, "dependencies": []}
        score = self.scorer.calculate(task)
        self.assertTrue(score >= 70)
