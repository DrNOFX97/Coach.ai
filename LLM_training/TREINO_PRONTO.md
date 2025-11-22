# Treino V3 Final Completo - Pronto para Executar

## Status: ✅ TUDO PREPARADO

Dataset: **1.127 exemplos** (953 base + 159 dos livros + 15 extras)
- Train: 1.014 exemplos (89.9%)
- Validation: 113 exemplos (10.1%)

---

## Para Treinar Agora

### Opção 1: Treino Completo (Recomendado)

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training

python3 scripts/train_lora.py \
    --train_data data/train_v3_final_complete.jsonl \
    --val_data data/valid_v3_final_complete.jsonl \
    --output_dir checkpoints_v3_final_complete \
    --epochs 3 \
    --batch_size 4 \
    --learning_rate 5e-4
```

### Opção 2: Fine-tuning do V2 Existente

```bash
python3 scripts/train_lora_incremental.py \
    --base_checkpoint checkpoints_v2 \
    --train_data data/train_v3_final_complete.jsonl \
    --val_data data/valid_v3_final_complete.jsonl \
    --output_dir checkpoints_v3_final_complete_finetune \
    --epochs 2
```

---

## Ficheiros Necessários

✅ data/train_v3_final_complete.jsonl (1.014 pares)
✅ data/valid_v3_final_complete.jsonl (113 pares)
✅ scripts/train_lora.py (pronto)
✅ checkpoints_v2/ (modelo anterior, se usar Opção 2)

---

## Depois do Treino

```bash
# Avaliar modelo
python3 scripts/compare_models.py \
    --model_v2 checkpoints_v2 \
    --model_v3 checkpoints_v3_expanded \
    --test_data test_queries.txt

# Testar respostas
python3 scripts/inference.py \
    --model checkpoints_v3_expanded \
    --query "Qual era a primeira sede do Farense?"
```

---

## Resumo de Dados Adicionados

```
Dataset V2: 953 exemplos
+ Livro 1 (TXT): 89 pares
+ Livro 2 (DOCX): 70 pares
+ Instalações Desportivas: 10 pares
+ Nova Sede (Complexo): 5 pares
= Dataset V3 Final Completo: 1.127 exemplos

Aumento total: +174 pares (+18.3%)
```

---

## Tudo Pronto! 🎯

Quando estiver descansado, execute o comando acima e o treino começará.

Estimado tempo de treino: 2-4 horas (dependendo de GPU)

---

**Criado**: Novembro 2024
**Status**: Pronto para executar
