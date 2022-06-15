import pytest

from models.customer.methods import Customer
from models.vehicle.methods import Vehicle

sample_vehicle = {
    "name": "Sample Vehicle",
    "price_per_day": 13.59,
}

sample_category = {
    "name": "Sample Category",
    "carry_capacity": 100,
}

sample_customer = {
    "name": "Mohammad Ayoub",
    "email": "test10@test.com",
    "number": "0123456789",
    "address": "Test Address",
}


@pytest.mark.parametrize("vehicle,category,customer",
                         [(sample_vehicle, sample_category, sample_customer)])
def test_create_category(vehicle, category, customer, client):
    assert category == sample_category
    assert vehicle == sample_vehicle

    response = client.post('/category/create', json=category)
    assert response.status_code == 200

    res = response.get_json()
    assert res['id'] is not None
    assert res['name'] == category['name']
    assert res['carry_capacity'] == category['carry_capacity']

    response = client.get('/category/' + str(res['id']))
    assert response.status_code == 200
    res = response.get_json()

    assert res['id'] is not None
    assert res['name'] == category['name']
    assert res['carry_capacity'] == category['carry_capacity']

    vehicle['category_id'] = res['id']
    category['id'] = res['id']

    response = client.post('/vehicle/create', json=vehicle)
    assert response.status_code == 200

    res = response.get_json()
    assert res['id'] is not None
    assert res['name'] == vehicle['name']
    assert res['price_per_day'] == vehicle['price_per_day']

    response = client.get('/vehicle/' + str(res['id']))
    assert response.status_code == 200
    res = response.get_json()

    assert res['id'] is not None
    assert res['name'] == vehicle['name']
    assert float(res['price_per_day']) == vehicle['price_per_day']
    assert res['category_id'] == category['id']

    vehicle = Vehicle(**res)
    assert vehicle.name == res['name']
    assert vehicle.price_per_day == res['price_per_day']
    assert vehicle.category_id == res['category_id']

    response = client.post('/customer/create', json=sample_customer)
    assert response.status_code == 200

    res = response.get_json()
    assert res['id'] is not None
    assert res['name'] == sample_customer['name']
    assert res['email'] == sample_customer['email']
    assert res['number'] == sample_customer['number']
    assert res['address'] == sample_customer['address']

    response = client.get('/customer/' + str(res['id']))
    assert response.status_code == 200
    res = response.get_json()

    assert res['id'] is not None
    assert res['name'] == sample_customer['name']
    assert res['email'] == sample_customer['email']
    assert res['number'] == sample_customer['number']
    assert res['address'] == sample_customer['address']
    customer['id'] = res['id']

    customer = Customer(**res)
    assert customer.name == res['name']
    assert customer.email == res['email']
    assert customer.number == res['number']
    assert customer.address == res['address']
    assert customer.id == res['id']

    response = client.post('/booking/create', json={
        "customer_id": customer.id,
        "vehicle_id": vehicle.id,
        "hire_date": "2020-01-02T00:00:00",
        "end_date": "2020-01-01T00:00:00",
    })

    assert response.status_code == 400
    res = response.get_json()
    assert res['error'] == "Hire date must be before end date."

    response = client.post('/booking/create', json={
        "customer_id": customer.id,
        "vehicle_id": vehicle.id,
        "hire_date": "2020-01-01T00:00:00",
        "end_date": "2020-01-15T00:00:00",
    })

    assert response.status_code == 400
    res = response.get_json()
    assert res['error'] == "Booking must be less than or equal to 7 days."

    response = client.post('/booking/create', json={
        "customer_id": customer.id,
        "vehicle_id": vehicle.id,
        "hire_date": "2020-01-01T00:00:00",
        "end_date": "2020-01-05T00:00:00",
    })

    assert response.status_code == 200
    res = response.get_json()
    assert res['id'] is not None
    assert res['customer_id'] == customer.id
    assert res['vehicle_id'] == vehicle.id
    assert res['hire_date'] == "2020-01-01 00:00:00"
    assert res['end_date'] == "2020-01-05 00:00:00"
    assert res['confirmed'] is False

    response = client.get('/booking/' + str(res['id']))
    assert response.status_code == 200
    res = response.get_json()

    assert res['id'] is not None
    assert res['customer_id'] == customer.id
    assert res['vehicle_id'] == vehicle.id
    assert res['hire_date'] == "2020-01-01 00:00:00"
    assert res['end_date'] == "2020-01-05 00:00:00"
    assert res['confirmed'] == 0 # This is supposed to be false, so this needs to be fixed from the data model.

    response = client.delete('/booking/' + str(res['id']))
    assert response.status_code == 200

    response = client.get('/booking/' + str(res['id']))
    assert response.status_code == 404

    response = client.delete('/vehicle/' + str(vehicle.id))
    assert response.status_code == 200

    response = client.delete('/category/' + str(category['id']))
    assert response.status_code == 200

    response = client.delete('/customer/' + str(customer.id))
    assert response.status_code == 200

