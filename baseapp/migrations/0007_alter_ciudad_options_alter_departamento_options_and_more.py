# Generated by Django 4.1.2 on 2024-03-13 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0006_alter_banco_updated_alter_ciudad_updated_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ciudad',
            options={'ordering': ['nombre'], 'verbose_name': 'Ciudad', 'verbose_name_plural': 'Ciudades'},
        ),
        migrations.AlterModelOptions(
            name='departamento',
            options={'ordering': ['nombre'], 'verbose_name': 'Departamento', 'verbose_name_plural': 'Departamentos'},
        ),
        migrations.AlterModelOptions(
            name='formapago',
            options={'ordering': ['nombre'], 'verbose_name': 'Forma de Pago', 'verbose_name_plural': 'Formas de Pago'},
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='created',
            new_name='_created',
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='creater',
            new_name='_creater',
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='deleted',
            new_name='_deleted',
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='deleter',
            new_name='_deleter',
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='state',
            new_name='_state',
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='updated',
            new_name='_updated',
        ),
        migrations.RenameField(
            model_name='banco',
            old_name='updater',
            new_name='_updater',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='created',
            new_name='_created',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='creater',
            new_name='_creater',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='deleted',
            new_name='_deleted',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='deleter',
            new_name='_deleter',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='state',
            new_name='_state',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='updated',
            new_name='_updated',
        ),
        migrations.RenameField(
            model_name='ciudad',
            old_name='updater',
            new_name='_updater',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='created',
            new_name='_created',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='creater',
            new_name='_creater',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='deleted',
            new_name='_deleted',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='deleter',
            new_name='_deleter',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='state',
            new_name='_state',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='updated',
            new_name='_updated',
        ),
        migrations.RenameField(
            model_name='formapago',
            old_name='updater',
            new_name='_updater',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='created',
            new_name='_created',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='creater',
            new_name='_creater',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='deleted',
            new_name='_deleted',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='deleter',
            new_name='_deleter',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='state',
            new_name='_state',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='updated',
            new_name='_updated',
        ),
        migrations.RenameField(
            model_name='tipodocumento',
            old_name='updater',
            new_name='_updater',
        ),
    ]
