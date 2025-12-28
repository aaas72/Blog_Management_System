import pytest
from datetime import timedelta
from utils.jwt_utils import create_access_token
from jose import jwt
import os

# Get configurations to create fake tokens
SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def test_expired_token(client):
    """
    Test accessing a protected route with an expired token.
    Should return 401 Unauthorized.
    """
    # Create a token that expired 5 minutes ago
    data = {"sub": "1", "username": "expired_user", "role": "author"}
    expired_token = create_access_token(data, expires_delta=timedelta(minutes=-5))
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    assert response.status_code == 401
    assert "expired" in response.json()["error"]["message"].lower()

def test_deleted_user_with_valid_token(client, db, author_token):
    """
    Test accessing a protected route with a valid token but the user has been deleted.
    Should return 401 Unauthorized (User not found).
    """
    # 1. We have a valid author_token from the fixture
    # 2. But we need to delete that specific user from the DB
    
    # First verify it works
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {author_token}"})
    assert response.status_code == 200
    username = response.json()["data"]["username"]
    
    # Now delete the user
    from models.user_model import User
    user = db.query(User).filter(User.username == username).first()
    db.delete(user)
    db.commit()
    
    # Try again with the SAME token
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {author_token}"})
    
    assert response.status_code == 401
    assert "User not found" in response.json()["error"]["message"]

def test_tampered_token_signature(client):
    """
    Test accessing with a token signed by a different secret key.
    Should return 401 Unauthorized.
    """
    # Manually create a token with a WRONG secret key
    data = {"sub": "1", "username": "hacker", "role": "admin"}
    fake_token = jwt.encode(data, "wrong_secret_key", algorithm=ALGORITHM)
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {fake_token}"}
    )
    
    assert response.status_code == 401
    # Depending on implementation, it might say "Invalid authentication credentials"

def test_token_missing_claims(client):
    """
    Test a token that is validly signed but missing critical info (username).
    Should return 401 Unauthorized.
    """
    # Create token without username
    data = {"sub": "1", "role": "author"} # No username
    token = create_access_token(data)
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 401
    # Our middleware checks for username specifically

def test_malformed_token(client):
    """
    Test sending garbage as a token.
    Should return 401 Unauthorized.
    """
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer garbage.token.here"}
    )
    assert response.status_code == 401
