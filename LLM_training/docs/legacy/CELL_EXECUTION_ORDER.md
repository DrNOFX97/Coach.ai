# 📋 Ordem de Execução das Células - Notebook QLoRA

## ⚠️ IMPORTANTE

**Execute as células NA ORDEM CORRETA!**

Algumas células dependem de outras. Se pular uma ou executar fora de ordem, você terá erros como:
- `NameError: name 'tracker' is not defined`
- `NameError: name 'memory_monitor' is not defined`
- etc.

---

## ✅ Ordem Correta de Execução

### **SEÇÃO 1: Setup (células 1-6)**
```
[1] imports (os, sys, json, etc)
[2] Verify M1 Mac
[3] Install MLX dependencies
[4] Import MLX libraries
[5] ✓ MLX libraries loaded
[6] Setup paths
```
**Status:** Pronto para continuar ✓

---

### **SEÇÃO 2: Dados (células 7-10)**
```
[7] Load JSONL data (50_anos_00.jsonl)
[8] Load biography data
[9] Validate and split data
[10] Save processed data
```
**Status:** Datasets criados ✓

---

### **SEÇÃO 3: Modelo (células 11-18)**
```
[11] QLoRA Configuration
[12] Training configuration
[13] Load base model with quantization
[14] Model info
[15] Memory monitoring class
[16] Create datasets
[17] ⚠️ CORRECTED Training functions
      - train_epoch()
      - validate_model()
[18] Warmup scheduler
```
**Status:** Modelo e funções carregadas ✓

---

### **SEÇÃO 4: Inicialização (célula 19 - NOVA)**
```
[19] ⭐ NEW: TrainingTracker class
     - Define class
     - Initialize: tracker = TrainingTracker(CHECKPOINTS_DIR)
```
**✓ IMPORTANTE:** Execute ANTES de começar treino!
**Status:** Tracker pronto ✓

---

### **SEÇÃO 5: Treino (célula 20)**
```
[20] Run QLoRA training
     - Usa: model, tokenizer, optimizer
     - Usa: train_dataset, val_dataset
     - Usa: tracker (definido na célula 19!)
     - Usa: memory_monitor
```
**⚠️ AVISO:** Leva 2-3 horas para 3 épocas!
**Status:** Treino começando ✓

---

### **SEÇÃO 6: Teste (células 21-22)**
```
[21] Test model generation
[22] Performance metrics
```
**Status:** Testa modelo treinado ✓

---

### **SEÇÃO 7: Export (células 23-26)**
```
[23] Save final QLoRA model
[24] Create integration guide
[25] Create QLoRA inference script
[26] Final summary
[27] Comparison: LoRA vs QLoRA
```
**Status:** Modelo exportado ✓

---

## 🚀 Resumo Rápido

### Para Treinar Completo:
```
Executar células: 1 → 2 → 3 → 4 → 5 → 6
                  7 → 8 → 9 → 10
                  11 → 12 → 13 → 14 → 15 → 16 → 17 → 18
                  19 (NOVO - muito importante!)
                  20 (começa treino)
                  21 → 22 (testar)
                  23 → 24 → 25 → 26 → 27 (exportar)
```

### Se Já Treinou Antes:
```
Executar apenas:
  19 (initialize tracker)
  20 (resume training)
```

---

## ⚠️ Erros Comuns e Soluções

### Erro: `NameError: name 'tracker' is not defined`
```
Causa: Pulou célula 19 (TrainingTracker)
Solução: Execute célula 19 ANTES de célula 20
```

### Erro: `NameError: name 'model' is not defined`
```
Causa: Pulou seção setup (células 11-18)
Solução: Execute células 11-18 primeiro
```

### Erro: `NameError: name 'train_dataset' is not defined`
```
Causa: Pulou seção dados (células 7-10)
Solução: Execute células 7-10 antes de 16
```

### Erro: Treino não inicia
```
Causa: Células fora de ordem
Solução: Comece do zero na ordem correta (1-20)
```

---

## 📊 Dependências Entre Células

```
Célula 1-6 (Setup)
    ↓
Célula 7-10 (Dados)
    ↓ (usa train_data, val_data)
Célula 11-18 (Modelo)
    ↓ (define model, tokenizer, datasets)
Célula 19 (Tracker) ⭐ IMPORTANTE
    ↓ (define tracker)
Célula 20 (Treino)
    ↓ (usa todas acima)
Célula 21-22 (Teste)
    ↓
Célula 23-27 (Export)
```

---

## ✅ Checklist Antes de Executar Célula 20

- [ ] Célula 1-6 executadas (imports e paths OK)
- [ ] Célula 7-10 executadas (datasets criados)
- [ ] Célula 11-18 executadas (modelo, tokenizer, funções carregadas)
- [ ] Célula 19 executada (tracker inicializado) ⭐ **CRÍTICO**
- [ ] Sem mensagens de erro nas células anteriores
- [ ] Memory disponível: `memory_monitor.log_memory()` > 3GB

