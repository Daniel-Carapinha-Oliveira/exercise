from django.db import models
from django.db.models import Q

from apps.core.mixins import MetaDataMixin


class MuscleGroup(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    image = models.ImageField(
        verbose_name='image',
        upload_to='img/muscle_groups/'
    )

    description = models.TextField(
        verbose_name='description',
    )

    class Meta:
        db_table = 'muscle_group'
        ordering = ['name']
        verbose_name = 'muscle group'
        verbose_name_plural = 'muscle groups'

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    # ForeignKeys
    muscle_group = models.ForeignKey(
        'exercises.MuscleGroup',
        on_delete=models.PROTECT,
        related_name='muscles',
        verbose_name='muscle group',
    )

    class Meta:
        db_table = 'muscle'
        ordering = ['name']
        verbose_name = 'muscle'
        verbose_name_plural = 'muscles'

    def __str__(self):
        return self.name


class MusclePart(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    # ForeignKeys
    muscle = models.ForeignKey(
        'exercises.Muscle',
        on_delete=models.PROTECT,
        related_name='muscle_parts',
        verbose_name='muscle',
    )

    class Meta:
        db_table = 'muscle_part'
        ordering = ['name']
        verbose_name = 'muscle part'
        verbose_name_plural = 'muscle parts'
        constraints = [
            models.UniqueConstraint(fields=['muscle', 'name'], name='unique_together_muscle_name')
        ]

    def save(self, *args, **kwargs):
        # Prefix the name with the related muscle's name
        self.name = f'{self.muscle.name} - {self.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Exercise(MetaDataMixin, models.Model):
    class WorkoutType(models.TextChoices):
        CALISTHENIC = 'calisthenics', 'Calisthenics'
        GYM = 'gym', 'Gym'

    name = models.CharField(
        verbose_name='name',
        max_length=100
    )

    description = models.TextField(
        verbose_name='description',
    )

    image = models.ImageField(
        verbose_name='image',
        upload_to='img/exercises/'
    )

    workout_type = models.CharField(
        max_length=20,
        choices=WorkoutType,
        verbose_name='workout type',
    )

    # Many-to-many: An exercise can train multiple muscle parts
    muscle_part = models.ManyToManyField(
        'exercises.MusclePart',
        related_name='exercises',
        verbose_name='muscle part',
    )

    class Meta:
        db_table = 'exercise'
        ordering = ['name']
        verbose_name = 'exercise'
        verbose_name_plural = 'exercises'
        # name must be unique only for rows where deleted_by is null
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=Q(deleted_by__isnull=True),
                name='unique_exercise_name_if_not_deleted'
            )
        ]

    def __str__(self):
        return self.name
