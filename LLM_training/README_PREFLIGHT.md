# 🚀 Safe Train - Sistema de Verificação Pré-Treino

Um sistema completo e automático que **verifica seu sistema antes de treinar** e **recomenda as melhores configurações para evitar crashes**.

## O Problema

O treino pode crashar por:
- ❌ Memória insuficiente
- ❌ Dependências faltando
- ❌ GPU não detectada
- ❌ Configuração inadequada
- ❌ Espaço em disco insuficiente

## A Solução

### ✅ Sistema de Verificação Automática

Antes de iniciar o treino, corra:

```bash
python3 scripts/preflight_check.py
```

Este script:
1. ✓ Verifica Python, MLX, todas as dependências
2. ✓ Detecta hardware (Apple Silicon, RAM, GPU)
3. ✓ Valida dados de treino
4. ✓ Testa carregamento de modelo
5. ✓ Verifica espaço em disco
6. ✓ **Recomenda configuração otimizada** para seu sistema

## Resultado

O script gera dois ficheiros:

```
checkpoints_qlora/
├── preflight_report.json       ← Relatório completo do diagnóstico
└── recommended_config.json     ← CONFIG OTIMIZADA PARA SEU SISTEMA
```

## Como Usar

### Passo 1: Diagnóstico do Sistema (2 minutos)

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training
python3 scripts/preflight_check.py
```

**Output esperado:**
```
================================================================================
  PREFLIGHT CHECK - LLM TRAINING
================================================================================

>>> 1. VERIFICAÇÃO DE HARDWARE
  ✓ Apple Silicon (M1/M2/M3) detectado
  ✓ Memória: 7.3 GB disponível
  ✓ CPU: 8 cores

>>> 2. VERIFICAÇÃO DE DEPENDÊNCIAS
  ✓ MLX
  ✓ MLX-LM
  ✓ Transformers
  ...

>>> 3. VERIFICAÇÃO DE GPU
  ✓ Metal GPU detectado e ativado

>>> 4. VERIFICAÇÃO DE DADOS
  ✓ Ficheiro de treino: train_v3_final_complete.jsonl (848 amostras)
  ✓ Ficheiro de validação: valid_v3_final_complete.jsonl (95 amostras)

>>> 5. VERIFICAÇÃO DE MODELO
  ✓ Modelo base encontrado (3.8 GB)
  ✓ Modelo carregado com sucesso

>>> 6. VERIFICAÇÃO DE ESPAÇO EM DISCO
  ✓ Espaço em disco suficiente (10.7 GB)

>>> 7. RECOMENDAÇÃO DE CONFIGURAÇÃO
  CONFIGURAÇÃO RECOMENDADA:
  • batch_size: 1
  • gradient_accumulation: 4
  • max_seq_length: 256
  • learning_rate: 0.0002
  • num_epochs: 3

  RAZÃO: Memória limitada (6-8 GB) - config reduzida

================================================================================
  RESUMO DO PREFLIGHT CHECK
================================================================================
  ✓ Passou: 16
  ✗ Falhou: 1 (espaço em disco - não crítico)
  ⚠ Avisos: 2 (Python version, memória)

✓ Relatório salvo: checkpoints_qlora/preflight_report.json
✓ Config salva: checkpoints_qlora/recommended_config.json
```

### Passo 2: Aplicar Configuração Recomendada

Abrir o ficheiro gerado:

```bash
cat checkpoints_qlora/recommended_config.json
```

#### Opção A: Via Notebook (RECOMENDADO)

```bash
jupyter notebook notebooks/mistral_qlora_training.ipynb
```

Procurar pela célula "Configuração do Treino" e atualizar:

```python
training_config = {
    "batch_size": 1,                    # ← DO recommended_config.json
    "gradient_accumulation": 4,         # ← DO recommended_config.json
    "max_seq_length": 256,              # ← DO recommended_config.json
    "learning_rate": 0.0002,            # ← DO recommended_config.json
    "num_epochs": 3,
    "warmup_steps": 50,
    "save_steps": 100,
    "eval_steps": 100,
    "log_steps": 10,
}
```

Depois corre as células normalmente.

#### Opção B: Via Script

```bash
nano scripts/train_qlora.py
```

Atualizar a seção `training_config` (linhas ~53-65) com os valores do `recommended_config.json`.

### Passo 3: Iniciar Treino

**Via Notebook:**
```bash
jupyter notebook notebooks/mistral_qlora_training.ipynb
# Executar células normalmente
```

**Via Script:**
```bash
python3 scripts/train_qlora.py
```

### Passo 4: Monitorar (Terminal Separada)

Enquanto o treino está em progresso, abra uma terminal **diferente**:

```bash
python3 scripts/monitor.py --refresh 5
```

Mostra em tempo real:
- Loss de treino e validação
- Uso de memória
- Checkpoint atual
- ETA até conclusão

### Passo 5: Após Treino

```bash
# Visualizar gráficos de resultados
python3 scripts/visualization.py --report

