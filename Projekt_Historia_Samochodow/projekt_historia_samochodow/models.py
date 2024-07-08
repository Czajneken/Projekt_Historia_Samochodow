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


FUEL_TYPES = (
    (1, "PB95"),
    (2, "PB98"),
    (3, "LPG+PB95"),
    (4, "LPG+PB98"),
    (5, "DIESEL"),
)


class Repair(models.Model):
    part = models.CharField(max_length=64, verbose_name="Nazwa części")
    part_number = models.CharField(max_length=64, verbose_name="Numer części")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cena")
    mileage = models.PositiveIntegerField(verbose_name="Przebieg")
    type_of_repair = models.IntegerField(choices=REPAIR_TYPES, verbose_name="Rodzaj naprawy")
    description = models.TextField(verbose_name="Opis")
    recommendations = models.TextField(verbose_name="Zalecenia")
    date_of_repair = models.DateField(verbose_name="Data naprawy")

    def __str__(self):
        return self.part


class Car(models.Model):
    brand = models.CharField(max_length=64, verbose_name="Marka")
    model = models.CharField(max_length=64, verbose_name="Model")
    color = models.CharField(max_length=20, verbose_name="Kolor")
    engine_size = models.PositiveSmallIntegerField(verbose_name="Pojemność silnika (w cm3)")
    engine_power_HP = models.PositiveSmallIntegerField(verbose_name="Moc silnika w KM")
    engine_power_kW = models.PositiveSmallIntegerField(verbose_name="Moc silnika w kW")
    mileage = models.PositiveIntegerField(verbose_name="Przebieg")
    type_of_fuel = models.IntegerField(choices=FUEL_TYPES, verbose_name="Rodzaj paliwa")
    body_type = models.IntegerField(choices=BODY_TYPES, verbose_name="Typ nadwozia")
    plate_number = models.CharField(max_length=15, verbose_name="Numer rejestracyjny")
    VIN = models.CharField(max_length=17)
    year_of_production = models.PositiveSmallIntegerField(verbose_name="Data produkcji")
    date_of_first_registration = models.DateField(verbose_name="Data pierwszej rejestracji")
    number_of_the_registration_certificate = models.CharField(max_length=15, verbose_name="Numer dowodu rejestracyjnego")
    car_photos = models.ImageField(upload_to='media', verbose_name="Zdjęcia samochodu")
    repairs = models.ManyToManyField(Repair, verbose_name="Przeprowadzone naprawy")

    def __str__(self):
        return self.plate_number


class CarOwner(models.Model):
    first_name = models.CharField(max_length=64, verbose_name="Imię")
    last_name = models.CharField(max_length=64, verbose_name="Nazwisko")
    phone_number = PhoneNumberField(unique=True, verbose_name="Telefon")
    email = models.EmailField(unique=True, verbose_name="Email")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False, verbose_name="Samochód")

    def __str__(self):
        return self.first_name


class Events(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Calendar Events')
        verbose_name_plural = ('Calendar Events')

    def __str__(self):
        return self.name
