#!/bin/bash

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete! To activate the environment in the future, run:"
echo "source venv/bin/activate"
echo ""
echo "Then you can run:"
echo "python main.py"