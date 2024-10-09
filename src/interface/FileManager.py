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


def loadOfxFile(path: str = 'extratos', file_name: str = 'Extrato-01-09-2024-a-01-10-2024 (1).ofx'):
    if file_name.endswith('.ofx'):
        try:
            with open(f'{path}/{file_name}', encoding='ISO-8859-1') as ofx_file:
                print(ofxparse.OfxParser.parse(ofx_file))
                parsed_data = ofxparse.OfxParser.parse(ofx_file)
            
            return parsed_data
        except:
            raise Exception("Arquivo não pode ser aberto")
    else:
        raise Exception("Arquivo inválido, arquivo deve ser do formato .ofx")
