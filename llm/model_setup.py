# llm/model_setup.py

from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_name="gpt2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()  # for inference
    return tokenizer, model
