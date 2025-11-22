import json
from pathlib import Path
import sys

# Add the parent directory to the path to import from mlx_lm
sys.path.insert(0, str(Path(__file__).parent.parent))

from mlx_lm import load

def split_data(file_path: Path, tokenizer, max_seq_length: int):
    """Splits the text in a JSONL file into chunks of max_seq_length."""
    with open(file_path, "r") as f:
        data = [json.loads(line) for line in f]

    new_data = []
    for item in data:
        text = item.get("text", "")
        if not text:
            continue

        tokens = tokenizer.encode(text)
        for i in range(0, len(tokens), max_seq_length):
            chunk = tokens[i : i + max_seq_length]
            new_data.append({"text": tokenizer.decode(chunk)})

    with open(file_path, "w") as f:
        for item in new_data:
            f.write(json.dumps(item) + "\n")

def main():
    """Main function to split the data."""
    project_root = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training")
    data_dir = project_root / "data"
    model_path = project_root / "models/mistral-7b-4bit"
    max_seq_length = 256

    print("[INFO] Loading tokenizer...", file=sys.stderr)
    _, tokenizer = load(str(model_path))
    print("[INFO] Tokenizer loaded.", file=sys.stderr)

    print("[INFO] Splitting train.jsonl...", file=sys.stderr)
    split_data(data_dir / "train.jsonl", tokenizer, max_seq_length)
    print("[INFO] train.jsonl split.", file=sys.stderr)

    print("[INFO] Splitting valid.jsonl...", file=sys.stderr)
    split_data(data_dir / "valid.jsonl", tokenizer, max_seq_length)
    print("[INFO] valid.jsonl split.", file=sys.stderr)

if __name__ == "__main__":
    main()
