import argparse
import sys
import torch # Import torch here

# --- Project-level Imports ---
from evaluation.sql_evaluation import main as run_sql_evaluation
from evaluation.json_evaluation import main as run_json_evaluation
# --- MODIFIED ---
# Import the main function from the new Go evaluation script.
from evaluation.evaluate_go import main as run_go_evaluation

def main():
    """
    Main entry point for the thesis project.
    
    This script uses command-line arguments to select and run the desired
    language evaluation (e.g., for SQL, JSON, or Go).
    """
    # Set up the argument parser to handle command-line inputs.
    parser = argparse.ArgumentParser(
        description="Run PDA-augmented generation evaluations for a specified language."
    )
    
    # Define the 'language' argument, which is required.
    parser.add_argument(
        "language",
        type=str,
        # --- MODIFIED ---
        # Add 'go' to the list of available choices.
        choices=["sql", "json", "go"],
        help="The language grammar to evaluate ('sql', 'json', or 'go')."
    )
    
    # Parse the arguments provided by the user.
    args = parser.parse_args()

    # Execute the corresponding evaluation function based on the user's choice.
    if args.language == "sql":
        print("--- Starting SQL Evaluation ---")
        run_sql_evaluation()
        print("--- SQL Evaluation Finished ---")
    elif args.language == "json":
        print("--- Starting JSON Evaluation ---")
        run_json_evaluation() 
        print("--- JSON Evaluation Finished ---")
    # --- MODIFIED ---
    # Add the case for running the Go evaluation.
    elif args.language == "go":
        print("--- Starting Go Evaluation ---")
        run_go_evaluation()
        print("--- Go Evaluation Finished ---")

if __name__ == "__main__":
    main()