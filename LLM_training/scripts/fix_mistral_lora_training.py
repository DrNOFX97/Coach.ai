#!/usr/bin/env python3
"""
Script para corrigir o notebook mistral_lora_training_corrigido_final.ipynb
"""

import json
import sys
from pathlib import Path

def fix_notebook(notebook_path):
    """
    Corrige os problemas no notebook que impedem o treino de arrancar
    
    Correções:
    1. Adiciona a importação de apply_lora
    2. Adiciona a aplicação do LoRA ao modelo após o carregamento
    3. Remove a linha duplicada na função de cálculo de perda
    """
    try:
        # Carregar o notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Backup do notebook original
        backup_path = notebook_path.with_suffix('.ipynb.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        print(f"✓ Backup criado em {backup_path}")
        
        # Correção 1: Adicionar importação de apply_lora
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if 'from mlx_lm import load, generate' in source:
                    # Adicionar importação de apply_lora
                    for i, line in enumerate(cell['source']):
                        if 'from mlx_lm import load, generate' in line:
                            cell['source'][i] = line.replace(
                                'from mlx_lm import load, generate', 
                                'from mlx_lm import load, generate\n    from mlx_lm.lora import apply_lora'
                            )
                    print("✓ Importação de apply_lora adicionada")
                    break
        
        # Correção 2: Adicionar aplicação do LoRA ao modelo
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if 'model, tokenizer = load(MODEL_NAME, adapter_path=None)' in source:
                    # Adicionar aplicação do LoRA
                    for i, line in enumerate(cell['source']):
                        if 'print(f"✓ Model loaded")' in line:
                            # Adicionar linhas após o carregamento do modelo
                            cell['source'].insert(i+1, '\n')
                            cell['source'].insert(i+2, '# Adaptar o modelo para LoRA - CORREÇÃO IMPORTANTE\n')
                            cell['source'].insert(i+3, 'print(f"Adaptando modelo para LoRA...")\n')
                            cell['source'].insert(i+4, 'model = apply_lora(model, **lora_config)\n')
                            cell['source'].insert(i+5, 'print(f"✓ Modelo adaptado para LoRA")\n')
                            print("✓ Aplicação do LoRA ao modelo adicionada")
                            break
        
        # Correção 3: Remover linha duplicada na função de cálculo de perda
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if 'def train_epoch(' in source and 'shift_logits = logits[:, :-1, :]' in source:
                    # Encontrar e remover a linha duplicada
                    found_first = False
                    lines_to_remove = []
                    
                    for i, line in enumerate(cell['source']):
                        if 'shift_logits = logits[:, :-1, :]' in line:
                            if found_first:
                                lines_to_remove.append(i)
                            else:
                                found_first = True
                    
                    # Remover linhas de trás para frente para não afetar os índices
                    for i in reversed(lines_to_remove):
                        cell['source'].pop(i)
                    
                    # Remover linha em branco extra se existir
                    for i, line in enumerate(cell['source']):
                        if line.strip() == "" and i > 0 and cell['source'][i-1].strip() == "":
                            cell['source'].pop(i)
                            break
                    
                    print("✓ Linha duplicada removida da função de cálculo de perda")
                    break
        
        # Salvar o notebook corrigido
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        
        print(f"✓ Notebook corrigido salvo em {notebook_path}")
        print("\nAs seguintes correções foram aplicadas:")
        print("1. Adicionada importação de apply_lora")
        print("2. Adicionada aplicação do LoRA ao modelo após o carregamento")
        print("3. Removida linha duplicada na função de cálculo de perda")
        print("\nAgora o treino deve arrancar corretamente!")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro ao corrigir o notebook: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        notebook_path = Path(sys.argv[1])
    else:
        notebook_path = Path("LLM_training/notebooks/mistral_lora_training_corrigido_final.ipynb")
    
    if not notebook_path.exists():
        print(f"✗ Arquivo não encontrado: {notebook_path}")
        sys.exit(1)
    
    success = fix_notebook(notebook_path)
    sys.exit(0 if success else 1)