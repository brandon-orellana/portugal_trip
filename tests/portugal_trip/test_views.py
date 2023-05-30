"""
This is my test for the views.
"""
# test_views.py

def test_index_ok(client):
    """
    To ensure response status code is ok (200).
    """
    response = client.get('/')
    # Assert that the status_code is 200 (OK)
    assert response.status_code == 200
