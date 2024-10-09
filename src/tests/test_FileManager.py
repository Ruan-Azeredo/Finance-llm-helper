import pytest

from interface import loadOfxFile, loadDir

def test_loadDir_returns_list_with_files():
    files = loadDir(path='extratos')

    assert isinstance(files, list)

    for file in files:
        assert isinstance(file, str)
        assert file.endswith('.ofx')

def test_loadDir_when_no_files():

    with pytest.raises(Exception) as error:
        loadDir(path='/ext')

    assert str(error.value) == "Nenhum arquivo encontrado"

def test_loadFile_returns_object_with_accounts():
    parsed_data = loadOfxFile(
        path='extratos',
        file_name='Extrato-01-09-2024-a-01-10-2024 (1).ofx'
    )

    assert hasattr(parsed_data, 'accounts')
    assert isinstance(parsed_data.accounts, list)

def test_loadFile_when_file_is_not_ofx():

    with pytest.raises(Exception) as error:
        loadOfxFile(
            path='extratos',
            file_name='Extrato.pdf'
        )

    assert str(error.value) == "Arquivo inválido, arquivo deve ser do formato .ofx"