Se algum item falhar, **NÃO execute célula 20**. Volte e corrija!

---

## 🎯 Fluxo de Execução Recomendado

### Primeira Vez (Treino Completo)
1. Abra notebook
2. Execute células 1-19 (setup até tracker)
   - Isso leva ~15-20 minutos
   - Carrega modelo, dados, etc.
3. Execute célula 20 (treino)
   - Leva 2-3 horas
   - Pode pausar com Ctrl+C
4. Depois (se quiser): execute 21-27 (teste e export)

### Se Interromper e Quiser Resumir
1. Abra notebook
2. Recarregue modelo: execute célula 13
3. Carregue tracker: execute célula 19
4. Retome treino: execute célula 20
   - Vai detectar checkpoint anterior e continuar

### Se Treino Completou
1. Abra notebook
2. Execute célula 20 (detecta que já completou)
3. Execute células 21-27 (teste e export)

---

## 📝 Notas Importantes

### Célula 19 (TrainingTracker) é CRÍTICA
- Define a classe `TrainingTracker`
- Inicializa `tracker = TrainingTracker(CHECKPOINTS_DIR)`
- Sem ela, célula 20 falha com `NameError`

### Se Aparecer Erro de Ordem
```
NameError: name 'XXX' is not defined
```

**Solução:** Sempre execute do zero na ordem correta:
```bash
# Kernel → Restart & Clear Output
# Depois execute células 1 → 2 → 3 ... → 20
```

### Não Pule Células!
Mesmo que pareçam simples, todas servem para:
- Validar ambiente
- Carregar dependências
- Inicializar variáveis globais

---

## 🔄 Se Tiver Que Recomeçar

```jupyter
# 1. Limpar kernel
Kernel → Restart & Clear Output

# 2. Executar células na ordem:
[1] imports
[2] verify M1
[3] install (descomente se primeira vez)
[4] import MLX
[5] MLX check
[6] setup paths
[7-10] dados
[11-18] modelo
[19] tracker ⭐
[20] treino

# 3. Se tudo OK: treino começa!
```

---

## ✨ Resultado Esperado

Quando tudo está correto e você executa célula 20:

```
======================================================================
TRAINING QLORA (OPTIMIZED FOR M1 MAC)
======================================================================

======================================================================
EPOCH 1/3
======================================================================

Epoch 1/3
[Memory] Epoch 1 start: 3400MB available
Training:   2%|█                        | 24/1207 [00:20<16:45, 0.74it/s]
  Step 20/1207 - Loss: 8.5234
  ✓ Checkpoint saved (step 200)
Epoch 1 - Avg Loss: 6.4521

Validation: 30%|██████████            | 9/30 [00:15<00:35, 0.59it/s]
  Val Loss: 5.1234
  ✓ Best model saved
  ✓ Epoch 1 complete

EPOCH 2/3
...
```

**Se você ver isso:** ✅ Tudo funcionando perfeitamente!

---

## 🎓 Por Que a Ordem Importa

### Células são **Stateful** (dependem de estado)

```python
# Célula 6: Define CHECKPOINTS_DIR
CHECKPOINTS_DIR = TRAINING_ROOT / "checkpoints_qlora"

# Célula 19: Usa CHECKPOINTS_DIR
tracker = TrainingTracker(CHECKPOINTS_DIR)

# Se pular célula 6 → erro em célula 19!
```

### Python Kernels Mantêm Memória
```python
# Se executar [20] sem [1-19]:
# Variáveis não existem → NameError

# Solução: Sempre execute em ordem ou reinicie kernel
```

---

## 📞 Troubleshooting por Erro

### `NameError: name 'tracker' is not defined`
- [ ] Célula 19 foi executada?
- [ ] Mensagem "✓ TrainingTracker initialized" apareceu?
- Se não: Execute célula 19 agora

### `NameError: name 'model' is not defined`
- [ ] Célula 13 foi executada?
- [ ] Mensagem "✓ Model loaded" apareceu?
- Se não: Execute células 11-18

### `FileNotFoundError: data/train_data.jsonl`
- [ ] Célula 10 foi executada?
- [ ] Arquivos existem em `data/`?
- Se não: Execute células 7-10

### Treino não inicia / fica pendurado
- [ ] Kernel restart + execute 1-20 novamente
- [ ] Verifique memória: `python scripts/diagnose_qlora.py`
- [ ] Reduza batch_size em célula 12

---

## ✅ Conclusão

**Execute as células NA ORDEM CORRETA!**

```
1-6 (Setup)
  ↓
7-10 (Dados)
  ↓
11-18 (Modelo)
  ↓
19 (Tracker) ⭐ IMPORTANTE
  ↓
20 (Treino começa!)
```

Seguindo essa ordem, tudo vai funcionar perfeitamente! 🚀

---

**Versão:** Final
**Data:** 2025-11-09
**Status:** ✅ Pronto para usar
