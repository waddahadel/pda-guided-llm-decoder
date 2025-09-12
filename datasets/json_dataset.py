from datasets import load_dataset

# we load the dataset
dataset = load_dataset("NousResearch/json-mode-eval", split="train")

# I just want to look at the first few samples
for i in range(3):
    sample = dataset[i]
    print(f"\n=== Sample {i} ===")
    print("PROMPT:")
    for msg in sample["prompt"]:
        print(f"{msg['role'].upper()}: {msg['content']}")
    print("\nREFERENCE COMPLETION:")
    print(sample["completion"])
    print("\n" + "="*50)