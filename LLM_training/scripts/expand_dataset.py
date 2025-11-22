#!/usr/bin/env python3
"""
Expand dataset by generating new Q&A pairs from additional sources.
Sources:
  1. resultados_completos.md - Complete game results
  2. presidentes.txt - List of presidents
  3. estatutos_scf_1924.md - Club bylaws (1924)
  4. Bio files - Player and staff biographies
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

def extract_results_qa(results_md: str) -> List[Dict[str, Any]]:
    """Extract Q&A pairs from complete results markdown."""
    qa_pairs = []

    # Find all match results in markdown table format
    # Pattern: | Jornada | Data | Jogo | Resultado |
    lines = results_md.split('\n')

    current_epoch = None

    for i, line in enumerate(lines):
        # Detect epoch headers (### Epoch 1, ### Época, etc.)
        if line.startswith('###') and ('Época' in line or 'época' in line or 'Jogos' in line):
            current_epoch = line.replace('#', '').strip()

        # Look for table rows with match data
        if '|' in line and 'Jogo' not in line and 'Data' not in line and current_epoch:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                try:
                    data = parts[2] if len(parts[2]) > 5 else None
                    jogo = parts[3]
                    resultado = parts[4]

                    if jogo and resultado and data:
                        # Parse match info
                        if '**' in jogo:  # Contains score
                            # Generate Q&A pairs
                            qa_pairs.extend(_generate_match_qa(jogo, data, current_epoch))
                except:
                    continue

    return qa_pairs

def _generate_match_qa(jogo: str, data: str, epoch: str) -> List[Dict[str, Any]]:
    """Generate Q&A pairs from a match description."""
    pairs = []

    # Clean up the jogo string
    jogo_clean = jogo.replace('**', '').strip()

    # Try to extract teams and score
    # Pattern: "Team A X - Y Team B"
    match_pattern = r'(.+?)\s+(\d+)\s*-\s*(\d+)\s+(.+)'
    m = re.search(match_pattern, jogo_clean)

    if m:
        team_a = m.group(1).strip()
        score_a = m.group(2)
        score_b = m.group(3)
        team_b = m.group(4).strip()

        # Determine if it was home or away
        is_home = 'SC Farense' in team_a or 'Farense' in team_a

        # Generate question 1: Specific result
        if is_home:
            prompt = f"Qual foi o resultado do Farense contra o {team_b} em {data}?"
            completion = f"O Farense jogou em casa e o resultado foi {score_a}-{score_b}. O Farense marcou {score_a} golos e sofreu {score_b}."
        else:
            prompt = f"Qual foi o resultado do Farense contra o {team_a} em {data}?"
            completion = f"O Farense jogou fora de casa e o resultado foi {score_b}-{score_a}. O Farense marcou {score_b} golos e sofreu {score_a}."

        pairs.append({
            "prompt": prompt,
            "completion": completion,
            "metadata": {
                "tipo": "resultado_especifico",
                "epoca": epoch,
                "competicao": "Histórico",
                "fonte": "resultados_completos.md"
            }
        })

        # Generate question 2: Winner
        if score_a > score_b:
            winner = team_a if 'Farense' in team_a else team_b
            opponent = team_b if 'Farense' in team_a else team_a
        elif score_b > score_a:
            winner = team_b if 'Farense' in team_b else team_a
            opponent = team_a if 'Farense' in team_b else team_b
        else:
            winner = None
            opponent = team_a if 'Farense' in team_b else team_b

        if winner:
            if 'Farense' in winner:
                prompt2 = f"O Farense ganhou contra o {opponent}?"
                completion2 = f"Sim, o Farense ganhou por {score_a}-{score_b}."
            else:
                prompt2 = f"O Farense ganhou contra o {opponent}?"
                completion2 = f"Não, o Farense perdeu por {score_b}-{score_a}."
        else:
            prompt2 = f"O Farense empatou contra o {opponent}?"
            completion2 = f"Sim, o jogo terminou em empate {score_a}-{score_b}."

        pairs.append({
            "prompt": prompt2,
            "completion": completion2,
            "metadata": {
                "tipo": "vencedor",
                "epoca": epoch,
                "competicao": "Histórico",
                "fonte": "resultados_completos.md"
            }
        })

    return pairs

def extract_presidents_qa() -> List[Dict[str, Any]]:
    """Generate Q&A pairs about club presidents."""
    pairs = []

    presidents_data = [
        ("1912-1917", "Francisco Rogério Dâmaso Tavares Bello"),
        ("1917-1922", "António Guerreiro da Silva Gago"),
        ("1922-1925", "Manoel Garcia Cárabe"),
        ("1925-1928", "Dr. Cândido Emílio de Sousa"),
        ("1928-1929", "João Machado Vaz Velho"),
        ("1929-1930", "Guilherme Nogueira"),
        ("1930-1932", "Dr. Francisco Prudêncio Jr."),
        ("1932-1937", "Francisco Viegas Louro Jr."),
        ("1938-1940", "Álvaro Trigo e Silva"),
    ]

    for period, president in presidents_data:
        years = period.split('-')
        start_year = int(years[0])

        pairs.append({
            "prompt": f"Quem era o presidente do Farense em {start_year}?",
            "completion": f"Em {start_year}, o presidente do Sporting Clube Farense era {president}.",
            "metadata": {
                "tipo": "presidente",
                "periodo": period,
                "fonte": "presidentes.txt"
            }
        })

        # Alternative phrasing
        pairs.append({
            "prompt": f"Qual era o presidente do Farense no período {period}?",
            "completion": f"No período {period}, o presidente era {president}.",
            "metadata": {
                "tipo": "presidente",
                "periodo": period,
                "fonte": "presidentes.txt"
            }
        })

    return pairs

def extract_bylaws_qa() -> List[Dict[str, Any]]:
    """Generate Q&A pairs about club bylaws."""
    pairs = []

    bylaws_qa = [
        (
            "Quando foi fundado o Sporting Clube Farense?",
            "O Sporting Clube Farense foi fundado em 1 de Abril de 1910, em Faro."
        ),
        (
            "Qual é o principal objetivo do Sporting Clube Farense?",
            "O principal objetivo do Clube é promover o desenvolvimento e a prática dos desportos atléticos, especialmente os ao ar livre."
        ),
        (
            "Qual é a cidade sede do Sporting Clube Farense?",
            "A cidade sede do Sporting Clube Farense é Faro."
        ),
        (
            "Quais são as cores representativas do Sporting Clube Farense?",
            "As cores representativas do Clube têm como base o branco, o preto e o emblema do Clube."
        ),
    ]

    for prompt, completion in bylaws_qa:
        pairs.append({
            "prompt": prompt,
            "completion": completion,
            "metadata": {
                "tipo": "estatutos",
                "ano": 1924,
                "fonte": "estatutos_scf_1924.md"
            }
        })

    return pairs

def main():
    """Main function to expand dataset."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    dados_root = Path("/Users/f.nuno/Desktop/chatbot_2.0/dados")

    print("📊 EXPANDINDO DATASET COM NOVAS FONTES\n")
    print("="*70)

    all_qa_pairs = []

    # 1. Extract from results
    print("\n[1/4] Extraindo de resultados_completos.md...")
    results_file = dados_root / "resultados" / "resultados_completos.md"
    if results_file.exists():
        with open(results_file, 'r', encoding='utf-8') as f:
            results_content = f.read()
        results_qa = extract_results_qa(results_content)
        all_qa_pairs.extend(results_qa)
        print(f"  ✓ {len(results_qa)} exemplos gerados")
    else:
        print(f"  ✗ Ficheiro não encontrado")

    # 2. Extract from presidents
    print("\n[2/4] Extraindo de presidentes.txt...")
    presidents_qa = extract_presidents_qa()
    all_qa_pairs.extend(presidents_qa)
    print(f"  ✓ {len(presidents_qa)} exemplos gerados")

    # 3. Extract from bylaws
    print("\n[3/4] Extraindo de estatutos_scf_1924.md...")
    bylaws_qa = extract_bylaws_qa()
    all_qa_pairs.extend(bylaws_qa)
    print(f"  ✓ {len(bylaws_qa)} exemplos gerados")

    # 4. Load existing dataset
    print("\n[4/4] Carregando dataset existente...")
    existing_file = data_dir / "farense_dataset_cleaned.jsonl"
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_pairs = [json.loads(line) for line in f]
        print(f"  ✓ {len(existing_pairs)} exemplos existentes")
    else:
        existing_pairs = []
        print(f"  ⚠ Ficheiro não encontrado, começando do zero")

    # Combine datasets
    print("\n" + "="*70)
    print(f"\n📈 RESUMO DA EXPANSÃO:\n")
    print(f"  Existentes:        {len(existing_pairs):4d}")
    print(f"  Novos:             {len(all_qa_pairs):4d}")
    print(f"  ─────────────────────")
    print(f"  Total:             {len(existing_pairs) + len(all_qa_pairs):4d}")
    print(f"  Aumento:           {len(all_qa_pairs)/max(1, len(existing_pairs))*100:.1f}%")

    # Save combined dataset
    combined_pairs = existing_pairs + all_qa_pairs

    output_file = data_dir / "farense_dataset_expanded.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in combined_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"\n✅ Dataset expandido salvo em: {output_file.name}")
    print(f"\n📂 Próximos passos:")
    print(f"  1. python3 scripts/split_data_proper.py")
    print(f"  2. Usar novo dataset para treino")

    # Show sample
    print(f"\n📌 AMOSTRA DE NOVOS DADOS:\n")
    for i, pair in enumerate(all_qa_pairs[:3]):
        print(f"Exemplo {i+1}:")
        print(f"  Q: {pair['prompt']}")
        print(f"  A: {pair['completion'][:80]}...")
        print()

if __name__ == "__main__":
    main()
