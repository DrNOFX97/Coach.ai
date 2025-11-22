# LLM Training Project - Comprehensive Architectural Overview

## Executive Summary

This is a **Large Language Model (LLM) fine-tuning project** focused on training a Mistral-7B model using **QLoRA** (Quantized Low-Rank Adaptation) on Apple Silicon Macs. The project specializes in creating a knowledge-base chatbot for **Sporting Clube Farense** (a Portuguese football club), trained on historical match records, player biographies, and club information spanning from 1913 to present day.

**Project Status:** Active development with completed QLoRA refactoring (LoRA legacy support maintained)

**Target Environment:** Mac M1/M2/M3 Pro/Max with MLX framework

---

## 1. Project Type and Purpose

### What is This Project?

This is a **specialized LLM fine-tuning and inference framework** for creating domain-specific language models with minimal computational resources. It focuses on:

1. Fine-tuning a base LLM (Mistral-7B) with proprietary data
2. Domain specialization for Farense football club historical knowledge
3. Efficient model compression via quantization
4. Seamless inference on resource-constrained environments
5. Training monitoring and metrics tracking

### Use Cases

- Answer questions about Farense football club history
- Provide player biographies and statistics
- Retrieve historical match results
- Integrate into chatbot backend (parent project: chatbot_2.0)

---

## 2. Technology Stack and Frameworks

### Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Base Model | Mistral-7B-v0.1 | Foundation LLM for fine-tuning |
| Hardware Framework | MLX | ML computations on M1/M2/M3 |
| Fine-tuning Method | QLoRA (Quantized LoRA) | Efficient adaptation with 4-bit quantization |
| Quantization | INT4 | Model compression (14GB → 3.5GB) |
| Data Format | JSONL | Question-answer pair format |
| Metrics & Monitoring | pandas, numpy, matplotlib | Training analysis and visualization |
| Utilities | tqdm, psutil, pydantic | Progress bars, system monitoring, validation |
| Interactive Development | Jupyter | Notebook-based training workflows |

### Key Dependencies

```
Core MLX:
- mlx              # ML computations on Apple Silicon
- mlx-lm          # Language model utilities
- mlx-data        # Data loading

Data & Numerics:
- numpy, pandas    # Numerical computing
- matplotlib       # Visualization

Utilities:
- tqdm             # Progress bars
- psutil           # System monitoring
- pydantic         # Data validation
```

**Python Version:** 3.11+ (required for MLX compatibility)

---

## 3. Directory Structure and Organization

### Project Layout

```
/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/

├── DOCS_INDEX.md                       # Main documentation hub
├── START.txt                           # Quick reference
├── ORGANIZED_SUMMARY.md               # Overview

├── docs/                              # Documentation (5 subdirectories)
│   ├── quickstart/                    # Get started (5 min guides)
│   ├── guides/                        # Deep technical documentation
│   ├── references/                    # Quick reference materials
│   ├── troubleshooting/               # Problem-solving
│   └── legacy/                        # Historic docs (preserved)

├── notebooks/                         # Jupyter notebooks
│   ├── mistral_qlora_training.ipynb   # Main training (CURRENT)
│   ├── mistral_qlora_training_monitored.ipynb
│   ├── train_with_monitoring.ipynb
│   └── mistral_lora_training.ipynb    # Legacy

├── scripts/                           # Python utilities
│   ├── train_qlora.py                # Main training script
│   ├── inference_qlora.py            # Model inference
│   ├── monitor.py                    # Real-time monitoring
│   ├── metrics.py                    # Metrics tracking
│   ├── visualization.py              # Training plots
│   ├── compare_models.py             # Model comparison
│   ├── clean_dataset.py              # Data cleaning
│   ├── split_data.py                 # Train/validation split
│   ├── validate_jsonl.py             # Data validation
│   └── [11 more utility scripts]

├── data/                             # Training datasets
│   ├── train.jsonl                   # ~1600 training samples
│   ├── valid.jsonl                   # ~200 validation samples
│   ├── farense_dataset.jsonl         # Combined dataset
│   └── train.jsonl.bak               # Backup

├── models/                           # Pre-quantized models
│   └── mistral-7b-4bit/             # INT4 quantized Mistral-7B

├── checkpoints_qlora/                # QLoRA training state (CURRENT)
│   ├── adapters/adapters.safetensors # Best model weights
│   ├── training_metrics.json
│   ├── training_metrics.csv
│   ├── training_state.json           # For resumption
│   └── training_summary.json

├── checkpoints/                      # LoRA training state (legacy)
│   └── [similar structure]

└── output/                           # Final exported models
    └── mistral-7b-farense-qlora/    # Exported QLoRA model
```

### Key Directories

**`/docs`** - Centralized documentation by purpose (quickstart, guides, references, troubleshooting)

**`/scripts`** - Standalone Python tools for training, inference, monitoring, data processing

**`/notebooks`** - Jupyter notebooks for interactive training (primary: mistral_qlora_training.ipynb)

