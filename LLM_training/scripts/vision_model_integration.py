#!/usr/bin/env python3
"""
Vision Model Integration (OPÇÃO 1)
Support for multimodal vision-language models

Compatible with:
  - Claude 3/3.5 Vision (Anthropic)
  - GPT-4V (OpenAI)
  - LLaVA (Open source)
  - Gemini Vision (Google)
"""

import json
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import hashlib


@dataclass
class VisionModelConfig:
    """Configuration for Vision Models."""
    model_name: str
    supports_image_urls: bool = True
    supports_base64: bool = True
    supports_local_paths: bool = True
    max_image_size_mb: float = 20.0
    supported_formats: List[str] = None

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["png", "jpg", "jpeg", "webp", "gif"]


# Predefined configurations for popular models
VISION_MODELS = {
    "claude-3-vision": VisionModelConfig(
        model_name="claude-3-5-sonnet-20241022",
        supports_image_urls=True,
        supports_base64=True,
        supports_local_paths=True,
        max_image_size_mb=20.0
    ),
    "gpt-4-vision": VisionModelConfig(
        model_name="gpt-4-vision-preview",
        supports_image_urls=True,
        supports_base64=True,
        supports_local_paths=False,
        max_image_size_mb=20.0
    ),
    "llava": VisionModelConfig(
        model_name="llava-1.5-7b-hf",
        supports_image_urls=True,
        supports_base64=True,
        supports_local_paths=True,
        max_image_size_mb=10.0
    ),
    "gemini-vision": VisionModelConfig(
        model_name="gemini-pro-vision",
        supports_image_urls=True,
        supports_base64=True,
        supports_local_paths=True,
        max_image_size_mb=20.0
    ),
}


class VisionDatasetBuilder:
    """Build datasets optimized for vision models."""

    def __init__(self, base_dataset_path: Path, photos_root: Path):
        self.base_dataset_path = base_dataset_path
        self.photos_root = photos_root
        self.dataset = self._load_dataset()

    def _load_dataset(self) -> List[Dict[str, Any]]:
        """Load base dataset."""
        dataset = []
        with open(self.base_dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    dataset.append(json.loads(line))
        return dataset

    def _create_vision_prompt(self, prompt: str, imagem: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a vision-compatible prompt.

        Formats:
          - Claude 3: Uses image block with content
          - GPT-4V: Uses image_url in content array
          - LLaVA: Uses image token placeholders
        """
        if not imagem:
            return {"type": "text", "text": prompt}

        return {
            "type": "image_and_text",
            "text": prompt,
            "image_path": imagem
        }

    def create_claude_vision_format(self, qa_pair: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format for Claude 3 Vision API.

        Example:
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "file",
                "media_type": "image/jpeg",
                "data": "<base64-encoded data>"
              }
            },
            {
              "type": "text",
              "text": "Pergunta aqui"
            }
          ]
        }
        """
        imagem = qa_pair.get('metadata', {}).get('imagem')

        content = []

        # Add image if available
        if imagem:
            img_path = self.photos_root.parent / imagem
            if img_path.exists():
                content.append({
                    "type": "image",
                    "source": {
                        "type": "file",
                        "path": str(img_path)
                    }
                })

        # Add text prompt
        content.append({
            "type": "text",
            "text": qa_pair['prompt']
        })

        return {
            "role": "user",
            "content": content,
            "metadata": qa_pair.get('metadata', {}),
            "expected_response": qa_pair.get('completion')
        }

    def create_gpt4v_format(self, qa_pair: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format for GPT-4V API.

        Example:
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": "https://example.com/image.jpg"
              }
            },
            {
              "type": "text",
              "text": "Pergunta aqui"
            }
          ]
        }
        """
        imagem = qa_pair.get('metadata', {}).get('imagem')

        content = []

        # Add image if available (requires URL or base64)
        if imagem:
            # For local paths, we'd need to serve or encode as base64
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"file://{imagem}",
                    "detail": "high"
                }
            })

        # Add text prompt
        content.append({
            "type": "text",
            "text": qa_pair['prompt']
        })

        return {
            "role": "user",
            "content": content,
            "metadata": qa_pair.get('metadata', {}),
            "expected_response": qa_pair.get('completion')
        }

    def create_llava_format(self, qa_pair: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format for LLaVA (local open-source model).

        Example:
        {
          "image": "path/to/image.jpg",
          "text": "Pergunta aqui",
          "prompt_type": "image_captioning"
        }
        """
        imagem = qa_pair.get('metadata', {}).get('imagem')

        return {
            "image": imagem if imagem else None,
            "text": qa_pair['prompt'],
            "completion": qa_pair.get('completion'),
            "metadata": qa_pair.get('metadata', {}),
            "model_type": "llava"
        }

    def create_vision_dataset(self, model_type: str = "claude-3-vision") -> List[Dict[str, Any]]:
        """Create dataset for specific vision model."""
        vision_dataset = []

        formatters = {
            "claude-3-vision": self.create_claude_vision_format,
            "gpt-4-vision": self.create_gpt4v_format,
            "llava": self.create_llava_format,
        }

        formatter = formatters.get(model_type, self.create_claude_vision_format)

        for qa_pair in self.dataset:
            # Only include pairs with images for vision training
            if 'imagem' in qa_pair.get('metadata', {}):
                vision_pair = formatter(qa_pair)
                vision_dataset.append(vision_pair)

        return vision_dataset

    def create_multimodal_dataset(self) -> List[Dict[str, Any]]:
        """
        Create universal multimodal dataset compatible with multiple vision models.
        """
        multimodal_dataset = []

        for qa_pair in self.dataset:
            imagem = qa_pair.get('metadata', {}).get('imagem')

            multimodal_pair = {
                "prompt": qa_pair['prompt'],
                "completion": qa_pair.get('completion'),
                "metadata": qa_pair.get('metadata', {}),
                "multimodal": {
                    "image": imagem if imagem else None,
                    "image_full_path": str(self.photos_root.parent / imagem) if imagem else None,
                    "has_image": bool(imagem),
                    "formats": {
                        "claude": self.create_claude_vision_format(qa_pair),
                        "gpt4v": self.create_gpt4v_format(qa_pair),
                        "llava": self.create_llava_format(qa_pair)
                    }
                }
            }

            multimodal_dataset.append(multimodal_pair)

        return multimodal_dataset


