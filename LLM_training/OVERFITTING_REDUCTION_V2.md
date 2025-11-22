# Overfitting Reduction Strategy - V2 Training Configuration

**Date:** 2025-11-19
**Status:** ✅ IMPLEMENTADO
**Script:** `scripts/train_qlora.py`

---

## 📋 Summary of Changes

The training configuration has been optimized to reduce overfitting observed in V1 (gap of 2.27 between train and validation loss).

---

## 🎯 Configuration Changes (V1 → V2)

### 1. LoRA Configuration

| Parameter | V1 | V2 | Change | Reason |
|-----------|----|----|--------|--------|
| **LoRA Rank** | 8 | 6 | ↓ 25% fewer parameters | Reduces model capacity, prevents memorization |
| **Dropout** | 0.0 | 0.08 | ✅ Added | Randomly drops neurons during training, reduces overfitting |
| **Scale (Alpha)** | 16 | 16 | - | Unchanged |

### 2. Training Configuration

| Parameter | V1 | V2 | Change | Reason |
|-----------|----|----|--------|--------|
| **Batch Size** | 4 | 2 | ↓ 50% smaller | Reduced effective batch = more regularization |
| **Gradient Accumulation** | 2 | 4 | ↑ 2x | Maintains effective batch size while reducing memory |
| **Learning Rate** | 5e-4 | 2e-4 | ↓ 60% slower | More controlled training, better convergence |
| **Early Stopping Patience** | N/A | 5 | ✅ Added | Stop after 5 validations without improvement |
| **Early Stopping Min Delta** | N/A | 0.001 | ✅ Added | Minimum improvement threshold (0.1%) |

### 3. Optimization Strategy

| Technique | Status | Impact |
|-----------|--------|--------|
| **Reduced LoRA Rank** | ✅ Active | 33% fewer trainable parameters |
| **Dropout Regularization** | ✅ Active | Prevents co-adaptation of neurons |
| **Lower Learning Rate** | ✅ Active | Smoother optimization landscape |
| **Smaller Batch Size** | ✅ Active | Noisier gradients = better regularization |
| **Early Stopping** | ✅ Automated | Stops when validation loss plateaus |
| **Gradient Accumulation** | ✅ Active | Effective batch larger than actual batch |

---

## 🔧 Implementation Details

### EarlyStoppingMonitor Class

A new class has been added to automatically monitor training and stop when overfitting is detected:

```python
class EarlyStoppingMonitor:
    """Monitora overfitting e aplica early stopping automático"""

    def __init__(self, patience=5, min_delta=0.001, restore_best_weights=True):
        self.patience = patience                    # Parar após N validações sem melhoria
        self.min_delta = min_delta                  # Melhoria mínima necessária
        self.best_val_loss = float('inf')
        self.patience_counter = 0                   # Contador de validações sem melhoria
        self.best_epoch = 0
        self.best_step = 0
        self.overfitting_gap_history = []
```

### Overfitting Detection Logic

During validation, the monitor calculates the gap between training and validation loss:

```
Overfitting Gap = Val Loss - Train Loss

Gap < 0.05:    ✅ EXCELENTE (perfect generalization)
Gap < 0.15:    ✅ BOM (good generalization)
Gap < 0.30:    ⚠️ MODERADO (light overfitting)
Gap >= 0.30:   ❌ CRÍTICO (severe overfitting)
```

### Integration in Training Loop

1. **Initialization**: Created `EarlyStoppingMonitor` before training
2. **Validation Phase**: After each validation, call `early_stopping.check()`
3. **Decision Point**: If patience counter reaches limit, set `should_stop = True`
4. **Graceful Exit**: Both inner (steps) and outer (epochs) loops break cleanly

---

## 📊 Expected Improvements

### Metrics (Predicted)

| Metric | V1 | V2 (Expected) | Target |
|--------|----|----|--------|
| **F-1 Score** | 0.9602 | 0.94-0.96 | ≥ 0.93 |
| **Train-Val Gap** | 2.27 | 0.10-0.20 | < 0.15 |
| **Overfitting Status** | HIGH | GOOD | EXCELENTE |
| **Training Duration** | ~4 hours | ~3-4 hours | Similar |

### Why These Improvements?

1. **Smaller batch size** → Noisier gradients → Better generalization
2. **Lower learning rate** → Smoother optimization → Less overfitting
3. **Dropout** → Prevents co-adaptation → Improves generalization
4. **Lower LoRA rank** → Fewer parameters → Less memorization
5. **Early Stopping** → Stops before model overfits → Optimal solution

---

## 🚀 How to Run V2 Training

### Option 1: Run Script Directly

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training
python3 scripts/train_qlora.py
```

### Option 2: Run in Jupyter Notebook

```bash
jupyter notebook notebooks/mistral_qlora_professional.ipynb
```

Then run all cells in order. The notebook will use the updated `train_qlora.py` configuration.

### During Training

Monitor progress in a separate terminal:

```bash
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

---

## 📈 What to Expect

### Training Output Example

