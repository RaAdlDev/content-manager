from unittest.mock import patch, AsyncMock

def test_create_article(client_writer):
    response = client_writer.post("/articles", 
        json={"title": "yes", "content": "yes again"})

    assert response.status_code == 200
    
def test_submit_article(client_writer):
    article = client_writer.post("/articles", json={"title": "yes", "content": "yes again"})
    article_id = article.json()["article_id"]
    response = client_writer.post(f"/articles/{article_id}/submit")

    assert response.status_code == 200
    assert response.json()["status"] == "PENDING_REVIEW"

def test_approve_article(client_admin, article_submit):
    with patch("routers.articles.new_notification", new_callable=AsyncMock):
        response = client_admin.post(f"/articles/{article_submit}/approve")

    assert response.status_code == 200
    assert response.json()["status"] == "PUBLISHED"

def test_reject_article(client_admin, article_submit):
    with patch("routers.articles.new_notification", new_callable=AsyncMock):
        response = client_admin.post(f"/articles/{article_submit}/reject", json={"rejection_reason": "yes"})

    assert response.status_code == 200
    assert response.json()["status"] == "REJECTED"

def test_edit_published(client_admin, article_approved):
    response = client_admin.patch(f"/articles/{article_approved}", json={"title": "no"})

    assert response.status_code == 409

def test_get_published(client_writer, article_approved):

    response= client_writer.get(f"/articles/{article_approved}")

    assert response.status_code == 200


def test_get_draft(client_writer, article_submit):
    article_response= client_writer.get(f"/articles/{article_submit}")

    assert article_response.status_code == 409





