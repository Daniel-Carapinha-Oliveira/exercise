from django.contrib import admin
from .models import Muscle, BodyPart

class MuscleAdmin(admin.ModelAdmin):
    list_display = ['name', 'body_part']
    list_filter = ['body_part']
    search_fields = ['name']
    ordering = ['name']


class BodyPartAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

admin.site.register(Muscle, MuscleAdmin)
admin.site.register(BodyPart, BodyPartAdmin)
