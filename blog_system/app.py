from fastapi import FastAPI
from middlewares.error_middleware import add_exception_handlers
from controllers import auth_controller, post_controller
from database.db import engine, Base
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

# Create tables if they don't exist (Production usually uses migrations like Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Management System", version="1.0.0")

# Add Exception Handlers
add_exception_handlers(app)

# Include Routers
app.include_router(auth_controller.router, prefix="/api")
app.include_router(post_controller.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Blog Management System API"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
