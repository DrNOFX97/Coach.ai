#!/usr/bin/env python3
"""
Vision Chat Demo
Example of how to use Vision Models with the image-enhanced dataset

Supports:
  - Claude 3/3.5 Vision (Anthropic)
  - GPT-4V (OpenAI)
  - LLaVA (Local open-source)
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any


class VisionChatDemo:
    """Demo for Vision-based chat."""

    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()
        self.pairs_with_images = self._filter_image_pairs()

    def _load_dataset(self) -> List[Dict[str, Any]]:
        """Load dataset."""
        dataset = []
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    dataset.append(json.loads(line))
        return dataset

    def _filter_image_pairs(self) -> List[Dict[str, Any]]:
        """Get only pairs with images."""
        return [p for p in self.dataset if 'imagem' in p.get('metadata', {})]

    def format_for_claude_vision(self, qa_pair: Dict[str, Any]) -> str:
        """
        Format for Claude Vision API call.
        """
        imagem = qa_pair.get('metadata', {}).get('imagem')

        claude_call = f"""
# Claude 3.5 Vision API Call

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {{
            "role": "user",
            "content": [
                {{
                    "type": "image",
                    "source": {{
                        "type": "file",
                        "path": "{imagem}"
                    }},
                }},
                {{
                    "type": "text",
                    "text": "{qa_pair['prompt']}"
                }}
            ],
        }}
    ],
)

print(message.content[0].text)
```

**Expected Response**: {qa_pair.get('completion', 'N/A')[:200]}...
"""
        return claude_call

    def format_for_gpt4v(self, qa_pair: Dict[str, Any]) -> str:
        """
        Format for GPT-4V API call.
        """
        imagem = qa_pair.get('metadata', {}).get('imagem')

        gpt_call = f"""
# GPT-4V API Call

```python
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {{
            "role": "user",
            "content": [
                {{
                    "type": "image_url",
                    "image_url": {{
                        "url": "file://{imagem}"
                    }}
                }},
                {{
                    "type": "text",
                    "text": "{qa_pair['prompt']}"
                }}
            ]
        }}
    ],
    max_tokens=1024,
)

print(response.choices[0].message.content)
```

**Expected Response**: {qa_pair.get('completion', 'N/A')[:200]}...
"""
        return gpt_call

    def format_for_llava(self, qa_pair: Dict[str, Any]) -> str:
        """
        Format for LLaVA local model.
        """
        imagem = qa_pair.get('metadata', {}).get('imagem')

        llava_call = f"""
# LLaVA Local Model Call

```python
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image

processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf")

image = Image.open("{imagem}")
prompt = "{qa_pair['prompt']}"

inputs = processor(text=prompt, images=image, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
response = processor.decode(output[0], skip_special_tokens=True)

print(response)
```

**Expected Response**: {qa_pair.get('completion', 'N/A')[:200]}...
"""
        return llava_call

    def show_example(self, index: int = 0, model_type: str = "claude-3-vision"):
        """Show example query with Vision Model code."""
        if index >= len(self.pairs_with_images):
            print(f"Error: Index {index} out of range. Available pairs: {len(self.pairs_with_images)}")
            return

        qa_pair = self.pairs_with_images[index]

        print("\n" + "="*80)
        print(f"EXEMPLO {index + 1}/{len(self.pairs_with_images)}")
        print("="*80 + "\n")

        # Display pair info
        print(f"PERGUNTA:")
        print(f"  {qa_pair['prompt']}\n")

        imagem = qa_pair.get('metadata', {}).get('imagem')
        print(f"IMAGEM:")
        print(f"  {imagem}\n")

        periodo = qa_pair.get('metadata', {}).get('periodo')
        tipo = qa_pair.get('metadata', {}).get('tipo')
        print(f"METADATA:")
        print(f"  Período: {periodo}")
        print(f"  Tipo: {tipo}\n")

        print(f"RESPOSTA ESPERADA:")
        print(f"  {qa_pair.get('completion', 'N/A')[:300]}...\n")

        # Show API code
        if model_type == "claude-3-vision":
            print(self.format_for_claude_vision(qa_pair))
        elif model_type == "gpt-4-vision":
            print(self.format_for_gpt4v(qa_pair))
        elif model_type == "llava":
            print(self.format_for_llava(qa_pair))

    def show_all_examples(self, limit: int = 5):
        """Show multiple examples."""
        print("\n" + "="*80)
        print(f"EXEMPLOS DE PARES COM IMAGEM ({limit} de {len(self.pairs_with_images)})")
        print("="*80 + "\n")

        for i, qa_pair in enumerate(self.pairs_with_images[:limit]):
            imagem = qa_pair.get('metadata', {}).get('imagem')
            periodo = qa_pair.get('metadata', {}).get('periodo')
            tipo = qa_pair.get('metadata', {}).get('tipo')

            print(f"{i+1}. {tipo} ({periodo})")
            print(f"   Pergunta: {qa_pair['prompt'][:60]}...")
            print(f"   Imagem:   {imagem}")
            print()


def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    print("="*80)
    print("VISION CHAT DEMO")
    print("="*80 + "\n")

    # Load hybrid dataset (has image references)
    print("Carregando dataset híbrido com imagens...")
    hybrid_dataset = data_dir / "farense_dataset_hybrid.jsonl"

    demo = VisionChatDemo(hybrid_dataset)

    print(f"✓ {len(demo.dataset)} pares carregados")
    print(f"✓ {len(demo.pairs_with_images)} pares com imagens\n")

    # Show overview
    print("="*80)
    print("OVERVIEW DE PARES COM IMAGEM")
    print("="*80 + "\n")

    demo.show_all_examples(limit=10)

    # Show detailed example with Claude Vision
    print("\n" + "="*80)
    print("EXEMPLO DETALHADO COM CLAUDE 3 VISION")
    print("="*80)

    demo.show_example(index=0, model_type="claude-3-vision")

    # Show example with GPT-4V
    print("\n" + "="*80)
    print("EXEMPLO COM GPT-4V")
    print("="*80)

    if len(demo.pairs_with_images) > 1:
        demo.show_example(index=1, model_type="gpt-4-vision")

    # Show example with LLaVA
    print("\n" + "="*80)
    print("EXEMPLO COM LLAVA (LOCAL)")
    print("="*80)

    if len(demo.pairs_with_images) > 2:
        demo.show_example(index=2, model_type="llava")

    print("\n" + "="*80)
    print("PRÓXIMOS PASSOS")
    print("="*80 + "\n")

    print("1. USAR COM CLAUDE 3 VISION:")
    print("   • Instalar: pip install anthropic")
    print("   • Setup: export ANTHROPIC_API_KEY='sua-chave'")
    print("   • Usar: Claude Vision API para analisar imagens\n")

    print("2. USAR COM GPT-4V:")
    print("   • Instalar: pip install openai")
    print("   • Setup: export OPENAI_API_KEY='sua-chave'")
    print("   • Usar: GPT-4V API para analisar imagens\n")

    print("3. USAR COM LLAVA (LOCAL):")
    print("   • Instalar: pip install transformers pillow torch")
    print("   • Download model: llava-hf/llava-1.5-7b-hf")
    print("   • Usar: Modelo local sem APIs\n")

    print("="*80)
    print("✨ DEMO COMPLETO!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
