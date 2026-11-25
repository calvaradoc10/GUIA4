"""Conservar las notas y evitar el borrado accidental al eliminar matrículas."""
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academico", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nota",
            name="matricula",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nota",
                to="academico.matricula",
            ),
        ),
    ]
