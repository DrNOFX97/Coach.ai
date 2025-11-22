#!/usr/bin/env python3
"""
Comprehensive narrative extraction from livro_scf_1.txt
Extracting detailed stories, personalities, and historical narratives
Target: 50+ additional Q&A pairs from rich narratives in the book
"""

import json
from typing import List, Dict, Any


def extract_narratives() -> List[Dict[str, Any]]:
    """Extract rich narratives and detailed stories from the book"""
    return [
        {
            "prompt": "Como era a vida quotidiana dos primeiros jogadores do Farense?",
            "completion": "Os primeiros jogadores do Farense reuniam-se numa pequena taberna propriedade de uma senhora espanhola, onde repunham as forças comendo um pequeno queijo e uma carcaça pelo módico preço de cerca de 10 réis. Essa mesma taberna servia de balneário improvisado e guarda-roupa, pois o Campo de São Francisco não tinha vestiários nem chuveiros. Esta simplicidade caracterizava a vida desportiva dos primeiros anos.",
            "metadata": {
                "tipo": "historia_social",
                "periodo": "1910-1915",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Senhora espanhola (dona da taberna)"
            }
        },
        {
            "prompt": "Como era o Largo do Sol Posto como sede do Farense?",
            "completion": "A primeira sede a sério do Farense ficava no Largo do Sol Posto, numa casa térrea de fachada triste e apagada, com uma porta e janela discretas. O mobiliário era extremamente simples: uma mesa, duas ou três cadeiras desemparelhadas que pareciam pedir socorro, alguns bancos coxos, e ao centro uma garrafa vazia com uma vela espetada. Mais parecia um antro de conspiradores do que um salão nobre. O clube permaneceu nela apenas 2-3 meses.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Largo do Sol Posto",
                "periodo": "1910-1915",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Como era a segunda sede do Farense no Largo Manuel Belmarço?",
            "completion": "A segunda sede ficava no Largo Manuel Belmarço (atualmente Largo D. Marcelino Franco), num prédio de melhor aparência com uma renda mensal de 33.000 réis, nem sempre paga a tempo. Este foi um avanço relativamente à sede anterior, demonstrando a crescente consolidação do clube. No entanto, António Gago afirma que a ordem foi contrária, com o Largo Manuel Belmarço sendo a primeira sede.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Largo Manuel Belmarço",
                "periodo": "1910-1920",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Como o Padre Mascarenhas apoiou o Sporting Farense?",
            "completion": "A terceira sede do Farense instalou-se em condições precárias e gratuitamente na sacristia da Igreja de S. Pedro, quando o prior era Padre Mascarenhas. O Padre Mascarenhas era um homem inovador e liberal, sendo o primeiro membro do clero regional a ir regularmente ao cinema. Sua ajuda foi fundamental para o clube ter um espaço durante este período crítico.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1915-1920",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Padre Mascarenhas"
            }
        },
        {
            "prompt": "Quem foi Maminhas e qual era o seu papel?",
            "completion": "Maminhas era o sacristão da Igreja de S. Pedro durante o tempo em que o Sporting Farense ocupava a sacristia como sede. Era um homem com ideias próprias e era conhecido como um 'sineiro alegre e grande adorador do deus Baco'. Maminhas era uma figura querida pela comunidade e apoiou o clube durante a sua estadia na Igreja.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1915-1920",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Maminhas"
            }
        },
        {
            "prompt": "Qual foi a trajectória das sedes do Farense no período 1920-1940?",
            "completion": "O Farense mudou-se várias vezes durante os anos 1920-1940. O clube ocupou: a Rua Conselheiro Bivar (primeiro andar, edifício amplo mas antigo), possível rés-do-chão do Grande Hotel (ponto cosmopolita de passagem), Rua D. Francisco Gomes (onde estava a Casa Verde), rés-do-chão da Sociedade Recreativa Farense (circa 1929), Rua Castilho 36 (1º andar), Rua 1º de Dezembro 7 (1º andar), e rés-do-chão do Clube Farense na Rua Santo António (ao lado da mercearia de António Gago). Esta 'valsa das sedes' reflecte as dificuldades financeiras crónicas do clube.",
            "metadata": {
                "tipo": "historia_sedes",
                "periodo": "1920-1940",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Quando se instalou o Farense na Rua Ferreira Neto?",
            "completion": "A actual sede do Sporting Clube Farense fica nos 1º e 2º andares do nº 6 da Rua Ferreira Neto. As opiniões divergem sobre quando se instalou lá: alguns dizem fim da década de 40, outros início da década de 50, o jornal do clube sugere 1955. Já lá estão há quase 30 anos. O prédio é tipicamente algarvio com toque oriental e telhado de quatro águas coberto por telha mourisca, pertencendo à família Neto.",
            "metadata": {
                "tipo": "historia_sedes",
                "local": "Rua Ferreira Neto 6",
                "periodo": "1950-1982",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "O que prometeu a Câmara Municipal em 1970?",
            "completion": "Em 6 de Março de 1970, por ocasião do sexagésimo aniversário do clube (1 Abril), a Câmara Municipal ofereceu/cedeu terreno. Em 11 de Março de 1970, a Câmara aprovou por unanimidade uma condição importante: o terreno cedido e benfeitorias reverteriam gratuitamente para a Câmara se o ginásio-sede não fosse construído em 10 anos. Porém, até 1982, as obras de construção nem sequer começaram, apesar dos esboços já contemplados.",
            "metadata": {
                "tipo": "historia_sedes",
                "periodo": "1970-1982",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual era a situação do Farense nos anos 1940s?",
            "completion": "O clube atravessou uma crise profunda de identidade nos anos 1940s. Entre 1946 e 1948, o clube chamou-se 'Clube Desportivo de Faro'. Nesse período, estava instalado na Rua do Compromisso (onde atualmente fica a Associação dos Diminuídos Mentais). Tinha vários meses de renda atrasados e o senhorio não hesitou em avançar com ação de despejo. Esta crise evidencia as dificuldades crónicas que o clube enfrentava.",
            "metadata": {
                "tipo": "historia_crise",
                "periodo": "1946-1948",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual foi o reconhecimento do Farense em 1979?",
            "completion": "O Sporting Clube Farense foi reconhecido como coletividade de utilidade pública em 1979. Este reconhecimento foi importante após um processo que demonstrou a importância social e desportiva do clube para a comunidade farense. Representou uma validação oficial do papel do clube na vida cívica da cidade.",
            "metadata": {
                "tipo": "historia_institucional",
                "periodo": "1979",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual era a perspectiva para o futuro do Farense em 1982?",
            "completion": "Em 1982, apesar de pessimismos críticos sobre as dificuldades crónicas, o historiador acredita que o Farense merecia 'muito melhor sorte'. Havia perspectiva de novos projetos para um ginásio-sede moderno, cujo arranque estava para breve segundo informações do Sr. José Custódio. Havia esperança de que os problemas estruturais pudessem ser finalmente resolvidos.",
            "metadata": {
                "tipo": "reflexao_futura",
                "periodo": "1980-1982",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Como era a evolução do primeiro campo de futebol do Farense?",
            "completion": "O primeiro campo de futebol digno desse nome ficava no Largo de São Francisco. Não era um estádio na verdadeira acepção, tinha reduzidas dimensões e não representava bem a cidade. Não era vedado. Quando se pretendia cobrar entrada, o quartel de infantaria dava contributo instalando um sistema rudimentar de cordas e lonas, abrigando também os assistentes nos dias quentes. Esta improvisação era característica dos primeiros tempos.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Largo São Francisco",
                "periodo": "1910-1920",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual foi a contribuição do Dr. Cândido de Sousa para o futebol farense?",
            "completion": "O Dr. Cândido de Sousa foi um dirigente empreendedor e amigo desinteressado do clube. Como principal impulsionador, patrocinou a construção do Campo da Estrada da Senhora da Saúde através da sociedade 'Algarve's Sporting Field' (constituída em 1923). A sua quota na sociedade elevava-se a cerca de 300 contos (a maior), demonstrando a sua dedicação ao desenvolvimento do futebol em Faro.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1920-1930",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Dr. Cândido de Sousa"
            }
        },
        {
            "prompt": "Como era o Campo da Estrada da Senhora da Saúde?",
            "completion": "O Campo da Estrada da Senhora da Saúde foi um avanço significativo. Quando concluído, tinha maiores dimensões, era vedado, com bancadas, espaço para peões, balneários e pista de ciclismo. O Farense pagava 33.200 réis por jogo para o utilizar. Este campo representava a modernização das instalações desportivas e foi palco de grandes encontros de nível nacional.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Estrada Senhora Saúde",
                "periodo": "1920-1930",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual foi o evento inaugural importante no Campo da Senhora da Saúde?",
            "completion": "Logo no início, o Campo da Estrada da Senhora da Saúde foi palco de grandes encontros de nível nacional. Destaca-se a final do Campeonato de Portugal em 1923 (ou 1924, conforme fontes), que opôs o Sporting Clube de Portugal à Associação Académica de Coimbra, terminando com vitória do Sporting por 3-0. Presentes estavam Francisco Stromp (capitão do Sporting), Ribeiro da Costa (capitão da Académica), e Garcia Cárabe.",
            "metadata": {
                "tipo": "partido_historico",
                "local": "Senhora Saúde",
                "periodo": "1923-1924",
                "fonte": "livro_scf_1.txt",
                "evento": "Final Campeonato Portugal"
            }
        },
        {
            "prompt": "Qual foi a história de Manuel Santo?",
            "completion": "Manuel Silvestre Mendonça dos Santos (depois naturalizado americano como Manuel Santo) emigrou para EUA em 1902, regressando em Abril de 1921 com poupanças. Vendo as precárias condições de prática desportiva e motivado pela rivalidade entre Farense, Lisboa-Faro e Olhanense, decidiu construir um estádio. Comprou terreno no 'espaldão' perto da Igreja de São Luís (cerca de 12.750 m2) e encomendou os planos no final de 1921 ou início de 1922.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1921-1923",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Manuel Santo"
            }
        },
        {
            "prompt": "O que foi o Santo Stadium?",
            "completion": "O Santo Stadium foi construído por Manuel Santo. Tinha maiores dimensões, era vedado, com bancadas de um lado, espaço para peões do outro, balneários e pista de ciclismo. Estava aberto a todas as associações desportivas da cidade, mas nenhuma o utilizava gratuitamente. Foi palco de grandes encontros de nível nacional que lhe deram renome e consolidou a importância de Faro no contexto futebolístico regional.",
            "metadata": {
                "tipo": "historia_campos",
                "local": "Santo Stadium",
                "periodo": "1923-1939",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual foi o primeiro treinador profissional do Farense?",
            "completion": "O Farense contratou o seu primeiro treinador especializado e profissional quando estava instalado no rés-do-chão do Clube Farense na Rua Santo António. Era Carlos Alves, um ex-internacional, grande impulsionador da ideia de criação de uma 'escola de treinadores'. Era avô do popular internacional do Benfica João Alves (as 'luvas pretas'). Carlos Alves desentendeu-se tanto com atletas como com dirigentes em 1939, marcando fim desta fase.",
            "metadata": {
                "tipo": "figura_historica",
                "periodo": "1939",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Carlos Alves"
            }
        },
        {
            "prompt": "Qual foi a relação entre Carlos Alves e João Alves?",
            "completion": "Carlos Alves era avô do famoso internacional do Benfica João Alves, conhecido como 'as luvas pretas'. Esta ligação familiar à Benfica e ao futebol nacional de elite mostra as conexões que o Farense conseguiu estabelecer. A influência de Carlos Alves como treinador profissional foi importante para modernizar o treino do futebol farense.",
            "metadata": {
                "tipo": "familia_historia",
                "periodo": "1939",
                "fonte": "livro_scf_1.txt",
                "pessoa": "Carlos Alves e João Alves"
            }
        },
        {
            "prompt": "Como o historiador descreve a 'valsa das sedes' do Farense?",
            "completion": "A 'valsa das sedes' é um sinal inequívoco das dificuldades do clube e da sua luta pela sobrevivência. O historiador compara o Farense a 'Fernão Mendes Pinto' em peregrinação imperturbável, passando por locais precários e frequentemente mudando para evitar problemas financeiros. A mudança contínua reflete a 'crónica e endémica falta de estruturas'.",
            "metadata": {
                "tipo": "analise_dificuldades",
                "periodo": "1910-1970",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual era a análise do historiador sobre os obstáculos do Farense?",
            "completion": "O historiador identifica obstáculos estruturais e financeiros crónic no desenvolvimento do Farense. A falta de instalações adequadas, dificuldades em pagar renda de sedes, e a dificuldade em manter dirigentes comprometidos foram problemas persistentes. Apesar destes obstáculos, o clube demonstrava uma resiliência notável.",
            "metadata": {
                "tipo": "analise_estruturas",
                "periodo": "1910-1982",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual era a situação financeira do Farense?",
            "completion": "O Sporting Clube Farense enfrentava dificuldades financeiras crónicas. O clube tinha frequentemente dificuldade em pagar a renda de sedes, resultando em ações de despejo. As quotas eram mantidas acessíveis para atrair sócios, mas isto limitava os recursos disponíveis. Apesar destes problemas, o clube conseguiu sobreviver e desenvolver-se gradualmente.",
            "metadata": {
                "tipo": "historia_financeira",
                "periodo": "1910-1982",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual era a perspectiva sobre a viabilidade futura do Farense?",
            "completion": "O historiador questiona se o Farense conseguirá sobreviver aos desafios futuros. O terreno oferecido pela Câmara em 1970 estava em risco devido à construção de uma nova estrada para o hospital. No entanto, o reconhecimento como coletividade de utilidade pública em 1979 e a perspectiva de novos projetos mantinham a esperança para o futuro.",
            "metadata": {
                "tipo": "analise_situacao",
                "periodo": "1980-1982",
                "fonte": "livro_scf_1.txt"
            }
        },
        {
            "prompt": "Qual era a importância histórica do Farense?",
            "completion": "O Sporting Clube Farense representava mais do que um clube desportivo. Era um símbolo do desenvolvimento cívico e social de Faro. A sua história reflectia as dificuldades de uma comunidade periférica em desenvolver estruturas modernas, mas também a resiliência e paixão da população farense pelo futebol.",
            "metadata": {
                "tipo": "legado",
                "periodo": "1910-1982",
                "fonte": "livro_scf_1.txt"
            }
        }
    ]


def main():
    """Extract all Q&A pairs and save to JSONL file"""
    all_qa = extract_narratives()

    print(f"{'='*60}")
    print(f"Total Q&A pairs extracted: {len(all_qa)}")
    print(f"{'='*60}\n")

    # Save to JSONL
    output_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/livros_qa_narratives.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in all_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    print(f"✓ Saved to: {output_file}")
    print(f"✓ Total lines: {len(all_qa)}")


if __name__ == "__main__":
    main()
