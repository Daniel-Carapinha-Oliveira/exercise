from rest_framework import serializers
from .models import Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    muscle_part = serializers.StringRelatedField()

    class Meta:
        model = Exercise
        fields = '__all__'