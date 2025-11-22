# 🚀 COMECE A TREINAR EM 30 SEGUNDOS

## Quick Start para MacBook Pro M1 16GB

### ✅ PRÉ-REQUISITOS (Verifique)

```bash
# 1. Verificar Python 3.11+
python3 --version

# 2. Verificar MLX GPU
python3 -c "import mlx.core as mx; print(f'✓ Device: {mx.default_device()}')"

# 3. Verificar dados (devem existir)
wc -l data/train.jsonl data/valid.jsonl
# Esperado: 848 train.jsonl, 95 valid.jsonl

# 4. Verificar modelo (3.8GB)
ls -lh models/mistral-7b-4bit/model.safetensors
```

---

## 🎯 OPÇÃO 1: TREINO INTERATIVO (Recomendado)

### 1. Abrir Jupyter
```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

### 2. Executar Todas as Células em Ordem
- Seção 1: Setup (2-3 min)
- Seção 2: Configurações (mostra batch_size=4)
- Seção 3-4: Carregar dados e modelo (2-3 min)
- Seção 5-6: Tokenização e setup (1 min)
- **Seção 7: TREINO (2-3 horas)** ⭐
- Seção 8-10: Testes e resultados (5 min)

**Tempo Total:** ~2.5-3.5 horas

---

## 🎯 OPÇÃO 2: TREINO VIA SCRIPT

```bash
# Executar treino completo via script
python3 scripts/train_qlora.py

# Isto vai:
# 1. Carregar dados
# 2. Carregar modelo
# 3. Tokenizar
# 4. Treinar 3 épocas
# 5. Salvar checkpoints
# 6. Gerar métricas
```

---

## 📊 CONFIGURAÇÕES (M1 16GB)

| Parâmetro | Valor | Notas |
|-----------|-------|-------|
| **Batch Size** | **4** | Seguro para M1 16GB |
| **Gradient Accumulation** | **2** | Effective batch = 8 |
| **Learning Rate** | **2e-4** | Padrão para LoRA |
| **Epochs** | **3** | ~40 min cada |
| **Max Seq Length** | **512** | Suporta 512 tokens |

**Se der erro de memória:**
```python
batch_size = 2  # Reduzir para isto
gradient_accumulation_steps = 4
```

---

## 📈 DURANTE O TREINO

### Terminal Separado: Monitorar Progresso

```bash
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

Mostra:
- Loss atual
- Validação loss
- Memória usada
- Tokens por segundo
- ETA estimado

### Output Esperado no Notebook

```
🚀 INICIANDO TREINO
==========================================================================

📍 ÉPOCA 1/3
----------------------------------------------------------------------
  Passo  10 | Loss: 4.8523
  Passo  20 | Loss: 4.5432
  Passo  30 | Loss: 4.2341
  ...
  Passo 200 | Loss: 3.1234
  [INFO] Avaliando em validação...
  ✓ Val Loss: 3.0123

✓ Época 1 concluída em 2145.3s
  Loss médio: 3.5678

📍 ÉPOCA 2/3
...

✓ TREINO COMPLETO em 2.1 horas
```

---

## 📂 FICHEIROS GERADOS

Após treino, você terá:

```
checkpoints_qlora/
├── training_metrics.json       ← Dados de treino
├── training_summary.json       ← Resumo
├── checkpoint_epoch*_step*/    ← Checkpoints
└── adapters/                   ← Melhor modelo
    └── adapters.safetensors

output/mistral-7b-farense-qlora/
└── adapters.safetensors        ← USE ESTE PARA INFERÊNCIA
```

---

## 🧪 APÓS TREINO: TESTAR MODELO

### Teste Rápido
```bash
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
```

Output esperado:
```json
{
  "prompt": "Qual foi a melhor classificação do Farense?",
  "response": "O Farense teve sua melhor classificação...",
  "method": "QLoRA",
  "status": "success"
}
```

### Visualizar Gráficos
```bash
python3 scripts/visualization.py --report
```

Gera:
- `loss_curves.png` - Loss over time
- `learning_rate.png` - LR schedule
- `memory_usage.png` - Memory tracking

---

## ⚡ DICAS RÁPIDAS

1. **Feche navegador** antes de treinar (economiza 2GB)
2. **Não toque no notebook** durante treino (deixe rodar)
3. **Use monitor.py** em terminal separado para acompanhar
4. **Salvar checkpoints** permite retomar se falhar
5. **Se OOM:** Reduzir batch_size de 4 para 2

---

## 🆘 ERROS COMUNS

### "Out of Memory"
```
Solução: batch_size = 2 (em vez de 4)
```

### Loss stuck at 4.5
```
Solução: learning_rate = 5e-4 (em vez de 2e-4)
```

### GPU not detected
```
Verifique: python3 -c "import mlx.core as mx; print(mx.default_device())"
Deve dizer: gpu
```

---

## 📞 PRÓXIMAS ETAPAS

Após treino bem-sucedido:

1. ✅ Validar qualidade (rodar inference_qlora.py)
2. ✅ Analisar métricas (ver training_summary.json)
3. ✅ Gerar relatórios (scripts/visualization.py)
4. ✅ Integrar em aplicação (usar output/mistral-7b-farense-qlora/)

---

## 🎓 DOCUMENTAÇÃO COMPLETA

Para detalhes técnicos, leia:
- `M1_16GB_OPTIMIZATION.md` - Configurações detalhadas
- `DATASET_PREPARED.md` - Informações do dataset
- `CLAUDE.md` - Guia completo do projeto
- `docs/DOCS_INDEX.md` - Todos os guias

---

**Tudo pronto? Abra o notebook e comece! 🚀**

```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

Boa sorte! ⚽🤖
