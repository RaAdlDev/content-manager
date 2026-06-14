def test_create_tag(client_admin):
    response = client_admin.post("/tag", json={"name": "category"})

    assert response.status_code == 200

def test_get_tag(client):
    response = client.get("/tag")

    assert response.status_code == 200