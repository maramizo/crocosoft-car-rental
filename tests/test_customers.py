import pytest

sample_customer = {
    "name": "Mohammad Ayoub",
    "email": "test@test.com",
    "number": "0123456789",
    "address": "Test Address",
}


@pytest.mark.parametrize("customer", [sample_customer])
def test_create_category(customer, client):
    assert customer == sample_customer

    response = client.post('/customers/create', data=customer)
    assert response.status_code == 404

    response = client.post('/customer/create', json=customer)
    assert response.status_code == 200

    res = response.get_json()
    assert res['id'] is not None
    assert res['name'] == customer['name']
    assert res['email'] == customer['email']
    assert res['number'] == customer['number']
    assert res['address'] == customer['address']

    response = client.get('/customer/' + str(res['id']))
    assert response.status_code == 200
    res = response.get_json()

    assert res['id'] is not None
    assert res['name'] == customer['name']
    assert res['email'] == customer['email']
    assert res['number'] == customer['number']
    assert res['address'] == customer['address']

    response = client.delete('/customer/' + str(res['id']))
    assert response.status_code == 200
