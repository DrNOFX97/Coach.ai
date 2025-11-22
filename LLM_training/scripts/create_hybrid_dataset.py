#!/usr/bin/env python3
"""
Create Hybrid Dataset with Image References (OPÇÃO 2)
Adds image references to existing Q&A pairs based on metadata matching
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict


def load_jsonl(filepath: Path) -> List[Dict[str, Any]]:
    """Load JSONL file."""
    pairs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                pairs.append(json.loads(line))
    return pairs


def save_jsonl(pairs: List[Dict[str, Any]], filepath: Path) -> None:
    """Save JSONL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')


def extract_year_from_periodo(periodo: str) -> Optional[int]:
    """Extract year from período string."""
    if not periodo:
        return None

    # Try to parse different formats
    try:
        # Format: "YYYY" or "YYYY-MM" or "YYYY-MM-DD"
        year = int(periodo.split('-')[0])
        if 1900 <= year <= 2030:
            return year
    except (ValueError, IndexError):
        pass

    return None


def get_decade(year: int) -> str:
    """Get decade folder name from year."""
    if year < 1910:
        return "1900-1909"
    decade_start = (year // 10) * 10
    decade_end = decade_start + 9
    return f"{decade_start}-{decade_end}"


def index_available_images(photos_root: Path) -> Dict[str, List[str]]:
    """Index all available images by decade."""
    image_index = defaultdict(list)

    equipas_path = photos_root / "equipas"
    if not equipas_path.exists():
        return image_index

    # List all decades
    for decade_folder in equipas_path.iterdir():
        if not decade_folder.is_dir():
            continue

        decade_name = decade_folder.name

        # Find all image files
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.webp']:
            for image_file in decade_folder.glob(ext):
                relative_path = f"dados/fotografias/equipas/{decade_name}/{image_file.name}"
                image_index[decade_name].append(relative_path)

    return image_index


def find_matching_image(periodo: str, tipo: str, image_index: Dict[str, List[str]]) -> Optional[str]:
    """Find matching image for a Q&A pair."""
    year = extract_year_from_periodo(periodo)

    if not year:
        return None

    decade = get_decade(year)

    if decade not in image_index or not image_index[decade]:
        return None

    # Try to find image matching the year or tipo
    images = image_index[decade]

    # Priority 1: Try to match specific year in filename
    year_str = str(year)
    for img in images:
        if year_str in img:
            return img

    # Priority 2: Try to match tipo
    tipo_keywords = {
        "equipa_historica": ["equipa", "team", "squad"],
        "partido_historico": ["jogo", "match", "game"],
        "figura_historica": ["jogador", "player", "presidente"],
        "historia_campos": ["campo", "field", "stadium"],
        "historia_sedes": ["sede", "headquarters"],
    }

    if tipo in tipo_keywords:
        keywords = tipo_keywords[tipo]
        for img in images:
            img_lower = img.lower()
            for keyword in keywords:
                if keyword in img_lower:
                    return img

    # Priority 3: Return first available image from decade
    if images:
        return images[0]

    return None


def add_image_references(dataset: List[Dict[str, Any]],
                        image_index: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """Add image references to Q&A pairs."""
    enhanced_dataset = []
    matched_count = 0

    for qa_pair in dataset:
        periodo = qa_pair.get('metadata', {}).get('periodo', '')
        tipo = qa_pair.get('metadata', {}).get('tipo', '')

        matching_image = find_matching_image(periodo, tipo, image_index)

        if matching_image:
            matched_count += 1
            # Add image reference to metadata
            qa_pair['metadata']['imagem'] = matching_image

        enhanced_dataset.append(qa_pair)

    return enhanced_dataset, matched_count


def create_vision_ready_dataset(dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Create Vision Model-ready format.
    Includes image paths and descriptions for Vision models.
    """
    vision_dataset = []

    for qa_pair in dataset:
        imagem = qa_pair.get('metadata', {}).get('imagem')

        if imagem:
            # Create vision-ready variant with image context
            vision_variant = {
                "prompt": qa_pair['prompt'],
                "completion": qa_pair['completion'],
                "metadata": qa_pair['metadata'],
                "vision_ready": True,
                "image_path": imagem,
                # Add image context to prompt for vision models
                "vision_prompt": f"{qa_pair['prompt']}\n[Imagem: {imagem}]"
            }
            vision_dataset.append(vision_variant)
        else:
            # Keep text-only variants
            vision_dataset.append(qa_pair)

    return vision_dataset


def generate_statistics(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate statistics about image coverage."""
    stats = {
        "total_pairs": len(dataset),
        "pairs_with_images": 0,
        "pairs_without_images": 0,
        "image_coverage_percentage": 0.0,
        "images_by_decade": defaultdict(int),
        "images_by_tipo": defaultdict(int),
    }

    for qa_pair in dataset:
        has_image = 'imagem' in qa_pair.get('metadata', {})

        if has_image:
            stats["pairs_with_images"] += 1
            imagem = qa_pair['metadata'].get('imagem', '')

            # Extract decade from image path
            if '/' in imagem:
                parts = imagem.split('/')
                for i, part in enumerate(parts):
                    if '-' in part and part[0].isdigit():
                        stats["images_by_decade"][part] += 1
                        break

            # Count by tipo
            tipo = qa_pair.get('metadata', {}).get('tipo', 'outro')
            stats["images_by_tipo"][tipo] += 1
        else:
            stats["pairs_without_images"] += 1

    if stats["total_pairs"] > 0:
        stats["image_coverage_percentage"] = (stats["pairs_with_images"] / stats["total_pairs"]) * 100

    return stats


def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    photos_root = project_root / "dados" / "fotografias"

    print("="*80)
    print("CRIANDO DATASET HÍBRIDO COM REFERÊNCIAS A IMAGENS")
    print("="*80 + "\n")

    # Step 1: Load dataset
    print("[1/5] Carregando dataset V3 expandido...")
    dataset_file = data_dir / "farense_dataset_v3_expanded.jsonl"
    dataset = load_jsonl(dataset_file)
    print(f"  ✓ {len(dataset)} pares carregados\n")

    # Step 2: Index available images
    print("[2/5] Indexando imagens disponíveis...")
    image_index = index_available_images(photos_root)
    total_indexed_images = sum(len(imgs) for imgs in image_index.values())
    print(f"  ✓ {total_indexed_images} imagens indexadas")
    print(f"  ✓ {len(image_index)} décadas com imagens\n")

    # Step 3: Add image references
    print("[3/5] Associando imagens aos pares Q&A...")
    enhanced_dataset, matched_count = add_image_references(dataset, image_index)
    print(f"  ✓ {matched_count} pares associados com imagens")
    print(f"  ✓ Cobertura: {(matched_count/len(dataset))*100:.1f}%\n")

    # Step 4: Save hybrid dataset
    print("[4/5] Salvando dataset híbrido...")
    hybrid_output = data_dir / "farense_dataset_hybrid.jsonl"
    save_jsonl(enhanced_dataset, hybrid_output)
    print(f"  ✓ Salvo: {hybrid_output.name}\n")

    # Step 5: Generate and display statistics
    print("[5/5] Gerando estatísticas...")
    stats = generate_statistics(enhanced_dataset)

    print("\n" + "="*80)
    print("ESTATÍSTICAS DO DATASET HÍBRIDO")
    print("="*80 + "\n")

    print(f"Total de pares:              {stats['total_pairs']}")
    print(f"Pares com imagem:            {stats['pairs_with_images']} ({stats['image_coverage_percentage']:.1f}%)")
    print(f"Pares sem imagem:            {stats['pairs_without_images']}")

    print(f"\n{'─'*80}")
    print("IMAGENS POR DÉCADA:")
    print(f"{'─'*80}\n")

    for decade in sorted(stats['images_by_decade'].keys()):
        count = stats['images_by_decade'][decade]
        percentage = (count / stats['pairs_with_images']) * 100 if stats['pairs_with_images'] > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"  {decade}: {count:3d} pares ({percentage:5.1f}%) {bar}")

    print(f"\n{'─'*80}")
    print("IMAGENS POR TIPO DE CONTEÚDO:")
    print(f"{'─'*80}\n")

    top_tipos = sorted(stats['images_by_tipo'].items(), key=lambda x: x[1], reverse=True)[:10]
    for tipo, count in top_tipos:
        percentage = (count / stats['pairs_with_images']) * 100 if stats['pairs_with_images'] > 0 else 0
        print(f"  {tipo:25s}: {count:3d} pares ({percentage:5.1f}%)")

    print("\n" + "="*80)
    print("✨ DATASET HÍBRIDO PRONTO!")
    print("="*80 + "\n")

    print(f"Ficheiro: {hybrid_output.name}")
    print(f"Formato: JSONL com referências a imagens")
    print(f"Uso: Frontend carrega imagem quando 'imagem' está em metadata")


if __name__ == "__main__":
    main()