def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    photos_root = project_root / "dados" / "fotografias"

    print("="*80)
    print("INTEGRÇÃO DE MODELOS DE VISÃO")
    print("="*80 + "\n")

    # Initialize builder
    print("[1/4] Inicializando construtor de dataset...")
    hybrid_dataset_path = data_dir / "farense_dataset_hybrid.jsonl"
    builder = VisionDatasetBuilder(hybrid_dataset_path, photos_root)
    print(f"  ✓ {len(builder.dataset)} pares carregados\n")

    # Create datasets for different models
    print("[2/4] Criando datasets para diferentes modelos...\n")

    for model_type in ["claude-3-vision", "gpt-4-vision", "llava"]:
        print(f"  • Criando para {model_type}...")
        model_dataset = builder.create_vision_dataset(model_type)

        output_file = data_dir / f"farense_dataset_vision_{model_type}.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for pair in model_dataset:
                f.write(json.dumps(pair, ensure_ascii=False) + '\n')

        print(f"    ✓ {len(model_dataset)} pares salvos em {output_file.name}")

    print()

    # Create universal multimodal dataset
    print("[3/4] Criando dataset multimodal universal...")
    multimodal_dataset = builder.create_multimodal_dataset()

    multimodal_output = data_dir / "farense_dataset_multimodal.jsonl"
    with open(multimodal_output, 'w', encoding='utf-8') as f:
        for pair in multimodal_dataset:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"  ✓ {len(multimodal_dataset)} pares salvos em {multimodal_output.name}\n")

    # Print statistics
    print("[4/4] Gerando estatísticas...\n")

    print("="*80)
    print("ESTATÍSTICAS DOS DATASETS DE VISÃO")
    print("="*80 + "\n")

    image_count = sum(1 for p in builder.dataset if 'imagem' in p.get('metadata', {}))
    print(f"Total de pares (base):            {len(builder.dataset)}")
    print(f"Pares com imagens:                {image_count}")
    print(f"Cobertura:                        {(image_count/len(builder.dataset))*100:.1f}%\n")

    print("DATASETS CRIADOS:")
    print("─" * 80)
    print(f"  1. farense_dataset_vision_claude-3-vision.jsonl")
    print(f"     → Otimizado para Claude 3/3.5 Vision (Anthropic)")
    print(f"  2. farense_dataset_vision_gpt-4-vision.jsonl")
    print(f"     → Otimizado para GPT-4V (OpenAI)")
    print(f"  3. farense_dataset_vision_llava.jsonl")
    print(f"     → Otimizado para LLaVA (Open-source local)")
    print(f"  4. farense_dataset_multimodal.jsonl")
    print(f"     → Universal (compatible com todos)")

    print("\n" + "="*80)
    print("✨ DATASETS DE VISÃO PRONTOS!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
