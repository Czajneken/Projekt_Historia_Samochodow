# Generated by Django 4.2.13 on 2024-07-02 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projekt_historia_samochodow', '0010_alter_car_repairs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='body_type',
            field=models.IntegerField(choices=[(1, 'Coupe'), (2, 'Hatchback'), (3, 'Kabriolet'), (4, 'Kombi'), (5, 'Minivan'), (6, 'Pickup'), (7, 'Sedan'), (8, 'SUV'), (9, 'Van')], verbose_name='Typ nadwozia'),
        ),
        migrations.AlterField(
            model_name='car',
            name='type_of_fuel',
            field=models.IntegerField(choices=[(1, 'PB95'), (2, 'PB98'), (3, 'LPG+PB95'), (4, 'LPG+PB98'), (5, 'DIESEL')], verbose_name='Rodzaj paliwa'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='type_of_repair',
            field=models.IntegerField(choices=[(1, 'Alternatory i akumulatory'), (2, 'Chłodzenie'), (3, 'Doloty powietrza'), (4, 'Filtry'), (5, 'Hamulce'), (6, 'Klimatyzacje i nagrzewnice'), (7, 'Lusterka'), (8, 'Nadwozie'), (9, 'Oleje i płyny'), (10, 'Opony i felgi'), (11, 'Paski klinowe i wielorowkowe'), (12, 'Przeguby, półosie i wały napędowe'), (13, 'Rozruch i zapłon'), (14, 'Rozrządy'), (15, 'Silniki i skrzynie biegów'), (16, 'Smarowanie'), (17, 'Sprzęgła'), (18, 'Układy kierownicze'), (19, 'Układy wtryskowe'), (20, 'Wycieraczki i szyby'), (21, 'Wydechy'), (22, 'Zasilanie paliwem'), (23, 'Zawieszenie i amortyzatory'), (24, 'Żarówki i oświetlenie')], verbose_name='Rodzaj naprawy'),
        ),
    ]
