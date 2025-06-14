import json
import torch
from datasets import load_dataset
from llm.model_setup import load_model
from llm.pda_augumented_generation import generate_with_pda


def extract_prompt(prompt_list):
    # Only system and user messages
    return "\n".join(msg["content"] for msg in prompt_list
                     if msg["role"] in ("system", "user"))

def extract_reference_completion(sample):
    return sample["completion"]



def generate_standard(prompt, model, tokenizer, max_new_tokens=200):
    """Free‑form GPT‑2 sampling (top‑k / nucleus) without PDA constraints."""
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

    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return (
        full_text[len(prompt) :].strip()  # strip the echoed prompt
        if full_text.startswith(prompt)
        else full_text.strip()
    )


def main():
    # Dataset
    dataset = load_dataset("NousResearch/json-mode-eval", split="train")

    # Model + tokenizer (loaded via helper)
    model_name = "google/gemma-2-2b"

    tokenizer, model = load_model(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model.to(device)


    num_samples = 100
    standard_correct = 0
    pda_correct = 0

    for i, example in enumerate(dataset):
        if i >= num_samples:
            break

        prompt_str = extract_prompt(example["prompt"])
        reference_completion = extract_reference_completion(example)

        print(f"\n=== Sample {i + 1} ===")

        # --- Standard generation ---
        std_gen = generate_standard(prompt_str, model, tokenizer)
        std_correct = std_gen.strip() == reference_completion.strip()
        print(f"Standard generation correct? {std_correct}")
        print(f"  Output: {std_gen}")
        print(f"  Reference: {reference_completion}")

        # --- PDA‑guided generation ---
        pda_gen = generate_with_pda(prompt_str, model, tokenizer)
        pda_correct_flag = pda_gen.strip() == reference_completion.strip()
        print(f"PDA-guided generation correct? {pda_correct_flag}")
        print(f"  Output: {pda_gen}")
        print(f"  Reference: {reference_completion}")

        if std_correct:
            standard_correct += 1
        if pda_correct_flag:
            pda_correct += 1

    # Summary
    print("\n--- Evaluation Summary ---")
    print(
        f"Samples evaluated: {num_samples}\n"
        f"Standard generation correct completions: {standard_correct} "
        f"({standard_correct / num_samples * 100:.2f}%)\n"
        f"PDA-guided generation correct completions: {pda_correct} "
        f"({pda_correct / num_samples * 100:.2f}%)"
    )


if __name__ == "__main__":
    main()
