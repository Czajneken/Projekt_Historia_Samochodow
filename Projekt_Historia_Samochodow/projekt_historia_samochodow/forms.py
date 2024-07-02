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


class SearchCarReportForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['number_of_the_registration_certificate']
