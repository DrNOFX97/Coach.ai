import json
import sys

def fix_jsonl(input_path, output_path):
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for i, line in enumerate(infile):
            if not line.strip():
                print(f"Skipping empty line {i+1}", file=sys.stderr)
                continue
            try:
                # Try to load the JSON to check for errors
                json.loads(line)
                # If it's valid, write it to the output
                outfile.write(line)
            except json.JSONDecodeError as e:
                print(f"Error in line {i+1}: {e}", file=sys.stderr)
                # Attempt to fix the line by escaping control characters
                fixed_line = line.replace('\n', '\\n').replace('\t', '\\t')
                try:
                    json.loads(fixed_line)
                    outfile.write(fixed_line)
                    print(f"  - Fixed and wrote line {i+1}", file=sys.stderr)
                except json.JSONDecodeError as e2:
                    print(f"  - Could not fix line {i+1}: {e2}", file=sys.stderr)

if __name__ == "__main__":
    input_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/train.jsonl"
    output_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/train_fixed.jsonl"
    fix_jsonl(input_file, output_file)