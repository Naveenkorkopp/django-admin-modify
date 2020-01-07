import uuid
import pickle
import base64
from django.db import models
from django.apps import apps


class Customer(models.Model):
    """
        Model to mimic AppUser model from clearbridge_core , Adds some more required fields,
            Has link to the AppUser model.
    """
    class Meta:
        app_label = "alchemy_common"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        index_together = [
            ["clearbridge_appuser_id", "user_selected_level"],
        ]

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid1
    )
    clearbridge_appuser_id = models.IntegerField(
        unique=True,
        null=False,
        blank=False
    )
    user_selected_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    postal_code = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    gender = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    eligible_for_rewards = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        help_text='Use this setting to tell the loyalty system to ignore this customer in future reward draws.'
    )
    subscription_token = models.CharField(
        max_length=255,
        editable=False,
        unique=True,
        null=True,
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class Segment(models.Model):
    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid1
    )
    name = models.CharField(
        max_length=128
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    queryset = models.TextField()
    sql_query = models.TextField(
    )
    model_name = models.CharField(
        max_length=128,
    )
    app_label = models.CharField(
        max_length=128,
    )
    field_name = models.CharField(
        max_length=128,
    )
    url = models.TextField()
    filter_params = models.TextField()

    is_initialized = models.BooleanField(
        default=False,
        help_text="True only if the initial customer ENTER/LEAVE events have been created in the DB for this segment."
    )
    is_deleted = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        app_label = "alchemy_common"
        verbose_name = "Segment"
        verbose_name_plural = "Segments"
        ordering = ['created_at']

    @property
    def num_customers(self):
        try:
            m = apps.get_model(self.app_label, self.model_name)
            qs = m.objects.all()
            qs.query = pickle.loads(base64.b64decode(self.queryset))
            count = qs.values_list(self.field_name).distinct().count()
        except Exception:
            return '<Unknown number of customers>'
        return count
