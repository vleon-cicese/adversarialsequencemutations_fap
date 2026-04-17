#!/usr/bin/env python3

import gc
import os
import re
import sys
import traceback

import torch
from transformers import AutoTokenizer, EsmForProteinFolding


def read_fasta(path: str):
    entries = []
    header = None
    seq_parts = []

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    sequence = "".join(seq_parts).upper()
                    if sequence:
                        entries.append((header, sequence))
                header = line[1:].strip()
                seq_parts = []
            else:
                seq_parts.append(line)

    if header is not None:
        sequence = "".join(seq_parts).upper()
        if sequence:
            entries.append((header, sequence))

    return entries


def safe_name(text: str) -> str:
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.-]", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unnamed"


def sanitize_sequence(seq: str) -> str:
    seq = re.sub(r"\s+", "", seq).upper()
    allowed = set("ACDEFGHIKLMNPQRSTVWYBXZUO")
    return "".join(ch for ch in seq if ch in allowed)


def write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text if text.endswith("\n") else text + "\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python run_esmfold.py input.fasta output_dir")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    entries = read_fasta(input_fasta)
    if not entries:
        print(f"No FASTA entries found in {input_fasta}")
        sys.exit(1)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("facebook/esmfold_v1")

    print("Loading model on CPU...")
    model = EsmForProteinFolding.from_pretrained(
        "facebook/esmfold_v1",
        low_cpu_mem_usage=True
    )
    model.eval()
    model.trunk.set_chunk_size(16)

    success = 0
    failed = 0

    for i, (header, raw_sequence) in enumerate(entries, start=1):
        name = safe_name(header)
        out_pdb = os.path.join(output_dir, f"{name}.pdb")
        done_file = os.path.join(output_dir, f"{name}.done.txt")
        fail_file = os.path.join(output_dir, f"{name}.failed.txt")

        if os.path.isfile(out_pdb) and os.path.isfile(done_file):
            print(f"[{i}/{len(entries)}] Skipping {name} (already done)")
            continue

        sequence = sanitize_sequence(raw_sequence)
        if not sequence:
            failed += 1
            write_text(fail_file, "Sequence became empty after sanitization")
            print(f"[{i}/{len(entries)}] FAILED {name}: empty sequence")
            continue

        print(f"[{i}/{len(entries)}] Running {name} (len={len(sequence)})")

        try:
            inputs = tokenizer(
                [sequence],
                return_tensors="pt",
                add_special_tokens=False,
            )

            with torch.no_grad():
                output = model(**inputs, num_recycles=1)

            pdb_list = model.output_to_pdb(output)
            if not pdb_list or not pdb_list[0]:
                raise ValueError("Empty PDB output")

            with open(out_pdb, "w", encoding="utf-8") as f:
                f.write(pdb_list[0])

            write_text(done_file, f"OK\t{name}\tlen={len(sequence)}")
            success += 1
            print(f"[{i}/{len(entries)}] Saved {out_pdb}")

        except Exception as e:
            failed += 1
            err = (
                f"FAILED {name}\n"
                f"Sequence length: {len(sequence)}\n"
                f"Exception: {type(e).__name__}: {e}\n\n"
                f"{traceback.format_exc()}"
            )
            write_text(fail_file, err)
            print(f"[{i}/{len(entries)}] FAILED {name}: {type(e).__name__}: {e}")
            gc.collect()
            continue

    print(f"DONE. Success={success}, Failed={failed}")


if __name__ == "__main__":
    main()
