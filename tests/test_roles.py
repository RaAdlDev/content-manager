def test_reader_create_article(reader_client):
    response = reader_client.post("/articles", json={"title": "no", 
            "content": "auth"})
    
    assert response.status_code == 403

def test_writer_approve(client_writer, article_submit):
    response = client_writer.post(f"/articles/{article_submit}/approve")

    assert response.status_code == 403

def test_invalid_token(client):
    response = client.get("/articles")

    assert response.status_code == 401

