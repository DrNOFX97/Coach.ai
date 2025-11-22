import json
import sys

def validate_jsonl(file_path):
    """
    Validates a JSONL file, checking if each line is a valid JSON object.
    """
    error_count = 0
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error in line {i+1}: {e}", file=sys.stderr)
                print(f"  -> Offending line: {line[:100]}...", file=sys.stderr)
                error_count += 1
    
    if error_count == 0:
        print(f"Validation successful: All {i+1} lines in {file_path} are valid JSON.")
    else:
        print(f"\nValidation failed: Found {error_count} invalid JSON lines in {file_path}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_jsonl.py <file_path>")
        sys.exit(1)
    
    validate_jsonl(sys.argv[1])

