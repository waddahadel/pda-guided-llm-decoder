from pda.toy_lang_pda import ToyLangPDA

def test_token_validation_sequence():
    tokens = ['let', 'x', '=', '5', '+', '3', ';', 'print', '(', 'x', ')', ';']
    pda = ToyLangPDA()
    pda.reset()

    results = []
    for token in tokens:
        valid = pda.is_valid_token(token)
        state = pda.get_state()
        results.append((token, valid, state))

    

    # For now, just print the results for manual check
    for token, valid, state in results:
        print(f"Token: {token:>6} | Valid: {valid} | State: {state}")

def test_balanced_parens():
    pda = ToyLangPDA()
    assert pda.accepts("(x = 1)") is True

def test_unbalanced_parens():
    pda = ToyLangPDA()
    assert pda.accepts("(x = 1") is False
