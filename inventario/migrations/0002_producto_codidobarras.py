# Generated by Django 4.1.2 on 2023-09-06 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codidoBarras',
            field=models.CharField(blank=True, max_length=24, null=True, unique=True),
        ),
    ]
