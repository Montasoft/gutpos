# Generated by Django 4.1.2 on 2024-03-09 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_alter_compra_created_alter_compra_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='compradetalles',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='estadocompra',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pagocompra',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]