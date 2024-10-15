import pytest
import inspect
from unittest.mock import mock_open, patch

from pTypes import FileTransaction
from interface import loadDataFromOfxFile, loadDataFromCsvFile, loadDir

def test_loadDir_returns_list_with_files():
    files = loadDir(path='tests/extratos')

    assert isinstance(files, list)

    for file in files:
        assert isinstance(file, str)
        assert file.endswith('.ofx')


def test_loadDir_when_no_files():

    with pytest.raises(Exception) as error:
        loadDir(path='/ext')

    assert str(error.value) == "Nenhum arquivo encontrado"


def test_loadDataFromOfxFile_returns_file_transactions_data():
    transactions_data = loadDataFromOfxFile(
        path='tests/extratos',
        file_name='Extrato-01-09-2024-a-01-10-2024 (1).ofx'
    )

    assert isinstance(transactions_data, list)

    # Get Props existents in FileTransaction
    allowed_keys = {
        param.name 
        for param in inspect.signature(FileTransaction.__init__).parameters.values()
        if param.name != 'self'
    }
    
    for transaction in transactions_data:

        # Just get Props existents in FileTransaction
        filtered_transaction = {key: value for key, value in transaction.items() if key in allowed_keys}

        transactionClass = FileTransaction(**filtered_transaction)
        assert isinstance(transactionClass, FileTransaction)


def test_loadDataFromOfxFile_when_file_is_not_ofx():

    with pytest.raises(Exception) as error:
        loadDataFromOfxFile(
            path='src/tests/extratos',
            file_name='Extrato.pdf'
        )

    assert str(error.value) == "Arquivo inválido, arquivo deve ser do formato .ofx"


def test_loadDataFromOfxFile_when_file_not_found():

    file_name = 'abacaxi.ofx'
    path = 'src/tests/extratos'

    with pytest.raises(Exception) as error:
        loadDataFromOfxFile(
            path=path,
            file_name=file_name
        )

    assert str(error.value) == f"Arquivo {file_name} não encontrado no caminho {path}"


