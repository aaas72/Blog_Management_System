
def test_create_post(client, author_token):
    response = client.post(
        "/api/posts",
        json={"title": "Test Post", "content": "This is a test post content."},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == "Test Post"
    assert response.json()["data"]["status"] == "draft"

def test_list_posts_public(client, author_token, admin_token):
    # Create and publish a post
    create_res = client.post(
        "/api/posts",
        json={"title": "Public Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    client.post(
        f"/api/posts/{post_id}/publish",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    
    response = client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) >= 1
    assert data[0]["title"] == "Public Post"

def test_get_single_post(client, author_token):
    # Create post
    create_res = client.post(
        "/api/posts",
        json={"title": "Single Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == post_id

def test_get_post_not_found(client):
    response = client.get("/api/posts/99999")
    assert response.status_code == 404

def test_update_post(client, author_token):
    # Create post
    create_res = client.post(
        "/api/posts",
        json={"title": "Old Title", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Update
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "New Title", "content": "New Content"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "New Title"

def test_update_post_unauthorized(client, author_token, admin_token):
    # Admin creates a post
    create_res = client.post(
        "/api/posts",
        json={"title": "Admin Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Author tries to update it
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "Hacked Title", "content": "Hacked Content"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 403

def test_delete_post(client, author_token):
    # Create post
    create_res = client.post(
        "/api/posts",
        json={"title": "Delete Me", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Delete
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 200
    
    # Verify deleted
    get_res = client.get(f"/api/posts/{post_id}")
    assert get_res.status_code == 404

def test_delete_post_as_admin(client, author_token, admin_token):
    # Author creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Author Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Admin deletes it (should be allowed)
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_my_posts(client, author_token):
    client.post(
        "/api/posts",
        json={"title": "My Post 1", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    client.post(
        "/api/posts",
        json={"title": "My Post 2", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    
    response = client.get(
        "/api/posts/mine",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2

def test_publish_post(client, author_token):
    # Create a post first
    create_res = client.post(
        "/api/posts",
        json={"title": "Post to Publish", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Publish it
    response = client.post(
        f"/api/posts/{post_id}/publish",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "published"

def test_create_post_invalid_role(client, reader_token):
    response = client.post(
        "/api/posts",
        json={"title": "Reader Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {reader_token}"}
    )
    assert response.status_code == 403

def test_admin_publish_author_post(client, author_token, admin_token):
    # Author creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Author Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Admin publishes it
    response = client.post(
        f"/api/posts/{post_id}/publish",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "published"

def test_author_publish_other_post(client, author_token, admin_token):
    # Admin creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Admin Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Author tries to publish it
    response = client.post(
        f"/api/posts/{post_id}/publish",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 403

def test_reader_publish_post(client, reader_token, author_token):
    # Author creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Author Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Reader tries to publish it
    response = client.post(
        f"/api/posts/{post_id}/publish",
        headers={"Authorization": f"Bearer {reader_token}"}
    )
    assert response.status_code == 403

def test_admin_update_author_post(client, author_token, admin_token):
    # Author creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Author Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Admin updates it
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "Admin Updated", "content": "New Content longer"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Admin Updated"

def test_reader_update_post(client, reader_token, author_token):
    # Author creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Author Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Reader tries to update it
    # Should fail due to permission denied (403), not IntegrityError
    # We expect 403 Forbidden because readers cannot update posts
    response = client.put(
        f"/api/posts/{post_id}",
        json={"title": "Reader Update", "content": "New Content longer"},
        headers={"Authorization": f"Bearer {reader_token}"}
    )
    assert response.status_code == 403

def test_author_delete_other_post(client, author_token, admin_token):
    # Admin creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Admin Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Author tries to delete it
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 403

def test_reader_delete_post(client, reader_token, author_token):
    # Author creates post
    create_res = client.post(
        "/api/posts",
        json={"title": "Author Post", "content": "Content longer than 10 chars"},
        headers={"Authorization": f"Bearer {author_token}"}
    )
    post_id = create_res.json()["data"]["id"]
    
    # Reader tries to delete it
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {reader_token}"}
    )
    assert response.status_code == 403
