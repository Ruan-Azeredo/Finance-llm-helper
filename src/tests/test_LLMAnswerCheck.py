from useCases import llmAnswerCheck

def test_llmAnswerCheck_success():

    categories = ["cat", "dog"]
    category = "dog"

    answer = llmAnswerCheck(categories, category)

    assert category == answer
    assert category in categories

def test_llmAnswerCheck_when_category_is_not_in_categories():

    categories = ["cat", "dog"]
    category = "fish"

    answer = llmAnswerCheck(categories, category)

    assert answer == False
    assert category not in categories