import django_filters
from .models import Exercise, BodyPart, Muscle, MusclePart


class ExerciseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    workout_type = django_filters.ChoiceFilter(
        choices=Exercise.WorkoutType.choices,
        empty_label="Not selected"
    )
    body_part = django_filters.ModelChoiceFilter(
        queryset=BodyPart.objects.all(),
        field_name='muscle_part__muscle__body_part',
        to_field_name='id',
        label='Body Part',
        empty_label="Not selected"
    )
    muscle = django_filters.ModelChoiceFilter(
        queryset=Muscle.objects.none(),
        field_name='muscle_part__muscle',
        to_field_name='id',
        label='Muscle',
        empty_label="Not selected"
    )
    muscle_part = django_filters.ModelChoiceFilter(
        queryset=MusclePart.objects.none(),
        field_name='muscle_part',
        to_field_name='id',
        label='Muscle Part',
        empty_label="Not selected"
    )

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'workout_type', 'body_part', 'muscle', 'muscle_part']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Narrow down muscles by body_part
        body_part = self.data.get('body_part')
        if body_part:
            try:
                body_part_id = int(body_part)
                qs = Muscle.objects.filter(body_part_id=body_part_id)
                self.filters['muscle'].queryset = qs
                self.form.fields['muscle'].queryset = qs
                self.form.fields['muscle'].empty_label = "None available" if not qs.exists() else "Not selected"
            except (ValueError, TypeError):
                pass
        else:
            self.filters['muscle'].queryset = Muscle.objects.none()
            self.form.fields['muscle'].queryset = Muscle.objects.none()
            self.form.fields['muscle'].empty_label = "Select a body part"

        # Narrow down muscle_parts by muscle
        muscle = self.data.get('muscle')
        if muscle:
            try:
                muscle_id = int(muscle)
                qs = MusclePart.objects.filter(muscle_id=muscle_id)
                self.filters['muscle_part'].queryset = qs
                self.form.fields['muscle_part'].queryset = qs
                self.form.fields['muscle_part'].empty_label = "None available" if not qs.exists() else "Not selected"
            except (ValueError, TypeError):
                pass
        else:
            self.filters['muscle_part'].queryset = MusclePart.objects.none()
            self.form.fields['muscle_part'].queryset = MusclePart.objects.none()
            self.form.fields['muscle_part'].empty_label = "Select a muscle"
