# Generated by Django 4.2.13 on 2024-07-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt_historia_samochodow', '0018_remove_car_repairs_car_repairs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='repairs',
            field=models.ManyToManyField(to='projekt_historia_samochodow.repair', verbose_name='Przeprowadzone naprawy'),
        ),
    ]
