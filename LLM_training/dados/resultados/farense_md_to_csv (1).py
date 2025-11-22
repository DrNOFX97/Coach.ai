import re
import csv
import json
from datetime import datetime
from collections import defaultdict

def limpar_texto(texto):
    """Remove emojis e caracteres especiais"""
    texto = re.sub(r'[âœ…âž–âŒðŸ†âš½ðŸ¥…ðŸ"ˆðŸ"‰ðŸ"ŠðŸ"…âž¡ï¸]', '', texto)
    return texto.strip()

def determinar_local_e_adversario(jogo_str):
    """Determina se jogo foi em casa/fora e identifica o adversário"""
    jogo_str = limpar_texto(jogo_str)
    
    if jogo_str.startswith('SC Farense') or jogo_str.startswith('**SC Farense'):
        match = re.search(r'SC Farense\s*\*?\*?\s*(\d+)\s*-\s*(\d+)\s+(.+)', jogo_str)
        if match:
            golos_farense = int(match.group(1))
            golos_adversario = int(match.group(2))
            adversario = match.group(3).strip()
            return 'Casa', adversario, golos_farense, golos_adversario
    else:
        match = re.search(r'(.+?)\s+(\d+)\s*-\s*\*?\*?(\d+)\s+SC Farense', jogo_str)
        if match:
            adversario = match.group(1).strip()
            golos_adversario = int(match.group(2))
            golos_farense = int(match.group(3))
            return 'Fora', adversario, golos_farense, golos_adversario
    
    return None, None, None, None

