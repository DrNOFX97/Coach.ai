#!/usr/bin/env python3
"""
Extract Q&A pairs about Sporting Clube Farense sports facilities
Based on document about cedência de terrenos and inaugurações
"""

import json
from typing import List, Dict, Any


def extract_installations_qa() -> List[Dict[str, Any]]:
    """Extract Q&A about sports facilities and installations."""
    return [
        {
            "prompt": "Quanto terreno recebeu o Sporting Clube Farense em Maio de 1982?",
            "completion": "Em Maio de 1982, através de escritura, o Sporting Clube Farense recebeu a cedência de dois terrenos. Um terreno de 3.777 m2 foi destinado para construção do Complexo Desportivo, e outro terreno de 3.011 m2 foi cedido no Parque Desportivo da Pênha.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1982",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual foi a primeira instalação inaugurada no complexo desportivo do Farense?",
            "completion": "A primeira instalação inaugurada foi o Ginásio, em 1987. Esta foi uma fase importante na modernização das infraestruturas desportivas do clube, marcando o início da concretização do Complexo Desportivo.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1987",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Quando foi inaugurado o Pavilhão do Sporting Clube Farense?",
            "completion": "O Pavilhão do Sporting Clube Farense foi inaugurado em 1988, um ano após a inauguração do Ginásio. Esta foi a segunda fase importante das instalações do Complexo Desportivo.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1988",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual foi a data da inauguração oficial do Complexo Sócio-Desportivo do Sporting Clube Farense?",
            "completion": "A inauguração oficial do Complexo Sócio-Desportivo do Sporting Clube Farense (SCFarense) foi realizada em 1 de Setembro de 1989. Esta foi uma data memorável que marcou a conclusão das principais instalações do complexo, incluindo o Ginásio e o Pavilhão.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1989-09-01",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Como evoluiu a construção do complexo desportivo do Farense entre 1982 e 1989?",
            "completion": "A evolução foi gradual mas consistente. Em Maio de 1982, o clube recebeu a cedência de terrenos (3.777 m2 e 3.011 m2). Em 1987, inaugurou o Ginásio. Em 1988, inaugurou o Pavilhão. Finalmente, em 1 de Setembro de 1989, realizou-se a inauguração oficial do Complexo Sócio-Desportivo, consolidando as infraestruturas do clube.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1982-1989",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual era a área do terreno cedido ao Farense para o Complexo Desportivo?",
            "completion": "O terreno cedido ao Sporting Clube Farense para construção do Complexo Desportivo tinha uma área de 3.777 metros quadrados. Esta área permitiu a construção de instalações adequadas, incluindo o Ginásio e o Pavilhão que foram inaugurados posteriormente.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1982",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Onde se localiza o segundo terreno cedido ao Farense em 1982?",
            "completion": "O segundo terreno, com uma área de 3.011 metros quadrados, foi cedido no Parque Desportivo da Pênha. Este terreno complementava o primeiro (3.777 m2) na infraestrutura desportiva geral do clube.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Parque Desportivo da Pênha",
                "periodo": "1982",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual era o nome completo do complexo inaugurado em 1989?",
            "completion": "O nome completo do complexo inaugurado em 1 de Setembro de 1989 era 'Complexo Sócio-Desportivo do SCFarense' (Sporting Clube Farense). Este nome refletia a natureza multifuncional das instalações, que serviam tanto para atividades desportivas como sociais.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1989",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Que tipo de instalações incluía o Complexo Sócio-Desportivo do Farense?",
            "completion": "O Complexo Sócio-Desportivo do Sporting Clube Farense incluía um Ginásio, inaugurado em 1987, e um Pavilhão, inaugurado em 1988. Estas duas estruturas principais foram concluídas e inauguradas oficialmente em conjunto em 1 de Setembro de 1989.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1987-1989",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        },
        {
            "prompt": "Qual foi a importância da cedência de terrenos em 1982 para o Farense?",
            "completion": "A cedência de terrenos em Maio de 1982 foi crucial para o futuro do Sporting Clube Farense. Permitiu a construção de infraestruturas modernas que o clube necessitava há muitos anos. Os dois terrenos cedidos (3.777 m2 e 3.011 m2) forneceram a base para a construção do Complexo Sócio-Desportivo, que foi finalmente inaugurado em 1989.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1982-1989",
                "fonte": "Documento cedência de terrenos SCFarense"
            }
        }
    ]


def main():
    """Main function."""
    print("="*80)
    print("EXTRAÇÃO DE Q&A SOBRE INSTALAÇÕES DESPORTIVAS")
    print("="*80 + "\n")

    qa_pairs = extract_installations_qa()

    print(f"Total de pares extraídos: {len(qa_pairs)}\n")

    # Save to JSONL
    output_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/installations_qa.jsonl"
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
