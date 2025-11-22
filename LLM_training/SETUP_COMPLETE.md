# ✅ SETUP COMPLETO - PRONTO PARA TREINO

## Resumo do Que Foi Feito

### 1. ✅ Dataset Preparado
- **Total:** 943 exemplos
- **Treino:** 848 exemplos (89.9%)
- **Validação:** 95 exemplos (10.1%)
- **Formato:** JSONL com estrutura prompt/completion
- **Limpeza:** Normalização de épocas realizada
- **Validação:** 100% de registos válidos

**Ficheiros:**
- `data/train.jsonl` - Dataset de treino (pronto)
- `data/valid.jsonl` - Dataset de validação (pronto)

### 2. ✅ Notebook Otimizado Criado
**Ficheiro:** `notebooks/mistral_qlora_training_m1_optimized.ipynb`

Este notebook está especificamente otimizado para seu **MacBook Pro M1 16GB** com:
- ✓ Batch size = 4 (seguro para M1 16GB)
- ✓ Gradient accumulation = 2 (effective batch = 8)
- ✓ Learning rate = 2e-4 (ótimo para LoRA)
- ✓ 3 épocas (bom para dataset de 943 exemplos)
- ✓ Sistema completo de métricas e logging
- ✓ Checkpointing automático para recuperação

### 3. ✅ Documentação Criada

#### Documentação de Configuração
- **`M1_16GB_OPTIMIZATION.md`** - Guia detalhado de otimizações
  - Explicação de cada parâmetro
  - Uso de memória esperado
  - Trajetória de loss prevista
  - Troubleshooting completo

- **`CONFIG_SUMMARY.txt`** - Resumo visual das configurações
  - Fácil de consultar durante treino
  - Parâmetros principais highlighted
  - Checklist pré-treino

- **`START_TRAINING_M1.md`** - Quick start em 30 segundos
  - Instruções diretas
  - Sem complicações
  - Pronto para executar

#### Documentação do Dataset
- **`DATASET_PREPARED.md`** - Análise completa do dataset
  - Estatísticas detalhadas
  - Distribuição de dados
  - Informações de qualidade
  - Recomendações

#### Documentação do Projeto
- **`CLAUDE.md`** - Guia para futuros Claude Code
  - Arquitetura completa
  - Como estender
  - Troubleshooting
  - Comandos comuns

### 4. ✅ Scripts Auxiliares

#### Script de Split Atualizado
- **`scripts/split_data_proper.py`** - Novo script de split
  - Mantém formato JSONL intacto
  - Split 90/10 reproducível
  - Seed 42 para determinismo

#### Scripts Já Disponíveis
- `scripts/train_qlora.py` - Treino via script (alternativa)
- `scripts/inference_qlora.py` - Testar modelo
- `scripts/monitor.py` - Monitoramento em tempo real
- `scripts/visualization.py` - Gerar gráficos
- `scripts/clean_dataset.py` - Limpeza de dados (já usado)

---

## 🎯 Configurações M1 16GB (Resumo)

### Batch Size
```
batch_size = 4
gradient_accumulation_steps = 2
Effective Batch Size = 8

Memória usada: ~3-4 GB por batch
Total máximo: ~10-11 GB (de 16 GB disponíveis)
```

### Learning & Training
```
Learning Rate: 2e-4
Warmup Steps: 100
Num Epochs: 3
Max Seq Length: 512
```

### LoRA Configuration
```
Rank: 8
Scale: 16
Target Modules: 7 (q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj)
```

### Checkpointing
```
Save Checkpoint: Every 200 steps
Validate: Every 200 steps
Log: Every 10 steps
```

---

## 📊 Tempo Estimado

| Fase | Duração | Notas |
|------|---------|-------|
| Setup & Verificação | 2-3 min | Carregar imports e dados |
| Load Modelo | 1-2 min | Primeira vez pode ser mais lenta |
| Tokenização | 1 min | Converter texto em tokens |
| **TREINO ÉPOCA 1** | **~40 min** | Loss: 4.5 → 3.0 |
| **TREINO ÉPOCA 2** | **~40 min** | Loss: 3.0 → 2.0 |
| **TREINO ÉPOCA 3** | **~40 min** | Loss: 2.0 → 1.5 |
| Testes & Export | 5 min | Validação final |
| **TOTAL** | **~2-3 horas** | Tempo total de execução |

---

## 🚀 Como Começar

### Passo 1: Pré-requisitos (5 min)

```bash
# Verificar Python
python3 --version  # Deve ser 3.11+

# Verificar GPU
python3 -c "import mlx.core as mx; print(f'Device: {mx.default_device()}')"

# Verificar dados
wc -l data/train.jsonl data/valid.jsonl

# Verificar modelo
ls -lh models/mistral-7b-4bit/model.safetensors
```

### Passo 2: Abrir Notebook

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

### Passo 3: Executar Células

1. **Seção 1:** Setup (2-3 min)
   - ✓ Imports e verificações

2. **Seção 2:** Configurações (30 seg)
   - ✓ Mostra batch_size=4 e outros parâmetros

3. **Seção 3-4:** Dados e Modelo (2-3 min)
   - ✓ Carrega 943 exemplos
   - ✓ Carrega Mistral-7B

4. **Seção 5-6:** Tokenização (1 min)
   - ✓ Converte em tokens

