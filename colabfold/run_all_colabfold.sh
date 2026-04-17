#!/bin/bash

echo "Starting ColabFold batch run..."

export TF_FORCE_UNIFIED_MEMORY=1
export XLA_PYTHON_CLIENT_MEM_FRACTION=4.0
export TF_FORCE_GPU_ALLOW_GROWTH=true

for f in Similar/*.fasta Novel/*.fasta; do
  name=$(basename "$f" .fasta)

  if [ ! -d "results_$name" ]; then
    echo "Running $name..."
    colabfold_batch --num-recycle 2 "$f" "results_$name"
  else
    echo "Skipping $name (already exists)"
  fi
done

echo "All jobs finished!"
