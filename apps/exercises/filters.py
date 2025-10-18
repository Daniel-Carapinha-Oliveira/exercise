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

        # --- Helper function to reduce repetition ---
        def set_dependent_queryset(parent_field, child_field, model, fk_field, empty_default):
            parent_id = self.data.get(parent_field)
            if parent_id and str(parent_id).isdigit():
                qs = model.objects.filter(**{fk_field: parent_id})
                self.filters[child_field].queryset = qs

                if not qs.exists():
                    self.filters[child_field].extra['empty_label'] = "None available"
                else:
                    self.filters[child_field].extra['empty_label'] = "Not selected"
            else:
                self.filters[child_field].queryset = model.objects.none()
                self.filters[child_field].extra['empty_label'] = empty_default


        set_dependent_queryset(
            parent_field='body_part',
            child_field='muscle',
            model=Muscle,
            fk_field='body_part_id',
            empty_default="Select a body part first"
        )

        set_dependent_queryset(
            parent_field='muscle',
            child_field='muscle_part',
            model=MusclePart,
            fk_field='muscle_id',
            empty_default="Select a muscle first"
        )
