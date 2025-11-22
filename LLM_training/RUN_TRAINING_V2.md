# 🚀 How to Run Training V2 - Overfitting Reduction

**Date:** 2025-11-19
**Status:** ✅ READY TO RUN

---

## 📋 Quick Start

### Option 1: Run Jupyter Notebook (RECOMMENDED) ✅

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training
jupyter notebook notebooks/train_v2_optimized.ipynb
```

Then:
1. Select kernel: **Python 3.11 (MLX)** (from Jupyter kernel dropdown)
2. Run all cells in order: `Cell → Run All`
3. Monitor progress in notebook output

**Expected duration:** 3-4 hours

---

### Option 2: Run Script (Terminal)

If using the Jupyter kernel Python directly:

```bash
# Find the MLX Python path
jupyter kernelspec list | grep mlx

# Then run training (adjust path as needed)
/Users/f.nuno/[path-to-mlx-venv]/bin/python3 scripts/train_qlora.py
```

---

## 📊 What to Expect

### During Training

You'll see output like this:

```
================================================================================
🎯 CONFIGURATION V2 - OVERFITTING REDUCTION
================================================================================
LoRA Rank: 6 (reduced from 8)
Dropout: 0.08 (added for regularization)
Batch Size: 2 (reduced from 4)
Learning Rate: 2e-4 (reduced from 5e-4)
Early Stopping: Patience=5, Min Delta=0.001
================================================================================

📦 A carregar modelo e dados...
A carregar modelo: models/mistral-7b-4bit

📊 A carregar datasets...
Amostras de treino: 848
Amostras de validação: 95

🔤 A tokenizar...
✅ Tokens de treino: 848
✅ Tokens de validação: 95

================================================================================
🚀 INICIANDO TREINO V2 - OVERFITTING REDUCTION
================================================================================

📚 Época 1/3
────────────────────────────────────────────────────────────────────────────
Treino: 100%|████████████████| 424/424 [35:12<00:00,  5.01s/batch]

✅ Val Loss (step 200): 2.1234

📊 Análise de Validação:
  ✅ Melhor Val Loss: 2.1234
  ℹ️  Sem melhoria (0/5)

✓ Checkpoint guardado em: checkpoints_qlora/checkpoint_epoch0_step200
```

### Early Stopping Example

If overfitting is detected:

```
📊 Análise de Validação:
  ⚠️  Overfitting moderado (gap=0.1567)
  ℹ️  Sem melhoria (5/5)

⏹️  EARLY STOPPING ATIVADO!
   Sem melhoria por 5 validações consecutivas
   Melhor modelo: Época 1, Step 250
   Melhor Val Loss: 1.8234

🏁 Treino terminado por Early Stopping
```

### Final Analysis

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

## 🎯 Configuration Changes (V1 → V2)

| Parameter | V1 | V2 | Purpose |
|-----------|----|----|---------|
| **LoRA Rank** | 8 | 6 | 25% fewer parameters → less memorization |
| **Dropout** | 0.0 | 0.08 | Prevents co-adaptation → better generalization |
| **Batch Size** | 4 | 2 | Noisier gradients → regularization |
| **Learning Rate** | 5e-4 | 2e-4 | Slower optimization → flatter minima |
| **Early Stopping** | None | Yes | Stops when val_loss plateaus |

**Target:** Reduce train-val gap from 2.27 → < 0.15 ✅

---

## 📈 Expected Improvements

### Metrics (Predicted)

| Metric | V1 | V2 (Target) |
|--------|----|----|
| **F-1 Score** | 0.9602 | ≥ 0.93 |
| **Train-Val Gap** | 2.27 | < 0.15 |
| **Overfitting Status** | HIGH | GOOD |
| **Training Time** | ~4 hours | ~3-4 hours |

---

## ✅ Pre-Training Checklist

- [x] Configuration V2 implemented in `train_qlora.py`
- [x] Notebook `train_v2_optimized.ipynb` created
- [x] Disk space cleaned (1.4GB freed)
- [x] EarlyStoppingMonitor integrated
- [ ] **Dataset files ready:**
  - `data/train_v3_final_complete.jsonl` (848 examples)
  - `data/valid_v3_final_complete.jsonl` (95 examples)
- [ ] **Model base exists:**
  - `models/mistral-7b-4bit/` (3.8GB)
- [ ] **Jupyter kernel configured:**
  - Run `jupyter kernelspec list` to verify Python 3.11 MLX kernel

---

## 🔍 Monitoring Training

### Option 1: Monitor in Another Terminal

```bash
# In a separate terminal, navigate to the project
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training

# Run monitoring script
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

This shows:
- Real-time loss trajectory
- Memory usage
- ETA to completion
- Current best model metrics

### Option 2: Watch Metrics File

```bash
# In terminal, watch the metrics JSON in real-time
tail -f checkpoints_qlora/training_metrics.json | jq '.[(-1)]'
```

---

## 📊 After Training

### 1. Evaluation (30 minutes)

```bash
python3 scripts/evaluation_metrics.py --output-dir checkpoints_qlora
```

