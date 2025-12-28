from database.db import engine, Base, SessionLocal
from models.user_model import User, UserRole
from utils.password_utils import get_password_hash
import logging

# Create tables
Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    try:
        admin_username = "admin"
        existing_admin = db.query(User).filter(User.username == admin_username).first()
        if not existing_admin:
            print("Seeding admin user...")
            admin_user = User(
                username=admin_username,
                password_hash=get_password_hash("Admin@123"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user seeded successfully.")
        else:
            print("Admin user already exists.")
    except Exception as e:
        print(f"Error seeding admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
