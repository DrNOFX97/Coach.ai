# 🚀 Safe Train - START HERE

**Sistema automático de diagnóstico + recomendação de configuração para evitar crashes no treino.**

---

## ⚡ TL;DR (30 segundos)

```bash
# 1. Diagnóstico (2 min)
python3 scripts/preflight_check.py

# 2. Ver config recomendada
cat checkpoints_qlora/recommended_config.json

# 3. Abrir notebook
jupyter notebook notebooks/mistral_qlora_training.ipynb

# 4. Atualizar valores de config no notebook (copiar/colar do passo 2)

# 5. Executar treino
# (Correr células do notebook)

# 6. Monitorar (terminal SEPARADA)
python3 scripts/monitor.py --refresh 5
```

---

## 📋 Workflow Completo (5 minutos para setup, 2-3 horas para treino)

```
┌─────────────────────────────────────────┐
│ PASSO 1: Diagnóstico (5 min)            │
├─────────────────────────────────────────┤
│ $ python3 scripts/preflight_check.py    │
│ → Gera recommended_config.json          │
│ → Valida todo o sistema                 │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ PASSO 2: Ver Config (1 min)             │
├─────────────────────────────────────────┤
│ $ cat checkpoints_qlora/recommended..   │
│ → Copiar valores para memória           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ PASSO 3: Abrir Notebook (1 min)         │
├─────────────────────────────────────────┤
│ $ jupyter notebook notebooks/...        │
│ → Localizar seção "Configuração"        │
│ → Colar valores do Passo 2              │
│ → Executar células                      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ PASSO 4: Monitorar (Terminal 2)         │
├─────────────────────────────────────────┤
│ $ python3 scripts/monitor.py            │
│ → Ver loss, memória, ETA em tempo real  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ PASSO 5: Analisar Resultados            │
├─────────────────────────────────────────┤
│ $ python3 scripts/visualization.py      │
│ $ python3 scripts/inference_qlora.py    │
└─────────────────────────────────────────┘
```

---

## 📁 Ficheiros Criados

### Sistema Automático

| Ficheiro | Função |
|----------|--------|
| `scripts/preflight_check.py` | ✅ Diagnóstico completo do sistema |
| `scripts/safe_train.py` | ✅ Wrapper com menu interativo |
| `train_safe.sh` | ✅ Script bash para iniciar treino seguro |

### Documentação

| Ficheiro | Conteúdo |
|----------|----------|
| **[Você está aqui]** | Índice e quick start |
| `README_PREFLIGHT.md` | Guia detalhado do sistema de verificação |
| `SAFE_TRAIN_QUICK_START.md` | Workflow completo e troubleshooting |
| `APPLY_RECOMMENDED_CONFIG.md` | Como atualizar notebook com config recomendada |

### Configuração Gerada (após preflight_check.py)

| Ficheiro | Conteúdo |
|----------|----------|
| `checkpoints_qlora/preflight_report.json` | Relatório completo de diagnóstico |
| `checkpoints_qlora/recommended_config.json` | **Config otimizada para seu sistema** ⭐ |

---

## 🎯 Começar Agora

### Opção A: Via Script (Automático - RECOMENDADO)

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training
./train_safe.sh
```

O script vai:
1. Executar preflight_check
2. Mostrar config recomendada
3. Perguntar se quer abrir notebook ou executar script
4. Guiar através dos passos

### Opção B: Via Manual (Passo a Passo)

```bash
# 1. Diagnóstico
python3 scripts/preflight_check.py

# 2. Ver config recomendada
cat checkpoints_qlora/recommended_config.json

# 3. Abrir notebook e atualizar valores
jupyter notebook notebooks/mistral_qlora_training.ipynb

