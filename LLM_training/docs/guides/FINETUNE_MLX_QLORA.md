# 🚀 Finetuning LLMs with QLoRA on Mac M1 using MLX

This guide provides clear and simple instructions to finetune a Large Language Model (LLM) using QLoRA with the MLX framework, specifically optimized for Apple Silicon (Mac M1/M2/M3) devices.

## ✨ Why QLoRA on Mac M1 with MLX?

QLoRA offers significant advantages for finetuning LLMs on Apple Silicon:
- **Reduced Model Size:** Quantization to INT4 reduces model size (e.g., 14GB to 3.5GB).
- **Lower VRAM Usage:** Requires less memory, enabling training on devices with limited VRAM (e.g., 4-6GB vs 8-10GB).
- **Faster Training:** Up to 30% faster training times.
- **Similar Quality:** Achieves nearly identical performance to full LoRA.

## 📋 Prerequisites

### Hardware
-   **Mac M1/M2/M3 (Pro or Max recommended):** Essential for MLX framework.
-   **Minimum 4GB VRAM:** More VRAM allows for larger batch sizes and sequence lengths.
-   **~5GB Disk Space:** For model downloads and checkpoints.

### Software
-   **Python 3.11+:** Ensure you have a compatible Python version.
-   **Required Libraries:**
    ```bash
    pip install mlx mlx-lm mlx-data numpy pandas tqdm pydantic psutil jupyter
    ```

## 🛠️ Environment Setup

1.  **Verify Python Version:**
    ```bash
    python3 --version
    # Expected output: Python 3.11.x or higher
    ```

2.  **Install Dependencies:**
    ```bash
    pip install mlx mlx-lm mlx-data numpy pandas tqdm pydantic psutil jupyter
    ```

3.  **Verify MLX Installation:**
    ```bash
    python3 -c "import mlx.core as mx; print('✓ MLX OK')"
    # Expected output: ✓ MLX OK
    ```
    This also attempts to enable the Metal GPU. If you see "✓ CPU mode", ensure your MLX installation is correct and your system is configured for Metal.

## 📊 Data Preparation

Your project already includes pre-processed data files:
-   `data/train_data.jsonl` (training examples)
-   `data/val_data.jsonl` (validation examples)

These files are in JSONL format, where each line is a JSON object typically containing `prompt` and `completion` fields. The training notebook will automatically load these.

## 🚀 QLoRA Finetuning Process

The primary tool for finetuning is the Jupyter Notebook: `notebooks/mistral_qlora_training.ipynb`.

1.  **Navigate to the Project Directory:**
    ```bash
    cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training
    ```

2.  **Open the Jupyter Notebook:**
    ```bash
    jupyter notebook notebooks/mistral_qlora_training.ipynb
    ```
    Your web browser will open with the Jupyter interface.

3.  **Execute Cells Step-by-Step:**
    Go through the notebook and execute each cell in order. The notebook is structured into logical sections:

    *   **Section 1: Setup (Cells 1-6)**
        *   Imports necessary libraries (MLX, numpy, etc.).
        *   Verifies Mac M1 detection and enables Metal GPU.
        *   Configures project paths for data, checkpoints, and output.

    *   **Section 2: Data (Cells 7-10)**
        *   Loads `train_data.jsonl` and `val_data.jsonl`.

    *   **Section 3: Model QLoRA (Cells 11-17)**
        *   Loads the base model (e.g., `mistralai/Mistral-7B-v0.1`) with INT4 quantization. This step downloads the model if not already present and applies quantization.

    *   **Section 4: Training (Cells 18-20)**
        *   Initiates the QLoRA training process. You will see real-time progress, including loss values and memory usage. Checkpoints are saved automatically.

    *   **Section 5: Test (Cells 21-22)**
        *   After training, this section allows you to test the finetuned model by generating responses to a sample prompt.

    *   **Section 6: Export (Cells 23-26)**
        *   Saves the final finetuned model and related scripts to the `output/` directory.

### Customizing Training Configurations

The notebook includes `qlora_config` and `training_config` dictionaries that you can modify to suit your hardware and desired training intensity.

**Example `qlora_config`:**
```python
qlora_config = {
    "quantization": "int4",      # 4-bit quantization
    "group_size": 64,            # Quantization group size
    "lora_rank": 8,              # LoRA decomposition rank
    "lora_alpha": 16,            # LoRA scaling factor
    "target_modules": ["q_proj", "v_proj", "k_proj"], # Modules to apply LoRA to
    "bias": "none",
}
```

**Example `training_config` (for M1 Pro 16GB RAM):**
```python
training_config = {
    "num_epochs": 3,              # Number of training epochs
    "batch_size": 2,              # Batch size per step
    "gradient_accumulation": 2,   # Accumulate gradients over multiple steps
    "learning_rate": 2e-4,        # Learning rate
    "max_seq_length": 512,        # Maximum sequence length for tokenization
    "warmup_steps": 100,          # Warmup steps for learning rate scheduler
}
```

Adjust `batch_size`, `gradient_accumulation`, and `max_seq_length` based on your Mac's VRAM.

## ⏱️ Expected Training Times

