from rest_framework import serializers
from .models import Exercise, MusclePart


class ExerciseSerializer(serializers.ModelSerializer):
    workout_type = serializers.ChoiceField(
        choices=Exercise.WorkoutType.choices,
        error_messages={
            'invalid_choice': f'Choose one of the following choices: {[choice.value for choice in Exercise.WorkoutType]}'
        }
    )

    muscle_part = serializers.CharField(
        max_length=100,
        required=True,
    )

    class Meta:
        model = Exercise
        fields = '__all__'

    def validate_muscle_part(self, value):
        names = list(MusclePart.objects.values_list('name', flat=True))
        if value not in names:
            raise serializers.ValidationError(
                f'Choose one of following choices: {names}'
            )
        return value
