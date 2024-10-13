from useCases import personalizePrompt

def test_personalizePrompt_returns_string():
    template = personalizePrompt("Teste", ["Teste"])
    assert isinstance(template, str)