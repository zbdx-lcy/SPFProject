# Generated by Django 3.0 on 2024-01-21 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('temperature', '0001_initial'),
        ('formulation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rheological_data',
            fields=[
                ('rh_id', models.IntegerField(primary_key=True, serialize=False)),
                ('temp_mark', models.IntegerField()),
                ('time_min', models.FloatField()),
                ('time_s', models.FloatField()),
                ('temp', models.FloatField()),
                ('energy_storage_mod', models.FloatField()),
                ('loss_mod', models.FloatField()),
                ('loss_factor', models.FloatField()),
                ('complex_viscosity', models.FloatField()),
                ('clearances', models.FloatField()),
                ('normal_force', models.FloatField()),
                ('torsion', models.FloatField()),
                ('state_mark', models.CharField(max_length=10)),
                ('formulation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formulation.formulations')),
                ('temperature_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='temperature.temperature')),
            ],
        ),
    ]
