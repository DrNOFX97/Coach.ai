# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LLM Training & Fine-tuning Pipeline for Farense Football Club Chatbot**

This project trains a Mistral-7B language model using QLoRA (Quantized Low-Rank Adaptation) on Portuguese historical data about Sporting Clube Farense. The result is a specialized chatbot that answers questions about the club's history, players, results, and classifications.

- **Framework:** MLX (Apple Silicon optimized)
- **Model:** Mistral-7B (quantized to 4-bit)
- **Training Method:** QLoRA with gradient accumulation
- **Hardware Target:** Mac M1/M2/M3 with 4-6GB VRAM
- **Language:** Portuguese
- **Domain:** Football club history and Q&A

---

## Common Development Commands

### Data Preparation
```bash
# Validate JSONL format
python3 scripts/validate_jsonl.py data/farense_dataset.jsonl

# Clean and normalize dataset
python3 scripts/clean_dataset.py

# Split into 90% train / 10% validation
python3 scripts/split_data.py
```

### Training

**Start Training (Notebook - Recommended)**
```bash
jupyter notebook notebooks/mistral_qlora_training.ipynb
```

**Or via Script**
```bash
python3 scripts/train_qlora.py
```

**Monitor Training in Real-time (separate terminal)**
```bash
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

### Inference & Testing

**Test Trained Model**
```bash
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
```

**Compare LoRA vs QLoRA Performance**
```bash
python3 scripts/compare_models.py
```

**Diagnose QLoRA Setup**
```bash
python3 scripts/diagnose_qlora.py
```

### Analysis & Visualization

**Generate Training Plots**
```bash
python3 scripts/visualization.py --report
```

**Analyze Metrics**
```bash
python3 << 'EOF'
import json
with open('checkpoints_qlora/training_metrics.json') as f:
    metrics = json.load(f)
    print(f"Final Loss: {metrics[-1]['loss']}")
    print(f"Best Val Loss: {min(m['val_loss'] for m in metrics)}")
EOF
```

### Validation & Debugging

**Pre-training Checklist**
```bash
# 1. Check hardware
python3 -c "import mlx.core as mx; print(f'Device: {mx.default_device()}')"

# 2. Validate all data files
python3 scripts/validate_jsonl.py data/farense_dataset.jsonl
python3 scripts/clean_dataset.py
python3 scripts/split_data.py

# 3. Check model loading
python3 scripts/diagnose_qlora.py
```

**Test Monitoring System**
```bash
python3 scripts/test_monitoring.py
```

**Recover Interrupted Training**
```bash
python3 scripts/recovery_and_save.py
```

---

## Code Architecture & Structure

### High-Level System Flow

```
Raw Data (dados/)
    ↓
[Data Processing] → clean_dataset.py, split_data.py
    ↓
Structured JSONL (data/train.jsonl, data/valid.jsonl)
    ↓
[Model Loading] → Mistral-7B 4-bit quantized
    ↓
[Training Loop] → train_qlora.py (3 epochs, ~2-3 hours)
    ├─ Tokenization (text → integers)
    ├─ Forward pass
    ├─ Loss calculation
    ├─ Backward pass & gradient update
    ├─ Checkpoint saving every N steps
    └─ Validation evaluation
    ↓
[Monitoring] → monitor.py (real-time tracking)
    ↓
[Checkpoints & Metrics] → checkpoints_qlora/
    ├─ checkpoint_epoch*_step*/
    ├─ training_metrics.json
    ├─ training_metrics.csv
    └─ Best model adapters/
    ↓
[Visualization] → visualization.py (post-training)
    ├─ Loss curves
    ├─ Memory usage plots
    └─ Learning rate schedules
    ↓
[Model Export] → output/mistral-7b-farense-qlora/
    ├─ adapters.safetensors
    ├─ adapter_config.json
    └─ training_config.json
    ↓
[Inference] → inference_qlora.py
    ├─ Load base model + adapters
    ├─ Generate responses
    └─ JSON output
