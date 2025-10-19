from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('body_parts', views.body_parts, name='body_parts'),
    path('exercises', views.Exercises.as_view(), name='exercises'),
    path('muscles', views.muscles, name='muscles'),
    path('api/muscles/', views.get_muscles, name='api_muscles'),
    path('api/muscle-parts/', views.get_muscle_parts, name='api_muscle_parts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
