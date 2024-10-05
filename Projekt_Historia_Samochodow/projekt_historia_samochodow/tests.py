import pytest
import datetime
import tempfile

from .models import (
    Repair,
    Car,
    CarOwner,
    Event
)


@pytest.mark.django_db
def test_car_model(car):
    assert Car.objects.count() == 1
    assert Car.objects.get(brand="Test brand") == car


@pytest.mark.django_db
def test_car_owner_model(car_owner):
    assert CarOwner.objects.count() == 1
    assert CarOwner.objects.get(first_name="John") == car_owner


@pytest.mark.django_db
def test_repair_model(repair):
    assert Repair.objects.count() == 1
    assert Repair.objects.get(part="test part") == repair


@pytest.mark.django_db
def test_event_model(event):
    assert Event.objects.count() == 1
    assert Event.objects.get(title="Test event") == event


@pytest.mark.django_db
def test_main_view(client):
    response = client.get('http://127.0.0.1:8000/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_car_report_view(client, car):
    response = client.get('http://127.0.0.1:8000/search_car_report/')
    assert response.status_code == 200
    response_post = client.post(
        '/search_car_report/',
        {
            'number_of_the_registration_certificate': 'KL16278398I0987',
        }
    )
    assert response_post.status_code == 200
    assert Car.objects.get(number_of_the_registration_certificate='KL16278398I0987')


@pytest.mark.django_db
def test_add_car_view(client):
    response = client.get('http://127.0.0.1:8000/add_car')
    assert response.status_code == 200
    response_post = client.post(
        '/add_car',
        {
            'brand': 'Test brand',
            'model': 'Test model',
            'color': 'Test color',
            'engine_size': 1998,
            'engine_power_HP': 200,
            'engine_power_kW': 100,
            'mileage': 15000,
            'type_of_fuel': 1,
            'body_type': 1,
            'plate_number': 'OP7T76',
            'VIN': 'PL987901625T5267',
            'year_of_production': 2023,
            'date_of_first_registration': datetime.date(2023, 1, 1),
            'number_of_the_registration_certificate': 'KL16278398I0987',
            'car_photos': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        }
    )
    assert response_post.status_code == 200
    car1 = Car.objects.get(brand='Test brand')
    assert car1.model == 'Test model'
    assert car1.color == 'Test color'
    assert car1.engine_size == 1998
    assert car1.engine_power_HP == 200
    assert car1.engine_power_kW == 100
    assert car1.mileage == 15000
    assert car1.type_of_fuel == 1
    assert car1.body_type == 1
    assert car1.plate_number == 'OP7T76'
    assert car1.VIN == 'PL987901625T5267'
    assert car1.year_of_production == 2023
    assert car1.date_of_first_registration == datetime.date(2023, 1, 1)
    assert car1.number_of_the_registration_certificate == 'KL16278398I0987'
    assert car1.car_photos == tempfile.NamedTemporaryFile(suffix=".jpg").name


@pytest.mark.django_db
def test_add_car_owner_view(client, car):
    response = client.get('http://127.0.0.1:8000/add_car_owner')
    assert response.status_code == 200
    response_post = client.post(
        '/add_car_owner',
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '569842362',
            'email': 'john@example.com',
            'car': 1
        }
    )
    assert response_post.status_code == 302
    car_owner1 = CarOwner.objects.get(first_name='John')
    assert car_owner1.last_name == 'Doe'
    assert car_owner1.phone_number == '569842362'
    assert car_owner1.email == 'john@example.com'
    assert car_owner1.car == car


@pytest.mark.django_db
def test_add_repair(client, car):
    response = client.get('/add_repair/')
    assert response.status_code == 200
    response_post = client.post(
        '/add_repair/',
        {
            'part': 'test part',
            'part_number': 'hs812',
            'type_of_repair': 1,
            'price': 200.00,
            'mileage': 15000,
            'description': 'test test',
            'recommendations': 'some recommendations',
            'date_of_repair': datetime.date(2023, 1, 1),
            'car': 1
        }
    )
    assert response_post.status_code == 302, response_post.context['form'].errors
    repair1 = Repair.objects.get(part='test part')
    assert repair1.part_number == 'hs812'
    assert repair1.type_of_repair == 1
    assert repair1.price == 200.00
    assert repair1.mileage == 15000
    assert repair1.description == 'test test'
    assert repair1.recommendations == 'some recommendations'
    assert repair1.date_of_repair == datetime.date(2023, 1, 1)
    assert repair1.car == car
    assert Repair.objects.count() == 1


@pytest.mark.django_db
def test_mechanic_view(client):
    username = 'admin'
    password = 'admin'
    client.login(username=username, password=password)
    response = client.get('http://127.0.0.1:8000/mechanic')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client):
    response = client.get('http://127.0.0.1:8000/login')
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
    response = client.get('http://127.0.0.1:8000/logout')
    assert response.status_code == 302


@pytest.mark.django_db
def test_car_list_view(client):
    response = client.get('http://127.0.0.1:8000/car_list')
    assert response.status_code == 200


@pytest.mark.django_db
def test_car_owner_list_view(client):
    response = client.get('http://127.0.0.1:8000/car_owner_list')
    assert response.status_code == 200


@pytest.mark.django_db
def test_car_mileage_update(client, car):
    response = client.get(f'http://127.0.0.1:8000/update_mileage/{car.pk}')
    assert response.status_code == 200
    response_post = client.post(
        f'/update_mileage/{car.pk}',
        {
            'mileage': 15000,
        }
    )
    car.mileage = response_post.context['mileage']
    car.save()
    assert response_post.context['mileage'] == car.mileage
    assert response_post.status_code == 302
