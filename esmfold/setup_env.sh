#!/bin/bash

cd ~/esmfold_local

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

pip install torch torchvision torchaudio
pip install transformers accelerate sentencepiece safetensors

echo "Environment ready"
