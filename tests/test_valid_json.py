from tokenizors import json_tokenizor
from pda.json_pda import JsonPDA


def test_valid_json_object():
    json_str = '{"name": "Wadah", "age": 25, "is_student": false}'
    tokenizer = json_tokenizor.JsonTokenizer()
    tokens = tokenizer.tokenize(json_str)

    pda = JsonPDA()
    assert pda.accepts(tokens) is True


def test_valid_nested_json():
    json_str = '{"user": {"name": "Wadah", "skills": ["Python", "ML"]}}'
    tokenizer = json_tokenizor.JsonTokenizer()
    tokens = tokenizer.tokenize(json_str)

    pda = JsonPDA()
    assert pda.accepts(tokens) is True


def test_invalid_json_missing_comma():
    json_str = '{"name": "Wadah"  "age": 25}'  # Missing comma between fields
    tokenizer = json_tokenizor.JsonTokenizer()
    tokens = tokenizer.tokenize(json_str)

    pda = JsonPDA()
    assert pda.accepts(tokens) is False


def test_invalid_json_extra_closing():
    json_str = '{"name": "Wadah"}}'
    tokenizer = json_tokenizor.JsonTokenizer()
    tokens = tokenizer.tokenize(json_str)

    pda = JsonPDA()
    assert pda.accepts(tokens) is False
