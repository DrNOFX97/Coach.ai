#!/usr/bin/env python3
"""
EXTRAÇÃO MEGA E ULTRA-COMPLETA de Q&A dos livros históricos.
Objetivo: Extrair 60+ pares cobrindo TUDO da história do Farense.

Cobertura adicional:
- Sedes (múltiplas mudanças, localizações)
- Campos (São Francisco, Senhora da Saúde, Santo Stadium, São Luís)
- Pessoas fundadoras e dirigentes
- Crises e períodos de dificuldade
- Estruturas físicas e financeiras
"""

import json
from pathlib import Path
from typing import List, Dict, Any

def extract_mega_qa() -> List[Dict[str, Any]]:
    """Extract mega comprehensive Q&A pairs from all book sources."""
    pairs = []

    # ==================== SEDES DO CLUBE ====================

    pairs.append({
        "prompt": "Qual era a primeira sede do Sporting Clube Farense?",
        "completion": "A primeira sede não era fixa. José de Sousa Ferradeira, num tom divertido, afirmava: 'Nessa altura a sede era móvel; variava conforme o banco de jardim que estivesse disponível'. António Gago confirma que as primeiras reuniões tiveram lugar num recanto do Jardim Manuel Bivar denominado 'Montanha Russa'.",
        "metadata": {"tipo": "historia_sedes", "periodo": "1910-1912", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Onde era o ponto de encontro dos primeiros jogadores do Farense?",
        "completion": "Os atletas reuniam-se numa pequena taberna propriedade de uma senhora espanhola, onde repunham as forças comendo um pequeno queijo e uma carcaça pelo módico preço de cerca de 10 réis. Essa mesma taberna servia de balneário improvisado e guarda-roupa, pois o Campo de São Francisco não tinha vestiários nem chuveiros.",
        "metadata": {"tipo": "historia_sedes", "periodo": "1910-1915", "fonte": "livro_scf_1.txt", "pessoa": "Senhora espanhola"}
    })

    pairs.append({
        "prompt": "Qual foi a primeira sede fixa do Farense no Largo do Sol Posto?",
        "completion": "Segundo Manuel de Sousa, a primeira sede a sério ficava no Largo do Sol Posto, numa casa térrea de fachada triste e apagada, com uma porta e janela discretas. O mobiliário era extremamente simples: uma mesa, duas ou três cadeiras desemparelhadas que pareciam pedir socorro, alguns bancos coxos, e ao centro uma garrafa vazia com uma vela espetada. Mais parecia um antro de conspiradores do que um salão nobre. O clube permaneceu nela apenas 2-3 meses.",
        "metadata": {"tipo": "historia_sedes", "local": "Largo Sol Posto", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Para onde se mudou o Farense após o Largo do Sol Posto?",
        "completion": "Segundo Manuel de Sousa, a segunda sede ficava no Largo Manuel Belmarço (atualmente Largo D. Marcelino Franco), num prédio de melhor aparência com uma renda mensal de 33.000 réis, nem sempre paga a tempo. No entanto, António Gago afirma que a ordem foi contrária: primeira sede no Largo Manuel Belmarço, segunda no Largo do Sol Posto.",
        "metadata": {"tipo": "historia_sedes", "local": "Largo Manuel Belmarço", "periodo": "1910-1920", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual foi a terceira sede do Farense?",
        "completion": "A terceira sede instalou-se em condições precárias e gratuitamente na sacristia da Igreja de S. Pedro, quando o prior era Padre Mascarenhas e o sacristão Maminhas. O Padre Mascarenhas era inovador e liberal, sendo o primeiro membro do clero regional a ir regularmente ao cinema. Maminhas tinha ideias próprias e era um 'sineiro alegre e grande adorador do deus Baco'.",
        "metadata": {"tipo": "historia_sedes", "local": "Igreja S. Pedro", "periodo": "1915-1920", "fonte": "livro_scf_1.txt", "pessoas": ["Padre Mascarenhas", "Maminhas"]}
    })

    pairs.append({
        "prompt": "Que outras sedes o Farense ocupou?",
        "completion": "O Farense mudou-se para a Rua Conselheiro Bivar (primeiro andar, edifício amplo mas antigo, onde está o Círculo Cultural do Algarve), possível rés-do-chão do Grande Hotel (ponto cosmopolita de passagem), Rua D. Francisco Gomes (por cima da Casa Verde, quando Sr. Fernandes era diretor), rés-do-chão da Sociedade Recreativa Farense (circa 1929), Rua Castilho 36 (1º andar), Rua 1º de Dezembro 7 (1º andar), rés-do-chão do Clube Farense na Rua Santo António (ao lado da mercearia de António Gago, depois transformada em casa de gelados).",
        "metadata": {"tipo": "historia_sedes", "periodo": "1920-1940", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual é a atual sede do Sporting Clube Farense?",
        "completion": "A atual sede fica nos 1º e 2º andares do nº 6 da Rua Ferreira Neto. As opiniões divergem sobre quando se instalou lá: alguns dizem fim da década de 40, outros início da década de 50, o jornal do clube sugere 1955. Já lá estão há quase 30 anos. O prédio é tipicamente algarvio com toque oriental e telhado de quatro águas coberto por telha mourisca, pertencendo à família Neto.",
        "metadata": {"tipo": "historia_sedes", "local": "Rua Ferreira Neto 6", "periodo": "1950-1982", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "O que foi a proposta de terreno pela Câmara Municipal ao Farense?",
        "completion": "Em 6 de Março de 1970, por ocasião do sexagésimo aniversário do clube (1 Abril), a Câmara Municipal ofereceu cedem terreno. Em 11 de Março de 1970, aprovou por unanimidade adicionar que o terreno cedido e benfeitorias reverteriam gratuitamente para a Câmara se o ginásio-sede não fosse construído em 10 anos. Porém, até 1982, as obras de construção nem sequer começaram, apesar dos esboços já contemplados.",
        "metadata": {"tipo": "historia_sedes", "periodo": "1970-1982", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual foi o reconhecimento do Farense como coletividade?",
        "completion": "O Sporting Clube Farense foi reconhecido como coletividade de utilidade pública em 1979. Este reconhecimento veio após um processo que demonstrou a importância social e desportiva do clube para a comunidade farence.",
        "metadata": {"tipo": "historia_institucional", "periodo": "1979", "fonte": "livro_scf_1.txt"}
    })

    # ==================== CAMPOS DE FUTEBOL ====================

    pairs.append({
        "prompt": "Qual foi o primeiro campo de futebol do Farense?",
        "completion": "O primeiro campo de futebol digno desse nome ficava no Largo de São Francisco. Não era um estádio na verdadeira acepção, tinha reduzidas dimensões e não representava bem a cidade. Não era vedado. Quando se pretendia cobrar entrada, o quartel de infantaria dava contributo instalando um sistema rudimentar de cordas e lonas, abrigando também os assistentes nos dias quentes.",
        "metadata": {"tipo": "historia_campos", "local": "Largo São Francisco", "periodo": "1910-1920", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como se construiu o Campo da Estrada da Senhora da Saúde?",
        "completion": "O principal impulsionador foi o Dr. Cândido de Sousa, dirigente empreendedor e amigo desinteressado do clube. O terreno foi adquirido por uma sociedade por quotas chamada 'Algarve's Sporting Field' (constituída em 1923). A quota do Dr. Cândido de Sousa elevava-se a cerca de 300 contos (a maior). Outro sócio importante era Vaz Velho. O campo, quando concluído, era de maiores dimensões, vedado, com bancadas, espaço para peões, balneários e pista de ciclismo. O Farense pagava 39.200 réis por jogo para o utilizar.",
        "metadata": {"tipo": "historia_campos", "local": "Estrada Senhora Saúde", "periodo": "1920-1923", "fonte": "livro_scf_1.txt", "pessoas": ["Dr. Cândido de Sousa"]}
    })

    pairs.append({
        "prompt": "Qual foi o evento inaugural importante no Campo da Senhora da Saúde?",
        "completion": "Logo no início, foi palco de grandes encontros de nível nacional. Destaca-se a final do Campeonato de Portugal em 1923 (ou 1924, conforme fontes), que opôs o Sporting Clube de Portugal à Associação Académica de Coimbra, terminando com vitória do Sporting por 3-0. Presentes Francisco Stromp (capitão do Sporting) e Ribeiro da Costa (capitão da Académica), além de Garcia Cárabe.",
        "metadata": {"tipo": "historia_campos", "local": "Senhora Saúde", "periodo": "1923-1924", "fonte": "livro_scf_1.txt", "evento": "Final Campeonato Portugal"}
    })

    pairs.append({
        "prompt": "Como foi construído o Santo Stadium?",
        "completion": "Manuel Silvestre Mendonça dos Santos (depois naturalizado americano como Manuel Santo) emigrou para EUA em 1902, regressando em Abril de 1921 com poupanças. Vendo as precárias condições de prática desportiva e motivado pela rivalidade entre Farense, Lisboa e Faro e Olhanense, decidiu construir um estádio. Comprou terreno no 'espaldão' perto da Igreja de São Luís: cerca de 12.750 m2, mais terreno para sua casa tipo Villa Pinto estilo colonial. Encomendou os planos no final de 1921 ou início de 1922. Seria um dos primeiros estádios em Portugal com características específicas para futebol.",
        "metadata": {"tipo": "historia_campos", "local": "Santo Stadium", "periodo": "1921-1923", "fonte": "livro_scf_1.txt", "pessoas": ["Manuel Santo"]}
    })

    pairs.append({
        "prompt": "O que era o Santo Stadium?",
        "completion": "O Santo Stadium foi construído por Manuel Santo. Tinha maiores dimensões, era vedado, com bancadas de um lado, espaço para peões do outro, balneários e pista de ciclismo. Estava aberto a todas as associações desportivas da cidade, mas nenhuma o utilizava gratuitamente. Foi palco de grandes encontros de nível nacional que lhe deram renome.",
        "metadata": {"tipo": "historia_campos", "local": "Santo Stadium", "periodo": "1923-1939", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual é o nome atual do principal estádio de Faro?",
        "completion": "O estádio que sucedeu ao Santo Stadium é conhecido por vários nomes: 'Campo de Futebol de S. Luís', 'Estádio de S. Luís', 'Campo Municipal de Futebol de S. Luís' ou 'Estádio Municipal de S. Luís'. Também era conhecido como 'Santo Stadium' antes desta nomenclatura.",
        "metadata": {"tipo": "historia_campos", "local": "S. Luís", "periodo": "1939-1982", "fonte": "livro_scf_1.txt"}
    })

    # ==================== TREINO PROFISSIONAL ====================

    pairs.append({
        "prompt": "Qual foi o primeiro treinador profissional do Farense?",
        "completion": "Segundo José António Gonçalves, o Farense contratou o seu primeiro treinador especializado e profissional quando estava instalado no rés-do-chão do Clube Farense na Rua Santo António. Era Carlos Alves, um ex-internacional, grande impulsionador da ideia de criação de uma 'escola de treinadores'. Era avô do popular internacional do Benfica João Alves (as 'luvas pretas'). Carlos Alves desentendeu-se tanto com atletas como com dirigentes em 1939, marcando fim desta fase.",
        "metadata": {"tipo": "historia_treinadores", "pessoa": "Carlos Alves", "periodo": "1939", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual era a situação do Farense nos anos 1940s?",
        "completion": "O clube atravessou uma crise de identidade nos anos 1940s. Entre 1946 e 1948, chamou-se 'Clube Desportivo de Faro'. Nesse período, estava instalado na Rua do Compromisso (onde atualmente fica a Associação dos Diminuídos Mentais). Tinha vários meses de renda atrasados e o senhorio não hesitou em avançar com ação de despejo. Posteriormente, o Farense subiu à 1ª Divisão em 1970.",
        "metadata": {"tipo": "historia_crise", "periodo": "1946-1948", "fonte": "livro_scf_1.txt"}
    })

    # ==================== PERSONALIDADES E DIRIGENTES ====================

    pairs.append({
        "prompt": "Quem foram os primeiros administradores da sociedade 'Algarve's Sporting Field'?",
        "completion": "Segundo os estatutos de 1923, o Conselho de Administração durante o primeiro triênio era constituído por: Dr. Cândido Emílio de Sousa, João Machado Vaz Velho e Manuel Garcia Cárabe. Particularmente interessante é que estes três acionistas foram ou viriam a ser presidentes das sucessivas direções do Sporting Farense.",
        "metadata": {"tipo": "figura_historica", "periodo": "1923", "fonte": "livro_scf_1.txt", "pessoas": ["Dr. Cândido Emílio de Sousa", "João Machado Vaz Velho", "Manuel Garcia Cárabe"]}
    })

    pairs.append({
        "prompt": "Qual era o contexto económico de Portugal quando Farense foi fundado?",
        "completion": "O Sporting Farense foi fundado em 1910, poucos meses antes da queda da monarquia portuguesa (5 de Outubro de 1910). Isto significa que a República portuguesa foi proclamada poucos meses após a fundação do clube, num período de grande transformação nacional.",
        "metadata": {"tipo": "contexto_nacional", "periodo": "1910", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Como era a estrutura futebolística regional quando o Farense se mudava entre sedes?",
        "completion": "A 'valsa das sedes' do Farense refletia as dificuldades do clube. Entre múltiplas mudanças (Largo Sol Posto, Largo Manuel Belmarço, Igreja S. Pedro, várias ruas diferentes), o clube enfrentava dificuldades financeiras crónicas e endémicas. A falta de estruturas adequadas era um problema constante que acompanhava a organização.",
        "metadata": {"tipo": "analise_estruturas", "periodo": "1910-1950", "fonte": "livro_scf_1.txt"}
    })

    # ==================== FACTOS E RECORDES ====================

    pairs.append({
        "prompt": "Qual foi o placar memorável da viagem a Beja?",
        "completion": "Em 1917-1918, o Farense jogou dois encontros em Beja com resultados memoráveis: 3-1 contra o Águias Futebol Clube no primeiro dia, e espectacular 13-0 contra 'Os Onze Amigos' no segundo dia. Apesar destes resultados avassaladores, os organizadores não quiseram reembolsar o transporte do Farense.",
        "metadata": {"tipo": "partido_historico", "local": "Beja", "periodo": "1917-1918", "fonte": "livro_scf_1.txt", "resultado": "13-0"}
    })

    pairs.append({
        "prompt": "Qual era a previsão de capacidade de sócio espanhola?",
        "completion": "A taberna da senhora espanhola que servia como ponto de encontro dos primeiros jogadores tinha um preço muito acessível: um pequeno queijo e uma carcaça pelo módico preço de cerca de 10 réis. Este era o orçamento dos jogadores operários do Farense.",
        "metadata": {"tipo": "historia_social", "periodo": "1910-1915", "fonte": "livro_scf_1.txt"}
    })

    # ==================== ANÁLISE E REFLEXÃO ====================

    pairs.append({
        "prompt": "Como o historiador descreve o problema das sedes do Farense?",
        "completion": "A 'valsa das sedes' é um sinal inequívoco das dificuldades do clube e da sua luta pela sobrevivência. O autor compara o Farense a 'Fernão Mendes Pinto' em peregrinação imperturbável, passando por locais precários e frequentemente mudando para evitar problemas financeiros. A mudança contínua refletia a 'crónica e endémica falta de estruturas'.",
        "metadata": {"tipo": "analise_dificuldades", "periodo": "1910-1970", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "Qual é a situação do Farense no início dos anos 1980s?",
        "completion": "Na década de 1980 (1982), o Farense ainda enfrentava incertezas. O terreno oferecido pela Câmara Municipal (com prazo de 10 anos para construção do ginásio-sede) estava sendo cerceado pela construção de nova estrada para o hospital. O talhão estava em risco de desaparecer. O autor questiona: 'Conseguirá sobreviver?' Reflecte pessimismo crítico sobre a capacidade do clube em superar dificuldades económicas crónicas.",
        "metadata": {"tipo": "analise_situacao", "periodo": "1980-1982", "fonte": "livro_scf_1.txt"}
    })

    pairs.append({
        "prompt": "O que diz o historiador sobre o futuro do Farense?",
        "completion": "Apesar dos pessimismos críticos, o historiador acredita que o Farense merecia 'muito melhor sorte'. Reconhece coletividade de utilidade pública (1979), que não tudo é negro. Diz que 'nem tudo é negro' e há perspetiva de novos projetos para ginásio-sede moderno, cujo arranque estava para breve (informações do Sr. José Custódio).",
        "metadata": {"tipo": "reflexao_futura", "periodo": "1980-1982", "fonte": "livro_scf_1.txt"}
    })

    return pairs

def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    print("📚 EXTRAÇÃO MEGA ULTRA-COMPLETA DOS LIVROS\n")
    print("="*80)

    all_pairs = extract_mega_qa()

    print(f"\n✅ Total de {len(all_pairs)} exemplos extraídos\n")

    # Save to file
    output_file = data_dir / "livros_qa_mega.jsonl"
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