| Phase           | Time      | Observations                                   |
| :-------------- | :-------- | :--------------------------------------------- |
| Setup/Imports   | 2-3 min   | Loading libraries                              |
| Data            | 1-2 min   | Validating and preparing data                  |
| Model Load      | 5-10 min  | Download + quantization                        |
| **Training (1 epoch)** | **~30-40 min** | Real-time progress visible                     |
| **Training (3 epochs)** | **~1.5-2 hours** | Recommended for good quality                   |
| Validation      | 3-5 min   | Between epochs                                 |
| Export          | 1-2 min   | Saving final model                             |
| **TOTAL**       | **~2-3 hours** | Includes complete training (3 epochs)          |

## 📊 Monitoring Training in Real-Time

During training, you will observe output similar to this:

```
Epoch 1/3
Training: 45%|████████████▌              | 1207/2414
  [Memory] Epoch 1 start: 3625MB disponível
  Step 20/2414 - Loss: 2.5234
  Step 40/2414 - Loss: 2.1892
  [Memory] Step 40: 3500MB disponível
  Step 60/2414 - Loss: 1.8765
  ✓ Checkpoint saved (step 200)
  ...
Validating: 30%|███████                  | 9/30
  Val Loss: 1.4532
  ✓ Best model saved (Loss: 1.4532)
  ✓ Epoch 1 complete
```

**Key Metrics:**
-   **Loss:** Should decrease over time and across epochs. Lower is better.
-   **Memory:** Monitor VRAM usage; it should remain stable within the 4-6GB range for QLoRA.
-   **Tokens/sec:** Indicates generation speed (300-500 tokens/sec is good).

## 🚀 Using the Trained Model

### Option 1: Within the Jupyter Notebook
After the "Test" section, you can use the `generate_response` function (or similar) directly:
```python
from mlx_lm import generate

test_prompt = "Qual foi a melhor classificação do Farense?"
response = generate(
    model,
    tokenizer,
    prompt=test_prompt,
    max_tokens=100,
    verbose=False
)
print(f"Response: {response}")
```

### Option 2: Via Python Script
Your project includes an inference script: `scripts/inference_qlora.py`.
```bash
python scripts/inference_qlora.py "Sua pergunta aqui"
```

### Option 3: Integrate into a Backend (e.g., Node.js Express)
You can call the Python inference script as a subprocess from other applications:
```javascript
// Node.js example
const { spawn } = require('child_process');

function askFarenseBot(question) {
  return new Promise((resolve, reject) => {
    const process = spawn('python', [
      'scripts/inference_qlora.py',
      question
    ]);

    let output = '';
    process.stdout.on('data', (data) => {
      output += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(output);
          resolve(result.response);
        } catch (e) {
          reject(new Error(`Failed to parse JSON response: ${e.message}. Output: ${output}`));
        }
      } else {
        reject(new Error(`Python script exited with code ${code}. Output: ${output}`));
      }
    });
    process.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
  });
}

// Usage example
askFarenseBot("Conte-me sobre Hassan Nader")
  .then(response => console.log(response))
  .catch(error => console.error(error));
```

## ⚠️ Troubleshooting

### "Memória insuficiente" (Insufficient Memory)
-   **Solution:** In the notebook's `training_config`, reduce `batch_size` and `max_seq_length`. You might also increase `gradient_accumulation`.
    ```python
    training_config["batch_size"] = 1
    training_config["gradient_accumulation"] = 4 # If batch_size is 1
    training_config["max_seq_length"] = 256
    ```

### "Model not found"
-   **Solution:** Ensure MLX has internet access to download the base model (`mistralai/Mistral-7B-v0.1`). Also, try upgrading `mlx-lm`:
    ```bash
    pip install --upgrade mlx-lm
    ```

### Loss is increasing (Diverging)
-   **Solution:** Reduce the `learning_rate` and potentially increase `warmup_steps` in `training_config`.
    ```python
    training_config["learning_rate"] = 1e-4  # From 2e-4 to 1e-4
    training_config["warmup_steps"] = 200    # Increase warmup
    ```

### Training is too slow
-   **Solution:** If you have available VRAM, increase `batch_size`. Otherwise, reduce `max_seq_length`.
    ```python
    training_config["batch_size"] = 4  # If memory allows
    training_config["max_seq_length"] = 256 # Reduce sequence length
    ```

## 📁 Important Files in Your Project

```
LLM_training/
├── notebooks/
│   ├── mistral_qlora_training.ipynb    ← Primary notebook for QLoRA training
│   └── mistral_qlora_training_simple.ipynb ← Simplified training example
│
├── scripts/
│   ├── inference_qlora.py              ← Script for QLoRA model inference
│   └── compare_models.py               ← Utility to compare LoRA vs QLoRA models
│
├── output/
│   └── mistral-7b-farense-qlora/       ← Directory for the trained QLoRA model
│
├── checkpoints_qlora/                  ← Directory for QLoRA training checkpoints
│
├── data/
│   ├── train_data.jsonl                ← Training dataset
│   └── val_data.jsonl                  ← Validation dataset
│
├── QLORA_GUIDE.md                      ← Comprehensive QLoRA guide
├── QUICKSTART_QLORA.md                 ← Original quickstart guide
└── FINETUNE_MLX_QLORA.md               ← This guide
```

---

**Last Updated:** 2025-11-09
**Method:** QLoRA with MLX for Mac M1
