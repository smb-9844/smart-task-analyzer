from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json
from .scoring import TaskScorer

# --- FRONTEND ---
def home(request):
    """
    Serves the frontend template (index.html)
    """
    return render(request, "tasks/index.html")


# --- HELPER FUNCTION ---
def parse_task(task):
    """
    Validates and parses a task dictionary.
    Returns None if invalid.
    """
    title = task.get("title")
    due_date_str = task.get("due_date")
    if not title or not due_date_str:
        return None
    try:
        due_date = date.fromisoformat(due_date_str)
    except ValueError:
        return None
    return {
        "title": title,
        "due_date": due_date,
        "estimated_hours": task.get("estimated_hours", 1),
        "importance": task.get("importance", 5),
        "dependencies": task.get("dependencies", [])
    }


# --- ANALYZE TASKS ---
@csrf_exempt
def analyze(request):
    """
    Accepts a POST request with tasks JSON and optional strategy.
    Returns tasks with calculated scores, sorted by score descending.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        body = json.loads(request.body)
        tasks_data = body.get("tasks", [])  # List of tasks
        strategy = body.get("strategy", "default")

        scorer = TaskScorer()
        results = []

        for task in tasks_data:
            parsed_task = parse_task(task)
            if not parsed_task:
                continue

            parsed_task["score"] = round(scorer.calculate(parsed_task, strategy), 2)
            parsed_task["reason"] = f"Priority score: {parsed_task['score']}"
            results.append(parsed_task)

        # Sort tasks by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        # Convert due_date back to string for JSON
        for t in results:
            t["due_date"] = t["due_date"].isoformat()

        return JsonResponse(results, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# --- SUGGEST TOP 3 TASKS ---
@csrf_exempt
def suggest(request):
    """
    Accepts a POST request with tasks JSON.
    Returns top 3 tasks to work on today with explanation.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        tasks_data = json.loads(request.body)
        scorer = TaskScorer()
        results = []

        for task in tasks_data:
            parsed_task = parse_task(task)
            if not parsed_task:
                continue

            parsed_task["score"] = scorer.calculate(parsed_task)
            results.append(parsed_task)

        # Top 3 tasks
        suggestions = sorted(results, key=lambda t: t["score"], reverse=True)[:3]

        for s in suggestions:
            s["reason"] = f"Selected due to time sensitivity and importance. Score: {round(s['score'], 2)}"
            s["due_date"] = s["due_date"].isoformat()  # convert date for JSON

        return JsonResponse(suggestions, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