# 4. Monitorar em terminal separada
python3 scripts/monitor.py --refresh 5
```

### Opção C: Via wrapper Python

```bash
python3 scripts/safe_train.py
```

---

## 📊 O que o Preflight Check Faz

### Verifica ✓

- ✅ Python versão
- ✅ MLX, MLX-LM, Transformers instalados
- ✅ Metal GPU disponível
- ✅ Ficheiros de dados existem
- ✅ Modelo pode ser carregado
- ✅ Espaço em disco suficiente
- ✅ Memória disponível

### Recomenda ✨

Baseado NO SEU HARDWARE, gera configuração otimizada:
- `batch_size` ideal
- `gradient_accumulation` para sua RAM
- `max_seq_length` balanceado
- `learning_rate` adequado
- E mais...

---

## 🔧 Como Usar a Config Recomendada

### Passo 1: Abrir ficheiro

```bash
cat checkpoints_qlora/recommended_config.json
```

### Passo 2: Ver valores

```json
{
  "batch_size": 2,              ← COPIAR ESTE
  "gradient_accumulation": 2,   ← COPIAR ESTE
  "max_seq_length": 512,        ← COPIAR ESTE
  "learning_rate": 0.0003,      ← COPIAR ESTE
  ...
}
```

### Passo 3: Atualizar Notebook

Abra: `notebooks/mistral_qlora_training.ipynb`

Procure:
```python
training_config = {
    "batch_size": ...,           ← SUBSTITUIR
    "gradient_accumulation": ..., ← SUBSTITUIR
    "max_seq_length": ...,       ← SUBSTITUIR
    "learning_rate": ...,        ← SUBSTITUIR
}
```

Por:
```python
training_config = {
    "batch_size": 2,             ← DO recommended_config.json
    "gradient_accumulation": 2,  ← DO recommended_config.json
    "max_seq_length": 512,       ← DO recommended_config.json
    "learning_rate": 0.0003,     ← DO recommended_config.json
}
```

### Passo 4: Executar

Clicar em "Run All" ou Shift+Enter em cada célula

---

## ⚙️ Exemplos de Configurações por Hardware

### M1 Base (8GB) - CONFIG PADRÃO

```python
training_config = {
    "batch_size": 2,
    "gradient_accumulation": 2,
    "max_seq_length": 512,
    "learning_rate": 0.0003,
}
```

**Duração esperada:** 2.5 horas

### M1 Pro (16GB) - ALTA PERFORMANCE

```python
training_config = {
    "batch_size": 4,
    "gradient_accumulation": 2,
    "max_seq_length": 512,
    "learning_rate": 0.0005,
}
```

**Duração esperada:** 1.5 horas

### M1 Tight (< 6GB) - CONSERVADOR

```python
training_config = {
    "batch_size": 1,
    "gradient_accumulation": 8,
    "max_seq_length": 128,
    "learning_rate": 0.0001,
}
```

**Duração esperada:** 3-4 horas

---

## 🚨 Se Algo Dar Errado

### "Out of Memory" durante treino?

```python
# Aumentar acumulação de gradientes
"gradient_accumulation": 4,  # era 2

# OU reduzir batch size
"batch_size": 1,             # era 2

# OU reduzir sequence length
"max_seq_length": 256,       # era 512
```

### Loss não diminui?

```python
# Aumentar learning rate
"learning_rate": 0.0005,     # era 0.0003

# Aumentar warmup steps
"warmup_steps": 100,         # era 50
```

### Muito lento?

```python
# Aumentar batch_size (se houver memória)
"batch_size": 4,             # era 2

# Ou aumentar learning_rate
"learning_rate": 0.0005,     # era 0.0003
```

---

## 📚 Documentação Completa

| Documento | Para Quem | Tempo |
|-----------|-----------|--------|
| **Este ficheiro** | Quick start | 5 min |
| `README_PREFLIGHT.md` | Detalhes técnicos | 15 min |
| `SAFE_TRAIN_QUICK_START.md` | Workflow + troubleshooting | 30 min |
| `APPLY_RECOMMENDED_CONFIG.md` | Como atualizar notebook | 10 min |
| `docs/guides/QLORA_GUIDE.md` | Como QLoRA funciona | 45 min |

---

## ✅ Checklist Antes de Treinar

- [ ] Executei `python3 scripts/preflight_check.py`
- [ ] Verifiquei que não há ✗ erros críticos
- [ ] Vi os valores em `recommended_config.json`
- [ ] Atualizei o notebook com esses valores
- [ ] Salvei o notebook (Cmd+S)
- [ ] Tenho terminal separada para monitor pronta
- [ ] Fechei outras aplicações pesadas
- [ ] Tenho internet estável (se primeira execução)

---

## 🎬 Próximos Passos

1. **Escolha uma opção:**
   - ✅ `./train_safe.sh` (FÁCIL - guia interativo)
   - ✅ `python3 scripts/preflight_check.py` (MANUAL)
   - ✅ Ver `APPLY_RECOMMENDED_CONFIG.md` (DETALHADO)

2. **Esperar output do preflight check**

3. **Ver valores em `checkpoints_qlora/recommended_config.json`**

4. **Atualizar notebook com esses valores**

5. **Executar notebook**

6. **Monitorar em terminal separada:**
   ```bash
   python3 scripts/monitor.py --refresh 5
   ```

---

## 🆘 Ajuda

Se tiver dúvidas:

1. **Erros de instalação?**
   - Ver `README_PREFLIGHT.md` seção "Troubleshooting"

2. **Como atualizar notebook?**
   - Ler `APPLY_RECOMMENDED_CONFIG.md`

3. **Treino crashes durante execução?**
   - Ver `SAFE_TRAIN_QUICK_START.md` seção "Troubleshooting"

4. **Quer entender melhor os parâmetros?**
   - Ler `README_PREFLIGHT.md` seção "O que cada configuração significa"

---

## 🚀 Começar!

```bash
# Opção 1: Script automático (RECOMENDADO)
./train_safe.sh

# Opção 2: Preflight check manual
python3 scripts/preflight_check.py

# Opção 3: Ler guias primeiro
less APPLY_RECOMMENDED_CONFIG.md  # ou 'cat' em Windows
```

---

**Pronto para treinar? Vamos!** 🚀

Duvidas? Consulte `README_PREFLIGHT.md` ou `SAFE_TRAIN_QUICK_START.md`.
