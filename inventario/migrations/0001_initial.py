# Generated by Django 4.1.2 on 2023-08-30 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('creater', models.CharField(blank=True, max_length=30, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('updater', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('deleter', models.CharField(blank=True, max_length=30, null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'categoria de productos',
                'verbose_name_plural': 'categorias de Productos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='EstadoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('creater', models.CharField(blank=True, max_length=30, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('updater', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('deleter', models.CharField(blank=True, max_length=30, null=True)),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('creater', models.CharField(blank=True, max_length=30, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('updater', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('deleter', models.CharField(blank=True, max_length=30, null=True)),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True, verbose_name='descripcion')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategoria', to='inventario.categoria')),
            ],
            options={
                'verbose_name': 'Sub categoria de productos',
                'verbose_name_plural': 'Sub categorias de Productos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('creater', models.CharField(blank=True, max_length=30, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('updater', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('deleter', models.CharField(blank=True, max_length=30, null=True)),
                ('nombre', models.CharField(max_length=100)),
                ('costo', models.FloatField()),
                ('precioVenta', models.FloatField()),
                ('precioMayor', models.FloatField(blank=True, null=True)),
                ('iva', models.IntegerField(default=0)),
                ('existencias', models.FloatField()),
                ('dim_Alto', models.FloatField(blank=True, null=True)),
                ('dim_Ancho', models.FloatField(blank=True, null=True)),
                ('dim_fondo', models.FloatField(blank=True, null=True)),
                ('peso', models.FloatField(blank=True, null=True)),
                ('Nota', models.CharField(blank=True, max_length=200, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=528, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.categoria')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.estadoproducto')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.subcategoria')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'ordering': ['nombre'],
            },
        ),
    ]
