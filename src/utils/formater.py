from datetime import datetime

def formatAmount(amount: float) -> str:
    return f"{abs(amount):.2f}".replace('.', ',')

def formatDirection(amount: float) -> str:
    if amount < 0:
        return 'expense'
    return 'income'

def formatDate(date: str) -> str:
    if date is None:
        return ''
    
    if isinstance(date, datetime):
        return date.strftime("%d/%m/%Y")
    
    for date_format in ("%d/%m/%Y", "%d-%m-%Y"):  # Add formats here
        try:
            date_obj = datetime.strptime(date, date_format)
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            continue
        except Exception as error:
            raise Exception(f"Erro inesperado: {error}, date: {date}")
    return ''

def formatHaderKey(row: dict) -> dict:
    clear_row = {key.replace('\n', ''): value for key, value in row.items()}
    return clear_row
    