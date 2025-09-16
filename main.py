import sys
import torch

from evaluation.json_evaluation import main as run_json_evaluation

def main():
    """
    Main entry point for the thesis project.
    
    This script runs the PDA-augmented generation evaluation for JSON.
    """
    print("--- Starting JSON Evaluation ---")
    run_json_evaluation() 
    print("--- JSON Evaluation Finished ---")

if __name__ == "__main__":
    main()