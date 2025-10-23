import django_filters

from .models import Exercise, MuscleGroup, Muscle, MusclePart


class ExerciseFilter(django_filters.FilterSet):
    """
    Provides filtering options for the Exercise model, allowing users to filter
    exercises based on various attributes such as name, description, workout type,
    muscle group, muscle, and muscle part.

    Receives the filter data (typically from a GET request). Dynamically adjusts
    the available choices for muscles and muscle parts based on the selected
    muscle group and muscle.

    Returns a filtered queryset of Exercise objects matching the applied filters.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    workout_type = django_filters.ChoiceFilter(
        choices=Exercise.WorkoutType.choices,
        empty_label="-----------"
    )

    muscle_group = django_filters.ModelChoiceFilter(
        queryset=MuscleGroup.objects.all(),
        field_name='muscle_part__muscle__muscle_group',
        to_field_name='id',
        label='Muscle Group',
        empty_label="-----------"
    )

    muscle = django_filters.ModelChoiceFilter(
        queryset=Muscle.objects.none(),
        field_name='muscle_part__muscle',
        to_field_name='id',
        label='Muscle',
        empty_label="-----------"
    )

    muscle_part = django_filters.ModelChoiceFilter(
        queryset=MusclePart.objects.none(),
        field_name='muscle_part',
        to_field_name='id',
        label='Muscle Part',
        empty_label="-----------"
    )

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'workout_type', 'muscle_group', 'muscle', 'muscle_part']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically populate muscles if muscle_group is selected
        muscle_group = self.data.get('muscle_group')
        if muscle_group:
            self.filters['muscle'].queryset = Muscle.objects.filter(muscle_group_id=muscle_group)

        # Dynamically populate muscle parts if muscle is selected
        muscle = self.data.get('muscle')
        if muscle:
            self.filters['muscle_part'].queryset = MusclePart.objects.filter(muscle_id=muscle)
