import pytest

sample_category = {
    "name": "Sample Category",
    "carry_capacity": 100,
}


@pytest.mark.parametrize("category", [sample_category])
def test_create_category(category, client):
    assert category == sample_category

    response = client.post('/categories/create', data=category)
    assert response.status_code == 404

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

    response = client.delete('/category/' + str(res['id']))
    assert response.status_code == 200