# Testar modelo treinado
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
```

---

## Configurações Recomendadas por Hardware

### M1 Base (8GB RAM)
```json
{
  "batch_size": 2,
  "gradient_accumulation": 2,
  "max_seq_length": 512,
  "learning_rate": 0.0003
}
```

### M1 Pro (16GB RAM)
```json
{
  "batch_size": 4,
  "gradient_accumulation": 2,
  "max_seq_length": 512,
  "learning_rate": 0.0005
}
```

### M1 Max (32GB RAM)
```json
{
  "batch_size": 8,
  "gradient_accumulation": 1,
  "max_seq_length": 512,
  "learning_rate": 0.0005
}
```

### M1 com Pouca Memória (< 6GB)
```json
{
  "batch_size": 1,
  "gradient_accumulation": 8,
  "max_seq_length": 128,
  "learning_rate": 0.0001
}
```

---

## O Que Cada Configuração Significa

### batch_size
Quantas amostras processa de cada vez. Maior = mais memória, mais rápido.
- `1` = Muito lento mas usa pouca memória
- `2` = Equilíbrio
- `4+` = Rápido mas precisa muita memória

### gradient_accumulation
Simula batch_size maior sem usar mais memória. Acumula gradientes ao longo de vários passos.
- Aumentar se der "Out of Memory"
- `batch_size=1, grad_accum=4` ≈ `batch_size=4, grad_accum=1`

### max_seq_length
Comprimento máximo de cada exemplo. Maior = mais contexto mas mais memória.
- `128` = Muito curto
- `256` = Recomendado para memória limitada
- `512` = Recomendado para memória adequada

### learning_rate
Velocidade de aprendizagem do modelo. Maior = mais instável, mais rápido.
- `5e-4` = 0.0005 (taxa alta, risco de instabilidade)
- `3e-4` = 0.0003 (taxa média, recomendado)
- `1e-4` = 0.0001 (taxa baixa, convergência lenta)

### num_epochs
Quantas vezes passa pelos dados. 3 é padrão.

### warmup_steps
Passos iniciais com learning rate gradualmente aumentada. Evita instabilidade no início.

### save_steps / eval_steps
Frequência de salvar checkpoints e avaliar modelo.

---

## Troubleshooting

### Erro: "Out of Memory"

1. Reduzir `batch_size`: `4 → 2 → 1`
2. Aumentar `gradient_accumulation`: `2 → 4 → 8`
3. Reduzir `max_seq_length`: `512 → 256 → 128`

Recomendação: aumentar `gradient_accumulation` primeiro (mais eficiente que reduzir batch_size)

### Erro: "Model not found" ou "Downloading"

Normal! Primeira execução descarrega ~3.8GB do Mistral-7B. Pode levar 5-10 minutos.

### Treino muito lento

1. Aumentar `batch_size` (se houver memória)
2. Aumentar `learning_rate`
3. Reduzir `warmup_steps`

### Loss não diminui ou fica instável

1. Aumentar `learning_rate` gradualmente (ex: 1e-4 → 2e-4 → 3e-4)
2. Aumentar `warmup_steps`
3. Validar dados: `python3 scripts/validate_jsonl.py data/train.jsonl`

### GPU não está sendo usada

Corra: `python3 scripts/diagnose_qlora.py`

Se ver "Device: CPU" em vez de "Device: GPU":
1. Verificar instalação MLX: `pip install mlx`
2. Estar em Mac M1/M2/M3
3. Fechar outras aplicações pesadas

---

## Ficheiros Gerados

### Durante Preflight Check
```
checkpoints_qlora/
├── preflight_report.json
│   └── Relatório completo: hardware, dependências, dados, config
└── recommended_config.json
    └── Valores otimizados para seu sistema (COPIAR DAQUI!)
