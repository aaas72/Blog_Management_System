import pytest
from models.audit_model import AuditLog
from models.post_model import PostStatus
from database.db import Base

def test_audit_log_creation(client, db, admin_token):
    # 1. Create a post
    post_data = {
        "title": "Audit Test Post",
        "content": "This is a test content for audit logging."
    }
    response = client.post("/api/posts/", json=post_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    post_id = response.json()["data"]["id"]

    # Verify log creation
    log = db.query(AuditLog).filter(
        AuditLog.entity_type == "Post",
        AuditLog.entity_id == post_id,
        AuditLog.action == "CREATE"
    ).first()
    
    assert log is not None
    assert "Audit Test Post" in log.details

def test_audit_log_update(client, db, admin_token):
    # 1. Create a post
    post_data = {
        "title": "Original Title",
        "content": "Original Content"
    }
    response = client.post("/api/posts/", json=post_data, headers={"Authorization": f"Bearer {admin_token}"})
    post_id = response.json()["data"]["id"]

    # 2. Update the post
    update_data = {
        "title": "Updated Title"
    }
    response = client.put(f"/api/posts/{post_id}", json=update_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

    # Verify UPDATE log
    log = db.query(AuditLog).filter(
        AuditLog.entity_type == "Post",
        AuditLog.entity_id == post_id,
        AuditLog.action == "UPDATE"
    ).first()

    assert log is not None
    assert "old_title" in log.details
    assert "Original Title" in log.details
    assert "new_title" in log.details
    assert "Updated Title" in log.details

def test_audit_log_publish_archive_delete(client, db, admin_token):
    # 1. Create a post
    post_data = {"title": "Lifecycle Post", "content": "Long enough content to be published......."}
    response = client.post("/api/posts/", json=post_data, headers={"Authorization": f"Bearer {admin_token}"})
    post_id = response.json()["data"]["id"]

    # 2. Publish
    client.post(f"/api/posts/{post_id}/publish", headers={"Authorization": f"Bearer {admin_token}"})
    log = db.query(AuditLog).filter(AuditLog.entity_id == post_id, AuditLog.action == "PUBLISH").first()
    assert log is not None

    # 3. Archive
    client.post(f"/api/posts/{post_id}/archive", headers={"Authorization": f"Bearer {admin_token}"})
    log = db.query(AuditLog).filter(AuditLog.entity_id == post_id, AuditLog.action == "ARCHIVE").first()
    assert log is not None

    # 4. Restore
    client.post(f"/api/posts/{post_id}/restore", headers={"Authorization": f"Bearer {admin_token}"})
    log = db.query(AuditLog).filter(AuditLog.entity_id == post_id, AuditLog.action == "RESTORE").first()
    assert log is not None
    
    # 5. Delete (must be draft to delete? No, check logic. Delete is allowed if not archived.)
    # The restore puts it back to DRAFT.
    client.delete(f"/api/posts/{post_id}", headers={"Authorization": f"Bearer {admin_token}"})
    log = db.query(AuditLog).filter(AuditLog.entity_id == post_id, AuditLog.action == "DELETE").first()
    assert log is not None
