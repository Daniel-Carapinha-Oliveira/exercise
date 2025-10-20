from django.db import models


class Muscle(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    # ForeignKeys
    body_part = models.ForeignKey(
        'exercises.BodyPart',
        on_delete=models.PROTECT,
        related_name='muscles',
        verbose_name='body part',
    )

    class Meta:
        db_table = 'muscle'
        ordering = ['name']
        verbose_name = 'muscle'
        verbose_name_plural = 'muscles'

    def __str__(self):
        return self.name


class BodyPart(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    image = models.ImageField(
        verbose_name='image',
        upload_to='img/body_parts/'
    )

    description = models.TextField(
        verbose_name='description',
    )

    class Meta:
        db_table = 'body_part'
        ordering = ['name']
        verbose_name = 'body part'
        verbose_name_plural = 'body parts'

    def __str__(self):
        return self.name


class MusclePart(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100
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

    def __str__(self):
        return self.name


class Exercise(models.Model):
    class WorkoutType(models.TextChoices):
        CALISTHENIC = 'calisthenics', 'Calisthenics'
        GYM = 'gym', 'Gym'

    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
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

    # ForeignKeys
    muscle_part = models.ForeignKey(
        'exercises.MusclePart',
        on_delete=models.PROTECT,
        related_name='exercises',
        verbose_name='muscle part',
    )

    class Meta:
        db_table = 'exercise'
        ordering = ['name']
        verbose_name = 'exercise'
        verbose_name_plural = 'exercises'

    def __str__(self):
        return self.name
