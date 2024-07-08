from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import (
    BODY_TYPES,
    REPAIR_TYPES,
    FUEL_TYPES,
    Repair,
    Car,
    CarOwner
)


class SearchCarReportForm(forms.Form):
    number_of_the_registration_certificate = forms.CharField(label='Numer dowodu rejestracyjnego', max_length=15)


class AddCarForm(forms.Form):
    brand = forms.CharField(label='Marka', max_length=64)
    model = forms.CharField(label='Model', max_length=64)
    color = forms.CharField(label='Kolor', max_length=20)
    engine_size = forms.IntegerField(label='Pojemność silnika (w cm3)')
    engine_power_HP = forms.IntegerField(label='Moc silnika w KM')
    engine_power_kW = forms.IntegerField(label='Moc silnika w kW')
    mileage = forms.IntegerField(label='Przebieg')
    type_of_fuel = forms.ChoiceField(label='Rodzaj paliwa', choices=FUEL_TYPES)
    body_type = forms.ChoiceField(label='Rodzaj nadwozia', choices=BODY_TYPES)
    plate_number = forms.CharField(label='Numer rejestracyjny', max_length=15)
    VIN = forms.CharField(label='VIN', max_length=17)
    year_of_production = forms.IntegerField(label='Rok produkcji')
    date_of_first_registration = forms.DateField(label='Data pierwszej rejestracji')
    number_of_the_registration_certificate = forms.CharField(label='Numer dowodu rejestracyjnego', max_length=15)
    car_photos = forms.ImageField(label='Zdjęcia samochodu')
    # class Meta:
    #     model = Car
    #     exclude = ['repairs']


class AddCarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = "__all__"


class AddRepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = "__all__"