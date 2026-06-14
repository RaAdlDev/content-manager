def test_register(client):
    response = client.post(url="/auth/register", json={"email":"new@new.com", "password": "Test123*"})

    assert response.status_code == 200
    assert response.json()["status"] == "Successful Request"

def test_email_duplicated(client, create_writer_admin_reader):

    response = client.post(url="/auth/register", json={"email":"example@example.com", "password": "Test123*"})

    assert response.status_code == 409

def test_login(client, create_writer_admin_reader):
    user = create_writer_admin_reader["writer"]
    response = client.post(url="/auth/login", json={"email": user.email, "password": "Test123*"})

    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["token_type"] == "bearer"
   
    
def test_invalid_credentials(client, create_writer_admin_reader):
    user = create_writer_admin_reader["writer"]
    response = client.post(url="/auth/login", json={"email": user.email, "password": "bad_request"})

    assert response.status_code == 401

def test_deactivate_user(create_writer_admin_reader, client_admin):
    user = create_writer_admin_reader["writer"]
    user_id = user.user_id

    response = client_admin.patch(f"/auth/{user_id}/deactivate")

    assert response.status_code == 200

def test_new_writer(create_writer_admin_reader, client_admin):
    user = create_writer_admin_reader["reader"]
    user_id = user.user_id

    response = client_admin.patch(f"/auth/{user_id}/writer")

    assert response.status_code == 200

def test_new_admin(create_writer_admin_reader, client_admin):
    user = create_writer_admin_reader["reader"]
    user_id = user.user_id

    response = client_admin.patch(f"/auth/{user_id}/admin")

    assert response.status_code == 200

def test_new_admin_bad_status(create_writer_admin_reader, client_admin):
    user = create_writer_admin_reader["writer"]
    user_id = user.user_id

    response = client_admin.patch(f"/auth/{user_id}/writer")

    assert response.status_code == 409


    






