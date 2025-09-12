import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def load_model(model_name="google/gemma-2-2b"):
    """
    Loads the HuggingFace model and tokenizer with 4-bit quantization
    to ensure it fits on GPUs with limited VRAM.

    This uses the bitsandbytes library to significantly reduce the memory
    footprint of the model, making it ideal for cluster environments.
    """
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading model on device: {device}")
    if device == "cpu":
        print("--- WARNING: No GPU detected. Performance will be slow. ---")

   
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map="auto",
    )

    model.eval()
    return tokenizer, model
