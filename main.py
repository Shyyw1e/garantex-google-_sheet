from auth import get_auth_token
from garantex import get_p2p_deals
from google_sheets import append_data
from reports import calculate_revenue_and_tax, generate_quarterly_reports
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        # Получаем токен
        token = get_auth_token()

        # Запрашиваем все сделки
        deals = get_p2p_deals(token, currency="rub", state="completed", limit=1000)

        # Подготовка данных для записи в Google Sheets (лист с сделками)
        formatted_deals = [
            ["ID", "Дата", "Направление", "Сумма сделки", "Цена", "Валюта", "Покупатель", "Продавец", "Статус", "Комиссия"]
        ] + [[deal["id"], deal["created_at"], deal["direction"], deal["amount"],
              deal["price"], deal["currency"], deal["buyer"], deal["seller"], deal["state"], deal.get("fee_size", "")]
             for deal in deals]

        # Записываем сделки на Лист1
        append_data("Deals", formatted_deals)

        # Генерация и добавление отчетности
        commission, expenses, revenue, profit, tax = calculate_revenue_and_tax(deals)

        # Формируем и записываем отчет по Cashflow
        cashflow_data = [
            ["Тип", "Сумма"],
            ["Входящие потоки", revenue],
            ["Исходящие потоки", expenses]
        ]
        append_data("Cashflow", cashflow_data)

        # Формируем и записываем отчет по P&L
        pnl_data = [
            ["Показатель", "Сумма"],
            ["Доход", commission],
            ["Расходы", expenses],
            ["Прибыль (до налога)", profit]
        ]
        append_data("P&L", pnl_data)

        # Формируем и записываем отчет по налогам
        tax_data = [
            ["Показатель", "Сумма"],
            ["Налог на прибыль", tax]
        ]
        append_data("Taxes", tax_data)

        # Генерация и запись квартальных отчетов
        quarterly_reports = generate_quarterly_reports(deals)
        append_data("Quarterly", [["Quarter", "Revenue", "Expenses", "Profit"]] + [
            [quarter, data["revenue"], data["expenses"], data["profit"]] for quarter, data in quarterly_reports.items()
        ])

    except Exception as e:
        logging.error(f"Ошибка в выполнении скрипта: {e}")