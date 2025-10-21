from django.contrib import admin
from .models import Muscle, MuscleGroup, MusclePart, Exercise


class MuscleAdmin(admin.ModelAdmin):
    list_display = ['name', 'muscle_group']
    list_filter = ['muscle_group']
    search_fields = ['name']
    ordering = ['name']


class BodyPartAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


class MusclePartAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['muscle']
    search_fields = ['name']
    ordering = ['name']


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['muscle_part']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(Muscle, MuscleAdmin)
admin.site.register(MuscleGroup, BodyPartAdmin)
admin.site.register(MusclePart, MusclePartAdmin)
admin.site.register(Exercise, ExerciseAdmin)
