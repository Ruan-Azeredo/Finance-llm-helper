import ofxparse
import csv
import os
import io

from pTypes import FileTransaction
from utils import default_headers, formatHaderKey

def loadDir(path: str = 'extratos'):
    files = []

    try:
        for file in os.listdir(path):
            files.append(file)

    except:
        raise Exception("Nenhum arquivo encontrado")
    
    return files


def loadDataFromOfxFile(content: bytes):
    try:
        ofx_data = io.BytesIO(content)
        parsed_data = ofxparse.OfxParser.parse(ofx_data)
        

        result = []
        for account in parsed_data.accounts:
            for transaction in account.statement.transactions:
                transaction_dict = transaction.__dict__
                result.append(transaction_dict)
        
        return result

    except ofxparse.OfxParserException:
        raise Exception("Erro ao processar o arquivo OFX. O formato pode estar incorreto.")
    except Exception as error:
        raise Exception(f"Erro inesperado: {error}")



def openCsvFile(path: str, file_name: str):
    if file_name.endswith('.csv'):
        try:
            with open(f'{path}/{file_name}', newline='', encoding='utf-8') as csv_file:
                
                csv_content = csv_file.read()
                return csv_content

        except FileNotFoundError:
            raise Exception(f"Arquivo {file_name} não encontrado no caminho {path}")


async def loadDataFromCsvFile(content: bytes, headers: dict = default_headers):

    try:

        decoded_content = content.decode('utf-8')

        lines = decoded_content.splitlines()

        i = 20
        while i > 0:
            i = i - 1
            line = lines[0].strip()  # Lê a primeira linha e remove espaços extras
            lines.pop(0)  # Remove a linha já lida
            if headers['amount'][0] in line:
                if ';' in line:
                    headers_csv = line.split(';')
                    delimiter = ';'
                elif ',' in line:
                    headers_csv = line.split(',')
                    delimiter = ','
                break

        csv_reader = csv.DictReader(lines, fieldnames=headers_csv, delimiter=delimiter)

        result = []

        try:
            next(csv_reader)
        except:
            raise StopIteration()
        
        for i, row in enumerate(csv_reader, start = 1):
            clear_row = formatHaderKey(row)
            
            transaction = _process_abstract_row(i, clear_row, headers)

            result.append(transaction)
        
        return result

    except StopIteration as error:
        raise Exception("O arquivo CSV parece estar vazio")
    except Exception as error:
        raise Exception(f"Erro inesperado: {error}")

    
def _process_row(index, row) -> FileTransaction:
    valor_str = row.get('Valor')
    if valor_str:
        amount = float(valor_str.replace(',', '.'))
    else:
        amount = 0.0

    historico = row.get('Histórico') or ''
    descricao = row.get('Descrição') or ''

    transaction = {
        'id': index,
        'date': row.get('Data Lançamento'),
        'amount': amount,
        'memo': historico + ' ' + descricao,
    }

    if transaction['amount'] is None or len(transaction['memo']) == 0:
        raise Exception('A transação parece estar com os dados incompletos')
    else:
        return transaction
    
def _process_abstract_row(index, row, headers: dict[list]) -> FileTransaction:
    amount = ''
    if len(headers['amount']) > 1:
        for i, header in enumerate(headers['amount'], start = 1):
            if i == 1:
                amount = row[header]
            else:
                amount += ' ' + row[header]
    else:
        amount = row[headers['amount'][0]]

    date = ''
    if len(headers['date']) > 1:
        for i, header in enumerate(headers['date'], start = 1):
            if i == 1:
                date = row[header]
            else:
                date += ' ' + row[header]
    else:
        date = row[headers['date'][0]]

    description = ''
    if len(headers['description']) > 1:
        for i, header in enumerate(headers['description'], start = 1):
            if i == 1:
                description = row[header]
            else:
                description += ' ' + row[header]
    else:
        description = row[headers['description'][0]]

    transaction = {
        'id': index,
        'date': date,
        'amount': float(amount.replace(',', '.')),
        'memo': description,
    }

    if transaction['amount'] is None or len(transaction['memo']) == 0:
        raise Exception('A transação parece estar com os dados incompletos')
    else:
        return transaction