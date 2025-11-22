# 🚀 MacBook Pro M1 16GB - Treino do Modelo Mistral-7B QLoRA

## ⚡ Quick Start (30 segundos)

```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

Executa as 10 seções do notebook e treina o modelo em ~2-3 horas.

---

## 📖 Documentação Organizada

### 🎯 SE VOCÊ QUER... LEIA ISTO:

| Necessidade | Ficheiro | Tempo |
|---|---|---|
| **Começar AGORA** | `START_TRAINING_M1.md` | 5 min |
| **Ver configurações** | `CONFIG_SUMMARY.txt` | 2 min |
| **Entender tudo** | `M1_16GB_OPTIMIZATION.md` | 20 min |
| **Info do dataset** | `DATASET_PREPARED.md` | 10 min |
| **Projeto completo** | `CLAUDE.md` | 30 min |
| **Próximas etapas** | `SETUP_COMPLETE.md` | 15 min |

---

## 🎯 CONFIGURAÇÕES (RESUMO)

### Batch Size & Memory
```
Batch Size:                  4
Gradient Accumulation:       2
Effective Batch Size:        8

Memory Usage:
  • Modelo: 3.8 GB
  • Batch: 3-4 GB
  • Total: ~10-11 GB (de 16 GB) ✓
```

### Training Parameters
```
Learning Rate:               2e-4
Epochs:                      3
Max Seq Length:              512
Warmup Steps:                100
```

### LoRA Configuration
```
Rank:                        8
Scale:                       16
Target Modules:              7 (q, v, k, o, gate, up, down)
```

---

## 📊 ESPERADO

### Tempo por Época
```
Época 1: ~40 minutos | Loss: 4.5 → 3.0
Época 2: ~40 minutos | Loss: 3.0 → 2.0
Época 3: ~40 minutos | Loss: 2.0 → 1.5
────────────────────────────────────────
TOTAL:   ~2-3 horas
```

### Velocidade
```
Tokens/segundo:              300-500
Exemplos/segundo:            3-5
Passos/minuto:               180-300
```

---

## 📚 FICHEIROS DO PROJETO

### 📂 Estrutura
```
/LLM_training/
├── notebooks/
│   └── mistral_qlora_training_m1_optimized.ipynb  ← USE ESTE ⭐
│
├── data/
│   ├── train.jsonl          (848 exemplos)
│   └── valid.jsonl          (95 exemplos)
│
├── scripts/
│   ├── train_qlora.py       (alternativa)
│   ├── inference_qlora.py   (testar modelo)
│   ├── monitor.py           (acompanhar treino)
│   └── visualization.py     (gerar gráficos)
│
├── models/
│   └── mistral-7b-4bit/     (3.8 GB)
│
├── checkpoints_qlora/       (será criado)
│   ├── checkpoint_*/
│   ├── training_metrics.json
│   └── adapters/
│
└── output/                  (será criado)
    └── mistral-7b-farense-qlora/
        └── adapters.safetensors
```

---

## 🚀 Passo a Passo

### 1️⃣ Verificação (5 min)
```bash
python3 --version  # 3.11+?
python3 -c "import mlx.core as mx; print(mx.default_device())"  # gpu?
wc -l data/train.jsonl data/valid.jsonl  # 848 + 95?
ls -lh models/mistral-7b-4bit/model.safetensors  # 3.8GB?
```

### 2️⃣ Notebook (2-3 horas)
```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
# Execute células 1-10 em ordem
```

### 3️⃣ Monitoramento (opcional)
```bash
# Em terminal separado:
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

### 4️⃣ Teste (5 min)
```bash
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
python3 scripts/visualization.py --report
```

---

## ⚙️ Ajustes (Se Necessário)

### Memory Error?
```python
batch_size = 2
gradient_accumulation_steps = 4  # Mantém effective=8
```

### Loss Not Decreasing?
```python
learning_rate = 5e-4  # Aumentar 2.5x
num_epochs = 5  # Mais épocas
```

### Want Better Quality?
```python
num_epochs = 5
max_seq_length = 768  # Cuidado com memória!
```

---

## ✅ Checklist

- ☐ Python 3.11+
- ☐ MLX GPU detectado
- ☐ Dataset pronto (train.jsonl, valid.jsonl)
- ☐ Modelo pronto (3.8GB)
- ☐ Jupyter instalado
- ☐ Navegador fechado
- ☐ Aplicações pesadas fechadas
- ☐ Pronto para começar!

---

## 📞 Próximas Etapas

1. ✅ Treinar modelo (~2-3 horas)
2. ✅ Validar qualidade (`inference_qlora.py`)
3. ✅ Gerar relatórios (`visualization.py`)
4. ✅ Analisar métricas (`training_summary.json`)
5. ✅ Integrar em produção (`output/mistral-7b-farense-qlora/`)

---

## 🎓 Documentação

| Ficheiro | Conteúdo | Leitor |
|---|---|---|
| `START_TRAINING_M1.md` | Quick start (30 seg) | Todos |
| `CONFIG_SUMMARY.txt` | Resumo visual | Todos |
| `M1_16GB_OPTIMIZATION.md` | Guia completo | Técnico |
| `DATASET_PREPARED.md` | Info dataset | Data scientist |
| `CLAUDE.md` | Projeto completo | Developers |
| `SETUP_COMPLETE.md` | Setup detalhado | Setup |

---

## 🔗 Referências Rápidas

- **Batch Size Explicado:** `M1_16GB_OPTIMIZATION.md` (seção 2.1)
- **Trajetória Loss:** `CONFIG_SUMMARY.txt` (seção Loss Esperada)
- **Troubleshooting:** `M1_16GB_OPTIMIZATION.md` (seção 7.4)
- **Monitoramento:** `scripts/monitor.py`

---

## 📊 Dataset

- **Total:** 943 exemplos
- **Treino:** 848 (89.9%)
- **Validação:** 95 (10.1%)
- **Formato:** JSONL (prompt + completion)
- **Domínio:** História Farense ⚽
- **Qualidade:** 100% válido

---

## 🎯 Resultado Final

Após treino:
```
checkpoints_qlora/
├── training_metrics.json      ← Dados de treino
├── training_summary.json      ← Resumo
├── adapters/                  ← Melhor modelo
└── plots/                     ← Gráficos

output/mistral-7b-farense-qlora/
└── adapters.safetensors       ← Pronto para usar!
```

---

## ⚡ Performance

| Métrica | Esperado |
|---|---|
| Tokens/segundo | 300-500 |
| Exemplos/segundo | 3-5 |
| Tempo/época | 35-40 min |
| Tempo total | 2-3 horas |
| Memória máxima | ~11 GB |

---

## 🚀 Comece Agora!

```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

---

**Hardware:** MacBook Pro M1 16GB
**Modelo:** Mistral-7B (QLoRA)
**Dataset:** 943 Exemplos Farense
**Status:** ✅ Pronto para Treino

**Boa sorte! ⚽🤖**
