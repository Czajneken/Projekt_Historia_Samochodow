# Generated by Django 4.2.13 on 2024-07-10 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projekt_historia_samochodow', '0022_alter_repair_date_of_repair_alter_repair_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='repairs',
        ),
        migrations.AddField(
            model_name='repair',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projekt_historia_samochodow.car', verbose_name='Samochód'),
        ),
    ]
