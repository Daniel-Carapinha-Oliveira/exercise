import factory

from .models import (
    MuscleGroup,
    Muscle,
    MusclePart,
    Exercise
)


class MuscleGroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')
    image = factory.django.ImageField(
        filename=factory.Sequence(lambda n: f'muscle_group_{n}.jpg')
    )
    description = factory.Sequence(lambda n: f'description{n}')

    class Meta:
        model = MuscleGroup


class MuscleFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')
    muscle_group = factory.SubFactory('apps.exercises.factories.MuscleGroupFactory')

    class Meta:
        model = Muscle


class MusclePartFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')
    muscle = factory.SubFactory('apps.exercises.factories.MuscleFactory')

    class Meta:
        model = MusclePart


class ExerciseFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'name{n}')
    description = factory.Sequence(lambda n: f'description{n}')
    image = factory.django.ImageField(
        filename=factory.Sequence(lambda n: f'exercise_{n}.jpg')
    )
    workout_type = factory.Iterator([Exercise.WorkoutType.CALISTHENIC, Exercise.WorkoutType.GYM])
    created_by = factory.SubFactory('apps.core.factories.UserFactory')

    class Meta:
        model = Exercise
        skip_postgeneration_save = True

    @factory.post_generation
    def muscle_part(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.muscle_part.add(*extracted)
