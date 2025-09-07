from django.urls import path
from .views import exercises

urlpatterns = [
    path('exercises', exercises, name='exercises'),
]
