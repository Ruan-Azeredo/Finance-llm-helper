import ofxparse
import os


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
