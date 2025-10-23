from pytest_factoryboy import register

from apps.core.factories import UserFactory
from apps.exercises.factories import (
    MuscleGroupFactory,
    MuscleFactory,
    MusclePartFactory,
    ExerciseFactory
)

register(MuscleGroupFactory)
register(MuscleFactory)
register(MusclePartFactory)
register(ExerciseFactory)
register(UserFactory)
