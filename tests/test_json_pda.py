from tokenizors import json_tokenizor

def test_tokenizer():
    tokenizer = json_tokenizor.JsonTokenizer()
    input_str = '{"x": [1, 2, null]}'
    expected = ['{', '"x"', ':', '[', '1', ',', '2', ',', 'null', ']', '}']
    assert tokenizer.tokenize(input_str) == expected
