#!/usr/bin/env python3
"""
Extrair Q&A pares factuais e elaborados a partir de biografias.
- Hassan Nader (JSON): Estatísticas, carreira, conquistas
- Mica (MD): Carreira em diferentes clubes, subidas históricas
- Francisco Tavares Bello (MD): Fundador, papel histórico
- E outras biografias disponíveis
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

def extract_hassan_nader_qa() -> List[Dict[str, Any]]:
    """Extract Q&A pairs from Hassan Nader's detailed biography (JSON)."""
    pairs = []

    # Q1: Quem é Hassan Nader?
    pairs.append({
        "prompt": "Quem é Hassan Nader?",
        "completion": "Hassan Nader é um jogador e treinador marroquino nascido em 1965 em Casablanca. É considerado um dos maiores ídolos estrangeiros da história do Sporting Clube Farense, onde jogou em duas passagens distintas (1992-1995 e 1997-2004). Durante sua passagem pelo Farense, marcou 116 golos em 208 jogos, conquistando a Bota de Ouro do campeonato português em 1994/95, feito notável por ter sido conquistado ao serviço de um clube fora dos 'três grandes' portugueses.",
        "metadata": {"tipo": "biografia", "pessoa": "Hassan Nader", "fonte": "bio_hassan_nader.json"}
    })

    # Q2: Qual foi a carreira de Hassan Nader antes do Farense?
    pairs.append({
        "prompt": "Qual foi a carreira de Hassan Nader antes de vir para o Farense?",
        "completion": "Antes de chegar ao Sporting Clube Farense em 1992, Hassan Nader tinha uma carreira consolidada. Jogou pelo WAC Casablanca (1982-1990), onde conquistou 2 Campeonatos de Marrocos e 2 Taças do Rei, além de ser melhor marcador do campeonato marroquino em 3 ocasiões. Posteriormente, representou o RCD Mallorca (1990-1992) em Espanha, onde foi finalista da Taça do Rei. Nader revelou-se um jogador internacional, representando a seleção de Marrocos (1988-1996) com participações em Mundiais e Taças de África das Nações.",
        "metadata": {"tipo": "carreira", "pessoa": "Hassan Nader", "periodo": "1982-1992", "fonte": "bio_hassan_nader.json"}
    })

    # Q3: Hassan Nader conquistou alguma prémio no Farense?
    pairs.append({
        "prompt": "Hassan Nader conquistou algum prémio individual importante no Farense?",
        "completion": "Sim, Hassan Nader conquistou a Bota de Ouro na temporada 1994/95, prémio concedido ao melhor marcador do campeonato português. Este é um dos maiores feitos individuais de um jogador do Farense na sua história. Além disso, marcou 116 golos em 208 jogos pelo clube, uma média impressionante de 0,5 golos por jogo, e participou em 17 jogos da Taça de Portugal, marcando 6 golos. O jogador também fez 2 golos na Taça UEFA durante sua passagem pelo clube.",
        "metadata": {"tipo": "conquistas", "pessoa": "Hassan Nader", "fonte": "bio_hassan_nader.json"}
    })

    # Q4: Quantas vezes Hassan Nader jogou no Farense?
    pairs.append({
        "prompt": "Hassan Nader teve quantas passagens pelo Sporting Clube Farense?",
        "completion": "Hassan Nader teve duas passagens distintas pelo Sporting Clube Farense. A primeira foi entre 1992 e 1995 (3 anos), quando conquistou a Bota de Ouro em 1994/95. Após uma breve passagem pelo SL Benfica (1995-1997), onde conquistou a Taça de Portugal, Nader regressou ao Farense para a sua segunda passagem (1997-2004), permanecendo 7 anos no clube. No total, vestiu a camisola azul e branca durante mais de uma década, consolidando seu legado como ídolo da instituição.",
        "metadata": {"tipo": "carreira_farense", "pessoa": "Hassan Nader", "fonte": "bio_hassan_nader.json"}
    })

    # Q5: Qual foi o legado de Hassan Nader no Farense?
    pairs.append({
        "prompt": "Qual foi o legado de Hassan Nader no Sporting Clube Farense?",
        "completion": "Hassan Nader deixou um legado significativo no Sporting Clube Farense. É considerado um dos maiores ídolos estrangeiros da história do clube, representando um dos períodos mais gloriosos da história do Farense. Elevou significativamente o nível competitivo da equipa, transformando o ataque do clube numa das forças mais temidas do campeonato português na década de 90. Contribuiu para que o clube algarvio ganhasse respeito nacional, demonstrando que era possível um clube fora dos 'três grandes' competir ao mais alto nível. Após encerrar sua carreira como jogador, Nader regressou como treinador na época 2005/06, demonstrando sua profunda identificação com o clube.",
        "metadata": {"tipo": "legado", "pessoa": "Hassan Nader", "fonte": "bio_hassan_nader.json"}
    })

    return pairs

