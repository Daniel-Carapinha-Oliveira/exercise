from django.db import models
from django.contrib.auth import get_user_model
from apps.core.helpers import get_deleted_user

User = get_user_model()


class MetaDataMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='created at',
        auto_now_add=True
    )
    deleted_at = models.DateTimeField(
        verbose_name='deleted at',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET(get_deleted_user),
        related_name='created_%(class)s_set',
        verbose_name='created by'
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET(get_deleted_user),
        null=True,
        blank=True,
        related_name='deleted_%(class)s_set',
        verbose_name='deleted by'
    )

    class Meta:
        abstract = True
