import os
import json
from fastapi import FastAPI

app = FastAPI()

def get_db_config():
    """Secrets Manager から DB設定を取得"""
    secret_json = os.getenv("DB_SECRET")
    if secret_json:
        try:
            return json.loads(secret_json)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
    print("DB_SECRET environment variable not found")
    return None

@app.get("/")
def root():
    return {"message": "Hello App Runner with Secrets Manager!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-config")
def db_config():
    """DB設定確認（パスワード除く）"""
    config = get_db_config()
    if config:
        return {
            "host": config.get("host"),
            "port": config.get("port"),
            "dbname": config.get("dbname"),
            "username": config.get("username"),
            "password_set": bool(config.get("password")),
            "secrets_manager": "connected"
        }
    return {"error": "DB config not found", "secrets_manager": "failed"}

@app.get("/test-db")
def test_db():
    """DB接続テスト用エンドポイント"""
    config = get_db_config()
    if config:
        return {
            "message": "DB config loaded successfully",
            "host": config.get("host"),
            "dbname": config.get("dbname")
        }
    return {"error": "Cannot load DB config"}
