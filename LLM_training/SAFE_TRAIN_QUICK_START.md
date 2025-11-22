# Safe Train - Quick Start 🚀

Sistema automático de diagnóstico e recomendação de configuração para evitar crashes.

## TL;DR (Muito Resumido)

```bash
# 1. Verificar sistema e obter config recomendada
python3 scripts/safe_train.py

# 2. Seguir instruções impressas (abrir notebook com config recomendada)
jupyter notebook notebooks/mistral_qlora_training.ipynb

# 3. Numa terminal separada, monitorar treino
python3 scripts/monitor.py --refresh 5
```

---

## Modo Detalhado

### Passo 1: Executar Preflight Check

```bash
python3 scripts/preflight_check.py
```

Este script:
- ✓ Verifica Python, MLX, dependências
- ✓ Detecta hardware (M1/M2/M3, RAM disponível)
- ✓ Testa GPU/Metal availability
- ✓ Valida dados de treino
- ✓ Testa carregamento de modelo
- ✓ **Recomenda configuração otimizada** baseado no seu sistema

**Output:**
- `checkpoints_qlora/preflight_report.json` - Relatório completo
- `checkpoints_qlora/recommended_config.json` - Config otimizada para seu sistema

### Passo 2: Aplicar Configuração Recomendada

#### Opção A: Via Notebook (RECOMENDADO)

```bash
jupyter notebook notebooks/mistral_qlora_training.ipynb
```

1. Abra a célula "Configuração do Treino"
2. Atualize com valores de `checkpoints_qlora/recommended_config.json`:
   ```python
   training_config = {
       "batch_size": 2,              # ← DO ARQUIVO
       "gradient_accumulation": 2,   # ← DO ARQUIVO
       "learning_rate": 3e-4,        # ← DO ARQUIVO
       "max_seq_length": 512,        # ← DO ARQUIVO
       # ... resto igual
   }
   ```
3. Corra as células normalmente

#### Opção B: Via Script Python

```bash
# Editar scripts/train_qlora.py
nano scripts/train_qlora.py
```

Atualizar a seção `training_config`:
```python
training_config = {
    "batch_size": 2,              # ← VALOR RECOMENDADO
    "gradient_accumulation": 2,   # ← VALOR RECOMENDADO
    "learning_rate": 3e-4,        # ← VALOR RECOMENDADO
    # ... etc
}
```

Depois correr:
```bash
python3 scripts/train_qlora.py
```

### Passo 3: Monitorar Treino (Terminal Separada)

```bash
# Enquanto treino está em progresso, numa terminal diferente:
python3 scripts/monitor.py --refresh 5
```

Mostra em tempo real:
- Loss de treino/validação
- Uso de memória
- ETA até conclusão
- Checkpoint atual

### Passo 4: Após Treino

```bash
# Visualizar resultados
python3 scripts/visualization.py --report

# Testar modelo
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
```

---

## O Que Cada Config Faz

### batch_size
- **Alto (4)**: Mais memória, treino mais rápido, menos estável
- **Médio (2)**: Equilíbrio
- **Baixo (1)**: Pouca memória, treino mais lento

### gradient_accumulation
- Simula batch_size maior sem usar mais memória
- `batch_size=1, grad_accum=4` ≈ `batch_size=4, grad_accum=1` em memória
- Aumentar se houver OOM errors

### max_seq_length
- **512**: Sequências completas, mais memória
- **256**: Sequências cortadas, menos memória
- Aumentar se perder contexto

### learning_rate
- **5e-4**: Taxa alta, risco de instabilidade
- **3e-4**: Taxa média, recomendado
- **1e-4**: Taxa baixa, convergência lenta

---

## Cenários de Recomendação

### M1 com 8GB (Base Model)
```json
{
  "batch_size": 2,
  "gradient_accumulation": 2,
  "max_seq_length": 512,
  "learning_rate": 3e-4
}
```

### M1 Pro com 16GB
```json
{
  "batch_size": 4,
  "gradient_accumulation": 2,
  "max_seq_length": 512,
  "learning_rate": 5e-4
}
```

