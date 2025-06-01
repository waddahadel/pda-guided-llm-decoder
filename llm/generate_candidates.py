# llm/generate_candidates.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .model_setup import load_model

def get_top_k_candidates(prompt, k=10, model_name="gpt2", device="cpu"):
    tokenizer, model = load_model(model_name)
    model.to(device)

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits[:, -1, :]  # last token logits

    top_k_probs, top_k_indices = torch.topk(logits, k, dim=-1)
    tokens = [tokenizer.decode([idx]) for idx in top_k_indices[0]]
    return tokens
