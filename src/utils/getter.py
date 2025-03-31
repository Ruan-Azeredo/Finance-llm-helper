from datetime import datetime

def get_start_and_end_of_month_by_date(date: int) -> tuple[int, int]:

    transaction_month_number = datetime.fromtimestamp(date).month # month is 1-12
    transaction_month_year = datetime.fromtimestamp(date).year # year is 2023, 2024, etc.

    start_of_month = datetime(transaction_month_year, transaction_month_number, 1).timestamp()

    if transaction_month_number == 12:
        start_of_next_month = datetime(transaction_month_year + 1, 1, 1).timestamp()
    else:
        start_of_next_month = datetime(transaction_month_year, transaction_month_number + 1, 1).timestamp()

    return start_of_month, start_of_next_month