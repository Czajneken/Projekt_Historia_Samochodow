# Generated by Django 4.2.13 on 2024-07-10 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projekt_historia_samochodow', '0023_remove_car_repairs_repair_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projekt_historia_samochodow.car', verbose_name='Samochód'),
        ),
    ]
