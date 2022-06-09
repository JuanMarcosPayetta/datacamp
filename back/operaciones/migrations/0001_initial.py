# Generated by Django 3.0.5 on 2022-06-09 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_inidep', models.CharField(max_length=10)),
                ('cod_fao_alfa3', models.CharField(blank=True, max_length=3, null=True)),
                ('cod_fao_taxonomico', models.CharField(blank=True, max_length=13, null=True)),
                ('nombre_cientifico', models.CharField(max_length=255)),
                ('nombre_anterior_1', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_anterior_2', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_inidep', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Nombre_Vulgar_Especie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.Especie')),
            ],
        ),
        migrations.AddField(
            model_name='especie',
            name='orden',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='operaciones.Orden'),
        ),
        migrations.CreateModel(
            name='DetalleRedArrastre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_lance', models.PositiveIntegerField(null=True)),
                ('rumbo', models.CharField(max_length=5, null=True)),
                ('vel_arras', models.FloatField(null=True)),
                ('dist_arras', models.FloatField(null=True)),
                ('aber_vert', models.FloatField(null=True)),
                ('cab_filad', models.FloatField(null=True)),
                ('dist_alas', models.FloatField(null=True)),
                ('ang_pala_helice', models.FloatField(null=True)),
                ('dist_e_por', models.FloatField(null=True)),
                ('tension_red', models.FloatField(null=True)),
                ('area_barrida', models.FloatField(null=True)),
                ('observacion', models.CharField(max_length=150, null=True)),
                ('operacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estaciones.Operacion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetallePalangre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linea_madre_mat', models.FloatField(null=True)),
                ('linea_madre_largo', models.FloatField(null=True)),
                ('linea_madre_tramo', models.FloatField(null=True)),
                ('brazolada_largo', models.FloatField(null=True)),
                ('brazolada_separacion', models.FloatField(null=True)),
                ('brazolada_nro_tramo', models.FloatField(null=True)),
                ('anzuelos_nro_total', models.FloatField(null=True)),
                ('anzuelos_con_carnada', models.FloatField(null=True)),
                ('anzuelos_sin_carnada', models.FloatField(null=True)),
                ('carnada', models.CharField(max_length=100, null=True)),
                ('observacion', models.CharField(max_length=150, null=True)),
                ('operacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estaciones.Operacion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Captura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_lance', models.PositiveIntegerField(null=True)),
                ('especie_desc', models.CharField(max_length=255)),
                ('kg', models.DecimalField(decimal_places=4, max_digits=12)),
                ('cantidadXkilo', models.DecimalField(decimal_places=4, max_digits=12, null=True)),
                ('cant_ejemplares', models.IntegerField(blank=True, null=True)),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.Especie')),
                ('operacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estaciones.Operacion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]