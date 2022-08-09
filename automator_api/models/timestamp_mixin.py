from django.db import models


class TimestampMixin(models.Model):
    """Timestamp Mixin - adds created_at, updated_at, and deleted_at fields

    Args:
        created_at (DateTimeField): auto adds when created
        updated_at (DateTimeField): auto adds when using .save method
        deleted_at (DateTimeField): For soft deletes, when the object was "deleted"
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
