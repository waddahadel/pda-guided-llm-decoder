# Use official Python slim image as base
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy your project code into the container
COPY . /app

# Upgrade pip and install required Python packages
RUN pip install --upgrade pip
RUN pip install transformers>=4.0.0 datasets torch>=1.10.0 huggingface_hub tqdm numpy

# Default command to run when container starts; can be overridden in submit file
CMD ["python", "main sql"]
