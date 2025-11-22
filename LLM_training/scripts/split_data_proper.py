#!/usr/bin/env python3
"""
Split dataset into train/validation (90/10) maintaining JSONL format.
Uses the cleaned dataset from clean_dataset.py.
"""

import json
import random
from pathlib import Path

def split_dataset(input_file, train_file, valid_file, train_ratio=0.9, seed=42):
    """
    Split JSONL dataset into train and validation sets.

    Args:
        input_file: Path to input JSONL file
        train_file: Path to output train JSONL file
        valid_file: Path to output validation JSONL file
        train_ratio: Ratio of data for training (default 0.9 = 90%)
        seed: Random seed for reproducibility
    """

    # Set random seed for reproducibility
    random.seed(seed)

    # Read all data
    print(f"[INFO] Reading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    print(f"[INFO] Total records: {len(data)}")

    # Shuffle data
    random.shuffle(data)

    # Split
    split_idx = int(len(data) * train_ratio)
    train_data = data[:split_idx]
    valid_data = data[split_idx:]

    print(f"[INFO] Train set: {len(train_data)} records ({len(train_data)/len(data)*100:.1f}%)")
    print(f"[INFO] Valid set: {len(valid_data)} records ({len(valid_data)/len(data)*100:.1f}%)")

    # Write train set
    print(f"[INFO] Writing train set to {train_file}...")
    with open(train_file, 'w', encoding='utf-8') as f:
        for record in train_data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(f"[INFO] Train set written successfully")

    # Write validation set
    print(f"[INFO] Writing validation set to {valid_file}...")
    with open(valid_file, 'w', encoding='utf-8') as f:
        for record in valid_data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(f"[INFO] Validation set written successfully")

    # Verify
    print(f"\n[INFO] Verification:")
    with open(train_file) as f:
        train_count = len(f.readlines())
        print(f"  ✓ Train file has {train_count} lines")

    with open(valid_file) as f:
        valid_count = len(f.readlines())
        print(f"  ✓ Valid file has {valid_count} lines")

    print(f"  ✓ Total: {train_count + valid_count} lines")
    print(f"[INFO] Split complete!")

if __name__ == "__main__":
    # Paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    input_file = data_dir / "farense_dataset_cleaned.jsonl"
    train_file = data_dir / "train.jsonl"
    valid_file = data_dir / "valid.jsonl"

    # Check if input file exists
    if not input_file.exists():
        print(f"[ERROR] Input file not found: {input_file}")
        print(f"[INFO] Running clean_dataset.py first...")
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from clean_dataset import clean_dataset
        clean_dataset(
            str(data_dir / "farense_dataset.jsonl"),
            str(input_file)
        )

    # Split data
    split_dataset(
        input_file=input_file,
        train_file=train_file,
        valid_file=valid_file,
        train_ratio=0.9,
        seed=42
    )
