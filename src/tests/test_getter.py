from utils import get_start_and_end_of_month_by_date, formatDateStrToTimestamp

def test_get_start_and_end_of_month_by_date():
    start_of_month, start_of_next_month = get_start_and_end_of_month_by_date(formatDateStrToTimestamp('12/12/2024'))

    assert start_of_month == formatDateStrToTimestamp('01/12/2024')
    assert start_of_next_month == formatDateStrToTimestamp('01/01/2025')