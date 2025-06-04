# run_demo.py

from controlled_generation import generate_valid_json

if __name__ == "__main__":
    initial_prompt =  "Generate a JSON object representing Germany, with only three keys:\n{" # Start from an opening brace
    final_output = generate_valid_json(prompt=initial_prompt)
    print("\nFinal JSON output:\n", final_output)
