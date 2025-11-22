#!/usr/bin/env python3
"""
Script para verificar se as correções foram aplicadas corretamente ao notebook
"""

import json
import sys
from pathlib import Path

def verify_notebook(notebook_path):
    """
    Verifica se as correções foram aplicadas corretamente ao notebook
    """
    try:
        # Carregar o notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Verificar as correções
        corrections = {
            "import_apply_lora": False,
            "apply_lora_to_model": False,
            "removed_duplicate_line": True  # Assumimos que está correto até encontrarmos a duplicação
        }
        
        # Verificar a importação de apply_lora
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if 'from mlx_lm.lora import apply_lora' in source:
                    corrections["import_apply_lora"] = True
                    print("✓ Importação de apply_lora encontrada")
                
                # Verificar a aplicação do LoRA ao modelo
                if 'model = apply_lora(model, **lora_config)' in source:
                    corrections["apply_lora_to_model"] = True
                    print("✓ Aplicação do LoRA ao modelo encontrada")
                
                # Verificar se a linha duplicada foi removida
                if 'def train_epoch(' in source:
                    shift_logits_count = source.count('shift_logits = logits[:, :-1, :]')
                    if shift_logits_count > 1:
                        corrections["removed_duplicate_line"] = False
                        print("✗ Linha duplicada ainda presente na função de cálculo de perda")
                    else:
                        print("✓ Linha duplicada removida corretamente")
        
        # Verificar se todas as correções foram aplicadas
        all_corrected = all(corrections.values())
        
        if all_corrected:
            print("\n✓ Todas as correções foram aplicadas corretamente!")
            print("O notebook deve agora arrancar o treino sem problemas.")
        else:
            print("\n✗ Algumas correções não foram aplicadas corretamente:")
            if not corrections["import_apply_lora"]:
                print("  - Importação de apply_lora não encontrada")
            if not corrections["apply_lora_to_model"]:
                print("  - Aplicação do LoRA ao modelo não encontrada")
            if not corrections["removed_duplicate_line"]:
                print("  - Linha duplicada ainda presente na função de cálculo de perda")
        
        return all_corrected
    
    except Exception as e:
        print(f"✗ Erro ao verificar o notebook: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        notebook_path = Path(sys.argv[1])
    else:
        notebook_path = Path("LLM_training/notebooks/mistral_lora_training_corrigido_final.ipynb")
    
    if not notebook_path.exists():
        print(f"✗ Arquivo não encontrado: {notebook_path}")
        sys.exit(1)
    
    success = verify_notebook(notebook_path)
    sys.exit(0 if success else 1)