from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('muscle_groups', views.muscle_groups_page, name='muscle_groups_page'),
    path('get_muscles_queryset/', views.get_muscles_queryset, name='get_muscles_queryset'),
    path('get_muscle_parts_queryset/', views.get_muscle_parts_queryset, name='get_muscle_parts_queryset'),
    path('exercises', views.Exercises.as_view(), name='exercises'),
    path('api/exercises/', views.ExerciseAPIView.as_view(), name='api_exercises'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
