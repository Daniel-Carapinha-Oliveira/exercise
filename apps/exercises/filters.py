import django_filters
from .models import Exercise, BodyPart, Muscle, MusclePart


class ExerciseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    workout_type = django_filters.ChoiceFilter(
        choices=Exercise.WorkoutType.choices,
        empty_label="-----------"
    )

    body_part = django_filters.ModelChoiceFilter(
        queryset=BodyPart.objects.all(),
        field_name='muscle_part__muscle__body_part',
        to_field_name='id',
        label='Body Part',
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
        fields = ['name', 'description', 'workout_type', 'body_part', 'muscle', 'muscle_part']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically populate muscles if body_part is selected
        body_part = self.data.get('body_part')
        if body_part:
            self.filters['muscle'].queryset = Muscle.objects.filter(body_part_id=body_part)

        # Dynamically populate muscle parts if muscle is selected
        muscle = self.data.get('muscle')
        if muscle:
            self.filters['muscle_part'].queryset = MusclePart.objects.filter(muscle_id=muscle)
