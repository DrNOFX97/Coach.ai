#!/usr/bin/env python3
"""
Extrair Q&A pares factuais e elaborados a partir dos livros históricos do Farense.
- Fundação (1 de Abril de 1910)
- Primeiras equipas e jogadores históricos
- Rivalidades regionais (Olhanense, Lisboa e Faro)
- Partidas memoráveis e anedotas históricas
- Desenvolvimento do futebol algarvio
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

def extract_founding_qa() -> List[Dict[str, Any]]:
    """Extract Q&A pairs about club founding and early history."""
    pairs = []

    # Q1: Quando foi fundado o Sporting Clube Farense?
    pairs.append({
        "prompt": "Quando foi fundado o Sporting Clube Farense e qual foi a origem do seu nome?",
        "completion": "O Sporting Clube Farense foi fundado a 1 de Abril de 1910, coroando um longo esforço de entusiastas do futebol em Faro. O nome foi aceite por unanimidade pelos jogadores da nova associação desportiva, devido à grande admiração que sentiam pelo Sporting Clube de Portugal. Quanto ao equipamento, a escolha foi simples: como os rapazes de Faro só dispunham de fotografias a preto e branco do Sporting Clube de Lisboa, que naquela época tinha uma camisola bipartida (metade verde, metade branca), optaram por um jersey alvi-negro com calções pretos.",
        "metadata": {
            "tipo": "historia_fundacao",
            "data": "1910-04-01",
            "fonte": "livro_scf_1_organizado.md",
            "pessoas": "Fundadores do Farense"
        }
    })

    # Q2: Como era o futebol em Faro antes de 1910?
    pairs.append({
        "prompt": "Como era o futebol em Faro no início do século XX, antes da fundação do Farense?",
        "completion": "O futebol começou em Faro por volta de 1905, de forma muito rudimentar. Os primeiros jogadores compraram uma bola com uma dádiva de uma libra de ouro do bispo D. António Barbosa Leão e começaram a jogar no Largo da Sé, passando depois para o Largo de S. Francisco. As balizas eram improvisadas, o campo era muito rudimentar, mas o entusiasmo era absoluto. Os operários eram estudantes, soldados e marinheiros da Palmela, que ajudaram a erguer o Campo de S. Francisco. Esta organização desportiva rudimentar evoluiria, pouco anos depois, para o Sporting Clube Farense.",
        "metadata": {
            "tipo": "historia_inicial",
            "periodo": "1905-1910",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q3: Como era a primeira equipa do Farense?
    pairs.append({
        "prompt": "Qual era a composição da primeira equipa do Sporting Clube Farense?",
        "completion": "Segundo depoimento de Manuel de Sousa, um dos primeiros jogadores, a composição da equipa-base do Farense dos primeiros tempos (por volta de 1912) era: João Rodrigues (guarda-redes); Guerrilha e Manuel de Sousa (defesas); José Teixeira, Manuel Tavares da Cruz e José Aleixo (meio-campo); Francisco Lima ou Eduardo Vieira, António Marcos, João Gralho, Bento e José Nugas (avançados). Era uma equipa de grande dinâmica e talento, capaz de se bater de igual para igual com equipas de Lisboa e outras cidades maiores.",
        "metadata": {
            "tipo": "jogador_historia",
            "periodo": "1910-1915",
            "fonte": "livro_scf_1_organizado.md",
            "pessoas": ["João Rodrigues", "Manuel de Sousa", "João Gralho", "José Nugas"]
        }
    })

    # Q4: Qual era a origem social dos primeiros jogadores?
    pairs.append({
        "prompt": "Qual era a origem social e profissional dos primeiros jogadores do Farense?",
        "completion": "A equipa de honra do Farense tinha origens plebéias e muito humildes. João Rodrigues era soldador da fábrica Coelho; Manuel de Sousa era filho de moleiros; José Aleixo trabalhava no comércio de frutos; Eduardo Ventura era marceneiro; Albino era ferroviário; Guerrilha era sapateiro; Francisco Lima era despachante de alfândega; João Gralho era fundidor; Teixeira era factor dos Caminhos de Ferro. Não havia jogadores profissionais, nem ordenados elevados, nem 'luvas' ou prémios de jogo. Os jogadores compravam o próprio equipamento e pagavam uma quota mensal de 30 réis. Esta composição social contrastava fortemente com a do Sporting Clube de Portugal, fundado em Lisboa poucos anos antes pela nobreza portuguesa.",
        "metadata": {
            "tipo": "historia_social",
            "periodo": "1910-1915",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q5: Qual foi o papel da família Gralho no Farense?
    pairs.append({
        "prompt": "Qual foi a importância da família Gralho para o Sporting Clube Farense?",
        "completion": "A família Gralho teve um papel fundamental na história do Farense. João Gralho foi por volta de 1909/10 o grande promotor da criação do clube e seu principal impulsionador. Seguiu-se-lhe um irmão mais novo, José de Jesus, que também jogava na linha avançada, e Joaquim, conhecido como 'O 3.º homem', que foi um jogador excepcional e hábil. Ainda chegaram a jogar juntos. Depois António Gralho, considerado por muitos como o mais eminente da família, ingressou no Sporting de Lisboa durante o serviço militar, onde se colocou como um dos melhores marcadores. Jorge Gralho, outro irmão, esteve em grande evidência nos anos 30. O legado não parou: Walter (filho de José de Jesus) e Jorge Jr. (filho de António) também vestiram a camisola alvi-negra.",
        "metadata": {
            "tipo": "familia_historia",
            "pessoa": "Família Gralho",
            "fonte": "livro_scf_1_organizado.md",
            "pessoas": ["João Gralho", "José de Jesus Gralho", "Joaquim Gralho", "António Gralho", "Jorge Gralho"]
        }
    })

    return pairs

def extract_early_matches_qa() -> List[Dict[str, Any]]:
    """Extract Q&A pairs about early notable matches and rivalries."""
    pairs = []

    # Q1: Transferência de João Gralho
    pairs.append({
        "prompt": "Por que razão João Gralho deixou o Sporting Clube Farense?",
        "completion": "João Gralho, primeiro capitão e grande dinamizador do Farense, foi convencido a transferir-se para o Vitória de Setúbal. O clube sadino ficou muito impressionado com o dinâmico primeiro capitão do Sporting de Faro e com a sua facilidade de remate. Segundo os depoimentos da época, João Gralho preferiu 'ir pregar para outra freguesia' porque 'santos de casa não fazem milagres'. A sua transferência deixou o Farense numa fase depressiva de quase desorganização, felizmente de curta duração. Aí por volta de 1917, António Gago tomou a responsabilidade de revitalizar o clube.",
        "metadata": {
            "tipo": "jogador_historia",
            "pessoa": "João Gralho",
            "periodo": "1914-1917",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q2: Papel de António Gago
    pairs.append({
        "prompt": "Qual foi o papel de António Gago na recuperação do Farense?",
        "completion": "António Gago foi o homem que revitalizou o Farense por volta de 1917, quando o clube estava numa fase depressiva após a partida de João Gralho. Gago era empregado da mercearia Sequerra antes de trabalhar por conta própria. Como capitão da equipa, treinador e orientador técnico do clube, conquistou os Campeonatos do Algarve nas épocas de 1917/18 e 1921/22. Era muito rápido (tinha praticado atletismo em 100, 200 e 1.500 metros), corria pela linha lateral com grande eficiência de centros. A sua grande especialidade eram os golos directos de comer. Jogou largos anos no posto de ponta-direita, chegando a alinhar até aos 34 anos. Merece a gratidão de quantos vibram pelos leões de Faro.",
        "metadata": {
            "tipo": "jogador_historia",
            "pessoa": "António Gago",
            "periodo": "1917-1925",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q3: Viagem a Beja em 1917/18
    pairs.append({
        "prompt": "Qual foi o resultado da viagem do Farense a Beja em 1917-1918?",
        "completion": "O Farense foi convidado para disputar dois jogos particulares em Beja. A equipa enfrentou dificuldades já na chegada: os anfitriões não tinham preparado as passagens como prometido, e os jogadores tiveram de pagar os bilhetes do seu próprio bolso. No primeiro dia, o Farense defrontou o Águias Futebol Clube e venceu por 3-1. No segundo dia, jogou contra a equipa dos 'Onze Amigos' e conquistou uma vitória esmagadora de 13-0. Os organizadores, vexados pelos resultados, não quiseram reembolsar os visitantes nem pagar-lhes o regresso. Só com ajuda de um amigo residente em Beja, de nome Góinhas, que emprestou o dinheiro ao team, conseguiram regressar a Faro.",
        "metadata": {
            "tipo": "partido_historico",
            "periodo": "1917-1918",
            "fonte": "livro_scf_1_organizado.md",
            "competicao": "Particular"
        }
    })

    # Q4: Jogo contra Casa Pia em 1920
    pairs.append({
        "prompt": "Como se realizou o jogo do Farense contra o Casa Pia em 1920?",
        "completion": "Em 1920, o Casa Pia, que tinha ganho o Campeonato de Lisboa, estava de regresso de Sevilha quando ficou bloqueado em Tunes devido a uma greve dos ferroviários. Obrigados a pernoitar em Faro, os jogadores do Casa Pia foram contactados pelos dirigentes do clube algarvio. No dia seguinte realizou-se um desafio que surpreendeu a população local: o Casa Pia venceu o Farense por 3-1. Este encontro teve grande relevo porque mostrou que o Casa Pia, apesar de ser o campeão de Lisboa, ainda era capaz de derrotar a potência algarvia.",
        "metadata": {
            "tipo": "partido_historico",
            "periodo": "1920",
            "fonte": "livro_scf_1_organizado.md",
            "competicao": "Particular"
        }
    })

    return pairs

def extract_olhanense_rivalry_qa() -> List[Dict[str, Any]]:
    """Extract Q&A pairs about the famous Farense vs Olhanense rivalry."""
    pairs = []

    # Q1: Origem da rivalidade
    pairs.append({
        "prompt": "Quando começou a rivalidade entre o Farense e o Olhanense?",
        "completion": "A rivalidade entre Farense e Olhanense começou já nos tempos heróicos do futebol algarvio. Faro e Olhão mantinham relações de vizinhança nem sempre amenas, sendo cidades próximas mas culturalmente distintas. Olhão era mais prospera graças às suas fábricas de conservas de peixe e armadores endinheirados, enquanto Faro era mais administrativa e burocrática. O clubismo era cego e pitoresco, e o facciosismo exacerbado. Desde cedo, era muito maior e mais áspera a rivalidade entre os dois grandes clubes algarvios, especialmente nos tempos iniciais quando ambos buscavam a filiação no Sporting Clube de Portugal.",
        "metadata": {
            "tipo": "rivalidade",
            "clubes": ["Farense", "Olhanense"],
            "periodo": "1912-1920",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q2: Jogo em Olhão em 1918 com violência
    pairs.append({
        "prompt": "O que aconteceu no jogo do Farense em Olhão em 1918?",
        "completion": "Em 1918, o Farense deslocou-se a Olhão para disputar um jogo crucialmente importante. O Farense foi vaiado desde o início, respirando-se uma atmosfera de massacre. Apesar do meio ambiente ingrato, o Farense conseguiu estruturar bem o seu conjunto, basear o jogo na defesa sólida e contra-ataques rápidos. Venceu pela marca retumbante de 6-1. O pior veio depois: a multidão fanatizada pela 'futebolite' aguda preparava-se para espancar a turma visitante. Os elementos do Farense só conseguiram livrar-se ao dum arraial de pancadaria descomunal quando, abandonando qualquer retirada estratégica, meteram a trouxa debaixo do braço e arrancaram em correria desenfreada até à Estação da C.P., que ficava próxima.",
        "metadata": {
            "tipo": "partido_historico",
            "periodo": "1918",
            "competicao": "Campeonato Algarve",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q3: Meia-final em Olhão em 1922
    pairs.append({
        "prompt": "Como foi o desafio de meia-final entre Farense e Olhanense em 28 de Maio de 1922?",
        "completion": "Em 28 de Maio de 1922, Farense e Olhanense defrontaram-se em Olhão numa crucial meia-final do Campeonato do Algarve. O Farense tinha vencido, em Faro, a primeira mão por 4-2. Neste jogo em Olhão, a grande inovação foi um sistema de cronometragem efectuado fora das quatro linhas, não pelo juiz, mas por outro personagem (como acontecia na bola ao cesto). O jogo foi intenso: Joaquim Gralho abriu o activo para o Farense. O Olhanense empatou com um golo de Júlio Costa. Na segunda parte, o Farense dominava quando Manuel Florindo endossou a bola a José Gralho, que marcou. Logo após, João Gralho aproveitou um erro da defesa para fazer o terceiro golo. No final, gerou-se confusão dentro da grande área onde o árbitro mandou marcar penalty. Após protesto e reuniões, o Farense foi reconhecido vencedor da meia-final.",
        "metadata": {
            "tipo": "partido_historico",
            "periodo": "1922",
            "competicao": "Campeonato Algarve - Meia-final",
            "fonte": "livro_scf_1_organizado.md",
            "jogadores_destaque": ["Joaquim Gralho", "Manuel Florindo", "José Gralho", "João Gralho"]
        }
    })

    # Q4: O histórico jogo de 1923
    pairs.append({
        "prompt": "O que foi o histórico jogo entre Farense e Olhanense em 1923?",
        "completion": "Em 1923, realizou-se no Campo de S. Francisco o mais inolvidável e marcante jogo dos velhos tempos entre Farense e Olhanense. O Olhanense, dirigido por Cândido Ventura, tinha reforçado significativamente o seu plantel com Júlio Costa (do Benfica), os irmãos Montenegro (Chico e Cecílio), e Pais como avançado-centro categorizado. O jogo terminou com vitória esmagadora do Farense por 3-1, e o Olhanense abandonou o campo a meio da segunda parte, completamente abatido. Joaquim Gralho marcou dois golos. O mais hilariante foi o que aconteceu a seguir: estava combinado que o comboio apitaria no regresso para comemorar, mas quando os jogadores de Olhão se apearam com caras de enterro, a festa mudou de figura. O maquinista Albino, adepto do Farense, apitou até Olhão como de costume. José Nugas, que morava em Olhão, sofreu represálias após este jogo.",
        "metadata": {
            "tipo": "partido_historico",
            "periodo": "1923",
            "competicao": "Taça Algarve",
            "fonte": "livro_scf_1_organizado.md",
            "jogadores_destaque": ["Joaquim Gralho", "José Nugas"]
        }
    })

    # Q5: Consequências da vitória do Olhanense em 1924
    pairs.append({
        "prompt": "Como é que o Olhanense venceu o Campeonato de Portugal em 1924?",
        "completion": "Depois da vitória do Olhanense no Campeonato de Portugal em 1924, o Farense começou a perder velocidade e entrou num período de crise que se prolongaria até aos princípios dos anos 30. No Campeonato de Portugal de 1924, os Campeonatos eram disputados por eliminatórias. Farense e Olhanense estavam empatados no campeonato distrital, pelo que se disputou um jogo de desempate em Vila Real de Santo António, em terreno neutro. O Olhanense conseguiu ganhar o derby decisivo devido à marcação de um penalty - penalty muito discutível segundo António Gago, visto que o defesa José da Silva caiu na grande área e a bola passou sobre a sua mão de forma puramente casual. Apesar desta controvérsia, o Olhanense seguiu para a competição máxima do país e tornou-se Campeão de Portugal nesse ano.",
        "metadata": {
            "tipo": "partido_historico",
            "periodo": "1924",
            "competicao": "Campeonato Portugal",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    return pairs

def extract_regional_development_qa() -> List[Dict[str, Any]]:
    """Extract Q&A pairs about football development in the Algarve."""
    pairs = []

    # Q1: Organização do futebol algarvio
    pairs.append({
        "prompt": "Como se organizou o futebol no Algarve nos primeiros anos?",
        "completion": "O futebol no Algarve foi organizado progressivamente através de várias associações. Em 1914, fundou-se a União de Futebol de Faro que englobava a Associação Académica do Liceu de Faro, Escola Normal de Faro, Sporting Clube Farense e Boavista Futebol Clube. O primeiro Campeonato de Faro foi disputado nesse ano, vencido pelo Farense. Em 1917, dissolvida a União, fundou-se a Associação de Futebol do Algarve, com sede no primeiro andar do edifício dos antigos correios. Em 1918, após fracasso, criou-se uma nova associação que finalmente foi fundada oficialmente em 1923 como Associação de Futebol de Faro, a qual se filiou na União Portuguesa de Futebol e Federação Portuguesa dos Sports Atléticas. Os estatutos foram aprovados a 27 de Outubro de 1924 pelo Governo Civil de Faro.",
        "metadata": {
            "tipo": "historia_regional",
            "periodo": "1914-1924",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q2: Posição do Farense entre os clubes algarvios
    pairs.append({
        "prompt": "Qual era a posição do Sporting Clube Farense entre os clubes algarvios?",
        "completion": "O Sporting Clube Farense era claramente o clube mais antigo e mais importante do Algarve. Se compararmos a data de fundação do Farense (1 de Abril de 1910) com outros clubes algarvios, vemos que o Sporting Clube Olhanense foi fundado em 27 de Abril de 1912, o Clube de Futebol Esperança de Lagos em 20 de Setembro de 1912, o Portimonense em 14 de Agosto de 1914, o Lusitano em 15 de Abril de 1916, o Silves em 4 de Abril de 1919, o Louletano em 6 de Junho de 1923. O Farense é portanto um dos mais longevos clubes da província e certamente o decano de quantos ainda hoje praticam o futebol. A sua hegemonia era inquestionável nas primeiras décadas.",
        "metadata": {
            "tipo": "historia_regional",
            "periodo": "1910-1925",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    # Q3: Importância de Francisco Tavares Bello
    pairs.append({
        "prompt": "Qual foi o papel de Francisco Tavares Bello na organização do futebol algarvio?",
        "completion": "Francisco Tavares Bello foi fundamental para organizar e estruturar o futebol algarvio. Como um dos fundadores do Farense e subsequentemente um dos seus dirigentes mais activos, participou na reunião de 16 de Outubro de 1921 no Ginásio Clube Farense que deu origem à Associação de Futebol do Algarve. Integrou a comissão encarregue de redigir os estatutos e organizar o primeiro campeonato regional. Em 1922, foi nomeado cronometrista oficial da final do 1.º Campeonato do Algarve, uma inovação para a época que demonstra o reconhecimento pela sua competência e rigor. Tavares Bello também colaborou no jornal O Sul Desportivo como comentarista sobre a história e a organização do futebol local, sendo verdadeiramente o 'arquitecto do desporto farense'.",
        "metadata": {
            "tipo": "figura_historica",
            "pessoa": "Francisco Tavares Bello",
            "periodo": "1910-1924",
            "fonte": "livro_scf_1_organizado.md"
        }
    })

    return pairs

def main():
    """Main function to extract Q&A pairs from books."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    print("📚 EXTRAINDO Q&A PARES DOS LIVROS HISTÓRICOS\n")
    print("="*80)

    all_pairs = []

    # Extract founding and early history
    print("\n[1/4] Extraindo histórico de fundação...")
    founding_pairs = extract_founding_qa()
    all_pairs.extend(founding_pairs)
    print(f"  ✓ {len(founding_pairs)} exemplos gerados")

    # Extract early matches
    print("\n[2/4] Extraindo partidas e jogadores históricos...")
    matches_pairs = extract_early_matches_qa()
    all_pairs.extend(matches_pairs)
    print(f"  ✓ {len(matches_pairs)} exemplos gerados")

    # Extract Olhanense rivalry
    print("\n[3/4] Extraindo rivalidade com Olhanense...")
    rivalry_pairs = extract_olhanense_rivalry_qa()
    all_pairs.extend(rivalry_pairs)
    print(f"  ✓ {len(rivalry_pairs)} exemplos gerados")

    # Extract regional development
    print("\n[4/4] Extraindo desenvolvimento regional...")
    regional_pairs = extract_regional_development_qa()
    all_pairs.extend(regional_pairs)
    print(f"  ✓ {len(regional_pairs)} exemplos gerados")

    print("\n" + "="*80)
    print(f"\n✅ Total de {len(all_pairs)} exemplos dos livros extraídos")

    # Save to file
    output_file = data_dir / "livros_qa.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"\n📂 Salvos em: {output_file.name}")

    # Show samples
    print(f"\n📌 AMOSTRAS:\n")
    for i, pair in enumerate(all_pairs[:5]):
        print(f"Exemplo {i+1}:")
        print(f"  Q: {pair['prompt']}")
        print(f"  A: {pair['completion'][:150]}...")
        print()

if __name__ == "__main__":
    main()
