from llm.generate_candidates import get_top_k_candidates
from tokenizors.json_tokenizor import JsonTokenizer
from pda.json_pda import JsonPDA


def generate_valid_json(
    prompt: str,
    max_steps: int = 20,
    top_k: int = 10,
    model_name: str = "gpt2"
):
    tokenizer = JsonTokenizer()
    pda = JsonPDA()

    # Step 1: Generate the initial JSON starting string WITHOUT PDA filtering
    current_prompt = prompt
    for _ in range(10):  # generate up to 10 tokens from natural language prompt
        candidates = get_top_k_candidates(current_prompt, k=top_k, model_name=model_name)
        if not candidates:
            print("No candidates from LLM.")
            return current_prompt

        # Just pick first candidate to extend prompt (no filtering)
        current_prompt += candidates[0]

    # Now find where the JSON actually starts (i.e., first '{' character)
    json_start = current_prompt.find("{")
    if json_start == -1:
        print("No JSON start found in generated text.")
        return current_prompt

    json_prompt = current_prompt[json_start:]
    print(f"Starting PDA filtering from JSON substring:\n{json_prompt}")

    # Step 2: Initialize PDA with the initial json_prompt
    tokens = tokenizer.tokenize(json_prompt)
    for token in tokens:
        if not pda.is_valid_token(token):
            print(f"PDA rejected initial JSON token: {token}")
            return json_prompt  # stop early if initial JSON is invalid

    current_prompt = json_prompt

    # Step 3: Now do PDA-filtered token generation continuing from json_prompt
    for step in range(max_steps):
        candidates = get_top_k_candidates(current_prompt, k=top_k, model_name=model_name)
        print(f"[Step {step}] Candidates before PDA filtering: {candidates}")

        for token in candidates:
            clean_token = token.lstrip()
            candidate_pda = pda.clone()
            try:
                # Only tokenize the new token, since current_prompt was already accepted
                tokenized = tokenizer.tokenize(clean_token)
            except SyntaxError:
                continue

            if len(tokenized) != 1:
                continue  # only allow single-token candidates

            if candidate_pda.is_valid_token(tokenized[0]):
                print(f"[Step {step}] Accepted token: {repr(token)}")
                pda = candidate_pda  # advance PDA state
                current_prompt += token
                break
        else:
            print(f"[Step {step}] No valid tokens found. Stopping.")
            break

    print("\n--- Final Generated JSON ---")
    print(current_prompt)
    return current_prompt
