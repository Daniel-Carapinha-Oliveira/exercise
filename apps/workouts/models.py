from django.db import models


class Muscle(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    # ForeignKeys
    body_part = models.ForeignKey(
        'workouts.BodyPart',
        on_delete=models.PROTECT,
        related_name='muscles',
        verbose_name='parte do corpo',
    )

    class Meta:
        db_table = 'Muscle'
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

    class Meta:
        db_table = 'BodyPart'
        ordering = ['name']
        verbose_name = 'body part'
        verbose_name_plural = 'body parts'

    def __str__(self):
        return self.name
