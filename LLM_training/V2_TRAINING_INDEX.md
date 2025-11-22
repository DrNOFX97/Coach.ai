# 📚 V2 Training - Complete Documentation Index

**Status:** ✅ Ready to train
**Date:** 2025-11-19
**Duration:** 3-4 hours estimated

---

## 🚀 START HERE (Choose Based on Your Need)

### ⏱️ Have 2 Minutes?
→ Read: **QUICK_START_V2.txt**
- Copy-paste command to start training
- What to expect
- Quick troubleshooting

### ⏱️ Have 10 Minutes?
→ Read: **PREPARATION_COMPLETE_V2.md**
- Overview of what was done
- Configuration changes
- How to start
- Checklist

### ⏱️ Have 30 Minutes?
→ Read: **FINAL_SUMMARY_V2.md**
- Executive summary
- All details organized
- Expected results
- Monitoring options

### ⏱️ Want Technical Details?
→ Read: **OVERFITTING_REDUCTION_V2.md**
- Deep technical explanation
- Why each change was made
- Expected improvements
- Configuration philosophy

### ⏱️ Need Step-by-Step Instructions?
→ Read: **RUN_TRAINING_V2.md**
- Complete guide with screenshots
- Troubleshooting
- What to do after training
- Comparison with V1

---

## 📁 Quick File Reference

### Execution Files

| File | Purpose | Status |
|------|---------|--------|
| `notebooks/train_v2_optimized.ipynb` | Main training notebook | ✅ Ready |
| `scripts/train_qlora.py` | Training script (alternative) | ✅ Updated |

### Documentation Files

| File | Length | Best For |
|------|--------|----------|
| `QUICK_START_V2.txt` | 100 lines | 2-min quick start |
| `PREPARATION_COMPLETE_V2.md` | 400 lines | Overview & checklist |
| `FINAL_SUMMARY_V2.md` | 300 lines | Executive summary |
| `OVERFITTING_REDUCTION_V2.md` | 500 lines | Technical deep-dive |
| `RUN_TRAINING_V2.md` | 400 lines | Step-by-step guide |
| `V2_TRAINING_INDEX.md` | This file | Navigation hub |

---

## 🎯 Common Questions

### "How do I start training?"

**Answer:** 3 simple steps
1. `cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training`
2. `jupyter notebook notebooks/train_v2_optimized.ipynb`
3. Click kernel dropdown → select "Python 3.11 (MLX)"
4. Press `Cell → Run All`

**Estimated time:** ~4 hours total

---

### "What changed from V1?"

**Answer:** 5 key changes (all to reduce overfitting)

| Change | V1 → V2 | Why |
|--------|---------|-----|
| LoRA Rank | 8 → 6 | 25% fewer parameters = less memorization |
| Dropout | 0.0 → 0.08 | Prevents neuron co-adaptation |
| Batch Size | 4 → 2 | Noisier gradients = better generalization |
| Learning Rate | 5e-4 → 2e-4 | Flatter minima = better generalization |
| Early Stopping | None → Yes | Stop before overfitting happens |

See: **OVERFITTING_REDUCTION_V2.md** for detailed explanation

---

### "What should I expect to see?"

**Answer:** During training, you'll see

```
Loading model & data...
Setting up training...
📚 Epoch 1/3
  Loss: 5.0 → 3.5 → 2.0 → 1.5 (decreasing ✅)
  Val Loss: 2.1 (following training loss ✅)

📚 Epoch 2/3
  Loss: 1.5 → 1.2 → 1.0 (still decreasing ✅)
  Val Loss: 1.1
  Overfitting Gap: 0.08 (✅ good!)

⏹️ EARLY STOPPING (plateau detected)
   Melhor modelo encontrado...

🔍 ANÁLISE FINAL
Status: ✅ BOM (gap < 0.15)
```

See: **RUN_TRAINING_V2.md** for expected output examples

---

### "Will the F-1 score stay the same?"

**Answer:** Yes, probably better or same

| Metric | V1 | V2 Target |
|--------|----|----|
| F-1 Score | 0.9602 | ≥ 0.93 |
| Status | Likely similar | ✅ Maintained |

The regularization will slightly reduce overfitting while maintaining quality.

See: **FINAL_SUMMARY_V2.md** for full comparison

---

### "How long will training take?"

**Answer:** 3-4 hours total

- **Epoch 1:** 35-40 minutes (loading/setup overhead)
- **Epoch 2:** 35-40 minutes + validation checks
- **Epoch 3:** May not run (early stopping usually triggers)
- **Total:** 1.5-3 hours (depends on early stopping)

---

### "What if something goes wrong?"

**Answer:** Refer to troubleshooting sections

**Quick fixes:**
- "No module named mlx" → Use Jupyter kernel dropdown
- "Training slow" → Normal for first epoch
- "Early stopping triggered" → Check final analysis for why
- "Disk space error" → Remove checkpoint_* directories

See: **RUN_TRAINING_V2.md** → Troubleshooting section

---

## 📊 Configuration at a Glance

### What's New in V2

```python
# New: Regularization
qlora_config["lora_parameters"]["dropout"] = 0.08

# New: Early Stopping
training_config["early_stopping_patience"] = 5
training_config["early_stopping_min_delta"] = 0.001

# New: Class
class EarlyStoppingMonitor:
    """Monitors overfitting, stops when plateau"""
```

### What Changed in V2

```python
# Reduced capacity
qlora_config["lora_parameters"]["rank"] = 6  # was 8

# Smaller batches
training_config["batch_size"] = 2  # was 4
training_config["gradient_accumulation"] = 4  # was 2

# Slower learning
training_config["learning_rate"] = 2e-4  # was 5e-4
```

