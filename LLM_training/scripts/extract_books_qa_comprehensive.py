#!/usr/bin/env python3
"""
Extração COMPLETA e ABRANGENTE de Q&A pares dos livros históricos.
Objetivo: Extrair DEZENAS de pares, não apenas 17.

Cobertura:
- Fundação e primeiros anos (1905-1914)
- Primeiras equipas e composições
- Personalidades históricas (jogadores e dirigentes)
- Equipamentos e uniformes
- Rivalidades regionais (Olhanense, Lisboa e Faro, Lusitano)
- Partidas memoráveis (8+)
- Desenvolvimento regional (associações, campeonatos)
- Anedotas e histórias
- Estatísticas e records
"""

import json
from pathlib import Path
from typing import List, Dict, Any

def extract_comprehensive_qa() -> List[Dict[str, Any]]:
    """Extract comprehensive Q&A pairs from historical books."""
    pairs = []

    # ==================== FUNDAÇÃO (1905-1910) ====================

    pairs.append({
        "prompt": "Quando foi fundado o Sporting Clube Farense?",
        "completion": "O Sporting Clube Farense foi fundado a 1 de Abril de 1910, coroando um longo esforço de entusiastas do futebol em Faro.",
        "metadata": {"tipo": "historia_fundacao", "data": "1910-04-01", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Por que o Sporting Clube Farense recebeu este nome?",
        "completion": "O nome foi aceite por unanimidade pelos jogadores da nova associação desportiva, pelo simples facto de terem grande admiração e simpatia pelo Sporting Clube de Portugal.",
        "metadata": {"tipo": "historia_fundacao", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual foi a origem do equipamento do Sporting Clube Farense?",
        "completion": "A camisola do Sporting Club de Lisboa, antes de ser às listas verdes e brancas, era bipartida no sentido longitudinal (metade esquerda verde, direita branca). Como os rapazes de Faro só dispunham de fotografias a preto e branco, optaram pelo jersey alvi-negro com calções pretos, que se tornou a identidade visual do clube.",
        "metadata": {"tipo": "historia_uniformes", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como era o futebol em Faro antes de 1910?",
        "completion": "O futebol começou em Faro por volta de 1905, de forma muito rudimentar. Os primeiros jogadores compraram uma bola com uma dádiva de uma libra de ouro do bispo D. António Barbosa Leão e começaram a jogar no Largo da Sé, depois no Largo de S. Francisco. As balizas eram improvisadas, o campo era muito rudimentar, mas o entusiasmo era absoluto.",
        "metadata": {"tipo": "historia_inicial", "periodo": "1905-1910", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual era o contexto de Faro quando o Sporting Clube Farense foi fundado?",
        "completion": "Faro era a capital do Algarve e a sua cidade mais cosmopolita e menos provinciana. O algarvio, apesar da desconfiança de políticos do Centro e Norte do país, sempre teve um espírito aberto e universalista, chegando até a considerar Lisboa apenas 'a maior aldeia de Portugal'.",
        "metadata": {"tipo": "contexto_historico", "periodo": "1910", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como se comparava o Sporting Clube Farense com outros clubes algarvios na época de fundação?",
        "completion": "O Sporting Clube Farense era um dos mais longevos da província e certamente o decano de quantos ainda hoje praticam o futebol. O Sporting Clube Olhanense foi fundado em 27 de Abril de 1912 (2 anos depois), o Clube de Futebol Esperança de Lagos em 20 de Setembro de 1912, o Portimonense em 14 de Agosto de 1914, e o Lusitano em 15 de Abril de 1916.",
        "metadata": {"tipo": "historia_regional", "periodo": "1910-1920", "fonte": "livro_scf_1.txt"}
    })

    # ==================== PRIMEIRAS EQUIPAS (1910-1915) ====================

    pairs.append({
        "prompt": "Qual era a composição da primeira equipa do Sporting Clube Farense?",
        "completion": "Segundo Manuel de Sousa, a composição da equipa-base do Farense por volta de 1912 era: João Rodrigues (guarda-redes); Guerrilha (defesa-direito), Manuel de Sousa (defesa-esquerdo); José Teixeira (meio-campo-direito), Manuel Tavares da Cruz (meio-campo-centro), José Aleixo (meio-campo-esquerdo); Francisco Lima ou Eduardo Vieira (avançado-direito), António Marcos (meio-avançado-direito), João Gralho (avançado-centro), Bento (meio-avançado-esquerdo), José Nugas (avançado-esquerdo).",
        "metadata": {"tipo": "composicao_equipa", "periodo": "1912", "fonte": "livro_scf_1.txt", "pessoas": ["João Rodrigues", "Manuel de Sousa", "Guerrilha", "José Teixeira", "Manuel Tavares da Cruz", "José Aleixo", "Francisco Lima", "Eduardo Vieira", "António Marcos", "João Gralho", "Bento", "José Nugas"]}
    })

    pairs.append({
        "prompt": "Qual era a outra composição alternativa da primeira equipa, segundo José Nugas?",
        "completion": "Segundo José Nugas, outra composição das primeiras equipas era: João Rodrigues (guarda-redes); José Aleixo (defesa-direito), Manuel de Sousa (defesa-esquerdo); Eduardo Ventura (meio-campo-direito), Albino (meio-campo-centro), Guerrilha (meio-campo-esquerdo); Francisco Lima (avançado-direito), José Gralho (meio-avançado-direito), João Gralho (avançado-centro), Teixeira (meio-avançado-esquerdo), José Nugas (avançado-esquerdo). Havia ainda outros jogadores que alinhavam alternadamente como José de Sousa Ferradeira, Manuel Tavares da Cruz e João Gregório.",
        "metadata": {"tipo": "composicao_equipa", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Quais eram as profissões dos primeiros jogadores do Sporting Clube Farense?",
        "completion": "Os primeiros jogadores do Farense tinham origens plebéias: João Rodrigues era soldador da fábrica Coelho; Manuel de Sousa era filho de moleiros do moinho da Torrinha; José Aleixo trabalhava com o pai no comércio de frutos; Eduardo Ventura era marceneiro; Albino era ferroviário; Guerrilha era sapateiro; Francisco Lima era despachante de alfândega; João Gralho era fundidor; José Gralho trabalhava na fundição do Pimenta; Teixeira era factor dos Caminhos de Ferro; José de Sousa Ferradeira era canteiro (depois professor); João Gregório era marinheiro.",
        "metadata": {"tipo": "historia_social", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Que alcunhas tinham os jogadores do Farense nos primeiros tempos?",
        "completion": "Os jogadores tinham alcunhas saborosas: Francisco Lima era 'Paquito'; José Bento era 'Calefactor' ou 'Calfador'; Eduardo Ventura era 'Eduardo Torto'; Manuel Tavares da Cruz era 'Manuel Arcado' ou 'Arcado'; José Aleixo era 'José da Avó'; João Rodrigues era 'João Cacana'.",
        "metadata": {"tipo": "jogador_alcunha", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como eram os custos de ser jogador do Farense nos primeiros tempos?",
        "completion": "Não havia jogadores profissionais no Farense, nem ordenados elevados, nem 'luvas' ou prémios de jogo. Os jogadores compravam o próprio equipamento e pagavam uma quota de 30 réis por mês (ou 5 réis semanais, conforme diferentes depoimentos).",
        "metadata": {"tipo": "historia_financeira", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    # ==================== FAMÍLIA GRALHO ====================

    pairs.append({
        "prompt": "Qual foi a importância da família Gralho para o Sporting Clube Farense?",
        "completion": "A família Gralho teve papel fundamental: João Gralho (por volta de 1909/10) foi o grande promotor da criação do clube e seu principal impulsionador. Seu irmão José de Jesus também jogava na linha avançada, e Joaquim (o 'terceiro homem') foi um jogador excepcional. António Gralho (quarto irmão) tornou-se um dos melhores marcadores do Sporting de Lisboa e foi chamado para a seleção nacional. Jorge Gralho (quinto irmão) esteve em grande evidência nos anos 30. Walter (filho de José de Jesus) e Jorge Jr. (filho de António) também vestiram a camisola alvi-negra.",
        "metadata": {"tipo": "familia_historia", "pessoa": "Família Gralho", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Por que João Gralho deixou o Sporting Clube Farense?",
        "completion": "João Gralho, primeiro capitão e grande dinamizador do Farense, foi convencido a transferir-se para o Vitória de Setúbal. O clube sadino ficou muito impressionado com o dinâmico primeiro capitão e com a sua facilidade de remate. Segundo o ditado popular 'santos de casa não fazem milagres', preferiu 'ir pregar para outra freguesia', transferindo-se com as suas botas e ferramentas de soldador.",
        "metadata": {"tipo": "jogador_transferencia", "pessoa": "João Gralho", "periodo": "1914-1917", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual foi a carreira de Joaquim Gralho fora do Farense?",
        "completion": "Joaquim Gralho, conhecid o como o 'terceiro homem', foi para o Olhanense e chegou a ser convidado para envergar a camisola das quinas (seleção portuguesa), mas o selecionador o preteriu a favor de João Francisco do Sporting de Lisboa. Era pequeno, franzino, mas com uma génio e habilidade diabólicas, esgueirando-se como uma enguia e poucos defesas conseguindo aguentá-lo. Uma máquina de fazer golos.",
        "metadata": {"tipo": "jogador_historia", "pessoa": "Joaquim Gralho", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como foi a carreira de António Gralho após deixar Faro?",
        "completion": "António Gralho, quarto irmão, quando chamado ao serviço militar em Lisboa, ingressou no Sporting Club de Portugal onde se cotou como o melhor marcador da equipa leonina. Foi chamado para fazer parte da seleção nacional. Há quem o considere o mais eminente de todos os Gralhos por ter tido mais possibilidades e estar mais em evidência.",
        "metadata": {"tipo": "jogador_historia", "pessoa": "António Gralho", "fonte": "livro_scf_1.txt"}
    })

    # ==================== ANTÓNIO GAGO ====================

    pairs.append({
        "prompt": "Qual foi o papel de António Gago na história do Sporting Clube Farense?",
        "completion": "António Gago revitalizou o Farense por volta de 1917, quando o clube estava em fase depressiva após a partida de João Gralho. Era empregado da mercearia Sequerra antes de trabalhar por conta própria. Como capitão, treinador e orientador técnico, conquistou os Campeonatos do Algarve nas épocas de 1917/18 e 1921/22. Jogou largos anos no posto de ponta-direita, chegando a alinhar até aos 34 anos.",
        "metadata": {"tipo": "jogador_historia", "pessoa": "António Gago", "periodo": "1917-1925", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Quais eram as características do jogo de António Gago?",
        "completion": "António Gago era muito rápido (tinha praticado atletismo em 100m, 200m e 1.500m). Corria pela linha lateral, chutando para a frente e cobrindo bem a bola, após o que centrava com muita eficiência. Sua grande especialidade eram os 'golos directos de comer'. Como capitão, demonstrava grande liderança e responsabilidade.",
        "metadata": {"tipo": "jogador_tecnica", "pessoa": "António Gago", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Quais eram os outros jogadores que António Gago destacava como grandes?",
        "completion": "António Gago destacava: Joaquim Gralho (avançado-centro, cerca de 1921/22) - esgueirando-se como uma enguia, poucos defesas conseguindo aguentar, máquina de fazer golos; Luís Madeira - guardião acrobático e desassombrado; Eduardo Vieira - verdadeiro modelo de correcção em campo, temível ponta-esquerda; Almeida Coelho - hábil interior direito ou esquerdo, adepto do jogo aberto e em profundidade; José Gralho - ponta-esquerda de respeito, experiente com jogadas bem urdidas.",
        "metadata": {"tipo": "jogador_lista", "periodo": "1918-1925", "fonte": "livro_scf_1.txt"}
    })

    # ==================== VIAGENS E PARTIDAS (1914-1920) ====================

    pairs.append({
        "prompt": "Como foi a ida do Farense a Setúbal em 1914?",
        "completion": "Uma seleção de Faro se deslocou a Setúbal em 1914 para disputar dois encontros contra os melhores futebolistas locais. Venceu o primeiro por 4-3 e perdeu o outro por 4-0. Dessa seleção faziam parte 10 jogadores do Farense, atestando bem a hegemonia regional e até nacional dos leões de Faro. O Farense era capaz de se bater de igual para igual com a Escola Académica de Lisboa, Liceu da Lapa, Pupilos do Exército, Casa Pia, Barreirense e Vitória de Setúbal.",
        "metadata": {"tipo": "partido_historico", "periodo": "1914", "local": "Setúbal", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como foi a viagem do Farense a Loulé em 1917-1918?",
        "completion": "O Farense participou num encontro que se integrava na Festa de Nossa Senhora da Piedade em Loulé. A viagem foi feita em carro de mula ('carroça atrelada à azémola'). Na subida final para Loulé, a mula recusou-se a dar mais um passo, e o Farense teve de fazer o derradeiro troço a pé. Os louletanos, muito bairristas, tinham contratado todos os bons jogadores das redondezas para enfrentar o Farense, mas o 'furacão farense' foi impotente e só apanharam 'duas ou três bolinhas'.",
        "metadata": {"tipo": "partido_historico", "periodo": "1917-1918", "local": "Loulé", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "O que aconteceu na viagem do Farense a Beja em 1917-1918?",
        "completion": "O Farense foi convidado para disputar dois jogos em Beja, com promessa de pagamento de passagens e estadia. Quando chegaram, o chefe da estação dos Caminhos de Ferro não tinha recebido comunicação, e o Farense teve de pagar bilhetes de bolso (só de ida). No primeiro dia, venceram o Águias Futebol Clube por 3-1, e no segundo dia desfizeram 'Os Onze Amigos' por 13-0. Os organizadores, vexados, não quiseram reembolsar nem pagar o regresso. Só com ajuda de um amigo residente em Beja chamado Góinhas conseguiram voltar.",
        "metadata": {"tipo": "partido_historico", "periodo": "1917-1918", "local": "Beja", "fonte": "livro_scf_1.txt", "resultados": ["3-1", "13-0"]}
    })

    pairs.append({
        "prompt": "Como foi o jogo entre Farense e Casa Pia em 1920?",
        "completion": "Em 1920, o Casa Pia (campeão de Lisboa) regressava de Sevilha e ficou bloqueado em Tunes devido a uma greve dos ferroviários. Obrigados a pernoitar em Faro, foram contactados pelos dirigentes do clube algarvio. No dia seguinte disputaram um desafio onde o Casa Pia venceu o Farense por 3-1. Este encontro foi importante porque mostrava que mesmo o campeão de Lisboa era capaz de derrotar a potência algarvia.",
        "metadata": {"tipo": "partido_historico", "periodo": "1920", "local": "Faro", "fonte": "livro_scf_1.txt", "resultado": "3-1"}
    })

    pairs.append({
        "prompt": "Como era a situação do Farense em 1914 em termos de competição?",
        "completion": "Segundo notícia do jornal 'O Sport Lisboa' de 5 de Setembro de 1914: 'Realizou-se no domingo, 23, no campo de S. Francisco, um desafio entre um grupo misto e o 1.º grupo do Sporting Clube Farense, saindo este vencedor por 6-0. O Sporting, desde o começo do ano até ao dia 23 de Agosto, jogou dez desafios de futebol, obtendo: vitórias 8, empates 1, derrotas 1, bolas a favor 34, bolas contra 6'.",
        "metadata": {"tipo": "partido_historico", "periodo": "1914", "fonte": "livro_scf_1.txt", "resultado": "6-0"}
    })

    pairs.append({
        "prompt": "Como foi a visita do Vitória de Setúbal a Faro?",
        "completion": "O Vitória de Setúbal visitou o Campo de S. Francisco. Durante a breve estadia, os sadinos bateram com facilidade a Associação Académica local (num sábado), e foram vencidos espectacularmente no domingo seguinte por um Farense em plena forma que 'dava cartas'.",
        "metadata": {"tipo": "partido_historico", "periodo": "1914", "local": "Faro", "fonte": "livro_scf_1.txt"}
    })

    # ==================== RIVALIDADE COM OLHANENSE (1918-1924) ====================

    pairs.append({
        "prompt": "O que aconteceu no jogo do Farense em Olhão em 1918?",
        "completion": "Em 1918, o Farense deslocou-se a Olhão com uma equipa reduzida e desfalcada (muitos elementos das reservas com desculpas). Foram vaiados desde o início, respirando-se uma atmosfera de massacre. Mas conseguiram estruturar bem o conjunto, baseando o jogo na defesa sólida e contra-ataques rápidos. Venceram pela marca retumbante de 6-1. Depois, a multidão fanatizada pela 'futebolite' aguda preparava-se para espancar o Farense. Só conseguiram livrar-se correndo para a Estação da CP em 'correria desenfreada'.",
        "metadata": {"tipo": "partido_historico", "periodo": "1918", "local": "Olhão", "fonte": "livro_scf_1.txt", "resultado": "6-1"}
    })

    pairs.append({
        "prompt": "Como foi o jogo de meia-final entre Farense e Olhanense a 28 de Maio de 1922?",
        "completion": "Farense e Olhanense defrontaram-se em Olhão numa crucial meia-final do Campeonato do Algarve. O Farense tinha vencido em Faro por 4-2. Neste jogo, inovação: sistema de cronometragem fora das quatro linhas, não pelo juiz mas por outro personagem (como na bola ao cesto). Joaquim Gralho abriu o activo aos 15 minutos. Olhanense empatou com Júlio Costa. Segunda parte: Manuel Florindo endossou a bola a José Gralho que marcou, João Gralho aproveitou um erro para o terceiro golo. Final: 3-1 para o Farense. Mas o árbitro deixou o jogo continuar, e Olhanense marcou um penalty discutível. Após protesto e reuniões, Farense foi reconhecido vencedor.",
        "metadata": {"tipo": "partido_historico", "periodo": "1922", "local": "Olhão", "fonte": "livro_scf_1.txt", "resultado": "3-1"}
    })

    pairs.append({
        "prompt": "Como foi o histórico jogo de 1923 entre Farense e Olhanense?",
        "completion": "Em 1923, realizou-se no Campo de S. Francisco o mais inolvidável jogo dos velhos tempos. O Olhanense, dirigido por Cândido Ventura, tinha reforçado-se com Júlio Costa (do Benfica), os irmãos Montenegro (Chico e Cecílio), e Pais como avançado-centro. O Farense venceu por 3-1, e o Olhanense abandonou o campo a meio da segunda parte. Joaquim Gralho marcou dois golos. O mais hilariante: estava combinado que o comboio apitaria no regresso para celebrar. Mas quando os jogadores de Olhão se apearam com 'caras de enterro', a festa mudou de figura. Albino (maquinista e antigo jogador do Farense) apitou até Olhão. José Nugas, que morava em Olhão, sofreu represálias - um marítimo de nome José Poleira pôs-lhe uma orelha 'a prémio'.",
        "metadata": {"tipo": "partido_historico", "periodo": "1923", "local": "Faro", "fonte": "livro_scf_1.txt", "resultado": "3-1"}
    })

    pairs.append({
        "prompt": "Como o Olhanense venceu o Campeonato de Portugal em 1924?",
        "completion": "Farense e Olhanense estavam empatados no campeonato distrital. O jogo de desempate desenrolou-se em Vila Real de Santo António (terreno neutro). O Olhanense conseguiu ganhar o derby decisivo devido à marcação de um penalty. Segundo António Gago, era um penalty muito discutível: na controversa jogada, o defesa José da Silva caiu na grande área, tendo a bola passado sobre a mão de forma puramente casual. Apesar desta controvérsia, o Olhanense seguiu para a competição máxima e tornou-se Campeão de Portugal.",
        "metadata": {"tipo": "partido_historico", "periodo": "1924", "local": "Vila Real Santo António", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Por que Cândido Ventura era um impulsionador diferente do Olhanense?",
        "completion": "Cândido Ventura não era um falso mecenas sem visão que deixaria o clube no atoleiro das dívidas. Procurava que o Olhanense desfrutasse de situação económica desafogada mas em bases sólidas. O Café Avenida era uma fonte de receita (com jogos de azar legais: dados, cartas, poker, banca francesa, roleta). Dinheiro de armadores e industriais de conservas era direcionado aos cofres do Olhanense. Multiplicavam-se diligências para recrutar jogadores de qualidade.",
        "metadata": {"tipo": "figura_historica", "pessoa": "Cândido Ventura", "clube": "Olhanense", "fonte": "livro_scf_1.txt"}
    })

    # ==================== TAÇAS E COMPETIÇÕES (1923) ====================

    pairs.append({
        "prompt": "O que aconteceu na Taça Gago Coutinho e Sacadura Cabral?",
        "completion": "Em 1922, houve desafio entre Farense e Sport Lisboa e Faro pela Taça Gago Coutinho e Sacadura Cabral. O Farense perdeu por 3-2. António Gago protestou alegando que o Lisboa e Faro tinha 'reforçado por elementos estranhos'. Numa carta formal, desafiou o capitão para novo jogo, com condições específicas: equipa constituída única e simplesmente por jogadores que tiveram parte nos desafios do Campeonato da Associação de Futebol do Algarve. Ofereceu uma Taça intitulada 'D. Maria Cúmano' com produto revertendo a favor do Hospital da Misericórdia.",
        "metadata": {"tipo": "partido_historico", "periodo": "1922", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "O que aconteceu na Taça Sagres (1923)?",
        "completion": "Durante a Taça Sagres, o Sport Lisboa e Faro empatou com o Lusitano Futebol Clube (que também era Campeão do Algarve). Cena cómica: Lusitano estava a perder 2-0 e Batista Salas abandonou dramaticamente o terreno. Após embaixada, regressou. Daí marcaram 2 golos, reduzindo Lisboa e Faro a 9 jogadores. Mas abandonariam depois, pretextando lesões. Na final pela Taça Sagres, Sporting Farense bateu Lisboa e Faro por 2-0. João Gralho obteve os dois golos.",
        "metadata": {"tipo": "partido_historico", "periodo": "1923", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como foi a Taça Mário Ramos (1923)?",
        "completion": "Contra o Fósforos, o Farense jogou com: Luís Madeira; Marcelino e Vieira; Marques, Bernardino de Carvalho e Martins; Gago, João Gralho, Anacleto, Paquito Lima e José Gralho. O Fósforos tinha: Arsénio; Alberto e Manuel; Tormenta, Augusto e Nicolau; Artur, Reis, Mário, João e Mengo. Resultado rápido no 1º tempo: Anacleto marcou, Lima enfiou o segundo, back-esquerdo do Fósforos fez auto-golo. Depois Fósforos reduziram, mas Anacleto marcou o quarto e João Gralho o quinto. Vencido contra o Lisboa e Faro por 3-2, ganhou por 2-1 na volta, sagrand-se vencedor.",
        "metadata": {"tipo": "partido_historico", "periodo": "1923", "fonte": "livro_scf_1.txt"}
    })

    # ==================== DESENVOLVIMENTO REGIONAL ====================

    pairs.append({
        "prompt": "Como se organizou o futebol no Algarve nos primeiros anos?",
        "completion": "Em 1914, fundou-se a União de Futebol de Faro englobando: Associação Académica do Liceu de Faro, Escola Normal de Faro, Sporting Clube Farense e Boavista Futebol Clube. O primeiro Campeonato de Faro (1914) foi vencido pelo Farense, Boavista em segundo. Em 1917, dissolvida a União, fundou-se Associação de Futebol do Algarve. Em 1918, após fracasso, criou-se nova associação que finalmente em 1923 foi fundada oficialmente como Associação de Futebol de Faro, filiada na União Portuguesa de Futebol e Federação Portuguesa dos Sports Atléticas. Em 27 de Outubro de 1924, teve estatutos aprovados pelo Governo Civil de Faro.",
        "metadata": {"tipo": "historia_regional", "periodo": "1914-1924", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual era a posição do Farense entre clubes algarvios?",
        "completion": "O Farense era o clube mais antigo e importante do Algarve. Comparando datas de fundação: Farense (1 Abril 1910), Olhanense (27 Abril 1912), Esperança Lagos (20 Setembro 1912), Portimonense (14 Agosto 1914), Lusitano (15 Abril 1916), Silves (4 Abril 1919), Louletano (6 Junho 1923). O Farense é portanto um dos mais longevos e o decano de quantos ainda hoje praticam o futebol.",
        "metadata": {"tipo": "historia_regional", "periodo": "1910-1925", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual foi o papel de Francisco Tavares Bello no desenvolvimento regional?",
        "completion": "Francisco Tavares Bello, um dos fundadores do Farense, foi fundamental para organizar e estruturar o futebol algarvio. Participou na reunião de 16 de Outubro de 1921 no Ginásio Clube Farense que deu origem à Associação de Futebol do Algarve. Integrou a comissão encarregada de redigir estatutos e organizar o primeiro campeonato regional. Em 1922, foi nomeado cronometrista oficial da final do 1.º Campeonato do Algarve, inovação para a época. Colaborou no jornal O Sul Desportivo como comentarista sobre história e organização do futebol local.",
        "metadata": {"tipo": "figura_historica", "pessoa": "Francisco Tavares Bello", "periodo": "1910-1924", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual foi a contexto da estrutura futebolística nacional quando Farense foi fundado?",
        "completion": "O órgão de cúpula da atividade futebolística chamava-se União Portuguesa de Football, criado em 31 de Março de 1914, englobando apenas três associações distritais: Lisboa (fundada 23 Setembro 1910), Portalegre (Outubro 1911), e Porto (10 Agosto 1912). Em 28 de Março de 1926, tomou nome de Federação de Football Association. Em 3 de Dezembro de 1938, constituída nos moldes atuais com denominação de Federação Portuguesa de Futebol.",
        "metadata": {"tipo": "contexto_nacional", "periodo": "1910-1938", "fonte": "livro_scf_1.txt"}
    })

    # ==================== CONTEXTO E ANÁLISE ====================

    pairs.append({
        "prompt": "Como o Farense se diferenciava do Sporting Clube de Lisboa?",
        "completion": "O Sporting de Lisboa foi fundado em Lisboa poucos anos depois do Farense pelo Visconde de Alvalade e seus nobres amigos. O Farense, em contraste, tinha origens 'plebéias' - seus jogadores eram operários (soldadores, ferroviários, sapateiros, moleiros, etc.). Este facto constitui para o historiador 'um título de nobreza nada despiciendo' - a verdadeira nobreza de origem povo.",
        "metadata": {"tipo": "analise_social", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual era a hegemonia do Farense no Algarve?",
        "completion": "Na década de 1910s-1920s, o Farense era inquestionavelmente hegemónico no Algarve. Era capaz de se bater de igual para igual com a Escola Académica de Lisboa, Liceu da Lapa, Pupilos do Exército, Casa Pia, Barreirense e Vitória de Setúbal. A fama do clube tinha transposto a 'fronteira' da Serra do Caldeirão. Só começaria a perder velocidade após a vitória do Olhanense no Campeonato de Portugal em 1924, entrando num período de crise que se prolongaria até princípios dos anos 30.",
        "metadata": {"tipo": "analise_hegemonia", "periodo": "1910-1924", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual era a situação financeira do Farense nos primeiros tempos?",
        "completion": "As finanças do Farense nunca eram 'famosas'. Qualquer deslocação era o 'Cabo das Tormentas'. Problemas de transporte (caroças de mula), falta de reembolsos prometidos, necessidade de empréstimos de amigos para viagens de regresso. Os jogadores não recebiam salários, apenas participavam com entusiasmo. Depois dos anos 20, o Olhanense começaria a ter muito mais posses (através do Café Avenida e jogos de azar), enquanto o Farense enfrentava dificuldades financeiras progressivas.",
        "metadata": {"tipo": "analise_financeira", "periodo": "1910-1924", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como era descrita a rivalidade entre Faro e Olhão?",
        "completion": "Faro e Olhão encontravam-se muito próximas mas mantinham relações de vizinhança nem sempre amenas. Não se tocavam quase, nem estavam ligadas como hoje. Olhão era mais próspera (conservas de peixe, armadores endinheirados, vida nocturna, jogos de azar), enquanto Faro era mais administrativa e burocrática. Havia 'cristalizações' evidentes, pessoas 'encaixadas' em casulos locais, o clubismo era 'cego e pitoresco', o facciosismo 'exacerbado'. Esta tensão explica a violência e dramatismo dos derbies.",
        "metadata": {"tipo": "analise_rivalidade", "periodo": "1910-1924", "fonte": "livro_scf_1.txt"}
    })

    return pairs

def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    print("📚 EXTRAÇÃO COMPLETA E ABRANGENTE DE Q&A PARES DOS LIVROS\n")
    print("="*80)

    all_pairs = extract_comprehensive_qa()

    print(f"\n✅ Total de {len(all_pairs)} exemplos extraídos dos livros históricos")

    # Save to file
    output_file = data_dir / "livros_qa_comprehensive.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"📂 Salvos em: {output_file.name}\n")

    # Show summary
    print("📊 RESUMO POR CATEGORIA:\n")
    tipos = {}
    for pair in all_pairs:
        tipo = pair.get('metadata', {}).get('tipo', 'outro')
        tipos[tipo] = tipos.get(tipo, 0) + 1

    for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        print(f"  {tipo:30s} {count:3d} pares")

if __name__ == "__main__":
    main()
