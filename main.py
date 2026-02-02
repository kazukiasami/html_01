import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from App Runner 🚀"}

@app.get("/env-check")
def env_check():
    return {
        "APP_ENV": os.getenv("APP_ENV"),
        "DATABASE_URL_exists": os.getenv("DATABASE_URL") is not None,
        "JWT_SECRET_exists": os.getenv("JWT_SECRET") is not None,
        "API_KEY_exists": os.getenv("API_KEY") is not None
    }
