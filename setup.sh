#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install the package in development mode
pip install -e .

echo "Setup complete! To activate the virtual environment, run: source venv/bin/activate" 