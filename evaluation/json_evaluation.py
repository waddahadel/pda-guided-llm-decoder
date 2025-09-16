import json
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

from llm.model_setup import load_model
from llm.pda_augmented_generation import generate_with_pda 
from llm.standard_generator import generate_standard
from pda.json_pda import JsonPDA

def extract_prompt(prompt_list: list) -> str:
    """Extracts and combines system and user messages for the prompt."""
    return "\n".join(msg["content"] for msg in prompt_list if msg["role"] in ("system", "user"))

def main():
    """Main function to run the JSON evaluation pipeline for PDA-guided generation."""
    # --- Evaluation Configuration ---
   ## just uncomment aone model and comment the other to use one ##
    MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"
#    MODEL_NAME = "google/gemma-2-2b-it"
    

    DATASET_NAME = "NousResearch/json-mode-eval"
    DATASET_SPLIT = "train"
    NUM_SAMPLES = 100


    # --- Setup ---
    print("Loading model and tokenizer...")
    tokenizer, model = load_model(MODEL_NAME)
    
    print(f"Loading dataset '{DATASET_NAME}'...")
    dataset = load_dataset(DATASET_NAME, split=DATASET_SPLIT, streaming=True)
    
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

        ##### prompt selection part, if it's better to be normal or with explicit instruction, comment out what is to be chosen #####
        

        # Option 2: Explicit Prompt (Often better for instruction-tuned models like Llama)
        explicit_instruction = "\n\nRespond with a single, valid JSON object and nothing else."
        prompt_str = prompt_str + explicit_instruction

        #######################################################################
        
        pda_gen = generate_with_pda(prompt_str, model, tokenizer, max_steps=200)
        std_gen = generate_standard(prompt_str, model, tokenizer, max_new_tokens=200)

        print("\n--- Final Comparison ---")
        print(f"[PDA Output]:\n{pda_gen}")
        print(f"[Standard Output]:\n{std_gen}")
        print(f"\n[Reference JSON]:\n{reference_completion}")
        print("=" * 70)

if __name__ == "__main__":
    main()