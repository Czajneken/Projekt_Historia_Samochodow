# Generated by Django 4.2.13 on 2024-06-29 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt_historia_samochodow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=64)),
                ('model', models.CharField(max_length=64)),
                ('color', models.CharField(max_length=20)),
                ('engine_size', models.PositiveSmallIntegerField()),
                ('engine_power_HP', models.PositiveSmallIntegerField()),
                ('engine_power_kW', models.PositiveSmallIntegerField()),
                ('mileage', models.PositiveIntegerField()),
                ('type_of_fuel', models.CharField(max_length=10)),
                ('body_type', models.CharField(choices=[(1, 'Coupe'), (2, 'Hatchback'), (3, 'Kabriolet'), (4, 'Kombi'), (5, 'Minivan'), (6, 'Pickup'), (7, 'Sedan'), (8, 'SUV'), (9, 'Van')])),
                ('plate_number', models.CharField(max_length=15)),
                ('VIN', models.IntegerField()),
                ('date_of_first_registration', models.DateField()),
                ('number_of_the_registration_certificate', models.CharField(max_length=15)),
                ('car_photos', models.ImageField(upload_to='media/%Y/%m/%d/')),
            ],
        ),
    ]