```

### Durante Treino
```
checkpoints_qlora/
├── checkpoint_epoch_0_step_100/    # Checkpoints intermediários
├── checkpoint_epoch_0_step_200/
├── checkpoint_epoch_1_step_100/
│   ...
├── adapters/                       # Melhor modelo encontrado
├── training_metrics.json           # Métricas detalhadas
├── training_metrics.csv            # CSV format
├── training_summary.json           # Resumo final
├── training_state.json             # Para resume se interromper
└── plots/                          # Gráficos gerados
    ├── loss.png
    ├── learning_rate.png
    └── memory_usage.png
```

---

## Workflow Visual

```
START
  │
  ├─→ python3 scripts/preflight_check.py
  │     ├─ Verifica tudo
  │     └─ Gera recommended_config.json
  │
  ├─→ Editar notebook/script com valores recomendados
  │
  ├─→ jupyter notebook mistral_qlora_training.ipynb
  │   ou
  │   python3 scripts/train_qlora.py
  │
  ├─ [Terminal separada:]
  │   python3 scripts/monitor.py
  │
  ├─→ Aguardar conclusão (2-3 horas)
  │     └─ Checkpoints salvos em checkpoints_qlora/
  │
  ├─→ python3 scripts/visualization.py --report
  │     └─ Ver gráficos de progresso
  │
  └─→ python3 scripts/inference_qlora.py "sua pergunta"
        └─ Testar modelo treinado
```

---

## Dúvidas Frequentes

**P: Por que o preflight check falhou?**
R: Abra `checkpoints_qlora/preflight_report.json` para ver detalhes. Resolva os problemas indicados.

**P: Posso ignorar avisos (⚠)?**
R: Avisos são informativos. Erros (✗) precisam ser resolvidos.

**P: A config recomendada pode estar errada?**
R: É baseada em seu hardware real. Se der erro, reduzir batch_size ou aumentar gradient_accumulation.

**P: Preciso correr preflight check sempre?**
R: Recomendado apenas primeira vez ou se hardware mudar. Sistema é estável depois.

**P: Posso treinar vários modelos em paralelo?**
R: Não. GPU Metal não suporta bem. Um treino de cada vez.

**P: Como retomar treino interrompido?**
R: Simplesmente correr o treino novamente. Detecta checkpoint automaticamente de `training_state.json`.

**P: Onde estão os ficheiros de treino?**
R: Em `data/train_v3_final_complete.jsonl` e `data/valid_v3_final_complete.jsonl`.

**P: Qual é a duração esperada do treino?**
R: ~2-3 horas em M1/M2 com 3 épocas. Varia com config.

---

## Próximos Passos

1. **Correr preflight check:**
   ```bash
   python3 scripts/preflight_check.py
   ```

2. **Ver configuração recomendada:**
   ```bash
   cat checkpoints_qlora/recommended_config.json
   ```

3. **Abrir notebook:**
   ```bash
   jupyter notebook notebooks/mistral_qlora_training.ipynb
   ```

4. **Atualizar valores de config** (seção "Configuração do Treino")

5. **Executar treino** (correr as células)

6. **Monitorar em terminal separada:**
   ```bash
   python3 scripts/monitor.py --refresh 5
   ```

---

## Suporte

Se tiver problemas:

1. Verificar `checkpoints_qlora/preflight_report.json`
2. Ler seção "Troubleshooting" acima
3. Consultar `docs/troubleshooting/QLORA_TROUBLESHOOTING.md`
4. Executar `python3 scripts/diagnose_qlora.py`

---

**Boa sorte com o treino!** 🚀

Para detalhes técnicos, ver `SAFE_TRAIN_QUICK_START.md`.
