import django_filters
from .models import Exercise, BodyPart, Muscle


class ExerciseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    workout_type = django_filters.ChoiceFilter(choices=Exercise.WorkoutType.choices)
    muscle = django_filters.ModelChoiceFilter(
        queryset=Muscle.objects.all(),
        field_name='muscle_part__muscle',
        to_field_name='id',
        label='Muscle'
    )
    body_part = django_filters.ModelChoiceFilter(
        queryset=BodyPart.objects.all(),
        field_name='muscle_part__muscle__body_part',
        to_field_name='id',
        label='Body Part'
    )

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'workout_type']