See: **OVERFITTING_REDUCTION_V2.md** for detailed explanation

---

## 📈 Expected Results

### After Training

You'll have:

✅ **Best Model** (automatically saved)
- Location: `checkpoints_qlora/adapters/adapters.safetensors`
- Status: Lowest validation loss found

✅ **Metrics** (captured incrementally)
- `checkpoints_qlora/training_metrics.json` - All metrics
- `checkpoints_qlora/training_metrics.csv` - Spreadsheet format

✅ **Analysis** (automatic)
- Overfitting gap calculated
- Status classified (BOM, MODERADO, etc.)
- Final losses printed

✅ **Model Export** (optional)
- Location: `output/mistral-7b-farense-qlora-v2/`
- Contains: adapters.safetensors, adapter_config.json

---

## 🔄 Next Steps After Training

### Step 1: Review Results (5 min)
- Check notebook output for overfitting analysis
- Verify gap < 0.15 (target)
- Confirm F-1 > 0.93 (target)

### Step 2: Evaluate Model (30 min)
```bash
python3 scripts/evaluation_metrics.py --output-dir checkpoints_qlora
```
Generates: Detailed metrics, visualizations, F-1 scores

### Step 3: Compare V1 vs V2 (10 min)
- Load V1 metrics from `checkpoints_qlora_v1_backup/`
- Load V2 metrics from `checkpoints_qlora/`
- Compare overfitting gap and F-1 scores

### Step 4: Decision (5 min)
- If V2 better → Use V2 ✅
- If V2 similar → Use V2 (better generalization) ✅
- If V2 worse → Analyze and iterate

---

## 💡 Key Concepts

### Overfitting Gap
```
Gap = Validation Loss - Training Loss

Gap < 0.05:   ✅ EXCELENTE (ideal)
Gap < 0.15:   ✅ BOM (good) ← TARGET
Gap < 0.30:   ⚠️ MODERADO (acceptable)
Gap >= 0.30:  ❌ CRÍTICO (bad) ← V1 WAS HERE (2.27!)
```

### Early Stopping
Stops training when validation loss stops improving:
- Patience: Wait 5 validations without improvement
- Min Delta: Require at least 0.1% improvement
- Result: Stops at optimal point, not before overfitting

### Regularization
Techniques that reduce overfitting:
- **Dropout:** Randomly disable neurons
- **Lower rank:** Fewer parameters to fit
- **Smaller batch:** Noisier gradients
- **Lower LR:** Smoother optimization

---

## 🎓 Learning Resources

### Understanding Overfitting
See: **OVERFITTING_REDUCTION_V2.md** → "Understanding the Changes" section

### Understanding QLoRA
See: **CLAUDE.md** → "QLoRA Configuration" section

### Understanding MLX
See: **CLAUDE.md** → "Hardware Target" section

---

## 📞 Getting Help

### For Quick Questions
→ Check: **QUICK_START_V2.txt**

### For Detailed Instructions
→ Read: **RUN_TRAINING_V2.md**

### For Technical Explanation
→ Read: **OVERFITTING_REDUCTION_V2.md**

### For Complete Overview
→ Read: **FINAL_SUMMARY_V2.md**

---

## ✅ Final Checklist

Before starting training, verify:

- ✅ Kernel available: `jupyter kernelspec list | grep mlx`
- ✅ Data ready: `ls -l data/train_v3_final_complete.jsonl`
- ✅ Model ready: `ls -l models/mistral-7b-4bit/`
- ✅ Disk space: `df -h .` (need 26GB free, have it)
- ✅ Notebook accessible: `ls notebooks/train_v2_optimized.ipynb`

All checks passing? → **Start training!** 🚀

---

## 📋 File Organization

```
/LLM_training/
├─ 📌 V2_TRAINING_INDEX.md (this file - start here!)
│
├─ 🚀 START HERE:
│  ├─ QUICK_START_V2.txt (2 min)
│  ├─ PREPARATION_COMPLETE_V2.md (10 min)
│  └─ FINAL_SUMMARY_V2.md (30 min)
│
├─ 📚 DETAILED DOCS:
│  ├─ OVERFITTING_REDUCTION_V2.md (technical)
│  └─ RUN_TRAINING_V2.md (step-by-step)
│
├─ 💾 EXECUTE:
│  ├─ notebooks/train_v2_optimized.ipynb (RECOMMENDED)
│  └─ scripts/train_qlora.py (alternative)
│
├─ 📊 DATA:
│  ├─ data/train_v3_final_complete.jsonl
│  └─ data/valid_v3_final_complete.jsonl
│
├─ 🤖 MODELS:
│  └─ models/mistral-7b-4bit/
│
└─ 📦 OUTPUT:
   ├─ checkpoints_qlora/ (during training)
   └─ output/ (final model)
```

---

## 🎯 Success Criteria

Training V2 is successful if:

✅ Executes without crashes
✅ Loss decreases over time
✅ Overfitting gap < 0.15
✅ F-1 score ≥ 0.93
✅ Early stopping engages appropriately
✅ Best model automatically saved

---

## 📝 Notes

- **All documentation is in this directory**
- **Choose reading based on your time/need**
- **Notebook is ready to execute immediately**
- **Training will complete in 3-4 hours**
- **Results will be automatically saved**

---

## 🚀 Ready to Start?

Execute:
```bash
jupyter notebook notebooks/train_v2_optimized.ipynb
```

Then:
1. Select kernel: **Python 3.11 (MLX)**
2. Run all: **Cell → Run All**
3. Wait ~4 hours
4. Review results

**Good luck!** 🎉

---

**Created:** 2025-11-19
**Status:** ✅ READY
**Next:** Start Jupyter notebook

