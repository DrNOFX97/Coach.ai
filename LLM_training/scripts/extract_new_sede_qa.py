#!/usr/bin/env python3
"""
Extract Q&A pairs about Complexo Sócio-Desportivo as the new sede
"""

import json
from typing import List, Dict, Any


def extract_new_sede_qa() -> List[Dict[str, Any]]:
    """Extract Q&A about the new headquarters at Complexo Sócio-Desportivo."""
    return [
        {
            "prompt": "Qual é a atual sede do Sporting Clube Farense desde 1989?",
            "completion": "A atual sede do Sporting Clube Farense desde 1989 é o Complexo Sócio-Desportivo. Este complexo foi construído após a cedência de terrenos pela Câmara Municipal em 1982. O Ginásio foi inaugurado em 1987, o Pavilhão em 1988, e a inauguração oficial de todo o Complexo Sócio-Desportivo realizou-se em 1 de Setembro de 1989.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Complexo Sócio-Desportivo",
                "periodo": "1989-atual",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Como foi a transição de sedes para o Complexo Sócio-Desportivo?",
            "completion": "O Sporting Clube Farense passou pela \"valsa das sedes\" durante muitos anos, ocupando vários locais em Faro desde a sua fundação em 1910. A última sede antes do Complexo era na Rua Ferreira Neto (desde 1950). Em 1982, após a cedência de terrenos pela Câmara Municipal, iniciou-se a construção do Complexo Sócio-Desportivo. Este representou um avanço significativo, fornecendo ao clube instalações modernas e adequadas, com Ginásio e Pavilhão, finalmente inaugurados em 1989.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Complexo Sócio-Desportivo",
                "periodo": "1989",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "O que significa o Complexo Sócio-Desportivo para o Sporting Clube Farense?",
            "completion": "O Complexo Sócio-Desportivo significa o fim da \"valsa das sedes\" que caracterizou a história do clube. Representa estabilidade institucional, instalações adequadas e profissionalizadas, e reconhecimento público da importância do clube. A sua inauguração em 1989 marca uma nova era na história do Sporting Clube Farense, com infraestruturas modernas que permitem o desenvolvimento desportivo e social do clube.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Complexo Sócio-Desportivo",
                "periodo": "1989-atual",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual foi a última sede do Farense antes do Complexo Sócio-Desportivo?",
            "completion": "A última sede do Sporting Clube Farense antes do Complexo Sócio-Desportivo era nos 1º e 2º andares do nº 6 da Rua Ferreira Neto. O clube estava instalado lá desde aproximadamente 1950. A mudança para o Complexo Sócio-Desportivo em 1989 representou uma evolução significativa, deixando para trás décadas de instalações precárias em vários locais da cidade.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Rua Ferreira Neto 6 → Complexo Sócio-Desportivo",
                "periodo": "1989",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual foi a importância do Complexo Sócio-Desportivo na história do Farense?",
            "completion": "O Complexo Sócio-Desportivo foi de enorme importância para o Sporting Clube Farense. Permitiu ao clube ter, pela primeira vez, instalações adequadas e permanentes. Isto pôs fim à instabilidade sede que caracterizava a sua história, forneceu infraestruturas modernas para treino e competição, e consolidou o papel do Farense como instituição desportiva importante em Faro. A sua inauguração em 1989 marca o início de uma nova era para o clube.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Complexo Sócio-Desportivo",
                "periodo": "1989-atual",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        }
    ]


def main():
    """Main function."""
    print("="*80)
    print("EXTRAÇÃO DE Q&A SOBRE NOVA SEDE (COMPLEXO SÓCIO-DESPORTIVO)")
    print("="*80 + "\n")

    qa_pairs = extract_new_sede_qa()

    print(f"Total de pares extraídos: {len(qa_pairs)}\n")

    # Save to JSONL
    output_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/new_sede_qa.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    print(f"✓ Salvo em: {output_file}\n")

    # Display extracted pairs
    print("="*80)
    print("PARES EXTRAÍDOS:")
    print("="*80 + "\n")

    for i, qa in enumerate(qa_pairs, 1):
        print(f"{i}. {qa['prompt']}")
        print(f"   → {qa['completion'][:100]}...\n")


if __name__ == "__main__":
    main()
