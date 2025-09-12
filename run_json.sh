#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Environment Setup ---
# We are using a Conda environment to manage dependencies.
echo "Activating Conda environment..."
source $(dirname $(dirname $(which conda)))/etc/profile.d/conda.sh
conda activate "$HOME/my_pda_env"
echo "Conda environment activated."

# --- Authentication ---
# Your Hugging Face access token.
#export HF_TOKEN="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"

echo "Installing required Python packages via pip..."
pip install -r requirements.txt --no-cache-dir

# Run the JSON evaluation using your main Python script
echo "Starting the JSON evaluation script..."
python main.py json
echo "JSON evaluation script finished."
