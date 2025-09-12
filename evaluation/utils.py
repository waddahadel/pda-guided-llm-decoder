import torch

def generate_standard(prompt: str, model, tokenizer, max_new_tokens: int = 100):
    """
    Generates a standard, unconstrained completion from the model.

    This function serves as the baseline to measure against the PDA-guided approach
    and is language-agnostic, making it suitable for reuse across different
    evaluation scripts.

    Args:
        prompt (str): The input text for the model.
        model: A HuggingFace CausalLM model instance.
        tokenizer: The corresponding tokenizer.
        max_new_tokens (int): The maximum number of new tokens to generate.

    Returns:
        str: The generated text from the model.
    """
    # Ensure the tokenizer has a pad token, using eos_token as a fallback
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            do_sample=True,  # Use sampling to see a wider range of potential errors
            top_k=50,
            top_p=0.95,
            temperature=0.8,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id
        )

    # Decode the full output
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Cleanly extract only the generated part that comes after the prompt
    if full_text.startswith(prompt):
        completion = full_text[len(prompt):]
    else:
        completion = full_text
    
    return completion.strip()