5. **Seção 7:** TREINO (2-3 horas) ⭐
   - ✓ **Deixe rodar sem interrupção**
   - ✓ Saída a cada 10 passos
   - ✓ Validação a cada 200 passos

6. **Seção 8-10:** Testes (5 min)
   - ✓ Testa geração
   - ✓ Salva modelo

### Passo 4: Monitoramento (Opcional, em Terminal Separado)

```bash
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

Mostra em tempo real:
- Loss atual
- Validação loss
- Memória usada
- ETA estimado

### Passo 5: Após Treino

```bash
# Visualizar gráficos
python3 scripts/visualization.py --report

# Testar modelo
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"

# Ver métricas
cat checkpoints_qlora/training_summary.json | jq
```

---

## 📁 Estrutura Final

```
/LLM_training/
├── CLAUDE.md                                    ← Para futuros Claude Code
├── CONFIG_SUMMARY.txt                          ← Resumo visual (CONSULTAR)
├── DATASET_PREPARED.md                         ← Info dataset
├── M1_16GB_OPTIMIZATION.md                     ← Detalhes otimizações
├── START_TRAINING_M1.md                        ← Quick start
├── SETUP_COMPLETE.md                           ← Este ficheiro
│
├── data/
│   ├── train.jsonl                             ← 848 exemplos (PRONTO)
│   ├── valid.jsonl                             ← 95 exemplos (PRONTO)
│   └── farense_dataset_cleaned.jsonl           ← Backup do limpo
│
├── notebooks/
│   ├── mistral_qlora_training_m1_optimized.ipynb  ← USE ESTE! ⭐
│   └── [outros notebooks]
│
├── scripts/
│   ├── train_qlora.py                          ← Alternativa ao notebook
│   ├── split_data_proper.py                    ← Novo script
│   ├── inference_qlora.py                      ← Testar modelo
│   ├── monitor.py                              ← Monitoramento
│   ├── visualization.py                        ← Gerar gráficos
│   └── [outros scripts]
│
├── models/
│   └── mistral-7b-4bit/                        ← Modelo base (3.8GB)
│
├── checkpoints_qlora/                          ← Será criado durante treino
│   ├── checkpoint_epoch*/                      ← Checkpoints
│   ├── training_metrics.json                   ← Métricas
│   ├── training_state.json                     ← Estado
│   └── adapters/                               ← Melhor modelo
│
└── output/
    └── mistral-7b-farense-qlora/               ← Será criado após treino
        ├── adapters.safetensors                ← Modelo final
        ├── adapter_config.json
        └── training_config.json
```

---

## ⚡ Configurações Rápidas (Se Necessário)

### Se Erro "Out of Memory"
```python
batch_size = 2
gradient_accumulation_steps = 4
# Effective batch = 8 (mantém-se igual)
```

### Se Loss Não Diminui
```python
learning_rate = 5e-4  # Aumentar 2.5x
num_epochs = 4  # Mais épocas
```

### Se Quer Melhor Qualidade
```python
num_epochs = 5
max_seq_length = 768
# Cuidado com memória!
```

---

## ✅ Checklist Final

Antes de começar:

- ☐ Python 3.11+ instalado
- ☐ MLX com GPU detectado (`mx.default_device() = gpu`)
- ☐ Dataset em `data/train.jsonl` e `data/valid.jsonl`
- ☐ Modelo em `models/mistral-7b-4bit/` (3.8GB)
- ☐ Jupyter instalado
- ☐ Notebook aberto: `mistral_qlora_training_m1_optimized.ipynb`
- ☐ Navegador fechado (economiza ~2GB RAM)
- ☐ Outras aplicações pesadas fechadas

---

## 🎓 Documentação de Referência

Para consultar durante/após treino:

1. **Quick Questions:** `CONFIG_SUMMARY.txt`
2. **Explicações Detalhadas:** `M1_16GB_OPTIMIZATION.md`
3. **Próximas Etapas:** `START_TRAINING_M1.md`
4. **Info Dataset:** `DATASET_PREPARED.md`
5. **Projeto Completo:** `CLAUDE.md`

---

## 🚀 Pronto Para Começar!

Tudo está configurado e otimizado para seu **MacBook Pro M1 16GB**.

**Comando para começar:**

```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

---

## 📊 Resultado Esperado

Após ~2-3 horas de treino, você terá:

1. ✅ **Checkpoints** em `checkpoints_qlora/`
   - Modelos intermédios salvos a cada 200 passos
   - Possibilidade de recuperação se falhar

2. ✅ **Métricas** em `checkpoints_qlora/training_metrics.json`
   - Loss ao longo do tempo
   - Validação loss
   - Timestamps e informações de épocas

3. ✅ **Modelo Final** em `output/mistral-7b-farense-qlora/`
   - `adapters.safetensors` - Usar isto para inferência
   - `adapter_config.json` - Configuração LoRA
   - `training_config.json` - Hiperparâmetros usados

4. ✅ **Gráficos** em `checkpoints_qlora/plots/`
   - Loss curves (train vs validation)
   - Memory usage over time
   - Learning rate schedule

---

**Status: ✅ PRONTO PARA TREINO**

**Data:** 18 Novembro 2025  
**Hardware:** MacBook Pro M1 16GB  
**Modelo:** Mistral-7B (QLoRA)  
**Dataset:** 943 exemplos Farense  
**Tempo Estimado:** 2-3 horas  

**Boa sorte! ⚽🤖**
