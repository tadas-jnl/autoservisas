# Generated by Django 5.2.3 on 2025-06-12 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0002_rename_auto_modelis_automodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_plate', models.CharField(help_text='Automobilio valstybinis NR', max_length=6, verbose_name='Valstybinis NR')),
                ('vin_code', models.CharField(help_text='Automobilio kėbulo numeris', max_length=17, verbose_name='VIN numeris')),
                ('client', models.CharField(max_length=100, verbose_name='Klientas')),
                ('automodel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.automodel', verbose_name='Automobilio modelis')),
            ],
        ),
    ]
