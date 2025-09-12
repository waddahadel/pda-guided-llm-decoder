import json
from llm.generate_candidates import get_top_k_candidates
from pda.json_pda import JsonPDA


def generate_with_pda(
    prompt: str,
    model,
    tokenizer,
    max_steps: int = 500,
    top_k: int = 50,
) -> str:
    """
    Generate syntactically valid JSON instances using PDA-guided decoding.
    This version uses a robust stopping condition to prevent premature termination.
    """
    pda = JsonPDA()
    generated_text = ""
    json_started = False
    
    print(f"--- Starting PDA-Guided JSON Generation ---")

    for step in range(max_steps):
        context = prompt + generated_text
        candidates = get_top_k_candidates(context, k=top_k, model=model, tokenizer=tokenizer)
        
        if not candidates:
    
            break

   
        token_accepted = False
        for token in candidates:
            if not json_started:
                first_char_index = -1
                for i, char in enumerate(token):
                    if char in "{[":
                        first_char_index = i
                        break
                
                if first_char_index != -1:
                    json_part = token[first_char_index:]
                    temp_pda = pda.clone()
                    is_token_valid = all(temp_pda.consume_char(c, partial=True) for c in json_part)
                    
                    if is_token_valid:
                        pda = temp_pda
                        generated_text += token
                        token_accepted = True
                        json_started = True
                        break
                else:
                    generated_text += token
                    token_accepted = True
                    break
            else:
                temp_pda = pda.clone()
                is_token_valid = all(temp_pda.consume_char(c, partial=True) for c in token)
                
                if is_token_valid:
               
                    pda = temp_pda
                    generated_text += token
                    token_accepted = True
                    break
               
        if not token_accepted:
        
            break

    start_brace = generated_text.find('{')
    start_bracket = generated_text.find('[')
    start_index = -1
    if start_brace != -1 and start_bracket != -1:
        start_index = min(start_brace, start_bracket)
    elif start_brace != -1:
        start_index = start_brace
    else:
        start_index = start_bracket
    final_json = generated_text[start_index:] if start_index != -1 else "{}"

   
    return final_json
