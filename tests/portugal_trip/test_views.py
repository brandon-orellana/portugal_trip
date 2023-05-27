# test_views.py

def test_index_ok(client):
    response = client.get('/')
    # Assert that the status_code is 200 (OK)
    assert response.status_code == 200
