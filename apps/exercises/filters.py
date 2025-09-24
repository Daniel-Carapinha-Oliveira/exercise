import django_filters
from .models import Exercise


class ExerciseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    workout_type = django_filters.ChoiceFilter(choices=Exercise.WorkoutType.choices)
    muscle_part = django_filters.CharFilter(field_name='muscle_part__name', lookup_expr='icontains')

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'workout_type', 'muscle_part']