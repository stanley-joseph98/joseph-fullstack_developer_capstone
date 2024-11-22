# Generated by Django 5.1.3 on 2024-11-22 14:51

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'Wagon'), ('HATCHBACK', 'Hatchback'), ('COUPE', 'Coupe'), ('CONVERTIBLE', 'Convertible'), ('MINIVAN', 'Minivan'), ('PICKUP', 'Pickup Truck'), ('SPORTS', 'Sports Car'), ('LUXURY', 'Luxury Car'), ('CROSSOVER', 'Crossover'), ('ROADSTER', 'Roadster'), ('VAN', 'Van'), ('MICRO', 'Microcar'), ('SUBCOMPACT', 'Subcompact'), ('COMPACT', 'Compact'), ('FULLSIZE', 'Full-Size'), ('OFFROAD', 'Off-Road Vehicle'), ('ELECTRIC', 'Electric Vehicle'), ('HYBRID', 'Hybrid Vehicle'), ('DIESEL', 'Diesel Vehicle'), ('FLEET', 'Fleet Vehicle'), ('MOTORHOME', 'Motorhome'), ('COUPE', 'Coupe'), ('TARGA', 'Targa'), ('SALOON', 'Saloon'), ('EXECUTIVE', 'Executive Car'), ('CITY', 'City Car'), ('PERFORMANCE', 'Performance Car'), ('SUPER', 'Supercar'), ('CLASSIC', 'Classic Car'), ('TAXI', 'Taxi'), ('AMBULANCE', 'Ambulance'), ('POLICE', 'Police Car'), ('STATION_WAGON', 'Station Wagon'), ('FAMILY', 'Family Car'), ('MIDSIZE', 'Midsize Car'), ('LIMOUSINE', 'Limousine')], default='SUV', max_length=25)),
                ('year', models.IntegerField(default=2024, validators=[django.core.validators.MaxValueValidator(2024), django.core.validators.MinValueValidator(2015)])),
                ('car_make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.carmake')),
            ],
        ),
    ]