**`/data`** - JSONL datasets (prompt/completion pairs with metadata about Farense)

**`/models`** - Pre-converted INT4 quantized Mistral-7B base model

**`/checkpoints_qlora`** - Training artifacts (metrics, checkpoints, state for resumption)

---

## 4. Key Architectural Patterns

### System Architecture

```
DATA LAYER
├─ Raw markdown/JSON (dados/)
├─ Convert to JSONL (farense_md_to_csv.py)
├─ Validate & clean (clean_dataset.py)
├─ Split train/validation (split_data.py)
└─ Result: train.jsonl, valid.jsonl

MODEL LOADING
├─ Base model: Mistral-7B-v0.1 (14 GB)
├─ Quantize to INT4 (mlx-lm convert)
└─ Result: mistral-7b-4bit/ (3.5 GB)

TRAINING ORCHESTRATION
├─ Entry: Jupyter notebook or train_qlora.py
├─ Load model + apply QLoRA layers
├─ Initialize optimizer (AdamW)
├─ For each epoch:
│  ├─ Load batches
│  ├─ Forward/backward pass
│  ├─ Log metrics (loss, memory, LR)
│  └─ Checkpoint if validation improves
└─ Export adapters + model

METRICS PERSISTENCE
├─ training_state.json (resume checkpoint)
├─ training_metrics.json (full history)
├─ training_metrics.csv (tabular format)
└─ adapters.safetensors (best weights)

INFERENCE
├─ Load base model + adapters
├─ Generate text from prompts
└─ Output JSON format (for API)
```

### Design Patterns

**Configuration-Driven:** All hyperparameters in config dicts (qlora_config, training_config)

**Metrics Tracking:** MetricsTracker accumulates per-step metrics, saves JSON/CSV incrementally

**Checkpoint Recovery:** training_state.json enables resumption from interruption

**Adapter-Based:** Only small LoRA weights trained (50MB), base model frozen (14GB)

---

## 5. Setup and Build Requirements

### Environment Setup

```bash
# 1. Python 3.11+
python3 --version

# 2. Install dependencies
pip install mlx mlx-lm mlx-data numpy pandas tqdm pydantic psutil matplotlib

# 3. Verify MLX
python3 -c "import mlx.core as mx; print('MLX OK')"

# 4. Verify model can load
python3 -c "from mlx_lm import load; m, t = load('models/mistral-7b-4bit'); print('OK')"

# 5. Validate data
python scripts/validate_jsonl.py data/train.jsonl
```

### Hardware Requirements

| Item | Minimum | Recommended |
|------|---------|------------|
| Mac Model | M1 | M1 Pro/Max, M2 Pro/Max, M3 |
| VRAM | 4 GB | 6+ GB |
| System RAM | 8 GB | 16+ GB |
| Disk Space | 10 GB | 20 GB |

### Training Timeline

```
Setup/Dependencies:     5-10 min
Model Download/Convert: 5-15 min (one-time)
Data Loading:          2-3 min
Training per epoch:    30-40 min (1790 samples, batch=2)
3 epochs:              ~1.5-2 hours
Export:                1-2 min
─────────────────────────────────
TOTAL:                 ~2-3 hours
```

---

## 6. Testing and Validation

### Data Validation

```bash
python scripts/validate_jsonl.py data/train.jsonl    # Check format
python scripts/clean_dataset.py                       # Stats + validation
python scripts/split_data.py --validate               # Verify split
```

### Model Testing

```bash
# Test model loading
python3 -c "from mlx_lm import load, generate; m, t = load('models/mistral-7b-4bit'); print(generate(m, t, 'test', 50))"

# Test with trained adapters
python scripts/inference_qlora.py "Your question?"

# Compare models
python scripts/compare_models.py
```

### Monitoring Tests

```bash
python scripts/test_monitoring.py                    # Test tracking
python scripts/monitor.py --output-dir checkpoints_qlora  # Real-time
```

### Diagnostic Tools

```bash
python scripts/diagnose_qlora.py                     # QLoRA diagnostics
python scripts/check_mlx_setup.py                    # System check
```

### Test Data

- **Training set:** data/train.jsonl (~1600 samples, 89%)
- **Validation set:** data/valid.jsonl (~200 samples, 11%)
- **Format:** JSON with 'prompt', 'completion', 'metadata' fields

---

## 7. Development Workflows

### Workflow 1: Training from Scratch

```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training

# Setup
python3.11 -m venv venv
source venv/bin/activate
pip install mlx mlx-lm mlx-data numpy pandas tqdm psutil pydantic matplotlib

# Validate
python scripts/validate_jsonl.py data/train.jsonl

# Train (Jupyter)
jupyter notebook notebooks/mistral_qlora_training.ipynb
# Execute cells: Setup → Data → Model → Training → Export

# OR Train (CLI)
python scripts/train_qlora.py
```

### Workflow 2: Training with Monitoring

