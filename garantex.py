import requests
import logging

API_BASE_URL = "https://garantex.org/api/v2/otc/deals"

def get_p2p_deals(token, **filters):
    headers = {"Authorization": f"Bearer {token}"}
    params = {k: v for k, v in filters.items() if v is not None}

    response = requests.get(API_BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        deals = response.json()
        # Сортировка сделок по id
        deals_sorted = sorted(deals, key=lambda x: x['id'])
        logging.info(f"Данные успешно получены с API Garantex.")
        return deals_sorted
    else:
        logging.error(f"Ошибка при получении данных: {response.status_code}, {response.text}")
        raise Exception(f"Error fetching deals: {response.status_code}, {response.text}")