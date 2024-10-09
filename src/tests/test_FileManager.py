from interface import loadFile

def test_loadFile_returns_object_with_accounts():
    parsed_data = loadFile(
        path='extratos',
        file_name='Extrato-01-09-2024-a-01-10-2024 (1).ofx'
    )

    assert hasattr(parsed_data, 'accounts')
    assert isinstance(parsed_data.accounts, list)