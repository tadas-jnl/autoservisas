# Generated by Django 5.2.3 on 2025-06-12 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0003_auto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(help_text='Suteiktos paslaugos aprašymas', max_length=200, verbose_name='Paslaugos pavadinimas')),
                ('price', models.FloatField(max_length=10, verbose_name='Paslaugos kaina')),
            ],
        ),
        migrations.CreateModel(
            name='OrderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(blank=True, null=True, verbose_name='Užsakymo data')),
                ('auto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.auto', verbose_name='Automobilis')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(blank=True, null=True, verbose_name='Kiekis')),
                ('order_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservisas.orderdata', verbose_name='Užsakymas')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservisas.service', verbose_name='Suteikta paslauga')),
            ],
        ),
    ]
