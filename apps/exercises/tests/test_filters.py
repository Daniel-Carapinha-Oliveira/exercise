import django_filters
import pytest

from apps.exercises.filters import ExerciseFilter
from apps.exercises.models import (
    MuscleGroup,
    Exercise
)

pytestmark = pytest.mark.django_db


class TestExerciseFilter:
    def test_filter_has_expected_fields(self):
        expected_fields = [
            'name',
            'description',
            'workout_type',
            'muscle_group',
            'muscle',
            'muscle_part',
        ]

        f = ExerciseFilter()
        actual_fields = list(f.filters.keys())

        # Assert the same field names
        assert set(actual_fields) == set(expected_fields), (
            f"Expected fields {expected_fields}, but got {actual_fields}"
        )

    def test_initial_query_sets(self, muscle_group_factory, muscle_factory, muscle_part_factory):
        muscle_group_factory.create_batch(10)
        muscle_factory.create_batch(10)
        muscle_part_factory.create_batch(10)

        f = ExerciseFilter()
        assert list(f.filters['muscle'].queryset) == []
        assert list(f.filters['muscle_part'].queryset) == []
        assert list(f.filters['muscle_group'].queryset) == list(MuscleGroup.objects.all())

    def test_inherits_filter_view(self):
        assert issubclass(ExerciseFilter, django_filters.FilterSet)

    def test_name_and_description_have_icontains_lookup(self):
        f = ExerciseFilter()

        name_filter = f.filters.get('name')
        description_filter = f.filters.get('description')

        assert name_filter.lookup_expr == 'icontains', (
            f"Expected 'icontains' lookup for 'name', got '{name_filter.lookup_expr}'"
        )

        assert description_filter.lookup_expr == 'icontains', (
            f"Expected 'icontains' lookup for 'description', got '{description_filter.lookup_expr}'"
        )

    def test_attributes_have_correct_field_types(self):
        expected_fields = {
            'name': django_filters.CharFilter,
            'description': django_filters.CharFilter,
            'workout_type': django_filters.ChoiceFilter,
            'muscle_group': django_filters.ModelChoiceFilter,
            'muscle': django_filters.ModelChoiceFilter,
            'muscle_part': django_filters.ModelChoiceFilter,
        }

        exercise_filter = ExerciseFilter()

        for field_name, field_type in expected_fields.items():
            field = exercise_filter.filters.get(field_name)
            # Assert that the field is an instance of the expected type
            assert isinstance(field, field_type), f"Field '{field_name}' should be a {field_type.__name__}"

    def test_workout_type_filter_has_correct_choices(self):
        exercise_filter = ExerciseFilter()
        workout_filter = exercise_filter.filters.get('workout_type')

        # Check that choices match Exercise.WorkoutType.choices
        expected_choices = list(Exercise.WorkoutType.choices)
        actual_choices = list(workout_filter.extra.get('choices', []))

        assert actual_choices == expected_choices, (
            f"workout_type choices should match Exercise.WorkoutType.choices. "
            f"Expected {expected_choices}, got {actual_choices}"
        )

    def test_dynamic_muscle_queryset(self, muscle_group_factory, muscle_factory):
        group1 = muscle_group_factory()
        muscle1 = muscle_factory(muscle_group=group1)
        muscle2 = muscle_factory(muscle_group=group1)
        muscle3 = muscle_factory(muscle_group=group1)

        f = ExerciseFilter(data={'muscle_group': str(group1.id)})
        muscles = f.filters['muscle'].queryset
        assert list(muscles) == [muscle1, muscle2, muscle3]

    def test_dynamic_muscle_part_queryset(self, muscle_group_factory, muscle_factory, muscle_part_factory):
        group1 = muscle_group_factory()
        muscle1 = muscle_factory(muscle_group=group1)

        muscle_part1 = muscle_part_factory(muscle=muscle1)
        muscle_part2 = muscle_part_factory(muscle=muscle1)
        muscle_part3 = muscle_part_factory(muscle=muscle1)

        f = ExerciseFilter(data={'muscle_group': str(group1.id), "muscle": str(muscle1.id)})
        muscle_parts = f.filters['muscle_part'].queryset
        assert list(muscle_parts) == [muscle_part1, muscle_part2, muscle_part3]
