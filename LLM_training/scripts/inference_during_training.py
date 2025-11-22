#!/usr/bin/env python3
"""
Inference Script for Farense Bot During Training
Permite fazer inferências com o modelo em treinamento (checkpoints actuais)

Usage:
    python scripts/inference_during_training.py "Qual foi a melhor classificação do Farense?"

    # Com adapter path customizado:
    python scripts/inference_during_training.py "Pergunta" --adapter-path checkpoints_qlora/adapters
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from mlx_lm import load, generate
except ImportError:
    print("Error: mlx-lm not installed. Run: pip install mlx mlx-lm", file=sys.stderr)
    sys.exit(1)

# Configuration
BASE_DIR = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training")
BASE_MODEL = str(BASE_DIR / "models/mistral-7b-4bit")
DEFAULT_ADAPTER_PATH = str(BASE_DIR / "checkpoints_qlora/adapters")
MAX_TOKENS = 200

def load_model(adapter_path=None):
    """Load model with QLoRA adapter (if available)"""
    adapter_path = adapter_path or DEFAULT_ADAPTER_PATH

    print(f"[INFO] Base model: {BASE_MODEL}", file=sys.stderr)
    print(f"[INFO] Adapter path: {adapter_path}", file=sys.stderr)

    try:
        adapter_path_obj = Path(adapter_path)

        if adapter_path_obj.exists():
            print(f"[INFO] Loading model com adapter...", file=sys.stderr)
            model, tokenizer = load(
                BASE_MODEL,
                adapter_path=adapter_path
            )
            print(f"[OK] Model loaded with QLoRA adapters", file=sys.stderr)
            return model, tokenizer, True
        else:
            print(f"[WARN] Adapter path não existe: {adapter_path}", file=sys.stderr)
            print(f"[INFO] Loading base model sem adapters...", file=sys.stderr)
            model, tokenizer = load(BASE_MODEL)
            print(f"[OK] Base model loaded (sem fine-tuning ainda)", file=sys.stderr)
            return model, tokenizer, False

    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}", file=sys.stderr)
        raise

def format_prompt(prompt):
    """Format prompt in Farense style"""
    return f"""### Pergunta:
{prompt}

### Resposta:"""

def generate_response(model, tokenizer, prompt, max_tokens=MAX_TOKENS):
    """Generate response for the given prompt"""
    formatted_prompt = format_prompt(prompt)

    print(f"[INFO] Gerando resposta...", file=sys.stderr)

    try:
        response = generate(
            model,
            tokenizer,
            prompt=formatted_prompt,
            max_tokens=max_tokens,
            verbose=False
        )
        # Remove the prompt from response
        response = response.replace(formatted_prompt, "").strip()
        return response

    except Exception as e:
        print(f"[ERROR] Generation failed: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Inference com modelo em treinamento",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/inference_during_training.py "Quem foi Hassan Nader?"
  python scripts/inference_during_training.py "Qual foi o melhor resultado?" --adapter-path checkpoints_qlora/adapters
  python scripts/inference_during_training.py "Quando foi fundado o Farense?" --max-tokens 300
        """
    )

    parser.add_argument("prompt", help="Pergunta para o modelo")
    parser.add_argument(
        "--adapter-path",
        default=DEFAULT_ADAPTER_PATH,
        help=f"Caminho aos adapters (default: {DEFAULT_ADAPTER_PATH})"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=MAX_TOKENS,
        help=f"Tokens máximos (default: {MAX_TOKENS})"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output em formato JSON"
    )

    args = parser.parse_args()

    prompt = args.prompt
    adapter_path = args.adapter_path
    max_tokens = args.max_tokens

    try:
        # Load model
        model, tokenizer, has_adapter = load_model(adapter_path)

        # Generate response
        response = generate_response(model, tokenizer, prompt, max_tokens)

        if response:
            if args.json:
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "prompt": prompt,
                    "response": response,
                    "model": "Mistral-7B (INT4)",
                    "adapter": "LoRA" if has_adapter else "None",
                    "status": "success"
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n📋 PERGUNTA:")
                print(f"   {prompt}\n")
                print(f"💬 RESPOSTA:")
                print(f"   {response}\n")
                print(f"ℹ️  Modelo: {'Mistral-7B com LoRA' if has_adapter else 'Mistral-7B Base'}")
        else:
            if args.json:
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "prompt": prompt,
                    "error": "Failed to generate response",
                    "status": "error"
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n❌ Erro ao gerar resposta", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        if args.json:
            result = {
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "error": str(e),
                "status": "error"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
