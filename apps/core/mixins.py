from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MetaDataMixin:
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
        on_delete=models.SET_NULL,
        verbose_name='created by'
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='deleted by'
    )