def processar_markdown(md_file, csv_file, jsonl_file):
    """Processa o markdown e gera CSV + JSONL"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    jogos = []
    competicao_atual = ""
    epoca_atual = ""
    
    linhas = conteudo.split('\n')
    
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        
        if linha.startswith('## Época'):
            epoca_match = re.search(r'Época (\d{4}/\d{2,4})', linha)
            if epoca_match:
                epoca_atual = epoca_match.group(1)
        
        if linha.startswith('###') and not linha.startswith('####'):
            competicao_atual = limpar_texto(linha.replace('#', '').strip())
        
        if '| Jornada |' in linha or '| J' in linha:
            i += 2
            
            while i < len(linhas):
                linha_dados = linhas[i].strip()
                
                if not linha_dados or not linha_dados.startswith('|'):
                    break
                
                colunas = [c.strip() for c in linha_dados.split('|')[1:-1]]
                
                if len(colunas) >= 4:
                    jornada = limpar_texto(colunas[0])
                    data = limpar_texto(colunas[1])
                    jogo = limpar_texto(colunas[2])
                    
                    local, adversario, golos_farense, golos_adversario = determinar_local_e_adversario(jogo)
                    
                    if local and adversario and golos_farense is not None:
                        if golos_farense > golos_adversario:
                            resultado_tipo = 'V'
                        elif golos_farense < golos_adversario:
                            resultado_tipo = 'D'
                        else:
                            resultado_tipo = 'E'
                        
                        jogo_info = {
                            'epoca': epoca_atual,
                            'competicao': competicao_atual,
                            'jornada': jornada,
                            'data': data,
                            'local': local,
                            'adversario': adversario,
                            'golos_farense': golos_farense,
                            'golos_adversario': golos_adversario,
                            'resultado': f"{golos_farense}-{golos_adversario}",
                            'resultado_tipo': resultado_tipo
                        }
                        
                        jogos.append(jogo_info)
                
                i += 1
            continue
        
        i += 1
    
    # Escrever CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        if jogos:
            fieldnames = ['epoca', 'competicao', 'jornada', 'data', 'local', 
                         'adversario', 'golos_farense', 'golos_adversario', 
                         'resultado', 'resultado_tipo']
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jogos)
    
    print(f"✅ {len(jogos)} jogos convertidos para CSV")
    
    # Gerar JSONL com perguntas
    gerar_perguntas_jsonl(jogos, jsonl_file)
    
    # Estatísticas
    vitorias = sum(1 for j in jogos if j['resultado_tipo'] == 'V')
    empates = sum(1 for j in jogos if j['resultado_tipo'] == 'E')
    derrotas = sum(1 for j in jogos if j['resultado_tipo'] == 'D')
    
    print(f"\n📊 Estatísticas Farense:")
    print(f"  • Vitórias: {vitorias}")
    print(f"  • Empates: {empates}")
    print(f"  • Derrotas: {derrotas}")
    print(f"  • Total de golos marcados: {sum(j['golos_farense'] for j in jogos)}")
    print(f"  • Total de golos sofridos: {sum(j['golos_adversario'] for j in jogos)}")

def gerar_perguntas_jsonl(jogos, jsonl_file):
    """Gera perguntas para treino de LLM"""
    
    perguntas = []
    
    # Perguntas simples (por jogo)
    for jogo in jogos[:500]:  # Limitar para não ficar muito grande
        
        # Pergunta 1: Resultado específico
        if jogo['data'] and jogo['data'] != 's/d' and jogo['data'] != 'N/D':
            local_texto = "em casa" if jogo['local'] == 'Casa' else "fora de casa"
            perguntas.append({
                "prompt": f"Qual foi o resultado do Farense contra o {jogo['adversario']} em {jogo['data']}?",
                "completion": f"O Farense jogou {local_texto} e o resultado foi {jogo['resultado']}. O Farense marcou {jogo['golos_farense']} golo{'s' if jogo['golos_farense'] != 1 else ''} e sofreu {jogo['golos_adversario']}.",
                "metadata": {
                    "tipo": "resultado_especifico",
                    "epoca": jogo['epoca'],
                    "competicao": jogo['competicao']
                }
            })
        
        # Pergunta 2: Quem ganhou
        if jogo['resultado_tipo'] == 'V':
            perguntas.append({
                "prompt": f"O Farense ganhou ou perdeu contra o {jogo['adversario']} na {jogo['competicao']}?",
                "completion": f"O Farense venceu por {jogo['resultado']}.",
                "metadata": {"tipo": "vencedor"}
            })
        elif jogo['resultado_tipo'] == 'D':
            perguntas.append({
                "prompt": f"O Farense ganhou contra o {jogo['adversario']}?",
                "completion": f"Não, o Farense perdeu por {jogo['resultado']}.",
                "metadata": {"tipo": "vencedor"}
            })
    
    # Perguntas agregadas
    
    # 1. Por adversário
    jogos_por_adversario = defaultdict(list)
    for jogo in jogos:
        jogos_por_adversario[jogo['adversario']].append(jogo)
    
    for adversario, jogos_adv in list(jogos_por_adversario.items())[:30]:  # Top 30 adversários
        if len(jogos_adv) >= 3:
            vitorias = sum(1 for j in jogos_adv if j['resultado_tipo'] == 'V')
            empates = sum(1 for j in jogos_adv if j['resultado_tipo'] == 'E')
            derrotas = sum(1 for j in jogos_adv if j['resultado_tipo'] == 'D')
            
            perguntas.append({
                "prompt": f"Qual o histórico do Farense contra o {adversario}?",
                "completion": f"O Farense jogou {len(jogos_adv)} vezes contra o {adversario}. Foram {vitorias} vitória{'s' if vitorias != 1 else ''}, {empates} empate{'s' if empates != 1 else ''} e {derrotas} derrota{'s' if derrotas != 1 else ''}.",
                "metadata": {
                    "tipo": "historico_adversario",
                    "adversario": adversario
                }
            })
            
            # Golos marcados
            total_golos = sum(j['golos_farense'] for j in jogos_adv)
            perguntas.append({
                "prompt": f"Quantos golos marcou o Farense contra o {adversario}?",
                "completion": f"O Farense marcou {total_golos} golos em {len(jogos_adv)} jogos contra o {adversario}.",
                "metadata": {"tipo": "golos_adversario"}
            })
    
    # 2. Por competição
    jogos_por_comp = defaultdict(list)
    for jogo in jogos:
        if jogo['competicao']:
            jogos_por_comp[jogo['competicao']].append(jogo)
    
    for comp, jogos_comp in list(jogos_por_comp.items())[:20]:  # Top 20 competições
        if len(jogos_comp) >= 5:
            vitorias = sum(1 for j in jogos_comp if j['resultado_tipo'] == 'V')
            
            perguntas.append({
                "prompt": f"Quantas vitórias teve o Farense na {comp}?",
                "completion": f"O Farense teve {vitorias} vitória{'s' if vitorias != 1 else ''} em {len(jogos_comp)} jogos na {comp}.",
                "metadata": {
                    "tipo": "vitorias_competicao",
                    "competicao": comp
                }
            })
    
    # 3. Por época
    jogos_por_epoca = defaultdict(list)
    for jogo in jogos:
        if jogo['epoca']:
            jogos_por_epoca[jogo['epoca']].append(jogo)
    
    for epoca, jogos_epoca in list(jogos_por_epoca.items())[-10:]:  # Últimas 10 épocas
        vitorias = sum(1 for j in jogos_epoca if j['resultado_tipo'] == 'V')
        golos_marcados = sum(j['golos_farense'] for j in jogos_epoca)
        golos_sofridos = sum(j['golos_adversario'] for j in jogos_epoca)
        
        perguntas.append({
            "prompt": f"Como foi a época {epoca} do Farense?",
            "completion": f"Na época {epoca}, o Farense jogou {len(jogos_epoca)} jogos, com {vitorias} vitória{'s' if vitorias != 1 else ''}. Marcou {golos_marcados} golos e sofreu {golos_sofridos}.",
            "metadata": {
                "tipo": "resumo_epoca",
                "epoca": epoca
            }
        })
    
    # 4. Casa vs Fora
    jogos_casa = [j for j in jogos if j['local'] == 'Casa']
    jogos_fora = [j for j in jogos if j['local'] == 'Fora']
    
    vitorias_casa = sum(1 for j in jogos_casa if j['resultado_tipo'] == 'V')
    vitorias_fora = sum(1 for j in jogos_fora if j['resultado_tipo'] == 'V')
    
    perguntas.append({
        "prompt": "O Farense ganha mais em casa ou fora?",
        "completion": f"O Farense tem {vitorias_casa} vitórias em {len(jogos_casa)} jogos em casa, e {vitorias_fora} vitórias em {len(jogos_fora)} jogos fora. O Farense ganha mais {'em casa' if vitorias_casa > vitorias_fora else 'fora'}.",
        "metadata": {"tipo": "casa_vs_fora"}
    })
    
    # 5. Maiores goleadas
    maiores_vitorias = sorted([j for j in jogos if j['resultado_tipo'] == 'V'], 
                             key=lambda x: x['golos_farense'] - x['golos_adversario'], 
                             reverse=True)[:3]
    
    if maiores_vitorias:
        lista_vitorias = []
        for jogo in maiores_vitorias:
            lista_vitorias.append(f"{jogo['resultado']} contra o {jogo['adversario']}")
        
        perguntas.append({
            "prompt": "Quais foram as maiores vitórias do Farense?",
            "completion": f"As maiores vitórias do Farense foram: {', '.join(lista_vitorias)}.",
            "metadata": {"tipo": "maiores_vitorias"}
        })
    
    # 6. Melhor época
    melhores_epocas = sorted(jogos_por_epoca.items(), 
                            key=lambda x: sum(1 for j in x[1] if j['resultado_tipo'] == 'V'),
                            reverse=True)[:3]
    
    if melhores_epocas:
        melhor_epoca = melhores_epocas[0]
        vits = sum(1 for j in melhor_epoca[1] if j['resultado_tipo'] == 'V')
        
        perguntas.append({
            "prompt": "Qual foi a melhor época do Farense?",
            "completion": f"Uma das melhores épocas foi {melhor_epoca[0]}, com {vits} vitórias em {len(melhor_epoca[1])} jogos.",
            "metadata": {"tipo": "melhor_epoca"}
        })
    
    # Guardar JSONL
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for p in perguntas:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')
    
    print(f"✅ {len(perguntas)} perguntas geradas em {jsonl_file}")
    
    # Estatísticas de perguntas
    tipos = defaultdict(int)
    for p in perguntas:
        tipos[p['metadata']['tipo']] += 1
    
    print(f"\n📋 Tipos de perguntas geradas:")
    for tipo, count in sorted(tipos.items(), key=lambda x: -x[1]):
        print(f"  • {tipo}: {count}")

if __name__ == "__main__":
    processar_markdown('resultados_completos.md', 'farense_resultados.csv', 'farense_dataset.jsonl')
    print("\n🎯 Ficheiros gerados:")
    print("  • farense_resultados.csv (dados estruturados)")
    print("  • farense_dataset.jsonl (perguntas para treino)")