def test_loadDataFromCsvFile_returns_file_transactions_data():
    mock_csv_data_list = [
        {
            'csv_data': "Data Lançamento;Valor;Histórico;Descrição\n01/01/2023;100,00;Payment;Salary\n02/01/2023;200,50;Refund;Product",
            'headers': {
                'amount': ['Valor'],
                'description': ['Descrição', 'Histórico'],
                'date': ['Data Lançamento']
            },
        },
        {
            'csv_data':"""
Data,Valor,Identificador,Descrição
03/09/2024,-16.40,66d6feed-d7cd-4af6-8037-0c4ad3da86a8,Transferência enviada pelo Pix - DANIELLE VITORIA DE MORAIS TORRES - •••.784.787-•• - BANCO INTER (0077) Agência: 1 Conta: 11969232-5
03/09/2024,-10.00,66d729e7-f93c-4ef3-a860-256a6ecd0cce,Transferência enviada pelo Pix - Ana Lucia Malacarne Milanez - •••.660.257-•• - PICPAY (0380) Agência: 1 Conta: 22880928-2
03/09/2024,-90.00,66d72d04-6cc7-497c-a607-13b915898029,Transferência enviada pelo Pix - Maria Vitoria Favero - •••.242.007-•• - PICPAY (0380) Agência: 1 Conta: 49981920-9
03/09/2024,-5.50,66d74d27-afe7-42a3-b120-e40d78bffce0,Transferência enviada pelo Pix - BIC SOLUCOES EM ALIMENTACAO - 07.648.286/0001-65 - SICOOB CONEXÃO Agência: 3007 Conta: 244634-0
03/09/2024,300.00,66d787b9-b76e-4a4b-b193-2564e8faa43a,Transferência Recebida - Solange Adelia Favero - •••.982.257-•• - NU PAGAMENTOS - IP (0260) Agência: 1 Conta: 64125244-7
03/09/2024,-100.00,66d78b3d-ee13-4456-ab86-e01d1502e0cc,Aplicação RDB
03/09/2024,-10.00,66d78b61-93ed-4cb4-b973-4fbed5f72223,Transferência enviada pelo Pix - Maria Vitoria Favero - •••.242.007-•• - PICPAY (0380) Agência: 1 Conta: 49981920-9
03/09/2024,142.00,66d78c5e-1738-4d85-9f64-4e8cc2bd988d,Transferência recebida pelo Pix - MARIA VITORIA FAVERO - •••.242.007-•• - BCO DO BRASIL S.A. (0001) Agência: 1261 Conta: 12983-6
04/09/2024,-3.50,66d852fa-f784-4c8f-908b-174d14317e28,Transferência enviada pelo Pix - BIC SOLUCOES EM ALIMENTACAO - 07.648.286/0001-65 - SICOOB CONEXÃO Agência: 3007 Conta: 244634-0
04/09/2024,-20.00,66d87da5-39cd-45ae-a48c-fea37c5b7d38,Transferência enviada pelo Pix - Tamires Macedo Correa - •••.083.957-•• - BANCO SICOOB S.A. (0756) Agência: 3007 Conta: 64269321-8
05/09/2024,-1.00,66d9bbba-d1ce-41fd-a89b-a12220341b28,Transferência enviada pelo Pix - BIC SOLUCOES EM ALIMENTACAO LTDA - 07.648.286/0001-65 - MERCADO PAGO IP LTDA. (0323) Agência: 1 Conta: 7084420322-7
05/09/2024,-2.00,66d9d303-53e3-4d91-bff0-044a25db78d5,Transferência enviada pelo Pix - Laura Costa Pereira - •••.688.467-•• - NU PAGAMENTOS - IP (0260) Agência: 1 Conta: 83263914-5
05/09/2024,-147.49,66da0635-2c56-447c-9e3d-edbad72e4d85,Compra no débito - Supermercado Casagrand
""",
            'headers': {
                'amount': ['Valor'],
                'description': ['Descrição'],
                'date': ['Data']
            }        
        },
        {
            'csv_data':
    """
    Extrato Conta Corrente 
Conta ;55844227
Período ;01/09/2024 a 01/10/2024

Data Lançamento;Histórico;Descrição;Valor;Saldo
01/10/2024;Crédito Evento B3;* Prov * Dividendos 3                  Vulc3;0,37
01/10/2024;Crédito Evento B3;* Prov * Juros S/capital 3                  Itsa4;0,06
01/10/2024;Crédito Evento B3;* Prov * Juros S/capital 1                  Itub4;0,01
29/09/2024;Pix enviado ;Weldis Alves Da Silva;-15,00
28/09/2024;Pix enviado ;Fereguetti E Silva Ltda;-33,96
28/09/2024;Pix enviado ;Thayza Vinturini Moitinho;-9,35
28/09/2024;Pix enviado ;Iarly Lorencini Dos Santos;-18,33
27/09/2024;Pix recebido;Antoniel Martins Silva A Rocha;64,00
27/09/2024;Crédito Evento B3;* Prov * Juros S/capital 4                  Bbas3;0,63
""",
            'headers': {
                'amount': ['Valor'],
                'description': ['Descrição', 'Histórico'],
                'date': ['Data Lançamento']
            }
        }
    ]

    for mock_csv_data in mock_csv_data_list:
        with patch('builtins.open', mock_open(read_data=mock_csv_data['csv_data'])):
            
            transactions_data = loadDataFromCsvFile('extratos', 'extrato.csv', headers=mock_csv_data['headers'])
            assert isinstance(transactions_data, list)

            # Get Props existents in FileTransaction
            allowed_keys = {
                param.name 
                for param in inspect.signature(FileTransaction.__init__).parameters.values()
                if param.name != 'self'
            }
            
            for transaction in transactions_data:

                # Just get Props existents in FileTransaction
                filtered_transaction = {key: value for key, value in transaction.items() if key in allowed_keys}

                transactionClass = FileTransaction(**filtered_transaction)
                assert isinstance(transactionClass, FileTransaction)


def test_loadDataFromCsvFile_when_file_is_not_csv():

    with pytest.raises(Exception) as error:
        loadDataFromCsvFile('extratos', 'extrato.pdf')

    assert str(error.value) == "Arquivo inválido, arquivo deve ser do formato .csv"


def test_loadDataFromCsvFile_when_file_not_found():

    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(Exception) as error:
            loadDataFromCsvFile('extratos', 'extrato.csv')

        assert str(error.value) == "Arquivo extrato.csv não encontrado no caminho extratos"


def test_loadDataFromCsvFile_when_data_is_empty():

    empty_csv_data = "Data Lançamento;Valor;Histórico;Descrição\n"
    
    with patch('builtins.open', mock_open(read_data=empty_csv_data)):
        with pytest.raises(Exception) as error:
            loadDataFromCsvFile('extratos', 'extrato.csv')

        assert str(error.value) == "O arquivo CSV parece estar vazio"