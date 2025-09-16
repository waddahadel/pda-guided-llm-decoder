def generate_standard(prompt, model, tokenizer, max_new_tokens=200):
    device = model.device  # get model device (cpu or cuda)
    
    # Tokenize with attention mask and pad token
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    
    # Move tensors to the same device as the model
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Ensure pad_token_id is set
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # Generate
    output_ids = model.generate(
        input_ids,
        attention_mask=attention_mask,
        pad_token_id=tokenizer.pad_token_id,
        max_new_tokens=max_new_tokens
    )[0]

    # Decode only the new tokens
    output_text = tokenizer.decode(
        output_ids[len(input_ids[0]):],
        skip_special_tokens=True
    )
    return output_text.strip()
