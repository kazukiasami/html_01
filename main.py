import os
import json
import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_db_connection():
    secret = os.getenv("DB_SECRET")
    if not secret:
        raise RuntimeError("DB_SECRET is not set")

    creds = json.loads(secret)

    return psycopg2.connect(
        host=creds["host"],
        port=creds["port"],
        user=creds["username"],
        password=creds["password"],
        dbname=creds["dbname"],
        connect_timeout=5
    )

@app.get("/")
async def root():
    return {"message": "Hello from App Runner 🚀"}

@app.get("/health/db")
async def health_check_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result[0] == 1:
            return {"status": "DB疎通OK"}
        else:
            raise HTTPException(status_code=500, detail="DB connection failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection error: {str(e)}")

# デバッグ用エンドポイント
@app.get("/debug/env")
async def debug_env():
    return {
        "DB_SECRET_exists": bool(os.getenv("DB_SECRET")),
        "DB_SECRET_length": len(os.getenv("DB_SECRET", "")) if os.getenv("DB_SECRET") else 0
