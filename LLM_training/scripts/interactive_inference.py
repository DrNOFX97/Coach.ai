#!/usr/bin/env python3
"""
Interactive Inference Console for Farense Bot
Permite conversa contínua com o modelo durante o treino

Usage:
    python scripts/interactive_inference.py
    python scripts/interactive_inference.py --adapter-path checkpoints_qlora/adapters
"""

import sys
import json
from pathlib import Path
from datetime import datetime

try:
    from mlx_lm import load, generate
    import mlx.core as mx
except ImportError:
    print("Error: mlx-lm not installed. Run: pip install mlx mlx-lm", file=sys.stderr)
    sys.exit(1)

# Configuration
BASE_DIR = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training")
BASE_MODEL = str(BASE_DIR / "models/mistral-7b-4bit")
DEFAULT_ADAPTER_PATH = str(BASE_DIR / "checkpoints_qlora/adapters")
MAX_TOKENS = 200

class FarenseBot:
    def __init__(self, adapter_path=None):
        self.adapter_path = adapter_path or DEFAULT_ADAPTER_PATH
        self.model = None
        self.tokenizer = None
        self.has_adapter = False
        self.load_model()

    def load_model(self):
        """Load model with adapter"""
        print(f"\n🔄 Carregando modelo...", file=sys.stderr)
        print(f"   Base: {BASE_MODEL}", file=sys.stderr)
        print(f"   Adapter: {self.adapter_path}", file=sys.stderr)

        try:
            adapter_path_obj = Path(self.adapter_path)

            if adapter_path_obj.exists():
                print(f"   ✅ Adapter encontrado", file=sys.stderr)
                self.model, self.tokenizer = load(
                    BASE_MODEL,
                    adapter_path=self.adapter_path
                )
                self.has_adapter = True
                print(f"✅ Modelo carregado com LoRA adapters\n", file=sys.stderr)
            else:
                print(f"   ⚠️  Adapter não encontrado", file=sys.stderr)
                self.model, self.tokenizer = load(BASE_MODEL)
                self.has_adapter = False
                print(f"⚠️  Modelo carregado em versão base (sem fine-tuning ainda)\n", file=sys.stderr)

        except Exception as e:
            print(f"❌ Erro ao carregar: {e}", file=sys.stderr)
            raise

    def format_prompt(self, user_input):
        """Format prompt"""
        return f"""### Pergunta:
{user_input}

### Resposta:"""

    def generate_response(self, user_input, max_tokens=MAX_TOKENS):
        """Generate response"""
        formatted_prompt = self.format_prompt(user_input)

        try:
            response = generate(
                self.model,
                self.tokenizer,
                prompt=formatted_prompt,
                max_tokens=max_tokens,
                verbose=False
            )
            # Remove prompt from response
            response = response.replace(formatted_prompt, "").strip()
            return response

        except Exception as e:
            print(f"❌ Erro ao gerar: {e}", file=sys.stderr)
            return None

    def chat(self):
        """Interactive chat loop"""
        print("\n" + "="*80)
        print("🤖 FARENSE BOT - MODO INTERATIVO")
        print("="*80)
        print(f"\nModelo: {'Mistral-7B com LoRA' if self.has_adapter else 'Mistral-7B Base'}")
        print(f"Device: {mx.default_device()}")
        print(f"\nDigite 'sair' para terminar\n")

        conversation_count = 0

        while True:
            try:
                user_input = input("📝 Você: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                    print(f"\n👋 Até logo! ({conversation_count} conversas)")
                    break

                print(f"\n🤔 Processando...", end='', flush=True)
                response = self.generate_response(user_input)
                print(f"\r               \r", end='', flush=True)  # Clear "Processando..."

                if response:
                    print(f"🤖 Farense: {response}\n")
                    conversation_count += 1
                else:
                    print(f"❌ Falha ao gerar resposta\n")

            except KeyboardInterrupt:
                print(f"\n\n👋 Interrompido! ({conversation_count} conversas)")
                break
            except Exception as e:
                print(f"❌ Erro: {e}\n")

        print("\n" + "="*80)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Interactive inference com Farense Bot"
    )
    parser.add_argument(
        "--adapter-path",
        default=DEFAULT_ADAPTER_PATH,
        help=f"Caminho aos adapters (default: {DEFAULT_ADAPTER_PATH})"
    )

    args = parser.parse_args()

    try:
        bot = FarenseBot(adapter_path=args.adapter_path)
        bot.chat()
    except Exception as e:
        print(f"❌ Erro fatal: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
