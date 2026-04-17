#!/usr/bin/env bash
set -Eeuo pipefail

cd "$HOME/esmfold_local"
source .venv/bin/activate

mkdir -p esm_results
mkdir -p logs

run_one() {
  local fasta="$1"
  local name
  name="$(basename "$fasta" .fasta)"
  local outdir="$HOME/esmfold_local/esm_results/$name"
  local logfile="$HOME/esmfold_local/logs/${name}.log"

  mkdir -p "$outdir"

  echo "Running $name"
  python run_esmfold.py "$fasta" "$outdir" >"$logfile" 2>&1 || true
  echo "Finished $name"
}

for f in Similar/*.fasta Novel/*.fasta; do
  [ -e "$f" ] || continue
  run_one "$f"
done

echo "ALL DONE"
