from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('muscle_groups', views.muscle_groups, name='muscle_groups'),
    path('exercises', views.Exercises.as_view(), name='exercises'),
    path('api/muscles/', views.get_muscles, name='api_muscles'),
    path('api/muscle-parts/', views.get_muscle_parts, name='api_muscle_parts'),
    path('api/exercises/', views.ExerciseAPIView.as_view(), name='api_exercises'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
