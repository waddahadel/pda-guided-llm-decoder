import json
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

from llm.model_setup import load_model
from llm.pda_augmented_generation import generate_with_pda 
from pda.json_pda import JsonPDA
from evaluation.utils import generate_standard

def extract_prompt(prompt_list: list) -> str:
    """Extracts and combines system and user messages for the prompt."""
    return "\n".join(msg["content"] for msg in prompt_list if msg["role"] in ("system", "user"))

def is_valid_json(s: str) -> bool:
    """Validate if a string is proper JSON."""
    try:
        if not s.strip().startswith('{') or not s.strip().endswith('}'):
             return False
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False

def main():
    """Main function to run the entire JSON evaluation pipeline."""
    # --- Evaluation Configuration ---
    MODEL_NAME = "google/gemma-2-2b-it"
    
    
    DATASET_NAME = "NousResearch/json-mode-eval"
    DATASET_SPLIT = "train"
    NUM_SAMPLES = 100

    # --- setup ---
    print("Loading model and tokenizer...")
    tokenizer, model = load_model(MODEL_NAME)
    
    print(f"Loading dataset '{DATASET_NAME}'...")

    dataset = load_dataset(DATASET_NAME, split=DATASET_SPLIT, streaming=True)
    
    results = []

    print(f"\n--- Starting Evaluation on {NUM_SAMPLES} samples ---")
    dataset_iterator = iter(dataset)
    for i in range(NUM_SAMPLES):
        try:
            example = next(dataset_iterator)
        except StopIteration:
            break

        print(f"\n\n{'='*25} Processing Sample {i + 1} {'='*25}")

        prompt_str = extract_prompt(example["prompt"])
        reference_completion = example["completion"]

        # 1. PDA-guided generation (this function already has the step-by-step prints)
        pda_gen = generate_with_pda(prompt_str, model, tokenizer, max_steps=200)

        
        print("\n--- Final Comparison ---")
        print(f"[PDA Output]:\n{pda_gen}")
        
        print(f"\n[Reference JSON]:\n{reference_completion}")
        print("=" * 70)
        
        is_std_valid = is_valid_json(std_gen)
        
        try:
            norm_ref = ' '.join(json.dumps(json.loads(reference_completion), sort_keys=True).split())
        except json.JSONDecodeError:
            norm_ref = reference_completion 

        try:
            norm_std = ' '.join(json.dumps(json.loads(std_gen), sort_keys=True).split())
            std_em = (norm_std == norm_ref)
        except json.JSONDecodeError:
            std_em = False

        try:
            norm_pda = ' '.join(json.dumps(json.loads(pda_gen), sort_keys=True).split())
            pda_em = (norm_pda == norm_ref)
        except json.JSONDecodeError:
            pda_em = False

        results.append({
            "id": i,
            "prompt": prompt_str,
            "reference_json": reference_completion,
            "standard_gen": std_gen,
            "pda_gen": pda_gen,
            "std_is_valid": is_std_valid,
            "std_exact_match": std_em,
            "pda_exact_match": pda_em,
        })

   


    


if __name__ == "__main__":
    main()
