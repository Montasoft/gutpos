# Generated by Django 4.1.2 on 2024-03-04 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_banco'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banco',
            options={'ordering': ['nombre'], 'verbose_name': 'Banco', 'verbose_name_plural': 'Bancos'},
        ),
    ]
