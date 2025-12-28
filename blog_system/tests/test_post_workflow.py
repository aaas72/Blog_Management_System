import pytest
from models.post_model import PostStatus
from utils.exceptions import ValidationError

def test_post_lifecycle_workflow(client, author_token):
    headers = {"Authorization": f"Bearer {author_token}"}

    # 1. Create a Draft
    response = client.post(
        "/api/posts",
        json={"title": "Lifecycle Post", "content": "This is a draft content for lifecycle test."},
        headers=headers
    )
    assert response.status_code == 200
    post_id = response.json()["data"]["id"]
    assert response.json()["data"]["status"] == PostStatus.DRAFT.value

    # 2. Try to Publish (Short Content) -> Fail
    # Create short content first (must be > 10 chars for Pydantic schema, but < 20 for Service logic)
    client.put(
        f"/api/posts/{post_id}",
        json={"title": "Short", "content": "Short Content"},
        headers=headers
    )
    response = client.post(
        f"/api/posts/{post_id}/publish",
        headers=headers
    )
    assert response.status_code == 400
    assert "content too short" in response.json()["error"]["message"].lower()

    # 3. Update to Valid Content
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "Valid Title", "content": "This content is definitely long enough to be published."},
        headers=headers
    )
    assert response.status_code == 200

    # 4. Publish Successfully
    response = client.post(
        f"/api/posts/{post_id}/publish",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == PostStatus.PUBLISHED.value

    # 5. Try to Update Published Post -> Fail
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "New Title"},
        headers=headers
    )
    assert response.status_code == 400
    assert "cannot update a published post" in response.json()["error"]["message"].lower()

    # 6. Archive Post
    response = client.post(
        f"/api/posts/{post_id}/archive",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == PostStatus.ARCHIVED.value

    # 7. Try to Delete Archived Post -> Fail
    response = client.delete(
        f"/api/posts/{post_id}",
        headers=headers
    )
    assert response.status_code == 400
    assert "cannot delete archived posts" in response.json()["error"]["message"].lower()

    # 8. Try to Update Archived Post -> Fail
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "Updated Title"},
        headers=headers
    )
    assert response.status_code == 400
    assert "cannot update an archived post" in response.json()["error"]["message"].lower()

    # 9. Restore Post
    response = client.post(
        f"/api/posts/{post_id}/restore",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == PostStatus.DRAFT.value

    # 10. Now Delete (Back to Draft) -> Success
    response = client.delete(
        f"/api/posts/{post_id}",
        headers=headers
    )
    assert response.status_code == 200
