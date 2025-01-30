import base64
import time
import random
import jwt
import requests
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# Конфигурация
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Ваш приватный ключ
UID = os.getenv("UID")      # UID от API Garantex
HOST = "garantex.org"

def get_auth_token():
    iat = int(time.time())
    claims = {
        "exp": iat + 3600,
        "jti": hex(random.getrandbits(12)).upper()
    }
    private_key = base64.b64decode(PRIVATE_KEY)
    jwt_token = jwt.encode(claims, private_key, algorithm="RS256")

    response = requests.post(
        f"https://dauth.{HOST}/api/v1/sessions/generate_jwt",
        json={"kid": UID, "jwt_token": jwt_token}
    )
    if response.status_code == 200:
        token = response.json().get("token")
        logging.info("JWT токен успешно получен.")
        return token
    else:
        logging.error(f"Ошибка при получении токена: {response.status_code}, {response.text}")
        raise Exception(f"Auth failed: {response.status_code}, {response.text}")