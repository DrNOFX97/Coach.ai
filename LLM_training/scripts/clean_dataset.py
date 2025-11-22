import json
import re

def extract_season_from_competicao(competicao):
    # Regex para encontrar padrões como "85/86", "1985/1986", "1985/86"
    match = re.search(r'(\d{2}|\d{4})/(\d{2}|\d{4})', competicao)
    if match:
        year1 = int(match.group(1))
        year2 = int(match.group(2))

        if year1 < 100:  # Assume XX/YY format, e.g., 85/86
            if year1 > 50:  # Assume 20th century, e.g., 1985
                year1 += 1900
            else:  # Assume 21st century, e.g., 2005
                year1 += 2000
        
        if year2 < 100: # Assume XX/YY format, e.g., 85/86
            if year2 < year1 % 100: # e.g. 85/84, means 1985/1984
                year2 += 1900
            else: # e.g. 85/86, means 1985/1986
                year2 += year1 - (year1 % 100)
        
        return f"{year1}/{year2}"
    return None

def infer_season_from_date(date_str):
    if not date_str or date_str == "-":
        return None
    
    # Regex para extrair o ano do formato YYYY-MM-DD
    match = re.search(r'(\d{4})-\d{2}-\d{2}', date_str)
    if match:
        year = int(match.group(1))
        # Assumimos que a época começa no ano X e termina no ano X+1
        # Por exemplo, 1983-12-01 -> época 1983/1984
        return f"{year}/{year + 1}"
    return None

def clean_dataset(input_file, output_file):
    cleaned_data = []
    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            entry = json.loads(line)
            
            original_epoca = entry['metadata'].get('epoca', '')
            competicao = entry['metadata'].get('competicao', '')
            prompt = entry['prompt']

            new_epoca = None

            # 1. Tentar extrair da competição
            if competicao:
                new_epoca = extract_season_from_competicao(competicao)
            
            # 2. Se não encontrou na competição, tentar inferir do prompt (data)
            if not new_epoca:
                # Extrair a data do prompt
                date_match = re.search(r'em (\d{4}-\d{2}-\d{2})', prompt)
                if date_match:
                    date_str = date_match.group(1)
                    new_epoca = infer_season_from_date(date_str)
            
            # Se ainda não encontrou, manter a original (se for válida e não for o placeholder)
            if not new_epoca and original_epoca and original_epoca != "1939/1940":
                new_epoca = original_epoca
            elif not new_epoca: # Fallback para um valor padrão se tudo falhar
                new_epoca = "Desconhecida" # Ou "" se preferir vazio

            entry['metadata']['epoca'] = new_epoca
            cleaned_data.append(entry)

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for entry in cleaned_data:
            f_out.write(json.dumps(entry, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    input_jsonl_file = "data/farense_dataset.jsonl"
    output_jsonl_file = "data/farense_dataset_cleaned.jsonl"
    clean_dataset(input_jsonl_file, output_jsonl_file)
    print(f"Ficheiro limpo guardado em: {output_jsonl_file}")
