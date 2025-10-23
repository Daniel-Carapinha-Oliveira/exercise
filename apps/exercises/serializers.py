from rest_framework import serializers

from .models import Exercise, MusclePart


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializes and deserializes Exercise model instances for API input and output.
    Handles validation and representation of exercise-related data.

    Receives Exercise model data and ensures proper validation, particularly for
    the muscle_part field, which must reference valid (existing) MusclePart (model) names.

    Returns validated and serialized Exercise data.
    """
    workout_type = serializers.ChoiceField(
        choices=Exercise.WorkoutType.choices,
        error_messages={
            'invalid_choice': f'Choose one of the following choices: {[choice.value for choice in Exercise.WorkoutType]}'
        }
    )

    muscle_part = serializers.SlugRelatedField(
        many=True,
        queryset=MusclePart.objects.all(),
        slug_field='name'
    )

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Exercise
        fields = '__all__'

    def validate_muscle_part(self, value):
        model_names = list(MusclePart.objects.values_list('name', flat=True))
        value_names = [object.name for object in value]

        # Check if any value in value_names is not in model_names
        invalid_names = [name for name in value_names if name not in model_names]

        if invalid_names:
            raise serializers.ValidationError(
                f'Must be a list of strings containing only the following: {list(model_names)}'
            )
        return value