### M1 com 6GB (Tight)
```json
{
  "batch_size": 1,
  "gradient_accumulation": 4,
  "max_seq_length": 256,
  "learning_rate": 2e-4
}
```

### Sem GPU (CPU Fallback)
```json
{
  "batch_size": 1,
  "gradient_accumulation": 8,
  "max_seq_length": 128,
  "learning_rate": 1e-4
}
```

---

## Troubleshooting

### "Out of Memory" Error

1. Reduzir `batch_size`: `4 → 2 → 1`
2. Aumentar `gradient_accumulation`: `2 → 4 → 8`
3. Reduzir `max_seq_length`: `512 → 256 → 128`

### Treino Muito Lento

1. Aumentar `batch_size` (se houver memória)
2. Aumentar `learning_rate`
3. Reduzir `max_seq_length`

### Loss não Diminui

1. Aumentar `learning_rate` (ex: 3e-4 → 5e-4)
2. Aumentar `warmup_steps`
3. Validar dados com: `python3 scripts/validate_jsonl.py data/train.jsonl`

### Treino Crashou

1. Correr `python3 scripts/preflight_check.py` novamente
2. Reduzir configs mais ainda
3. Fechar outras aplicações para libertar memória

---

## Ficheiros Gerados

Após correr `preflight_check.py`:

```
checkpoints_qlora/
├── preflight_report.json       # Relatório completo do sistema
└── recommended_config.json     # Config otimizada (COPIAR VALORES DAQUI)
```

Após treino:

```
checkpoints_qlora/
├── checkpoint_epoch_0_step_*   # Checkpoints intermediários
├── checkpoint_epoch_1_step_*
├── checkpoint_epoch_2_step_*
├── adapters/                   # Melhor modelo encontrado
├── training_metrics.json       # Métricas detalhadas
├── training_metrics.csv        # Metrics em CSV
├── training_summary.json       # Resumo final
└── training_state.json         # Estado para resume
```

---

## Workflow Completo

```
┌─────────────────────────────────────────┐
│ 1. Preflight Check                      │
│    python3 scripts/preflight_check.py   │
│    → Gera recommended_config.json       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 2. Aplicar Config Recomendada           │
│    • Editar notebook/script com valores │
│    • Ou copiar/colar da config JSON     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 3. Iniciar Treino                       │
│    jupyter notebook mistral_qlora_...   │
│    ou                                   │
│    python3 scripts/train_qlora.py       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 4. Monitorar (Terminal Separada)        │
│    python3 scripts/monitor.py           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 5. Analisar Resultados                  │
│    python3 scripts/visualization.py     │
│    python3 scripts/inference_qlora.py   │
└─────────────────────────────────────────┘
```

---

## Variáveis de Ambiente (Opcional)

```bash
# Forçar CPU (útil para debugging)
export MLX_FORCE_CPU=1
python3 scripts/train_qlora.py

# Verboso
export DEBUG=1
python3 scripts/train_qlora.py

# Especificar arquivo de treino
export TRAIN_FILE=data/seu_arquivo.jsonl
python3 scripts/train_qlora.py
```

---

## Dúvidas Frequentes

**P: O preflight check demora muito (modelo a descarregar)?**
R: Sim, primeira vez descarrega ~3.8GB. Dar tempo, não desligar.

**P: Qual config devo escolher?**
R: Use a gerada por `preflight_check.py` - é específica para seu sistema.

**P: Posso mudar config a meio do treino?**
R: Não, completar treino com config atual. Ajustar para próximo treino.

**P: Posso correr vários treinos em paralelo?**
R: Não, GPU Metal não suporta bem. Um de cada vez.

**P: Como retomar treino interrompido?**
R: Correr `train_qlora.py` novamente - detecta checkpoint automaticamente.

---

## Próximos Passos

1. **Correr preflight**: `python3 scripts/preflight_check.py`
2. **Ler recomendações**: Abrir `checkpoints_qlora/recommended_config.json`
3. **Aplicar config**: Editar notebook ou script
4. **Treinar**: Correr notebook ou script
5. **Monitorar**: Abrir monitor em terminal separada

**Boa sorte!** 🚀
