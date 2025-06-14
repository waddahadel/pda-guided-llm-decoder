from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_name="google/gemma-2-2b"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",  # or torch.float16
        device_map="auto",   # handles multi-GPU or CPU fallback
    )
    model.eval()
    return tokenizer, model
