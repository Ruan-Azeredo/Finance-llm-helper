from datetime import datetime

def formatDirectionByAmount(amount: float) -> str:
    if amount > 0:
        return 'income'
    
    return 'expense'

def formatAmountToString(amount: float) -> str:
    return f"{abs(amount):.2f}".replace('.', ',')

def formatAmountToFloat(amount: str) -> float:
        return float(amount.replace(',', '.'))
    
def formatTimestampToDateStr(timestamp: int) -> str:
    """
    :param timestamp: Timestamp em segundos.
    :return: Data no formato dd/mm/aaaa.
    """
    data = datetime.fromtimestamp(timestamp)
    return data.strftime("%d/%m/%Y")

def formatDateStrToTimestamp(data: str) -> int:
    """
    :param data: Data no formato dd/mm/aaaa.
    :return: Timestamp correspondente em segundos.
    """
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y")
        return int(data_formatada.timestamp())
    except ValueError:
        raise ValueError("Formato de data inválido. Use dd/mm/aaaa.")

def formatDate(date: str) -> str:
    if date is None:
        return ''
    
    if isinstance(date, datetime):
        return date.strftime("%d/%m/%Y")
    
    for date_format in ("%d/%m/%Y", "%d-%m-%Y"):
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

