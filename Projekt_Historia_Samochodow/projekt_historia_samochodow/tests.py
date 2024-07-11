import pytest

from .models import (
    Repair,
    Car,
    CarOwner,
    Event
)


@pytest.mark.django_db
def test_car_model(add_car):
    assert Car.objects.count() == 1
    assert Car.objects.get(brand="Test brand") == add_car


@pytest.mark.django_db
def test_car_owner_model(add_car_owner):
    assert CarOwner.objects.count() == 1
    assert CarOwner.objects.get(first_name="John") == add_car_owner


@pytest.mark.django_db
def test_repair_model(add_repair):
    assert Repair.objects.count() == 1
    assert Repair.objects.get(part="test part") == add_repair


@pytest.mark.django_db
def test_event_model(add_event):
    assert Event.objects.count() == 1
    assert Event.objects.get(title="Test event") == add_event


@pytest.mark.django_db
def test_main_view(client):
    response = client.get('http://127.0.0.1:8000/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_car_report_view(client):
    response = client.get('http://127.0.0.1:8000/search_car_report/')
    assert response.status_code == 200
    response_post = client.post(
        '/search_car_report/',
        {
            'number_of_the_registration_certificate': 'MC/MZD8888888',
        }
    )
    assert response_post.status_code == 302