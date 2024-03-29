# Generated by Django 4.1.2 on 2023-08-30 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('whatsapp', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('PQRF', models.CharField(choices=[('P', 'Petición'), ('Q', 'Queja'), ('R', 'Reclamo'), ('F', 'Felicitaciones')], default='F', max_length=1)),
                ('mensaje', models.TextField(max_length=1000)),
                ('imagen', models.FileField(upload_to='PQRF')),
                ('state', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creater', models.CharField(max_length=20)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updater', models.CharField(max_length=20)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('deleter', models.CharField(max_length=20)),
            ],
        ),
    ]
