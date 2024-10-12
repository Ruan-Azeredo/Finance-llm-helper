import ofxparse
import csv
import os

from src.pTypes import FileTransaction

def loadDir(path: str = 'extratos'):
    files = []

    try:
        for file in os.listdir(path):
            files.append(file)

    except:
        raise Exception("Nenhum arquivo encontrado")
    
    return files


def loadDataFromOfxFile(path: str = 'extratos', file_name: str = 'Extrato-01-09-2024-a-01-10-2024 (1).ofx'):
    if file_name.endswith('.ofx'):
        try:
            with open(f'{path}/{file_name}', encoding='ISO-8859-1') as ofx_file:
                print(ofxparse.OfxParser.parse(ofx_file))
                parsed_data = ofxparse.OfxParser.parse(ofx_file)
            

            result = []
            for account in parsed_data.accounts:
                for transaction in account.statement.transactions:
                    transaction_dict = transaction.__dict__
                    result.append(transaction_dict)
            
            return result

        except FileNotFoundError:
            raise Exception(f"Arquivo {file_name} não encontrado no caminho {path}")
        except ofxparse.OfxParserError:
            raise Exception("Erro ao processar o arquivo OFX. O formato pode estar incorreto.")
        except Exception as error:
            raise Exception(f"Erro inesperado: {error}")

    else:
        raise Exception("Arquivo inválido, arquivo deve ser do formato .ofx")

def loadDataFromCsvFile(path: str = 'extratos', file_name: str = 'extrato.csv'):
    if file_name.endswith('.csv'):
        try:

            with open(f'{path}/{file_name}', newline='', encoding='utf-8') as csv_file:
                while True:
                    line = csv_file.readline()

                    if 'Data Lançamento' in line:
                        headers = line.split(';')
                        break

                csv_file.seek(csv_file.tell())
                csv_reader = csv.DictReader(csv_file, fieldnames=headers, delimiter=';')

                result = []

                try:
                    next(csv_reader)
                except:
                    raise StopIteration()
                
                for i, row in enumerate(csv_reader, start = 1):
                    
                    transaction = _process_row(i, row)

                    result.append(transaction)
            
            return result

        except StopIteration as error:
            raise Exception("O arquivo CSV parece estar vazio")
        except FileNotFoundError:
            raise Exception(f"Arquivo {file_name} não encontrado no caminho {path}")
        except Exception as error:
            raise Exception(f"Erro inesperado: {error}")

    else:
        raise Exception("Arquivo inválido, arquivo deve ser do formato .csv")
    
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
        raise Exception('current transaction is incomplete')
    else:
        return transaction