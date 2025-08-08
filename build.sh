#!/bin/bash

cd src

npx prettier . --write

# Step 1: Change to /builder
cd ../builder || { echo "Failed to change directory to /builder"; exit 1; }

# Step 2: Run builder.py (assuming Python 3)
python3 builder.py || { echo "builder.py failed to run"; exit 1; }

# Step 3: Change to ../dist
cd ../dist || { echo "Failed to change directory to ../dist"; exit 1; }

npx prettier . --write
