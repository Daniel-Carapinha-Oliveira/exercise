from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import exercises, individual_exercises

urlpatterns = [
    path('exercises', exercises, name='exercises'),
    path('individual_exercises/<int:body_part_id>/', individual_exercises, name='individual_exercises')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)