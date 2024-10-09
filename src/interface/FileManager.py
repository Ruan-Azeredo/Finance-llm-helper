import ofxparse
import os


def loadDir(path: str = 'extratos'):
    files = []

    for file in os.listdir(path):
        files.append(file)

    return files


def loadFile(path: str = 'extratos', file_name: str = 'Extrato-01-09-2024-a-01-10-2024 (1).ofx'):

    with open(f'{path}/{file_name}', encoding='ISO-8859-1') as ofx_file:
        print(ofxparse.OfxParser.parse(ofx_file))
        parsed_data = ofxparse.OfxParser.parse(ofx_file)
    
    return parsed_data