```

### Directory Organization

```
/LLM_training/
├── docs/                          # Documentation (organized by category)
│   ├── DOCS_INDEX.md             # Central navigation hub
│   ├── quickstart/               # Quick start guides (5-10 min reads)
│   ├── guides/                   # Technical deep-dives
│   ├── references/               # Quick reference materials
│   ├── troubleshooting/          # Problem-solving guides
│   └── legacy/                   # Historical documentation
│
├── scripts/                       # Python utility scripts
│   ├── train_qlora.py            # Main training pipeline (CORE)
│   ├── inference_qlora.py        # Model inference (CORE)
│   ├── monitor.py                # Real-time training monitor
│   ├── visualization.py          # Generate training plots
│   ├── clean_dataset.py          # Data cleaning & validation
│   ├── split_data.py             # Train/val split (90/10)
│   ├── validate_jsonl.py         # JSONL format validation
│   ├── compare_models.py         # Benchmark QLoRA vs LoRA
│   ├── diagnose_qlora.py         # System diagnostics
│   └── [+10 more utility scripts]
│
├── notebooks/                     # Jupyter notebooks
│   ├── mistral_qlora_training.ipynb      # MAIN (recommended)
│   ├── mistral_qlora_training_simple.ipynb
│   ├── mistral_qlora_training_monitored.ipynb
│   └── [other variants]
│
├── data/                          # Processed training data (JSONL format)
│   ├── farense_dataset.jsonl     # Full dataset (~1000 examples)
│   ├── train.jsonl               # Training split (90%, 848 examples)
│   └── valid.jsonl               # Validation split (10%, 95 examples)
│
├── dados/                         # Raw source data (Portuguese)
│   ├── biografias/               # Player & president biographies
│   ├── resultados/               # Game results
│   ├── classificacoes/           # League standings
│   ├── jogadores/                # Player information
│   ├── fotografias/              # Team photos (organized by era)
│   └── outros/                   # Miscellaneous documents
│
├── models/                        # Pre-trained base models
│   └── mistral-7b-4bit/          # Mistral-7B quantized (3.8GB)
│       ├── model.safetensors     # Model weights
│       ├── tokenizer.json        # Tokenizer
│       └── config.json           # Model configuration
│
├── checkpoints_qlora/            # Training checkpoints (ACTIVE)
│   ├── checkpoint_epoch*_step*/  # Intermediate checkpoints
│   ├── adapters/                 # Best model found
│   ├── training_metrics.json     # Metrics (JSON)
│   ├── training_metrics.csv      # Metrics (CSV)
│   ├── training_summary.json     # Final summary
│   ├── training_state.json       # Resume state
│   └── plots/                    # Generated visualizations
│
├── output/                        # Final trained models
│   └── mistral-7b-farense-qlora/ # Production model
│       ├── adapters.safetensors
│       ├── adapter_config.json
│       └── training_config.json
│
├── lora.py                        # LoRA implementation classes
├── create_notebook.py             # Notebook generator
└── CLAUDE.md                      # This file
```

### Key Files & Their Responsibilities

#### Core Training (Must Understand)
- **`train_qlora.py` (409 lines)** - Main training pipeline
  - Handles data loading, tokenization, training loop
  - Manages checkpointing and metrics tracking
  - Implements gradient accumulation for larger effective batch size
  - See sections: `TrainingConfig`, `MetricsTracker`, `create_step_fn()`

- **`lora.py` (100 lines)** - LoRA layer implementation
  - Defines `LoRALinear` class for low-rank adaptation
  - Handles weight fusion and quantization
  - Used by `train_qlora.py` to apply LoRA to model

#### Core Inference (Production Use)
- **`inference_qlora.py` (70+ lines)** - Model inference in production
  - Loads base model + LoRA adapters
  - Generates text responses
  - Outputs JSON format

#### Data Pipeline
- **`clean_dataset.py`** - Validates and normalizes data
  - Extracts competition periods correctly
  - Checks for required fields (prompt, completion)
  - Removes duplicates

- **`split_data.py`** - Creates train/validation split
  - 90% training, 10% validation
  - Ensures no overlap between splits

#### Monitoring & Analysis
- **`monitor.py`** - Real-time training monitor
  - Reads `training_metrics.json` at intervals
  - Displays loss, validation loss, memory, ETA
  - Run in separate terminal during training

- **`visualization.py`** - Post-training analysis
  - Generates loss curves, memory plots
  - Creates publication-ready visualizations

### Architectural Patterns

**1. MetricsTracker Pattern** (in `train_qlora.py`)
- Centralizes all metric tracking
- Persists metrics incrementally to JSON/CSV
- Allows interruption/resumption of training

**2. Checkpoint & Recovery**
- Training saves state every N steps
- Automatic recovery from `training_state.json` if training interrupted
- Best model selected based on validation loss

**3. Lazy Loading**
- Model loaded once at startup
- Tokenization happens on-the-fly during training
- Gradients computed lazily by MLX for memory efficiency

**4. Layered Architecture**
```
Presentation Layer (Notebooks/CLI)
    ↓ (uses)
