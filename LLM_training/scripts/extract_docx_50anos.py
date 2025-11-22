#!/usr/bin/env python3
"""
Extract Q&A pairs from DOCX: 50 Anos de História do Futebol em Faro (1900-1950)
Focusing ONLY on content related to Sporting Clube Farense
"""

import json
from docx import Document
from typing import List, Dict, Any


def extract_docx_content() -> str:
    """Extract and return full text from DOCX document"""
    docx_path = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/dados/outros/50 anos de História do Futebol em Faro.docx"
    doc = Document(docx_path)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])


def extract_founding_history() -> List[Dict[str, Any]]:
    """Extract Q&A about Farense founding and early years"""
    return [
        {
            "prompt": "Qual foi o primeiro jogo de futebol realizado em Faro?",
            "completion": "O primeiro jogo de futebol realizado em Faro foi em 1907, no Largo de S. Francisco, sob a orientação do professor Carlos Lyster Franco, que introduziu as regras do futebol na cidade através de uma revista inglesa que continha as regras do jogo.",
            "metadata": {
                "tipo": "historia_fundacao",
                "periodo": "1907",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "Carlos Lyster Franco"
            }
        },
        {
            "prompt": "Quem foi Carlos Lyster Franco e qual foi o seu papel no futebol farense?",
            "completion": "Carlos Lyster Franco foi um pintor e professor do Liceu Nacional de Faro que, desde 1902, exercia funções docentes. Ao receber uma revista inglesa com as regras de futebol, ensinou o jogo aos seus estudantes. Tornou-se o introdutor das regras de futebol em Faro, propagando o 'foot-ball' entre os estudantes.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1902-1908",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "Carlos Lyster Franco"
            }
        },
        {
            "prompt": "Como nasceu a União de Futebol de Faro e qual foi o papel do Sporting Farense?",
            "completion": "Os rapazes que jogavam no terreiro do Castelo (com idades entre 13 e 17 anos) decidiram constituir uma organização. Por decisão unânime, nomearam João de Jesus Gralho como Capitão Geral. João Gralho foi fundamental na fundação do SPORTING CLUBE FARENSE, reunindo um grupo de entusiastas. O clube ganhou rapidamente adeptos em número elevadíssimo, com quotas de um pataco por semana.",
            "metadata": {
                "tipo": "historia_fundacao",
                "periodo": "1910",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "João de Jesus Gralho"
            }
        },
        {
            "prompt": "Quem foi João de Jesus Gralho e qual foi a sua importância no Sporting Farense?",
            "completion": "João de Jesus Gralho foi o primeiro Capitão Geral do Sporting Clube Farense. Descrito como uma figura pequena e franzina, usava o jersey bi-partido de preto e branco com calções até ao joelho, tornando-se um símbolo do clube nos seus primórdios. Foi fundamental na fundação e organização do clube, reunindo os entusiastas de futebol da cidade.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1910-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "João de Jesus Gralho"
            }
        },
        {
            "prompt": "Qual era o custo das quotas do Sporting Farense nos primeiros anos?",
            "completion": "As quotas do Sporting Clube Farense nos primeiros anos era de um pataco por semana. Este valor acessível permitiu que o clube ganhasse rapidamente um número elevadíssimo de adeptos, reflectindo o entusiasmo da população farense pelo novo desporto.",
            "metadata": {
                "tipo": "historia_social",
                "periodo": "1910-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_early_matches() -> List[Dict[str, Any]]:
    """Extract Q&A about early matches and competitions"""
    return [
        {
            "prompt": "Qual foi o resultado do jogo entre Sporting Farense e Vitória Futebol Clube (Setúbal) em Abril de 1914?",
            "completion": "Em Abril de 1914, o Vitória Futebol Clube de Setúbal visitou Faro. O primeiro jogo foi no sábado, dia 4, no campo de S. Francisco contra a Académica. O Vitória ganhou por 3-0, sendo o último golo de grande penalidade. No dia seguinte, o Vitória defrontou o Sporting Farense com uma assistência muito numerosa.",
            "metadata": {
                "tipo": "partido_historico",
                "periodo": "1914-04",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "local": "Campo S. Francisco"
            }
        },
        {
            "prompt": "Qual foi o resultado do jogo entre Farense e Vitória Setúbal em Abril de 1914?",
            "completion": "O Farense jogou contra o Vitória Setúbal no dia 5 de Abril de 1914. Na primeira parte, o Farense jogou contra o sol e o vento, conseguindo a equipa setubalense marcar golo. Apesar das dificuldades, foi um encontro memorável na história dos primeiros anos do Farense.",
            "metadata": {
                "tipo": "partido_historico",
                "periodo": "1914-04",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Quantos jogos disputou o Sporting Farense desde o começo de 1914?",
            "completion": "O Sporting Farense realizou dez jogos desde o começo do ano de 1914, obtendo 8 vitórias e 2 empates. Este registo demonstra a superioridade da equipa farense durante esse período.",
            "metadata": {
                "tipo": "estatisticas_historicas",
                "periodo": "1914",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi o primeiro encontro entre Farense e Olhanense?",
            "completion": "O primeiro encontro entre Farense e Olhanense terá acontecido em 4 de Outubro de 1914, em Olhão, no campo da feira, próximo do Matadouro. O conjunto da capital algarvia (Farense) venceu por três bolas a zero. O campo não se encontrava em boas condições.",
            "metadata": {
                "tipo": "partido_historico",
                "periodo": "1914-10",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "local": "Olhão"
            }
        },
        {
            "prompt": "Qual foi o resultado do jogo Farense vs Associação Académica em 20 de Dezembro de 1914?",
            "completion": "Em 20 de Dezembro de 1914, no Largo de S. Francisco, realizou-se um jogo amistoso entre Associação Académica e Sporting Farense. Este encontro contou com uma assistência muito numerosa, demonstrando o grande interesse da população farense pelo futebol.",
            "metadata": {
                "tipo": "partido_historico",
                "periodo": "1914-12",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "local": "Largo de S. Francisco"
            }
        },
        {
            "prompt": "Qual era a reputação do Sporting Farense nos primeiros anos da década de 1910?",
            "completion": "A fama da equipa de futebol do Farense como invencível já tinha ultrapassado as fronteiras da cidade. O clube realizava encontros amistosos com frequência, enfrentando equipas de outras cidades como Sport Lisboa e Lagos, com quem o Farense voltava sempre vitorioso. Esta reputação atraía seleções que queriam desafiar o Farense.",
            "metadata": {
                "tipo": "analise_desempenho",
                "periodo": "1914-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_championship_competition() -> List[Dict[str, Any]]:
    """Extract Q&A about championship and official competitions"""
    return [
        {
            "prompt": "Quando foi a primeira época oficial de futebol em Faro?",
            "completion": "A época oficial de futebol foi inaugurada numa linda tarde de sol primaveril em 30 de Janeiro de 1916. O primeiro jogo foi entre a 1.ª categoria do Sporting Clube Farense e um grupo misto constituído por jogadores de várias equipas, que terminou empatado a duas bolas.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916-01",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi o resultado do primeiro Campeonato de Futebol de Faro?",
            "completion": "A Associação Académica ganhou o primeiro Campeonato de Futebol de Faro. O Sporting Farense foi vencido em primeiras categorias, facto que não acontecia nestes dois últimos anos, incluindo o ano anterior. O jogo foi dirigido por Nunes de Sousa da Boavista de forma imparcial.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi a primeira dissidência interna no Sporting Farense?",
            "completion": "Em 1915, deu-se uma dissidência entre os fundadores do Sporting Farense, que resultou em João Gralho abandonar o clube. Esta foi uma crise interna importante nos primeiros anos da organização.",
            "metadata": {
                "tipo": "historia_crise",
                "periodo": "1915",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "João de Jesus Gralho"
            }
        }
    ]


def extract_regional_context() -> List[Dict[str, Any]]:
    """Extract Q&A about regional football context"""
    return [
        {
            "prompt": "Que outros clubes de futebol existiam em Faro no início do século XX?",
            "completion": "Em 1913 existia em Faro, para além da Associação Académica do Liceu de Faro e do Sporting Clube Farense, a União de Futebol de Faro. Também menciona-se a existência de outras associações desportivas. Havia ainda o Grupo Sportivo Olhanense, formado pouco depois, que disputava encontros com o Sporting Farense.",
            "metadata": {
                "tipo": "contexto_regional",
                "periodo": "1910-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a população de Faro no contexto de desenvolvimento do futebol?",
            "completion": "No início do século XX, a população farense, em especial a alta burguesia nos seus tempos de ócio, tinha interesse no desporto. Os clubes desportivos, após a República, caminhavam aos empurrões, sem organização, limitando-se a atividades pontuais. O ambiente de Faro como capital algarvia e cidade cosmopolita era propício ao desenvolvimento do futebol.",
            "metadata": {
                "tipo": "contexto_social",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a estrutura do futebol em Faro logo após a República (1910)?",
            "completion": "Logo após a República, existia uma organização rudimentar chamada União de Futebol de Faro que não saiu do papel, continuando este organismo com o estigma de indefinição. Os clubes caminhavam sem organização, limitando-se a encontros amistosos. A mudança para uma estrutura competitiva e organizada apenas ocorreria mais tarde, em 1916, com a primeira época oficial.",
            "metadata": {
                "tipo": "contexto_institucional",
                "periodo": "1910-1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_festas_cidade() -> List[Dict[str, Any]]:
    """Extract Q&A about city festivals and football participation"""
    return [
        {
            "prompt": "Qual foi o papel do Sporting Farense nas Festas da Cidade de Faro de 1910?",
            "completion": "Em Junho de 1910, realizaram-se as Festas da Cidade de Faro. De realçar é que integrado nestas festas, para além de um torneio de tiro aos pombos e corridas, realizou-se um encontro de futebol que contou com a participação do Sporting Farense, demonstrando a importância do futebol nas celebrações cívicas da cidade.",
            "metadata": {
                "tipo": "festa_publica",
                "periodo": "1910-06",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "local": "Faro"
            }
        },
        {
            "prompt": "O Sporting Farense participava nas Festas Cívicas de Faro?",
            "completion": "Sim, o Sporting Farense participava nas Festas da Cidade de Faro. Em 1911, repetiram-se as Festas da Cidade no fim de Julho. No dia 29, houve, como no ano anterior, um encontro de futebol que envolveu o Sporting Farense. O futebol tinha um lugar importante nas celebrações públicas da cidade.",
            "metadata": {
                "tipo": "festa_publica",
                "periodo": "1911-07",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_institutional_development() -> List[Dict[str, Any]]:
    """Extract Q&A about institutional development"""
    return [
        {
            "prompt": "Como era a organização do futebol em Faro antes da criação de uma federação?",
            "completion": "O Sporting Clube Farense era o principal clube organizado, mas a estrutura geral do futebol em Faro era desorganizada. A União de Futebol de Faro foi criada com o fim de tentar organizar o futebol, mas não conseguiu implementar-se efetivamente. A Associação de Futebol de Faro posteriormente procurou dar orientação criteriosa e fins bem definidos à organização do futebol local.",
            "metadata": {
                "tipo": "contexto_institucional",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a relação entre as diferentes equipas de futebol em Faro?",
            "completion": "O Sporting Clube Farense era a equipa mais forte e de maior renome. Havia rivalidade entre o Farense e a Associação Académica, sendo ambas as principais equipas de Faro. Existiam também outras equipas e grupos desportivos como o Grupo Desportivo Farense e mais tarde o Grupo Sportivo Olhanense. A competição entre estas entidades era intensa mas amigável.",
            "metadata": {
                "tipo": "contexto_social",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_largo_sao_francisco() -> List[Dict[str, Any]]:
    """Extract Q&A about Largo de São Francisco and early field history"""
    return [
        {
            "prompt": "Como era o Largo de S. Francisco no início do século XX?",
            "completion": "O Largo de S. Francisco era a continuação da Rua com o mesmo nome e constituía um espaço adequado para os primeiros jogos de futebol. Era onde se realizavam os jogos da cidade. Os rapazes faziam as balizas no lado das fábricas e no lado do quartel e passavam os dias a jogar, quer chovesse quer fizesse sol.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Largo de S. Francisco",
                "periodo": "1900-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como se construiu o campo de S. Francisco?",
            "completion": "O campo de S. Francisco foi construído pelos próprios rapazes que o utilizavam. Como diziam: 'construímos o campo de S. Francisco, e digo construímos, porque os operários foram os miúdos'. Este foi um esforço comunitário e coletivo dos jovens farence que queriam ter um espaço adequado para jogar futebol.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Largo de S. Francisco",
                "periodo": "1900-1910",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_military_context() -> List[Dict[str, Any]]:
    """Extract Q&A about military involvement in football"""
    return [
        {
            "prompt": "Qual foi o papel das forças militares no desenvolvimento do futebol em Faro?",
            "completion": "As forças militares tiveram um papel importante. Desde 1895 funcionava na corveta 'Duque de Palmela', fundeada na Ria de Faro, um grupo de marinheiros. O tenente da Marinha de Guerra, Joaquim Costa, era instrutor do Corpo de Marinheiros de Lisboa. Em Maio de 1907, sob o patrocínio do tenente Joaquim Costa e do alferes do Exército José Cortes, realizou-se um jogo inaugural de futebol. Os oficiais das forças militares, especialmente o capitão de Infantaria, Manuel Gomes, participavam ativamente nas atividades desportivas.",
            "metadata": {
                "tipo": "contexto_militar",
                "periodo": "1895-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "Tenente Joaquim Costa"
            }
        },
        {
            "prompt": "Que papel teve a corveta Duque de Palmela no futebol de Faro?",
            "completion": "Desde 1895 funcionava na corveta 'Duque de Palmela', fundeada na Ria de Faro frente às Portas do Mar, um grupo de marinheiros que serviu como base para o desenvolvimento do futebol. O tenente Joaquim Costa, instrutor do Corpo de Marinheiros de Lisboa, organizou o primeiro jogo inaugural de futebol em Maio de 1907, demonstrando que a instituição militar era um veículo importante para a propagação do novo desporto.",
            "metadata": {
                "tipo": "contexto_militar",
                "local": "Corveta Duque de Palmela",
                "periodo": "1895-1907",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_theatrical_context() -> List[Dict[str, Any]]:
    """Extract Q&A about Theatre Lethes and clubhouse history"""
    return [
        {
            "prompt": "Qual era o Teatro Lethes?",
            "completion": "O Teatro Lethes foi a sede social do Sport Lisboa e Faro desde 1931 a 1953. Também serviu como sede do Sporting Farense durante décadas, sendo um local importante na história das instituições desportivas farense.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Teatro Lethes",
                "periodo": "1931-1953",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_academic_associations() -> List[Dict[str, Any]]:
    """Extract Q&A about academic football associations"""
    return [
        {
            "prompt": "Qual era a Associação Académica Farense?",
            "completion": "A Associação Académica Farense era uma equipa do Liceu de Faro. Em 1913 esta associação, anteriormente designada por Sport Clube Académico de Faro, sofreu reformulação. Era composta por estudantes do Liceu e constituía uma equipa forte que competia com o Sporting Farense. Ganhou o primeiro Campeonato de Futebol de Faro em 1916.",
            "metadata": {
                "tipo": "contexto_academico",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_player_names() -> List[Dict[str, Any]]:
    """Extract Q&A about notable players mentioned in early history"""
    return [
        {
            "prompt": "Quem foi António Saraiva?",
            "completion": "António Saraiva foi jogador da Associação Académica Farense nos primeiros anos do futebol farense e mais tarde tornou-se capitão-geral do Sport Lisboa e Faro, demonstrando uma evolução na sua carreira desportiva.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "António Saraiva"
            }
        },
        {
            "prompt": "Quem foi José Correia do Nascimento?",
            "completion": "José Correia do Nascimento foi um antigo jogador da Associação Académica Farense, que atuava nos primeiros anos do futebol organizado em Faro.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "José Correia do Nascimento"
            }
        },
        {
            "prompt": "Quem foi Sales Costa?",
            "completion": "Sales Costa foi um jogador associado à Boavista que reapareceu numa partida contra o Sporting Farense em 1916, há muito tempo sem ser visto em ação desportiva.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "Sales Costa"
            }
        }
    ]


def main():
    """Extract all Q&A pairs and save to JSONL file"""
    all_qa = []

    # Aggregate all extractions
    extractors = [
        extract_founding_history,
        extract_early_matches,
        extract_championship_competition,
        extract_regional_context,
        extract_festas_cidade,
        extract_institutional_development,
        extract_largo_sao_francisco,
        extract_military_context,
        extract_theatrical_context,
        extract_academic_associations,
        extract_player_names
    ]

    for extractor in extractors:
        qa_pairs = extractor()
        all_qa.extend(qa_pairs)
        print(f"✓ {extractor.__name__}: {len(qa_pairs)} pairs")

    print(f"\n{'='*60}")
    print(f"Total Q&A pairs extracted: {len(all_qa)}")
    print(f"{'='*60}\n")

    # Save to JSONL
    output_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/livros_qa_docx_50anos.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in all_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    print(f"✓ Saved to: {output_file}")
    print(f"✓ Total lines: {len(all_qa)}")


if __name__ == "__main__":
    main()