```bash
# Terminal 1: Training
python scripts/train_qlora.py

# Terminal 2: Real-time dashboard
python scripts/monitor.py --output-dir checkpoints_qlora --refresh 5

# Terminal 3: Analyze
jupyter notebook
# Open visualization notebook, run plots every minute
```

### Workflow 3: Resume Training

```bash
# If interrupted, training_state.json auto-loads
python scripts/train_qlora.py
# Resumes from last epoch/step seamlessly
```

### Workflow 4: Inference and Testing

```bash
# Test single query
python scripts/inference_qlora.py "Qual foi o resultado do Farense em 1923?"

# Batch inference
python3 << 'EOF'
from mlx_lm import load, generate
model, tokenizer = load('models/mistral-7b-4bit', 
                       adapter_path='checkpoints_qlora/adapters')
for q in questions:
    response = generate(model, tokenizer, prompt=q, max_tokens=200)
    print(f"Q: {q}\nA: {response}\n")
EOF
```

### Workflow 5: Data Preparation

```bash
python scripts/farense_md_to_csv.py    # Convert markdown to JSONL
python scripts/clean_dataset.py        # Clean and validate
python scripts/split_data.py           # Split train/validation
python scripts/validate_jsonl.py data/train.jsonl
```

### Workflow 6: Hyperparameter Tuning

```bash
# Edit train_qlora.py configs:
qlora_config = {
    "num_layers": 8,           # Try: 4, 8, 12, 16
    "lora_parameters": {
        "rank": 8,             # Try: 4, 8, 16
        "scale": 16,           # Try: 8, 16, 32
    }
}

training_config = {
    "num_epochs": 3,           # Try: 1, 3, 5
    "batch_size": 2,           # Try: 1, 2, 4
    "learning_rate": 2e-4,     # Try: 1e-5, 2e-4, 5e-4
}

# Then retrain
```

### Essential Commands Reference

```bash
# Monitoring
python scripts/monitor.py --output-dir checkpoints_qlora --refresh 5

# Visualization
python scripts/visualization.py checkpoints_qlora

# Validation
python scripts/validate_jsonl.py data/train.jsonl

# Diagnostics
python scripts/diagnose_qlora.py

# Memory profiling
python -m memory_profiler scripts/train_qlora.py
```

---

## 8. Current Project Status

### Recent Activity

From git log:
- Latest: Phase 3e refactoring (error handling & logging)
- Complete: QLoRA migration from legacy LoRA
- Active: 20 organized documentation files
- Maintained: 9 legacy documentation files (preserved)

### Version Status

| Component | Status | Notes |
|-----------|--------|-------|
| QLoRA Training | Production | Fully functional, recommended |
| Data Pipeline | Stable | Clean JSONL format |
| Monitoring | Working | Real-time dashboards available |
| Inference | Production | Scripts + API-ready |
| Documentation | Complete | Well-organized and indexed |
| LoRA (legacy) | Deprecated | Maintained for compatibility |

### Known Notes

- Git status shows many deleted/untracked files: appears to be cleanup/migration
- Documentation recently reorganized into categorized structure
- Docstrings and comments in Portuguese (domain language)

---

## 9. Key Takeaways

### Essential Facts

1. **Specialized fine-tuning** - Not general ML; QLoRA-focused
2. **Use QLoRA, not LoRA** - checkpoints_qlora/, mistral_qlora_training.ipynb
3. **Mac Silicon optimized** - MLX framework, no GPU/CUDA
4. **JSONL format** - prompt/completion pairs with metadata
5. **Fully monitored** - Metrics saved every step
6. **Resumable** - Loads from checkpoint if interrupted

### First Steps

1. Read: `/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/DOCS_INDEX.md`
2. Read: `docs/quickstart/QUICKSTART_QLORA.md`
3. Run: `jupyter notebook notebooks/mistral_qlora_training.ipynb`
4. Monitor: `python scripts/monitor.py --output-dir checkpoints_qlora`
5. Test: `python scripts/inference_qlora.py "Your question"`

### Critical Paths

```
Training notebook:
  /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/notebooks/mistral_qlora_training.ipynb

Training script:
  /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/scripts/train_qlora.py

Inference script:
  /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/scripts/inference_qlora.py

Training data:
  /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data/train.jsonl

Model checkpoint:
  /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/checkpoints_qlora/adapters/

Documentation:
  /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/DOCS_INDEX.md
```

---

## 10. Integration with Parent Project (chatbot_2.0)

This LLM_training is a component of larger chatbot_2.0:

```
chatbot_2.0/
├── LLM_training/        (model creation - this project)
├── backend/             (REST API for inference)
├── frontend/            (web/mobile UI)
├── dados/              (raw data sources)
└── docs/               (project documentation)
```

**Integration flow:**
1. Training in LLM_training creates model
2. Export to output/mistral-7b-farense-qlora/
3. Backend loads and serves via REST API
4. Frontend calls /inference endpoint
5. Chatbot displays responses

---

**Analysis Complete: 2025-11-18**
**Document provides comprehensive overview for new developers**
