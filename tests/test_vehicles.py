import pytest

from models.vehicle.methods import Vehicle

sample_vehicle = {
    "name": "Sample Vehicle",
    "price_per_day": 13.59,
}

sample_category = {
    "name": "Sample Category",
    "carry_capacity": 100,
}


@pytest.mark.parametrize("vehicle,category", [(sample_vehicle, sample_category)])
def test_create_category(vehicle, category, client):
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

    response = client.delete('/vehicle/' + str(vehicle.id))
    assert response.status_code == 200

    response = client.delete('/category/' + str(category['id']))
    assert response.status_code == 200