```
📚 Época 1/3
────────────────────────────────────────────────────────────────────────────
Treino Época 1: 100%|████████| 424/424 [00:00<00:00, 9987.54it/s]

✅ Época 1 completa!
   Loss médio: 2.3456
   Val Loss médio: 2.1567

📊 Análise de Validação:
  ✅ Melhor Val Loss: 2.1567
  ℹ️  Sem melhoria (0/5)

(Epoch 2 continues...)

📊 Análise de Validação:
  ⚠️  OVERFITTING MODERADO DETECTADO (gap=0.1234)
  ℹ️  Sem melhoria (1/5)

(Epoch 2 continues with more validations...)

📊 Análise de Validação:
  ⚠️  OVERFITTING MODERADO DETECTADO (gap=0.1567)
  ℹ️  Sem melhoria (5/5)

⏹️  EARLY STOPPING ATIVADO!
   Sem melhoria por 5 validações consecutivas
   Melhor modelo: Época 1, Step 250
   Melhor Val Loss: 2.1234

🏁 Treino terminado por Early Stopping
```

### Final Overfitting Analysis

```
================================================================================
🔍 ANÁLISE FINAL DE OVERFITTING
================================================================================
Status: ✅ BOM (gap < 0.15)
Gap médio: 0.0890
Gap máximo: 0.1234
Gap mínimo: 0.0567
================================================================================
```

---

## ⚙️ Key Configuration Values

```python
# LoRA Configuration (Reduced Capacity)
{
    "rank": 6,              # ↓ From 8 (fewer parameters)
    "scale": 16,            # Unchanged
    "dropout": 0.08,        # ↑ From 0.0 (regularization)
}

# Training Configuration (More Conservative)
{
    "batch_size": 2,                      # ↓ From 4 (more regularization)
    "gradient_accumulation": 4,           # ↑ From 2 (effective batch = 8)
    "learning_rate": 2e-4,                # ↓ From 5e-4 (slower, smoother)
    "early_stopping_patience": 5,         # ✅ Stop after 5 evals without improvement
    "early_stopping_min_delta": 0.001,    # ✅ Minimum 0.1% improvement
}
```

---

## 📁 Modified Files

| File | Changes |
|------|---------|
| `scripts/train_qlora.py` | ✅ Updated LoRA config, training config, added EarlyStoppingMonitor class, integrated early stopping in training loop |
| `notebooks/mistral_qlora_professional.ipynb` | ℹ️ Will use new config on next run |

---

## 🔄 Next Steps After Training

1. **Evaluate Results** (30 minutes)
   - Run `python3 scripts/evaluation_metrics.py --output-dir checkpoints_qlora`
   - Check overfitting gap (target: < 0.15)
   - Verify F-1 score is still > 0.93

2. **Compare V1 vs V2** (10 minutes)
   - Create comparison table with metrics
   - Analyze improvement in generalization

3. **Fine-tune if Needed** (Optional)
   - If gap is still > 0.20: Increase dropout to 0.10, reduce rank to 4
   - If F-1 dropped below 0.93: Increase learning rate to 3e-4

4. **Deploy Final Model** (5 minutes)
   - Copy adapters to production directory
   - Update model version in deployment config

---

## 📊 Troubleshooting

### If Early Stopping Triggers Immediately

**Problem:** Training stops after just a few validations
**Solution:**
- Increase `early_stopping_patience` to 10
- Increase `early_stopping_min_delta` to 0.005

### If Overfitting Gap is Still > 0.20

**Problem:** Model still memorizing training data
**Solution:**
- Reduce batch_size to 1
- Increase dropout to 0.15
- Reduce learning_rate to 1e-4

### If F-1 Score Dropped Below V1

**Problem:** Regularization too strong
**Solution:**
- Increase learning_rate to 3e-4
- Reduce dropout to 0.05
- Increase LoRA rank to 7

---

## 🎓 Understanding the Changes

### Why Smaller Batch Size?

Smaller batches create noisier gradient estimates, which acts as a form of regularization. The model learns generalizable features instead of memorizing patterns.

### Why Lower Learning Rate?

A lower learning rate means slower convergence, allowing the optimizer to explore flatter minima in the loss landscape. Flatter minima tend to generalize better than sharp ones.

### Why Dropout?

Dropout randomly disables neurons during training, preventing co-adaptation. This forces the network to learn redundant representations that generalize better.

### Why Lower LoRA Rank?

LoRA rank controls the dimensionality of the adaptation. Lower rank means fewer parameters to tune, reducing the model's capacity to memorize training data.

---

## 📝 Configuration Philosophy

This V2 configuration follows the principle of **"less is more"**:

- **Smaller effective model** (lower rank) → Can't memorize as much
- **Noisier training** (smaller batch) → Learns generalizable patterns
- **Slower learning** (lower LR) → Finds better solutions
- **Dropout** → Forces robustness
- **Early stopping** → Prevents overfitting automatically

Together, these changes should reduce the training-validation gap from 2.27 to < 0.15, while maintaining F-1 score > 0.93.

---

## ✅ Checklist Before Running

- [x] Configuration updated in `train_qlora.py`
- [x] EarlyStoppingMonitor class implemented
- [x] Early stopping integrated in training loop
- [x] Python syntax verified (no errors)
- [ ] Dataset files exist (train_v3_final_complete.jsonl, valid_v3_final_complete.jsonl)
- [ ] Model base exists (models/mistral-7b-4bit/)
- [ ] Checkpoints directory ready (checkpoints_qlora/)
- [ ] Ready to start training!

---

**Status:** ✅ READY FOR TRAINING

To start: `python3 scripts/train_qlora.py`

Good luck! 🚀
