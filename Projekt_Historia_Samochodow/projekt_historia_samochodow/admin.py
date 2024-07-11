from django.contrib import admin

from .models import (
    Repair,
    Car,
    CarOwner,
    Event
)


admin.site.register(Repair)
admin.site.register(Car)
admin.site.register(CarOwner)
admin.site.register(Event)
