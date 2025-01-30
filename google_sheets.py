import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import logging
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем значения из .env
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Авторизация для работы с Google Sheets
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build('sheets', 'v4', credentials=credentials)

# Функция для добавления данных в Google Sheets
def append_data(sheet_name, data):
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{sheet_name}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": data}
    ).execute()
    logging.info(f"Данные успешно добавлены в лист: {sheet_name}")

# Функция для получения сделок с API Garantex
def get_p2p_deals(token, **filters):
    headers = {"Authorization": f"Bearer {token}"}
    params = {k: v for k, v in filters.items() if v is not None}

    response = requests.get("https://garantex.org/api/v2/otc/deals", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Ошибка при получении данных: {response.status_code}, {response.text}")
        raise Exception(f"Error fetching deals: {response.status_code}, {response.text}")