Business Logic Layer (train_qlora.py, inference_qlora.py)
    ↓ (uses)
Data Access Layer (JSONL files, checkpoints)
    ↓ (uses)
ML Framework Layer (MLX, transformers)
    ↓ (runs on)
Hardware Layer (Apple Silicon GPU)
```

---

## How to Extend the System

### Adding a New Data Source
1. Add raw data to `dados/` in appropriate subdirectory
2. Create conversion script (e.g., `scripts/convert_new_format.py`)
3. Output JSONL format with fields: `prompt`, `completion`, `metadata`
4. Run: `python3 scripts/clean_dataset.py`
5. Run: `python3 scripts/split_data.py`
6. Start training with updated `train.jsonl` and `valid.jsonl`

### Modifying Training Configuration
Edit `train_qlora.py` sections:
- `TrainingConfig` class: Adjust batch size, learning rate, num_epochs
- `QLORAConfig` class: Modify quantization settings or LoRA rank
- `create_step_fn()`: Change loss calculation or optimizer

### Supporting New Hardware
- MLX is Apple Silicon specific
- For CUDA/Linux: Would need to port to PyTorch/HuggingFace Transformers
- Modify: `train_qlora.py`, `inference_qlora.py`, model loading code
- Add device detection conditionals

### Adding Custom Metrics
1. Modify `MetricsTracker` class in `train_qlora.py`
2. Add new field to `log_step()` method
3. Update JSON/CSV output formats
4. Update `visualization.py` to plot new metrics

---

## Important Implementation Details

### Data Format (JSONL)
```json
{
  "prompt": "Qual foi o resultado do Farense contra [clube]?",
  "completion": "O Farense jogou fora de casa contra...",
  "metadata": {
    "tipo": "resultado_especifico",
    "epoca": "1913/1914",
    "competicao": "Jogos Pioneiros 1913-1916"
  }
}
```

### Training Parameters
- **Epochs:** 3
- **Batch Size:** 2 (1 for M1 base, 2+ for M1 Pro/Max)
- **Learning Rate:** 2e-4
- **Max Sequence Length:** 512 tokens
- **Gradient Accumulation:** 2 (effective batch = 4)
- **Checkpoint Frequency:** Every 200 steps
- **Validation Frequency:** Every 200 steps

### QLoRA Configuration
- **Quantization:** INT4 (4-bit)
- **LoRA Rank:** 8
- **LoRA Scale:** 16
- **Target Modules:** q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- **Dropout:** 0.0

### Expected Training Time
- **First epoch:** 35-40 minutes
- **Second epoch:** 35-40 minutes
- **Third epoch:** 35-40 minutes
- **Total:** ~2-3 hours on M1/M2 Pro

### Expected Loss Trajectory
```
Epoch 0: loss 4.5 → 3.2, val_loss 3.5 → 2.8
Epoch 1: loss 3.0 → 2.2, val_loss 2.6 → 2.1
Epoch 2: loss 2.0 → 1.5, val_loss 2.0 → 1.7
```

### Inference Performance
- Expected: 300-500 tokens/second on M1/M2
- If slower: GPU might not be utilized; check with `diagnose_qlora.py`

---

## Validation Checklist Before Training

Run these before starting training:

```bash
# 1. Verify data files exist and are valid
python3 scripts/validate_jsonl.py data/farense_dataset.jsonl

# 2. Clean dataset (removes duplicates, validates fields)
python3 scripts/clean_dataset.py

# 3. Create train/validation split (90/10)
python3 scripts/split_data.py

# 4. Verify model can load and GPU is available
python3 scripts/diagnose_qlora.py

# 5. Verify monitoring system works
python3 scripts/test_monitoring.py

