import json
import torch
from datasets import load_dataset
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from llm.pda_augumented_generation import generate_with_pda

def is_valid_json(s: str) -> bool:
    try:
        json.loads(s)
        return True
    except Exception:
        return False

def prompt_to_string(prompt_list):
    # Convert the list of {"role": ..., "content": ...} dicts into one string
    return "\n".join(msg['content'] for msg in prompt_list)

def generate_standard(prompt, model, tokenizer, max_new_tokens=200):
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            eos_token_id=tokenizer.eos_token_id,
        )
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated

def main():
    # Load dataset
    dataset = load_dataset("NousResearch/json-mode-eval", split="train")
    
    # Load model and tokenizer
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    num_samples = 100  # or len(dataset) if you want full
    standard_valid = 0
    pda_valid = 0

    for i, example in enumerate(dataset):
        if i >= num_samples:
            break
        
        prompt_list = example["prompt"]  # This is a list of dicts
        prompt_str = prompt_to_string(prompt_list)  # Convert to string

        print(f"\n=== Sample {i+1} ===")

        # Standard generation
        std_gen = generate_standard(prompt_str, model, tokenizer)
        std_valid = is_valid_json(std_gen)
        print(f"Standard generation valid JSON? {std_valid}")

        # PDA-guided generation
        pda_gen = generate_with_pda(prompt_str, model, tokenizer)
        pda_valid_flag = is_valid_json(pda_gen)
        print(f"PDA-guided generation valid JSON? {pda_valid_flag}")

        # Update counters
        if std_valid:
            standard_valid += 1
        if pda_valid_flag:
            pda_valid += 1

    print("\n--- Evaluation Summary ---")
    print(f"Samples evaluated: {num_samples}")
    print(f"Standard generation valid JSON: {standard_valid} ({standard_valid / num_samples * 100:.2f}%)")
    print(f"PDA-guided generation valid JSON: {pda_valid} ({pda_valid / num_samples * 100:.2f}%)")

if __name__ == "__main__":
    main()
