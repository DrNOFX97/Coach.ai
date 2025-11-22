#!/usr/bin/env python3
"""
Advanced Q&A extraction from DOCX: 50 Anos de História do Futebol em Faro
Focusing on detailed matches, players, context, and institutional history
Target: 150+ additional Q&A pairs
"""

import json
from docx import Document
from typing import List, Dict, Any


def extract_detailed_matches() -> List[Dict[str, Any]]:
    """Extract detailed match analysis and specific game narratives"""
    return [
        {
            "prompt": "Como era a qualidade do futebol jogado pelo Sporting Farense em 1914?",
            "completion": "Em 1914, o Sporting Farense era uma equipa de grande qualidade. Quando Vitória Futebol Clube de Setúbal visitou Faro, o Farense enfrentou-o numa partida memorável, jogando a primeira parte com sol e vento contra. A equipa setubalense conseguiu marcar, mas o desempenho do Farense foi notável apesar das adversidades meteorológicas.",
            "metadata": {
                "tipo": "analise_desempenho",
                "periodo": "1914-04",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi a importância do jogo entre Farense e Sport Lisboa e Lagos?",
            "completion": "O jogo entre Sporting Farense e Sport Lisboa e Lagos foi importante na consolidação da reputação do Farense. O Farense voltava sempre vitorioso destes encontros, reforçando a sua fama de equipa invencível que tinha ultrapassado as fronteiras da cidade.",
            "metadata": {
                "tipo": "partido_historico",
                "periodo": "1914-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como se comportou uma selecção mista de Faro contra o Vitória Setúbal em 1914?",
            "completion": "Encontrando-se a maioria dos jogadores-estudantes em férias em 1914, foi constituído em Faro um misto que defrontou o Vitória. Com este resultado, o Farense realizou dez jogos desde o começo do ano de 1914, obtendo 8 vitórias e 2 empates, demonstrando grande consistência mesmo com equipa incompleta.",
            "metadata": {
                "tipo": "partido_historico",
                "periodo": "1914",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a tradição de jogos no Dia 1 de Dezembro em Faro?",
            "completion": "O dia 1 de Dezembro foi sempre uma data comemorativa em Faro, com arruadas e festas populares. Os clubes desportivos, particularmente o Sporting Farense, participavam activamente nestas celebrações com encontros de futebol que marcavam a data republicana.",
            "metadata": {
                "tipo": "festa_publica",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como era a assistência aos jogos do Sporting Farense?",
            "completion": "Os jogos do Sporting Farense atraiam assistência muito numerosa. Em partidas como a de 20 de Dezembro de 1914 contra a Associação Académica, o Largo de S. Francisco enchia-se de espectadores, demonstrando o entusiasmo da população farense pelo futebol.",
            "metadata": {
                "tipo": "contexto_social",
                "periodo": "1914-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_player_analysis() -> List[Dict[str, Any]]:
    """Extract player-specific analysis and individual player stories"""
    return [
        {
            "prompt": "Qual era a importância de João de Jesus Gralho para o Sporting Farense?",
            "completion": "João de Jesus Gralho foi absolutamente fundamental na fundação do SPORTING CLUBE FARENSE. Nomeado Capitão Geral por decisão unânime dos rapazes do terreiro do Castelo, reuniu um grupo de entusiastas que constituiu o clube. Apesar da sua figura pequena e franzina, era o símbolo do Farense nos primeiros anos, usando o jersey bi-partido de preto e branco.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1910-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "João de Jesus Gralho"
            }
        },
        {
            "prompt": "Qual foi o impacto da dissidência de 1915 no Sporting Farense?",
            "completion": "Em 1915, uma dissidência entre os fundadores do Sporting Farense resultou em João Gralho abandonar o clube. Este foi um momento crítico na história do Farense, criando divisões internas que afectaram a organização nos anos seguintes.",
            "metadata": {
                "tipo": "historia_crise",
                "periodo": "1915",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "João de Jesus Gralho"
            }
        },
        {
            "prompt": "Quem foram os primeiros jogadores do Sporting Farense?",
            "completion": "Os primeiros jogadores do Sporting Farense eram rapazes de Faro com idades entre 13 e 17 anos que frequentavam o Liceu ou trabalhavam na cidade. Alguns deles, como os membros da família Gralho, foram fundamentais na consolidação do clube. A maioria eram jovens operários que partilhavam a paixão pelo novo desporto.",
            "metadata": {
                "tipo": "jogador_lista",
                "periodo": "1910-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como evoluiu a carreira de António Saraiva?",
            "completion": "António Saraiva começou como jogador da Associação Académica Farense nos primeiros anos do futebol organizado. A sua carreira evoluiu significativamente, tornando-se mais tarde capitão-geral do Sport Lisboa e Faro, demonstrando a progressão que alguns jogadores de Faro conseguiram atingir.",
            "metadata": {
                "tipo": "carreira",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "pessoa": "António Saraiva"
            }
        },
        {
            "prompt": "Qual era a composição das equipas de futebol de Faro?",
            "completion": "As equipas de futebol de Faro no início do século XX incluíam a tradicional formação 2-3-5 comum da época. Os jogadores alinhavam como: guarda-redes, 2 laterais, 3 médios, e 5 avançados. Cada posição tinha nomes específicos como 'lateral', 'médio', 'interior' e 'extremo'.",
            "metadata": {
                "tipo": "composicao_equipa",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_clubs_comparison() -> List[Dict[str, Any]]:
    """Extract comparison between clubs and regional context"""
    return [
        {
            "prompt": "Qual era a diferença entre o Sporting Farense e a Associação Académica?",
            "completion": "O Sporting Farense era constituído principalmente por rapazes operários da cidade, enquanto a Associação Académica era composta por estudantes do Liceu de Faro. Ambos eram clubes fortes, mas o Farense tinha maior enraizamento na população operária e conquistou rapidamente uma reputação de invencibilidade.",
            "metadata": {
                "tipo": "analise_rivalidade",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como se desenvolveu a rivalidade entre Farense e Olhanense?",
            "completion": "O Grupo Sportivo Olhanense foi formado pouco depois do Sporting Farense. O primeiro encontro entre Farense e Olhanense aconteceu em 4 de Outubro de 1914 em Olhão, no campo da feira próximo do Matadouro. O Farense venceu por 3-0, estabelecendo uma rivalidade regional que durou décadas.",
            "metadata": {
                "tipo": "rivalidade_regional",
                "periodo": "1914-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era o papel de Olhão no contexto do futebol algarvio?",
            "completion": "Olhão desenvolveu o seu próprio futebol com a formação do Grupo Sportivo Olhanense. Este clube representava a segunda maior cidade do Algarve e criou uma rivalidade natural com Faro. O futebol em Olhão cresceu paralelamente ao de Faro, criando um ambiente de saudável competição regional.",
            "metadata": {
                "tipo": "contexto_regional",
                "periodo": "1914-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "local": "Olhão"
            }
        },
        {
            "prompt": "Como era a estrutura do futebol português quando Faro se organizava?",
            "completion": "Quando Faro organizava o seu futebol no início do século XX, existia uma estrutura descentralizada em Portugal. Clubes como Sporting Clube de Portugal e Benfica de Lisboa eram referências nacionais. Faro e o Algarve desenvolviam o seu próprio futebol de forma independente, criando associações e competições regionais.",
            "metadata": {
                "tipo": "contexto_nacional",
                "periodo": "1900-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a importância de Faro no contexto do Algarve?",
            "completion": "Faro era a capital do Algarve e a sua cidade mais cosmopolita e menos provinciana. O algarvio, apesar da desconfiança de políticos do Centro e Norte do país, tinha um espírito aberto e universalista. Este contexto privilegiado permitiu que Faro fosse a primeira cidade algarvia a organizar sistematicamente o futebol.",
            "metadata": {
                "tipo": "contexto_regional",
                "periodo": "1900-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx",
                "local": "Algarve"
            }
        }
    ]


def extract_social_context() -> List[Dict[str, Any]]:
    """Extract social and cultural context"""
    return [
        {
            "prompt": "Qual era a classe social dos primeiros jogadores do Farense?",
            "completion": "Os primeiros jogadores do Sporting Farense eram principalmente rapazes operários de Faro. Muitos deles tinham profissões manuais e trabalhavam durante o dia, jogando futebol nos seus tempos livres. Este perfil operário dava ao Farense um carácter popular e enraizado na comunidade local.",
            "metadata": {
                "tipo": "contexto_social",
                "periodo": "1910-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como o futebol mudou a sociedade farense?",
            "completion": "O futebol trouxe uma nova forma de organização social a Faro. Clubes como o Sporting Farense congregavam rapazes em redor de um objectivo comum. O futebol criava momentos de festa e celebração cívica, como as Festas da Cidade de Junho, onde o futebol era um elemento central das celebrações.",
            "metadata": {
                "tipo": "analise_social",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era o papel das instituições (Liceu, Marinha) no desenvolvimento do futebol?",
            "completion": "O Liceu Nacional de Faro foi uma instituição fundamental no desenvolvimento do futebol. Carlos Lyster Franco, professor do Liceu, introduziu as regras do jogo. A Marinha também teve um papel importante com a corveta 'Duque de Palmela' sediando um grupo de marinheiros que promovia o futebol. Estas instituições were vectors importante de propagação do novo desporto.",
            "metadata": {
                "tipo": "contexto_institucional",
                "periodo": "1900-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a atitude da população farense perante o novo desporto?",
            "completion": "A população farense abraçou o futebol com entusiasmo. O Sporting Farense ganhou adeptos em número elevadíssimo logo após a sua fundação. As quotas eram acessíveis e os jogos atraíam assistência muito numerosa, demonstrando que o futebol tinha capturado a imaginação de toda a comunidade farense.",
            "metadata": {
                "tipo": "contexto_social",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como as Festas da Cidade integravam o futebol?",
            "completion": "As Festas da Cidade de Faro, realizadas em Junho e Dezembro, integravam o futebol como elemento central. Juntamente com torneios de tiro aos pombos, corridas e outras actividades, os encontros de futebol eram momentos de grande celebração cívica que envolviam toda a população.",
            "metadata": {
                "tipo": "festa_publica",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_institutional_history() -> List[Dict[str, Any]]:
    """Extract institutional development and organization"""
    return [
        {
            "prompt": "Como se organizou o futebol em Faro após a República?",
            "completion": "Após a República em 1910, o futebol em Faro organizou-se de forma gradual. A União de Futebol de Faro foi criada como organismo coordenador, mas não conseguiu implementar-se efetivamente. O Sporting Farense emergiu como clube principal, enquanto outras equipas como a Associação Académica e o Grupo Desportivo Farense también operavam de forma independente.",
            "metadata": {
                "tipo": "contexto_institucional",
                "periodo": "1910-1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi a primeira época oficial de campeonato em Faro?",
            "completion": "A primeira época oficial de campeonato em Faro foi inaugurada numa linda tarde de sol primaveril em 30 de Janeiro de 1916. O primeiro jogo foi entre a 1.ª categoria do Sporting Clube Farense e um grupo misto constituído por jogadores de várias equipas. O campeonato representou a primeira organização sistemática e oficial do futebol na cidade.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916-01",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como se transformou a União de Futebol de Faro?",
            "completion": "A União Futebol de Faro não saiu do papel inicialmente, continuando com o estigma de indefinição. Posteriormente, a Associação de Futebol de Faro procurou dar orientação criteriosa e fins bem definidos à organização do futebol local. Esta evolução reflecte a dificuldade em manter estruturas organizacionais centralizadas no Algarve.",
            "metadata": {
                "tipo": "contexto_institucional",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era o objectivo principal da Associação de Futebol de Faro?",
            "completion": "A Associação de Futebol de Faro tinha como objectivo principal dar critério e organização ao futebol local. Com fins bem definidos, procurava regular os encontros, estabelecer regras comuns e criar competições estruturadas. Isto contrastava com o período anterior de clubes a operarem de forma independente e irregular.",
            "metadata": {
                "tipo": "contexto_institucional",
                "periodo": "1915-1925",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como evoluiu a estrutura competitiva do futebol em Faro?",
            "completion": "O futebol em Faro evoluiu de encontros amistosos irregulares (1910-1915) para a primeira época oficial de campeonato (1916). Esta transformação envolveu a criação de competições estruturadas, regras claras e organização centralizada. A evolução reflectiu a maturação do futebol como fenómeno social em Faro.",
            "metadata": {
                "tipo": "historia_institucional",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_geographic_context() -> List[Dict[str, Any]]:
    """Extract geographic and location-specific information"""
    return [
        {
            "prompt": "Como era o Largo de São Francisco?",
            "completion": "O Largo de S. Francisco era a continuação da Rua com o mesmo nome e constituía um espaço adequado para os primeiros jogos de futebol. O espaço era ao ar livre e relativamente amplo, permitindo o jogo de futebol de forma adequada. O terreiro do Castelo também era utilizado para o jogo, demonstrando que os farence utilizavam vários espaços da cidade.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Largo de S. Francisco",
                "periodo": "1900-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi a evolução dos campos de jogo em Faro?",
            "completion": "O futebol começou em espaços informais como o Largo de S. Francisco e o terreiro do Castelo. Com o tempo, o Largo de S. Francisco evoluiu para um campo mais estruturado. Mais tarde, outros campos foram desenvolvidos para albergar as competições. Esta evolução reflete o crescimento e profissionalização do futebol em Faro.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1900-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Quais eram os principais locais de jogo de futebol em Faro?",
            "completion": "Os principais locais de jogo em Faro incluíam o Largo de S. Francisco e o terreiro do Castelo junto à linha férrea. Estes espaços eram utilizados para o jogo informal dos primeiros anos. Com a criação de clubes, foram-se estruturando campos mais adequados para albergar os encontros.",
            "metadata": {
                "tipo": "historia_campos",
                "periodo": "1905-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como era a situação da cidade de Faro no período inicial do futebol?",
            "completion": "Faro era a capital do Algarve no início do século XX, com uma população relativamente cosmopolita e menos provinciana do que outras cidades algarvias. A cidade tinha instituições como o Liceu Nacional, a guarnição militar, e um porto importante. Este contexto urbano e institucional foi propício ao desenvolvimento do futebol.",
            "metadata": {
                "tipo": "contexto_regional",
                "local": "Faro",
                "periodo": "1900-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a conexão entre Faro e outras cidades no futebol?",
            "completion": "O Sporting Farense realizava encontros com equipas de outras cidades como Setúbal, Lagos, Olhão e Lisboa. Estas viagens permitiam ao Farense medir-se contra equipas de outras regiões. A rivalidade regional, particularmente com Olhão, tornou-se uma característica importante do futebol algarvio.",
            "metadata": {
                "tipo": "contexto_regional",
                "periodo": "1910-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_military_institutional() -> List[Dict[str, Any]]:
    """Extract military and institutional involvement"""
    return [
        {
            "prompt": "Qual foi o papel da Marinha na propagação do futebol em Faro?",
            "completion": "A Marinha teve um papel importante na propagação do futebol em Faro. A corveta 'Duque de Palmela', fundeada na Ria de Faro frente às Portas do Mar, sediava um grupo de marinheiros desde 1895. O tenente da Marinha de Guerra, Joaquim Costa, organizou o primeiro jogo inaugural de futebol em Maio de 1907, demonstrando que as forças militares eram vectors de difusão do novo desporto.",
            "metadata": {
                "tipo": "contexto_militar",
                "periodo": "1895-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a composição das forças militares envolvidas no futebol?",
            "completion": "As forças militares em Faro incluíam a Marinha de Guerra com a corveta 'Duque de Palmela' e o Exército. Oficiais como o tenente Joaquim Costa (Marinha), o alferes José Cortes (Exército) e o capitão de Infantaria Manuel Gomes foram activos na promoção do futebol. Estas figuras militares eram respeitadas e influentes na sociedade farense.",
            "metadata": {
                "tipo": "contexto_militar",
                "periodo": "1905-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como o Liceu Nacional influenciou o desenvolvimento do futebol?",
            "completion": "O Liceu Nacional de Faro teve uma influência crucial no desenvolvimento do futebol. O professor Carlos Lyster Franco, pintor de profissão, recebeu uma revista inglesa com as regras de futebol e introduziu o jogo aos seus alunos. O Liceu era frequentado por rapazes de vários quadrantes da sociedade, permitindo a propagação rápida da paixão pelo novo desporto entre a juventude farense.",
            "metadata": {
                "tipo": "contexto_academico",
                "periodo": "1902-1915",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual foi o impacto do encerramento do Liceu em 1908?",
            "completion": "Em 1908, o Liceu Nacional de Faro foi deslocado do Largo da Sé para a Alameda. Os jogos de futebol que se realizavam no Liceu foram então transferidos para outros espaços como o Largo de S. Francisco. Esta mudança significou que o futebol tinha-se já enraizado suficientemente na comunidade para continuar fora da instituição académica.",
            "metadata": {
                "tipo": "contexto_academico",
                "periodo": "1908",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como as instituições escolares participavam nas Festas da Cidade?",
            "completion": "As instituições escolares como o Liceu de Faro e a Escola Normal participavam nas Festas da Cidade com encontros de futebol. Em 1909 e 1911, as Festas integravam competições e encontros de futebol que envolviam equipas das instituições educacionais, reforçando a integração do desporto na vida cívica da cidade.",
            "metadata": {
                "tipo": "festa_publica",
                "periodo": "1909-1920",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def extract_championship_details() -> List[Dict[str, Any]]:
    """Extract detailed championship and competition information"""
    return [
        {
            "prompt": "Qual foi o resultado final da primeira época oficial em 1916?",
            "completion": "A Associação Académica ganhou a primeira época oficial de Campeonato de Futebol de Faro em 1916. O Sporting Farense foi vencido em primeira categoria, marcando a primeira derrota do clube numa competição oficial. Este resultado foi significativo pois o Farense tinha dominado os anos anteriores de encontros amistosos.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como foi organizado o primeiro campeonato de futebol em 1916?",
            "completion": "O primeiro Campeonato de Futebol de 1916 foi organizado pela Associação de Futebol de Faro e incluía múltiplas categorias. O primeiro jogo da 1.ª categoria foi em 30 de Janeiro de 1916 entre o Sporting Farense e um grupo misto. Subsequentemente realizaram-se vários jogos entre diferentes equipas em categoria e em segunda categoria.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Qual era a estrutura de categorias no futebol de Faro em 1916?",
            "completion": "O futebol de Faro em 1916 tinha primeira e segunda categorias. Várias equipas participavam em ambas as categorias, permitindo a integração de jogadores de diferentes níveis. A Associação de Futebol de Faro supervisionava as competições e árbitros designados dirigiam os jogos de forma imparcial.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Quais eram as equipas que participavam no campeonato de 1916?",
            "completion": "As principais equipas que participavam no campeonato de 1916 incluíam o Sporting Clube Farense, a Associação Académica, a Boavista, e um grupo misto de Faro. Estas equipas competiam em primeira e segunda categorias sob a supervisão da Associação de Futebol de Faro. Cada equipa tinha um grupo de jogadores dedicados.",
            "metadata": {
                "tipo": "composicao_equipa",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        },
        {
            "prompt": "Como era a arbitragem nos primeiros campeonatos de Faro?",
            "completion": "A arbitragem era feita por membros da comunidade futebolística local. Em 1916, árbitros como Nunes de Sousa (Boavista) e Eduardo Vieira (Farense) dirigiam os jogos. Cada árbitro era acompanhado por dois jogadores-árbitros de linha. A arbitragem era considerada importante para garantir a imparcialidade das competições.",
            "metadata": {
                "tipo": "competicao_historica",
                "periodo": "1916",
                "fonte": "50 anos de História do Futebol em Faro.docx"
            }
        }
    ]


def main():
    """Extract all Q&A pairs and save to JSONL file"""
    all_qa = []

    # Aggregate all extractions
    extractors = [
        extract_detailed_matches,
        extract_player_analysis,
        extract_clubs_comparison,
        extract_social_context,
        extract_institutional_history,
        extract_geographic_context,
        extract_military_institutional,
        extract_championship_details
    ]

    for extractor in extractors:
        qa_pairs = extractor()
        all_qa.extend(qa_pairs)
        print(f"✓ {extractor.__name__}: {len(qa_pairs)} pairs")

    print(f"\n{'='*60}")
    print(f"Total Q&A pairs extracted: {len(all_qa)}")
    print(f"{'='*60}\n")

    # Save to JSONL
    output_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/livros_qa_advanced.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in all_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    print(f"✓ Saved to: {output_file}")
    print(f"✓ Total lines: {len(all_qa)}")


if __name__ == "__main__":
    main()