# Optional: Verify training can recover from checkpoint
python3 scripts/recovery_and_save.py
```

---

## Troubleshooting Guide

### Loss Not Decreasing
- **Check:** Data validation - run `validate_jsonl.py`
- **Check:** Learning rate - try 5e-4 if 2e-4 too slow
- **Check:** Batch size - ensure it matches available VRAM
- **Check:** Data distribution - examine samples in `data/train.jsonl`

### Out of Memory Errors
- Reduce `batch_size` (2 → 1)
- Reduce `max_seq_length` (512 → 256)
- Increase `gradient_accumulation` (2 → 4)
- Close other applications

### Training Interrupted (GPU Disconnected, Power Loss, etc.)
- Training state auto-saves to `checkpoints_qlora/training_state.json` every step
- Best model auto-saves to `checkpoints_qlora/adapters/`
- Rerunning training automatically detects and resumes from checkpoint
- If recovery fails: `python3 scripts/recovery_and_save.py`

### Model Won't Load
- Verify `models/mistral-7b-4bit/model.safetensors` exists (3.8GB)
- Check file permissions: `ls -la models/mistral-7b-4bit/`
- Verify MLX installation: `python3 -c "import mlx.core as mx"`

### Slow Inference
- Expected: 300-500 tokens/second
- If < 100 tokens/sec: GPU might not be used, check device output
- Profile with: `python3 scripts/compare_models.py`

---

## Documentation Map

Start here for detailed information:

1. **Quick Start (5 minutes)**
   - `docs/quickstart/QUICKSTART_QLORA.md` - Get up and running fast

2. **Complete Setup (10-15 minutes)**
   - `docs/quickstart/START_HERE.md` - Comprehensive setup guide

3. **Technical Deep-Dives (30-60 minutes)**
   - `docs/guides/QLORA_GUIDE.md` - How QLoRA works
   - `docs/guides/QLORA_VS_LORA.md` - LoRA comparison
   - `docs/guides/MONITORING_GUIDE.md` - Training monitoring

4. **Reference Materials (Quick lookup)**
   - `docs/references/QUICK_REFERENCE.md` - One-page cheat sheet
   - `docs/references/CHECKLIST.md` - Pre-training checklist

5. **Problem-Solving**
   - `docs/troubleshooting/QLORA_TROUBLESHOOTING.md` - FAQ & solutions

6. **Project Overview**
   - `DOCS_INDEX.md` - Central navigation hub

---

## Testing Strategy

This project uses **validation-in-layers** rather than formal pytest:

**Layer 1: Data Validation**
- `validate_jsonl.py` - Format & structure checks
- `clean_dataset.py` - Completeness & duplicates
- `split_data.py` - Correct 90/10 split

**Layer 2: Model Validation**
- `diagnose_qlora.py` - System diagnostics
- `verify_corrections.py` - Integrity checks

**Layer 3: Training Validation**
- Loss should decrease over epochs
- Validation loss should track training loss
- Memory usage should stay within limits
- Checkpoints should save correctly

**Layer 4: Inference Validation**
- Model should load without errors
- Generated text should be coherent
- Output JSON format should be valid
- Benchmark with `compare_models.py`

## Special Considerations for This Project

### Python Version
- Requires Python 3.11+ (MLX requirement)
- Check: `python3 --version`

### Apple Silicon Only
- This project is optimized for Apple Silicon (M1/M2/M3)
- Uses MLX framework which requires Apple GPU
- Cannot run on Intel Mac or Linux without major refactoring

### Memory Management
- Mistral-7B base model: 14GB unquantized → 3.8GB quantized (INT4)
- Effective training memory: 4-6GB depending on batch size
- LoRA adapters only: ~50MB additional parameters

### Portuguese Language Specificity
- All Q&A data is in Portuguese
- Tokenizer is Mistral's default (trained on multilingual data)
- Domain-specific: Farense football club history

---

## Performance Optimization Tips

### Speed Improvements
- Use gradient accumulation instead of larger batch size
- Reduce max_seq_length if many short examples
- Use INT4 quantization (already done by default)

### Memory Improvements
- Gradient accumulation allows effective batch size with small actual batches
- LoRA only trains 0.1% of parameters vs full fine-tuning
- INT4 quantization saves 75% model size

### Quality Improvements
- More training data → better quality
- More epochs if convergence not reached
- Lower learning rate if loss is volatile
- Validate on real user queries, not just metrics

---

## Key Git Considerations

When making changes:

1. **Don't commit large files** to data or models directories
2. **Keep documentation updated** when changing code architecture
3. **Add checkpoints to .gitignore** (already done)
4. **Commit training configurations** that work well
5. **Document experimental changes** in commit messages

Current git status shows many untracked files in `checkpoints/`, `models/`, `outputs/` - these should stay untracked as they're generated during training.
