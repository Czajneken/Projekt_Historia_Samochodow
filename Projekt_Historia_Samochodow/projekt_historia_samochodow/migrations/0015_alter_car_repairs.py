# Generated by Django 4.2.13 on 2024-07-05 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projekt_historia_samochodow', '0014_alter_car_repairs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='repairs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projekt_historia_samochodow.repair', verbose_name='Przeprowadzone naprawy'),
        ),
    ]
