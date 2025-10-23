import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField, SlugRelatedField

from apps.exercises.serializers import ExerciseSerializer
from apps.exercises.models import (
    MusclePart,
    Exercise
)

pytestmark = pytest.mark.django_db


class TestExerciseSerializer:
    def test_fields_setup(self, muscle_part_factory):
        s = ExerciseSerializer()

        muscle_part_factory.create_batch(10)

        # test workout_type
        assert isinstance(s.fields['workout_type'], serializers.ChoiceField)
        workout_type_field_choices = [choice for choice in s.fields['workout_type'].choices]
        exercise_workout_type_fields = [choice[0] for choice in Exercise.WorkoutType.choices]
        assert workout_type_field_choices == exercise_workout_type_fields

        # test muscle_part
        muscle_part_field = s.fields['muscle_part']
        assert isinstance(muscle_part_field, ManyRelatedField)
        assert isinstance(muscle_part_field.child_relation, SlugRelatedField)
        assert list(muscle_part_field.child_relation.queryset) == list(MusclePart.objects.all())

        assert muscle_part_field.child_relation.slug_field == 'name'
        assert muscle_part_field.child_relation.queryset is not None

        # test created_by
        assert isinstance(s.fields['created_by'], serializers.StringRelatedField)
        assert s.fields['created_by'].read_only is True

    def test_workout_type_invalid_choice_error_message(self):
        s = ExerciseSerializer()
        workout_type_field = s.fields['workout_type']

        invalid_value = 'this-is-not-a-choice'
        with pytest.raises(serializers.ValidationError) as excinfo:
            workout_type_field.run_validation(invalid_value)

        expected = f"Choose one of the following choices: {[choice.value for choice in Exercise.WorkoutType]}"
        assert expected in str(excinfo.value)

    def test_inherits_filter_view(self):
        assert issubclass(ExerciseSerializer, serializers.ModelSerializer)

    def test_serializer_meta_model_and_fields(self):
        s = ExerciseSerializer()

        # Check the model
        assert s.Meta.model == Exercise

        # Check fields
        model_fields = [field.name for field in Exercise._meta.get_fields()]
        serializer_fields = list(s.fields.keys())

        # All model fields should be in the serializer
        for field in model_fields:
            assert field in serializer_fields

    def test_muscle_part_must_be_an_already_existing(self, muscle_part_factory):
        muscle_part1 = muscle_part_factory(name='muscle_part1')
        muscle_part2 = muscle_part_factory(name='muscle_part2')
        muscle_part3 = muscle_part_factory(name='muscle_part3')

        image = Image.new('RGB', (1, 1), color='white')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", buffer.read(), content_type="image/jpeg")

        # will work
        for muscle_part in [muscle_part1, muscle_part2, muscle_part3]:
            data = {
                "name": "test",
                "description": "test desc",
                "image": image_file,
                "workout_type": "gym",
                "muscle_part": [muscle_part.name],
            }
            s = ExerciseSerializer(data=data)
            assert s.is_valid()

        # will not work
        data = {
            "name": "test",
            "description": "test desc",
            "image": image_file,
            "workout_type": "gym",
            "muscle_part": ['will not work'],
        }
        s = ExerciseSerializer(data=data)
        assert not s.is_valid()
