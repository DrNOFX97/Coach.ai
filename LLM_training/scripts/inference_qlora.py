#!/usr/bin/env python3
"""
QLoRA Inference Script for Mistral-7B - Farense Bot
Otimizado para Mac M1 com MLX

Usage:
    python scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
"""

import sys
import json
from pathlib import Path

try:
    from mlx_lm import load, generate
except ImportError:
    print("Error: mlx-lm not installed. Run: pip install mlx mlx-lm", file=sys.stderr)
    sys.exit(1)

# Configuration
BASE_MODEL = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/models/mistral-7b-4bit"
ADAPTER_PATH = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/checkpoints/adapters"
MAX_TOKENS = 200
QUANTIZATION = "int4"

def load_model():
    """Load model with QLoRA adapter and INT4 quantization"""
    print("[INFO] Loading QLoRA model with INT4 quantization...", file=sys.stderr)
    try:
        model, tokenizer = load(
            BASE_MODEL,
            adapter_path=ADAPTER_PATH
        )
        print("[OK] QLoRA model loaded successfully", file=sys.stderr)
        return model, tokenizer
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}", file=sys.stderr)
        raise

def generate_response(model, tokenizer, prompt):
    """Generate response for the given prompt"""
    print(f"[INFO] Processing: {prompt[:50]}...", file=sys.stderr)

    try:
        response = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=MAX_TOKENS,
            verbose=False
        )
        return response
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}", file=sys.stderr)
        return None

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        result = {
            "error": "Usage: python inference_qlora.py 'prompt'",
            "status": "error"
        }
        print(json.dumps(result))
        sys.exit(1)

    prompt = sys.argv[1]

    try:
        model, tokenizer = load_model()
        response = generate_response(model, tokenizer, prompt)

        if response:
            result = {
                "prompt": prompt,
                "response": response,
                "method": "QLoRA",
                "quantization": "int4",
                "status": "success"
            }
        else:
            result = {
                "prompt": prompt,
                "error": "Failed to generate response",
                "method": "QLoRA",
                "status": "error"
            }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        result = {
            "prompt": prompt,
            "error": str(e),
            "method": "QLoRA",
            "status": "error"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
