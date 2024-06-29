from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


BODY_TYPES = (
    (1, "Coupe"),
    (2, "Hatchback"),
    (3, "Kabriolet"),
    (4, "Kombi"),
    (5, "Minivan"),
    (6, "Pickup"),
    (7, "Sedan"),
    (8, "SUV"),
    (9, "Van"),
)


REPAIR_TYPES = (
    (1, "Alternatory i akumulatory"),
    (2, "Chłodzenie"),
    (3, "Doloty powietrza"),
    (4, "Filtry"),
    (5, "Hamulce"),
    (6, "Klimatyzacje i nagrzewnice"),
    (7, "Lusterka"),
    (8, "Nadwozie"),
    (9, "Oleje i płyny"),
    (10, "Opony i felgi"),
    (11, "Paski klinowe i wielorowkowe"),
    (12, "Przeguby, półosie i wały napędowe"),
    (13, "Rozruch i zapłon"),
    (14, "Rozrządy"),
    (15, "Silniki i skrzynie biegów"),
    (16, "Smarowanie"),
    (17, "Sprzęgła"),
    (18, "Układy kierownicze"),
    (19, "Układy wtryskowe"),
    (20, "Wycieraczki i szyby"),
    (21, "Wydechy"),
    (22, "Zasilanie paliwem"),
    (23, "Zawieszenie i amortyzatory"),
    (24, "Żarówki i oświetlenie"),
)


class CarOwner(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)


class Repair(models.Model):
    mileage = models.PositiveIntegerField()
    type_of_repair = models.CharField(choices=REPAIR_TYPES)
    description = models.TextField()
    part = models.CharField(max_length=64)
    part_number = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8 ,decimal_places=2)
    recommendations = models.TextField()
    date_of_repair = models.DateField()


class Car(models.Model):
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    color = models.CharField(max_length=20)
    engine_size = models.PositiveSmallIntegerField()
    engine_power_HP = models.PositiveSmallIntegerField()
    engine_power_kW = models.PositiveSmallIntegerField()
    mileage = models.PositiveIntegerField()
    type_of_fuel = models.CharField(max_length=10)
    body_type = models.CharField(choices=BODY_TYPES)
    plate_number = models.CharField(max_length=15)
    VIN = models.IntegerField()
    year_of_production = models.PositiveSmallIntegerField
    date_of_first_registration = models.DateField()
    number_of_the_registration_certificate = models.CharField(max_length=15)
    car_photos = models.ImageField(upload_to='zdj_samochodow/%Y/%m/%d/')
    owner = models.OneToOneField(CarOwner, on_delete=models.CASCADE, null=False)
    repairs = models.ManyToManyField(Repair)

