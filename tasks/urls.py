from django.urls import path
from .views import home, analyze, suggest

urlpatterns = [
    path("", home, name="home"),  # Serve the frontend
    path("analyze/", analyze, name="analyze"),
    path("suggest/", suggest, name="suggest"),
]
