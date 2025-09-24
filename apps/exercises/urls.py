from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import body_parts, exercises, AllExercises

urlpatterns = [
    path('body_parts', body_parts, name='body_parts'),
    path('exercises/<int:body_part_id>/', exercises, name='exercises'),
    path('all_exercises', AllExercises.as_view(), name='all_exercises')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)