import pytest

from django.db import models
from django.db.utils import IntegrityError, DataError

from apps.exercises.models import (
    MuscleGroup,
    Muscle,
    MusclePart,
    Exercise
)

pytestmark = pytest.mark.django_db


class TestMuscleGroupModel:
    def test_name_max_length(self, muscle_group_factory):
        name = 'x' * 101
        with pytest.raises(DataError):
            muscle_group_factory(name=name)

    def test_name_unique_field(self, muscle_group_factory):
        name = 'test_name'
        muscle_group_factory(name=name)
        with pytest.raises(IntegrityError):
            muscle_group_factory(name=name)

    def test_model_inherits_correct_field_types(self):
        expected_fields = {
            'name': models.CharField,
            'image': models.ImageField,
            'description': models.TextField
        }

        for field_name, field_type in expected_fields.items():
            field = MuscleGroup._meta.get_field(field_name)
            # Assert that the field is an instance of the expected type
            assert isinstance(field, field_type), f"Field '{field_name}' should be a {field_type.__name__}"

    def test_str_method(self, muscle_group_factory):
        obj = muscle_group_factory(name='test_name')
        assert obj.__str__() == 'test_name'

    def test_ordering(self, muscle_group_factory):
        muscle_groups = muscle_group_factory.create_batch(5)
        expected_order = sorted(muscle_groups, key=lambda muscle_group: muscle_group.name)
        assert list(MuscleGroup.objects.all()) == expected_order


class TestMuscleModel:
    def test_name_max_length(self, muscle_factory):
        name = 'x' * 101
        with pytest.raises(DataError):
            muscle_factory(name=name)

    def test_name_unique_field(self, muscle_factory):
        name = 'test_name'
        muscle_factory(name=name)
        with pytest.raises(IntegrityError):
            muscle_factory(name=name)

    def test_fk_muscle_group_on_delete_protect(self, muscle_factory, muscle_group_factory):
        muscle_group = muscle_group_factory()
        muscle_factory(name='test_name', muscle_group=muscle_group)
        with pytest.raises(IntegrityError):
            muscle_group.delete()

    def test_model_inherits_correct_field_types(self):
        expected_fields = {
            'name': models.CharField,
            'muscle_group': models.ForeignKey
        }

        for field_name, field_type in expected_fields.items():
            field = Muscle._meta.get_field(field_name)
            # Assert that the field is an instance of the expected type
            assert isinstance(field, field_type), f"Field '{field_name}' should be a {field_type.__name__}"

    def test_foreign_keys_point_to_the_correct_model(self):
        muscle_group_field = Muscle._meta.get_field('muscle_group')

        assert muscle_group_field.remote_field.model == MuscleGroup, "'muscle_group' should point to MuscleGroup model"

    def test_str_method(self, muscle_factory):
        obj = muscle_factory(name='test_name')
        assert obj.__str__() == 'test_name'

    def test_ordering(self, muscle_factory):
        muscle_groups = muscle_factory.create_batch(5)
        expected_order = sorted(muscle_groups, key=lambda muscle_group: muscle_group.name)
        assert list(Muscle.objects.all()) == expected_order


class TestMusclePartModel:
    def test_name_max_length(self, muscle_part_factory):
        name = 'x' * 101
        with pytest.raises(DataError):
            muscle_part_factory(name=name)

    def test_name_unique_field(self, muscle_part_factory, muscle_factory):
        muscle = muscle_factory()
        name = 'test_name'
        muscle_part_factory(name=name, muscle=muscle)
        with pytest.raises(IntegrityError):
            muscle_part_factory(name=name, muscle=muscle)

    def test_fk_muscle_group_on_delete_protect(self, muscle_part_factory, muscle_factory):
        muscle = muscle_factory()
        muscle_part_factory(name='test_name', muscle=muscle)
        with pytest.raises(IntegrityError):
            muscle.delete()

    def test_model_inherits_correct_field_types(self):
        expected_fields = {
            'name': models.CharField,
            'muscle': models.ForeignKey
        }

        for field_name, field_type in expected_fields.items():
            field = MusclePart._meta.get_field(field_name)
            # Assert that the field is an instance of the expected type
            assert isinstance(field, field_type), f"Field '{field_name}' should be a {field_type.__name__}"

    def test_foreign_keys_point_to_the_correct_model(self):
        muscle_field = MusclePart._meta.get_field('muscle')

        assert muscle_field.remote_field.model == Muscle, "'muscle' should point to Muscle model"

    def test_str_method(self, muscle_part_factory):
        obj = muscle_part_factory(name='test_name')
        assert obj.__str__() == f'test_name'

    def test_ordering(self, muscle_part_factory):
        muscle_parts = muscle_part_factory.create_batch(5)
        expected_order = sorted(muscle_parts, key=lambda muscle_part: muscle_part.name)
        assert list(MusclePart.objects.all()) == expected_order


class TestExerciseModel:
    def test_name_max_length(self, exercise_factory):
        name = 'x' * 101
        with pytest.raises(DataError):
            exercise_factory(name=name)

    def test_name_unique_field(self, exercise_factory, user_factory):
        name = 'test_name'
        user = user_factory()

        # this must work, cause files are deleted
        exercise_factory(name=name, deleted_by=user)
        exercise_factory(name=name, deleted_by=user)
        exercise_factory(name=name, deleted_by=user)

        # this must work, first not deleted
        exercise_factory(name=name)

        # this must not work, second not deleted
        with pytest.raises(IntegrityError):
            exercise_factory(name=name)

    def test_workout_type_class_choices_exist_and_are_limited(self):
        choices = Exercise.WorkoutType.choices
        assert len(choices) == 2, f"Expected 2 choices, got {len(choices)}"
        expected = [
            ('calisthenics', 'Calisthenics'),
            ('gym', 'Gym'),
        ]
        assert choices == expected, f"Expected {expected}, got {choices}"

    def test_workout_type_choices(self):
        field = Exercise._meta.get_field('workout_type')
        field_values = [choice[0] for choice in field.choices]

        workout_type_choices = list(Exercise.WorkoutType.values)

        assert field_values == workout_type_choices

    def test_model_inherits_correct_field_types(self):
        expected_fields = {
            'name': models.CharField,
            'description': models.TextField,
            'image': models.ImageField,
            'workout_type': models.CharField,
            'muscle_part': models.ManyToManyField
        }

        for field_name, field_type in expected_fields.items():
            field = Exercise._meta.get_field(field_name)
            # Assert that the field is an instance of the expected type
            assert isinstance(field, field_type), f"Field '{field_name}' should be a {field_type.__name__}"

    def test_muscle_part_points_to_the_correct_model(self):
        muscle_field = Exercise._meta.get_field('muscle_part')

        assert muscle_field.remote_field.model == MusclePart, "'muscle_part' should point to MusclePart model"

    def test_str_method(self, exercise_factory):
        obj = exercise_factory(name='test_name')
        assert obj.__str__() == 'test_name'

    def test_ordering(self, exercise_factory):
        exercises = exercise_factory.create_batch(5)
        expected_order = sorted(exercises, key=lambda exercise: exercise.name)
        assert list(Exercise.objects.all()) == expected_order
