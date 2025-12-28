
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path to import config if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
TEST_DB_NAME = "blog_test_db"

def init_test_db():
    # Connect to MySQL server (no specific DB) to create the test DB
    database_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}"))
        print(f"Database {TEST_DB_NAME} created or already exists.")

if __name__ == "__main__":
    init_test_db()
