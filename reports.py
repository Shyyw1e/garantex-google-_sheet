def calculate_revenue_and_tax(deals):
    total_revenue = 0
    total_expenses = 0
    total_commission = 0

    for deal in deals:
        amount = float(deal["amount"])
        fee_size = float(deal["fee_size"])  # Комиссия в валюте сделки
        commission = fee_size * amount  # Доход от комиссии по сделке
        total_commission += commission

        fee = float(deal["fee"])  # Комиссия в процентах
        total_expenses += fee * amount  # Расходы по сделке

        # Если сделка - это продажа, то добавляем её к выручке
        if deal["direction"] == "sell":
            total_revenue += amount

    # Прибыль = Выручка - Расходы
    profit = total_revenue - total_expenses

    # Налог на прибыль
    tax = 0.13 * profit if profit <= 2400000 else (0.13 * 2400000) + (0.15 * (profit - 2400000))

    return total_commission, total_expenses, total_revenue, profit, tax

def generate_quarterly_reports(deals):
    quarterly_data = {}
    for deal in deals:
        quarter = (int(deal["created_at"][5:7]) - 1) // 3 + 1
        year = deal["created_at"][:4]
        key = f"Q{quarter} {year}"

        if key not in quarterly_data:
            quarterly_data[key] = {"revenue": 0, "expenses": 0, "profit": 0}

        amount = float(deal["amount"])
        fee = float(deal["fee"]) * amount
        direction = deal["direction"]

        if direction == "sell":
            quarterly_data[key]["revenue"] += amount

        quarterly_data[key]["expenses"] += fee
        quarterly_data[key]["profit"] = quarterly_data[key]["revenue"] - quarterly_data[key]["expenses"]

    return quarterly_data