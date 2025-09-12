def generate_standard(prompt, model, tokenizer, max_new_tokens=200):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=max_new_tokens)[0]
    output_text = tokenizer.decode(output_ids[len(input_ids[0]):], skip_special_tokens=True)
    return output_text.strip()