This generates:
- `evaluation_report.json` - Detailed metrics
- `evaluation_summary.csv` - Quick reference
- Visualization PNGs

### 2. Compare V1 vs V2

Create a comparison table:
```python
import json

# Load V1 metrics
with open("checkpoints_qlora_v1_backup/training_metrics.json") as f:
    v1_metrics = json.load(f)

# Load V2 metrics
with open("checkpoints_qlora/training_metrics.json") as f:
    v2_metrics = json.load(f)

# Compare final metrics
v1_final = v1_metrics[-1]
v2_final = v2_metrics[-1]

print(f"V1 Loss: {v1_final['loss']:.4f}")
print(f"V2 Loss: {v2_final['loss']:.4f}")
print(f"V1 Val Loss: {v1_final.get('val_loss', 'N/A')}")
print(f"V2 Val Loss: {v2_final.get('val_loss', 'N/A')}")
```

### 3. Review Overfitting Status

Check the overfitting gap:

```
Gap < 0.05:   ✅ EXCELENTE (optimal)
Gap < 0.15:   ✅ BOM (good)
Gap < 0.30:   ⚠️ MODERADO (acceptable)
Gap >= 0.30:  ❌ CRÍTICO (needs improvement)
```

---

## 🆘 Troubleshooting

### "No module named 'mlx'"

**Problem:** Python doesn't have MLX installed

**Solution:**
```bash
# Find Jupyter's Python kernel
jupyter kernelspec list

# Use that Python directly
/path/to/jupyter/python -m pip list | grep mlx
```

### "CUDA out of memory"

**Problem:** Not relevant for Apple Silicon, but if memory issues:

**Solution:**
- Reduce batch_size: 2 → 1
- Increase gradient_accumulation: 4 → 8

### Early Stopping Triggers Immediately

**Problem:** Training stops after a few validations

**Solution:**
```python
# In notebook, modify:
early_stopping = EarlyStoppingMonitor(
    patience=10,  # Increase from 5
    min_delta=0.005  # Increase from 0.001
)
```

### Model Doesn't Load

**Problem:** `models/mistral-7b-4bit/` missing or incomplete

**Solution:**
```bash
ls -lh models/mistral-7b-4bit/
# Should see: config.json, model.safetensors, tokenizer.json
```

---

## 🎓 Understanding the Changes

### Why Lower Learning Rate?

Lower LR means slower convergence, allowing the optimizer to find flatter minima in the loss landscape. Flatter minima tend to generalize better.

### Why Smaller Batch Size?

Smaller batches create noisier gradient estimates, which acts as implicit regularization. The model learns generalizable features instead of memorizing.

### Why Dropout?

Dropout (0.08) randomly disables neurons during training, preventing co-adaptation and forcing the network to learn redundant, robust representations.

### Why Lower LoRA Rank?

LoRA rank controls adaptation dimensionality. Lower rank means fewer parameters, reducing the model's capacity to memorize training data specifics.

### Why Early Stopping?

Monitors validation loss and stops when it plateaus (no improvement for 5 validations). This prevents the model from overfitting to training data.

---

## 📝 Files Generated During Training

```
checkpoints_qlora/
├── adapters/                    # Best model found
│   └── adapters.safetensors    # LoRA weights
├── checkpoint_epoch0_step200/   # Intermediate checkpoints
├── checkpoint_epoch0_step400/
├── training_metrics.json        # Step-by-step metrics
├── training_metrics.csv         # Same as CSV
├── training_summary.json        # Final summary
├── training_state.json          # Resume info (if interrupted)
└── training_v2_results.png      # Visualization

output/
└── mistral-7b-farense-qlora-v2/
    ├── adapters.safetensors     # Final model
    └── adapter_config.json      # Configuration
```

---

## ✅ Success Criteria

Training V2 is successful if:

1. **Loss Decreases**: Training loss goes from ~5.0 → ~1.5
2. **Val Loss Improves**: Validation loss decreases consistently
3. **Overfitting Gap Reduces**: Gap < 0.15 (from V1's 2.27)
4. **Early Stopping Works**: Model stops before overfitting severely
5. **F-1 Score Maintained**: ≥ 0.93 (similar to V1's 0.96)

---

## 🚀 Next Steps After Training

1. **Evaluate** (30 min): Run `evaluation_metrics.py`
2. **Compare** (10 min): Create V1 vs V2 comparison table
3. **Decide** (5 min):
   - If V2 is better → Deploy V2
   - If V2 similar → Use V2 for better generalization
   - If V2 worse → Analyze and adjust hyperparameters
4. **Deploy** (5 min): Copy final model to production

---

## 📞 Need Help?

If training fails:

1. Check logs: `tail -100 training_v2.log` (if running from script)
2. Verify datasets: `wc -l data/train_v3_final_complete.jsonl`
3. Check GPU: `jupyter notebook` → check kernel device output
4. Review configuration: See `OVERFITTING_REDUCTION_V2.md`

---

**Status:** ✅ READY TO TRAIN

**Next Step:** Open Jupyter and run `notebooks/train_v2_optimized.ipynb`

Good luck! 🚀
