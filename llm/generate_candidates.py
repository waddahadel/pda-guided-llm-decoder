import torch

def get_top_k_candidates(prompt, k=10, model=None, tokenizer=None):
    if model is None or tokenizer is None:
        raise ValueError("Must provide both model and tokenizer")

    device = model.device
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits[:, -1, :]  

    top_k_probs, top_k_indices = torch.topk(logits, k, dim=-1)
    tokens = [tokenizer.decode([idx]) for idx in top_k_indices[0]]
    return tokens
