# Generated by Django 3.2.25 on 2024-03-26 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20240325_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
