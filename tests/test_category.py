def test_create_category(client_admin):
    response = client_admin.post("/category", json={"name": "category"})

    assert response.status_code == 200

def test_get_category(client):
    response = client.get("/category")

    assert response.status_code == 200