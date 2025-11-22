#!/usr/bin/env python3
"""
Combinar todos os datasets:
1. Dataset original (farense_dataset_v2.jsonl com biografias) - 953 exemplos
2. Dataset dos livros (livros_qa_final_consolidated.jsonl) - 159 exemplos
   - livro_scf_1.txt: 89 pares
   - 50 anos de História do Futebol em Faro.docx: 70 pares
   Inclui:
   - livros_qa_all.jsonl: 65 pares (original)
   - livros_qa_docx_50anos.jsonl: 30 pares (DOCX basic)
   - livros_qa_advanced.jsonl: 40 pares (DOCX advanced)
   - livros_qa_narratives.jsonl: 24 pares (TXT narratives)
= Dataset V3 Expandido (farense_dataset_v3_expanded.jsonl) - 1112 exemplos

Criar novo split 90/10 com seed=42
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any

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

def main():
    """Main function to combine datasets."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    print("📊 COMBINANDO DATASETS - VERSÃO V3\n")
    print("="*80)

    # Load existing dataset (v2 with biographies)
    print("\n[1/3] Carregando dataset v2 (com biografias)...")
    v2_file = data_dir / "farense_dataset_v2.jsonl"
    dataset_v2 = load_jsonl(v2_file)
    print(f"  ✓ {len(dataset_v2)} exemplos carregados")

    # Load books dataset
    print("\n[2/3] Carregando dataset dos livros (final consolidado)...")
    books_file = data_dir / "livros_qa_final_consolidated.jsonl"
    dataset_books = load_jsonl(books_file)
    print(f"  ✓ {len(dataset_books)} exemplos carregados")

    # Combine datasets
    print("\n[3/3] Combinando datasets...")
    dataset_v3 = dataset_v2 + dataset_books
    print(f"  ✓ {len(dataset_v3)} exemplos no total")

    print("\n" + "="*80)
    print("\n📈 RESUMO DA COMBINAÇÃO:\n")
    print(f"  Dataset V2 (original + biografias):  {len(dataset_v2):4d}")
    print(f"  Dataset Livros:                      {len(dataset_books):4d}")
    print(f"  ─────────────────────────────────────────")
    print(f"  Dataset V3 (total):                  {len(dataset_v3):4d}")
    print(f"  Aumento:                             {len(dataset_books)} exemplos")

    # Save combined dataset
    output_file = data_dir / "farense_dataset_v3_expanded.jsonl"
    save_jsonl(dataset_v3, output_file)
    print(f"\n✅ Dataset combinado salvo: {output_file.name}")

    # Split into train/validation (90/10)
    print("\n" + "="*80)
    print("\n🔄 CRIANDO SPLIT TRAIN/VALIDATION (90/10)...\n")

    random.seed(42)
    random.shuffle(dataset_v3)

    split_idx = int(len(dataset_v3) * 0.9)
    train_data = dataset_v3[:split_idx]
    valid_data = dataset_v3[split_idx:]

    # Save train dataset
    train_file = data_dir / "train_v3_expanded.jsonl"
    save_jsonl(train_data, train_file)
    print(f"  ✓ Train:      {len(train_data)} exemplos ({len(train_data)/len(dataset_v3)*100:.1f}%)")

    # Save validation dataset
    valid_file = data_dir / "valid_v3_expanded.jsonl"
    save_jsonl(valid_data, valid_file)
    print(f"  ✓ Validation: {len(valid_data)} exemplos ({len(valid_data)/len(dataset_v3)*100:.1f}%)")

    print(f"\n✅ Ficheiros salvos:")
    print(f"  - {train_file.name}")
    print(f"  - {valid_file.name}")

    # Analyze distribution
    print("\n" + "="*80)
    print("\n📊 ANÁLISE DE TIPOS DE DADOS (Dataset V3):\n")

    tipo_counts = {}
    for pair in dataset_v3:
        tipo = pair.get('metadata', {}).get('tipo', 'outro')
        tipo_counts[tipo] = tipo_counts.get(tipo, 0) + 1

    # Sort by count
    sorted_tipos = sorted(tipo_counts.items(), key=lambda x: x[1], reverse=True)

    for tipo, count in sorted_tipos:
        percentage = count / len(dataset_v3) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"  {tipo:25s} {count:4d} ({percentage:5.2f}%) {bar}")

    print("\n" + "="*80)
    print("\n📊 ESTATÍSTICAS FINAIS:\n")
    print(f"  Total de Exemplos:      {len(dataset_v3):4d}")
    print(f"  Treino (90%):           {len(train_data):4d}")
    print(f"  Validação (10%):        {len(valid_data):4d}")
    print(f"  Tipos Diferentes:       {len(tipo_counts):4d}")
    print(f"  Seed (reproducibilidade): 42")

    print("\n" + "="*80)
    print("\n✨ Dataset V3 pronto para treino!\n")

if __name__ == "__main__":
    main()