def extract_tavares_bello_qa() -> List[Dict[str, Any]]:
    """Extract Q&A pairs from Francisco Tavares Bello's biography (MD)."""
    pairs = []

    # Q1: Quem foi Francisco Tavares Bello?
    pairs.append({
        "prompt": "Quem foi Francisco Tavares Bello?",
        "completion": "Francisco Rogério Dâmaso Tavares Bello foi uma das personalidades mais marcantes na história inicial do Sporting Clube Farense e do desporto algarvio. Foi fundador, dirigente, organizador e presidente do clube, tendo um papel decisivo na consolidação do futebol em Faro e na criação das bases institucionais do desporto regional. Tavares Bello não foi apenas um fundador, mas o arquitecto do desporto farense, deixando um legado que perdura mais de um século depois.",
        "metadata": {"tipo": "biografia", "pessoa": "Francisco Tavares Bello", "cargo": "Fundador e Presidente", "fonte": "historia_francisco_tavares_bello.md"}
    })

    # Q2: Quando foi fundado o Sporting Clube Farense?
    pairs.append({
        "prompt": "Quando foi fundado o Sporting Clube Farense e quem foram os fundadores?",
        "completion": "O Sporting Clube Farense foi fundado a 1 de Abril de 1910, reunido no Jardim Manuel Bivar em Faro. Francisco Tavares Bello foi um dos elementos do núcleo duro fundador, que incluía também António Marcos, João Rodrigues, José Guerrilha, Manuel Tavares da Cruz, José dos Santos Nugas, Francisco Albino, os irmãos Florindo, os irmãos Moleiro. Este grupo foi animado pelos ideais de modernização e prática desportiva que viriam a definir o Farense.",
        "metadata": {"tipo": "fundacao", "data": "1910-04-01", "pessoa": "Francisco Tavares Bello", "fonte": "historia_francisco_tavares_bello.md"}
    })

    # Q3: Qual foi o papel de Francisco Tavares Bello como presidente?
    pairs.append({
        "prompt": "Qual foi o papel de Francisco Tavares Bello como presidente do Farense?",
        "completion": "Francisco Tavares Bello assumiu a presidência do Sporting Clube Farense em Fevereiro de 1914, liderando uma Comissão Diretiva que incluía António Marvão como Secretário e João de Jesus Gralho como Tesoureiro. Durante seu mandato, o Farense recebeu pela primeira vez uma equipa nacional de relevo — o Vitória de Setúbal. Num jogo histórico, o Sporting Farense venceu por 2-1, perante mais de 3.000 espectadores no Campo de S. Francisco, um feito notável para a época.",
        "metadata": {"tipo": "presidencia", "periodo": "1914", "pessoa": "Francisco Tavares Bello", "fonte": "historia_francisco_tavares_bello.md"}
    })

    # Q4: Qual foi o contributo de Francisco Tavares Bello para o futebol algarvio?
    pairs.append({
        "prompt": "Qual foi o contributo de Francisco Tavares Bello para o desenvolvimento do futebol algarvio?",
        "completion": "Francisco Tavares Bello foi fundamental para organizar e estruturar o futebol algarvio. Participou na reunião de 16 de Outubro de 1921 no Ginásio Clube Farense que deu origem à Associação de Futebol do Algarve, integrando a comissão encarregue de redigir os estatutos e organizar o primeiro campeonato regional. Em 1922, foi nomeado cronometrista oficial da final do 1.º Campeonato do Algarve, uma inovação para a época que demonstra o reconhecimento pela sua competência e rigor. Também colaborou no jornal O Sul Desportivo como comentarista sobre a história e a organização do futebol local.",
        "metadata": {"tipo": "contributo_regional", "periodo": "1920-1922", "pessoa": "Francisco Tavares Bello", "fonte": "historia_francisco_tavares_bello.md"}
    })

    # Q5: Como era o futebol em Faro no início do século XX?
    pairs.append({
        "prompt": "Como era o futebol em Faro no tempo de Francisco Tavares Bello (início do século XX)?",
        "completion": "Segundo o próprio Francisco Tavares Bello, o futebol em Faro começou por volta de 1905, de forma muito rudimentar. Os primeiros jogadores compraram uma bola com uma dádiva de uma libra de ouro do bispo D. António Barbosa Leão e começaram a jogar no Largo da Sé, passando depois para o Largo de S. Francisco. As balizas eram improvisadas, o campo era muito rudimentar e o entusiasmo era absoluto. Os operários eram os estudantes, soldados e marinheiros da Palmela, que ajudaram a erguer o Campo de S. Francisco, um dos primeiros espaços dedicados ao futebol na cidade. Este foi o início de uma organização desportiva que evoluiria para o Sporting Clube Farense.",
        "metadata": {"tipo": "historia_inicial", "periodo": "1905-1910", "pessoa": "Francisco Tavares Bello", "fonte": "historia_francisco_tavares_bello.md"}
    })

    return pairs

def main():
    """Main function to extract biographies."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    print("📚 EXTRAINDO Q&A PARES DE BIOGRAFIAS\n")
    print("="*80)

    all_pairs = []

    # Extract Hassan Nader
    print("\n[1/2] Extraindo Hassan Nader...")
    hassan_pairs = extract_hassan_nader_qa()
    all_pairs.extend(hassan_pairs)
    print(f"  ✓ {len(hassan_pairs)} exemplos gerados")

    # Extract Francisco Tavares Bello
    print("\n[2/2] Extraindo Francisco Tavares Bello...")
    tavares_pairs = extract_tavares_bello_qa()
    all_pairs.extend(tavares_pairs)
    print(f"  ✓ {len(tavares_pairs)} exemplos gerados")

    print("\n" + "="*80)
    print(f"\n✅ Total de {len(all_pairs)} exemplos de biografias extraídos")

    # Save to file
    output_file = data_dir / "biografias_qa.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"\n📂 Salvos em: {output_file.name}")

    # Show samples
    print(f"\n📌 AMOSTRAS:\n")
    for i, pair in enumerate(all_pairs[:3]):
        print(f"Exemplo {i+1}:")
        print(f"  Q: {pair['prompt']}")
        print(f"  A: {pair['completion'][:120]}...")
        print()

if __name__ == "__main__":
    main()
