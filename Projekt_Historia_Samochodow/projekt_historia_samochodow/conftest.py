import pytest
import tempfile
import datetime

from .models import (
    Repair,
    Car,
    CarOwner,
    Event
)


@pytest.fixture
def add_car():
    return Car.objects.create(
        brand="Test brand",
        model="Test model",
        color="Test color",
        engine_size=1998,
        engine_power_HP=200,
        engine_power_kW=100,
        mileage=15000,
        type_of_fuel=1,
        body_type=1,
        plate_number="OP7T76",
        VIN="PL987U901625T5267",
        year_of_production=2023,
        date_of_first_registration=datetime.date(2023, 1, 1),
        number_of_the_registration_certificate="KL16278398I0987",
        car_photos=tempfile.NamedTemporaryFile(suffix=".jpg").name,
    )


@pytest.fixture
def add_car_owner():
    car = Car.objects.create(
        brand="Test brand",
        model="Test model",
        color="Test color",
        engine_size=1998,
        engine_power_HP=200,
        engine_power_kW=100,
        mileage=15000,
        type_of_fuel=1,
        body_type=1,
        plate_number="OP7T76",
        VIN="PL987U901625T5267",
        year_of_production=2023,
        date_of_first_registration=datetime.date(2023, 1, 1),
        number_of_the_registration_certificate="KL16278398I0987",
        car_photos=tempfile.NamedTemporaryFile(suffix=".jpg").name,
    )

    return CarOwner.objects.create(
        first_name="John",
        last_name="Doe",
        phone_number="855693265",
        email="john@example.com",
        car=car
    )


@pytest.fixture
def add_repair():
    car = Car.objects.create(
        brand="Test brand",
        model="Test model",
        color="Test color",
        engine_size=1998,
        engine_power_HP=200,
        engine_power_kW=100,
        mileage=15000,
        type_of_fuel=1,
        body_type=1,
        plate_number="OP7T76",
        VIN="PL987U901625T5267",
        year_of_production=2023,
        date_of_first_registration=datetime.date(2023, 1, 1),
        number_of_the_registration_certificate="KL16278398I0987",
        car_photos=tempfile.NamedTemporaryFile(suffix=".jpg").name,
    )
    return Repair.objects.create(
        part="test part",
        part_number="tp987",
        type_of_repair=1,
        price=200.00,
        mileage=15000,
        description="Test description",
        recommendations="Test recommendations",
        date_of_repair=datetime.date(2023, 1, 1),
        car=car
    )


@pytest.fixture
def add_event():
    return Event.objects.create(
        title="Test event",
        start=datetime.date(2023, 1, 1),
        end=datetime.date(2023, 1, 1),
    )