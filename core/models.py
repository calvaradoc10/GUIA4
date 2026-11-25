
# core/models.py
# Modelo base que utilizarán los modelos académicos

from django.contrib.auth.models import User
from django.db import models


class ModeloBase(models.Model):
    # Usuario que registró la información
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_registrados",
        verbose_name="Registrado por",
    )

    # Fecha en que se creó el registro
    fecha_creacion = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )

    # Fecha de la última modificación
    fecha_modificacion = models.DateTimeField(
        "Última modificación",
        auto_now=True
    )

    class Meta:
        abstract = True
