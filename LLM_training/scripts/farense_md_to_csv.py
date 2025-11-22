import re
import csv
from datetime import datetime

def limpar_texto(texto):
    """Remove emojis e caracteres especiais"""
    # Remove emojis comuns
    texto = re.sub(r'[âœ…âž–âŒðŸ†âš½ðŸ¥…ðŸ"ˆðŸ"‰ðŸ"ŠðŸ"…âž¡ï¸]', '', texto)
    return texto.strip()

def extrair_golos(resultado_str):
    """Extrai golos de strings como '2-1', '3-0', etc."""
    if not resultado_str or resultado_str == '-':
        return None, None
    
    # Limpar o resultado de texto extra
    resultado_str = resultado_str.split()[0]  # Pega só a primeira parte
    
    match = re.match(r'(\d+)-(\d+)', resultado_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def determinar_local_e_adversario(jogo_str):
    """Determina se jogo foi em casa/fora e identifica o adversário"""
    jogo_str = limpar_texto(jogo_str)
    
    # Padrão: "SC Farense X - Y Adversário" (casa)
    # ou "Adversário X - Y SC Farense" (fora)
    
    if jogo_str.startswith('SC Farense') or jogo_str.startswith('**SC Farense'):
        # Jogo em casa
        match = re.search(r'SC Farense\s*\*?\*?\s*(\d+)\s*-\s*(\d+)\s+(.+)', jogo_str)
        if match:
            golos_farense = int(match.group(1))
            golos_adversario = int(match.group(2))
            adversario = match.group(3).strip()
            return 'Casa', adversario, golos_farense, golos_adversario
    else:
        # Jogo fora
        match = re.search(r'(.+?)\s+(\d+)\s*-\s*\*?\*?(\d+)\s+SC Farense', jogo_str)
        if match:
            adversario = match.group(1).strip()
            golos_adversario = int(match.group(2))
            golos_farense = int(match.group(3))
            return 'Fora', adversario, golos_farense, golos_adversario
    
    return None, None, None, None

def processar_markdown(md_file, csv_file):
    """Processa o markdown e gera CSV"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    jogos = []
    competicao_atual = ""
    epoca_atual = ""
    
    # Dividir por linhas
    linhas = conteudo.split('\n')
    
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        
        # Detectar época (ex: "## Época 1939/1940")
        if linha.startswith('## Época'):
            epoca_match = re.search(r'Época (\d{4}/\d{2,4})', linha)
            if epoca_match:
                epoca_atual = epoca_match.group(1)
        
        # Detectar competição
        if linha.startswith('###') and not linha.startswith('####'):
            competicao_atual = limpar_texto(linha.replace('#', '').strip())
        
        # Detectar tabela (cabeçalho com pipes)
        if '| Jornada |' in linha or '| J' in linha:
            # Pular linha separadora
            i += 2
            
            # Processar linhas de dados
            while i < len(linhas):
                linha_dados = linhas[i].strip()
                
                if not linha_dados or not linha_dados.startswith('|'):
                    break
                
                # Split por pipes
                colunas = [c.strip() for c in linha_dados.split('|')[1:-1]]
                
                if len(colunas) >= 4:
                    jornada = limpar_texto(colunas[0])
                    data = limpar_texto(colunas[1])
                    jogo = limpar_texto(colunas[2])
                    resultado = limpar_texto(colunas[3])
                    
                    # Extrair informações do jogo
                    local, adversario, golos_farense, golos_adversario = determinar_local_e_adversario(jogo)
                    
                    if local and adversario and golos_farense is not None:
                        # Determinar resultado
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
    
    print(f"✅ {len(jogos)} jogos convertidos para {csv_file}")
    
    # Estatísticas
    vitorias = sum(1 for j in jogos if j['resultado_tipo'] == 'V')
    empates = sum(1 for j in jogos if j['resultado_tipo'] == 'E')
    derrotas = sum(1 for j in jogos if j['resultado_tipo'] == 'D')
    
    print(f"\n📊 Estatísticas:")
    print(f"  • Vitórias: {vitorias}")
    print(f"  • Empates: {empates}")
    print(f"  • Derrotas: {derrotas}")
    print(f"  • Total de golos marcados: {sum(j['golos_farense'] for j in jogos)}")
    print(f"  • Total de golos sofridos: {sum(j['golos_adversario'] for j in jogos)}")

if __name__ == "__main__":
    processar_markdown('resultados_completos.md', 'farense_resultados.csv')
