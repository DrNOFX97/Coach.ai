# 🧠 Coach.ai - LLM Finetuning Platform

**Coach.ai** is a modern, web-based interface designed to simplify the process of fine-tuning Large Language Models (LLMs) on Apple Silicon. It leverages the **MLX framework** for high-performance local training and provides a guided, user-friendly experience.

---

## 🏗️ Architecture Overview

The project is built as a full-stack application:

### 1. Frontend (`Coach.ai/`)
*   **Framework:** React + Vite
*   **Styling:** Custom CSS with a "Deep Navy & Electric Blue" premium aesthetic.
*   **Key Components:**
    *   `WizardLayout`: Manages the 5-step workflow.
    *   `SystemCheck`: Detects hardware (RAM, GPU, Disk) and recommends settings.
    *   `Configuration`: Interactive form for model/dataset/hyperparameters.
    *   `Training`: Real-time visualization of loss curves and logs.

### 2. Backend (`backend/`)
*   **Framework:** FastAPI (Python)
*   **Role:** Acts as the bridge between the UI and the training scripts.
*   **Key Endpoints:**
    *   `/system-info`: Returns hardware stats and **Smart Presets**.
    *   `/validate-dataset`: Analyzes JSONL files for errors and stats.
    *   `/start-training`: Launches the training process in a background thread.
    *   `/training-status`: Polls for metrics to update the UI.

### 3. Training Engine (`LLM_training/`)
*   **Core Script:** `scripts/train_qlora.py` (Refactored for dynamic config).
*   **Frameworks:**
    *   **MLX:** Primary engine for Apple Silicon (Metal).
    *   **PyTorch:** Fallback/Alternative (Stub implemented).
*   **Optimization:** Uses `mx.compile` for 2x-5x speedup on Mac.

---

## ✨ Key Features

### 🖥️ Intelligent System Check
*   Automatically detects **Available RAM** and **GPU** (Metal vs CUDA).
*   Calculates **Smart Presets** (Conservative, Balanced, Aggressive) tailored to your specific hardware to prevent crashes (OOM).

### 🎛️ Interactive Configuration
*   **Presets Mode:** One-click configuration based on hardware analysis.
*   **Custom Mode:** Full control over Batch Size, Learning Rate, Epochs, etc.
*   **Tooltips:** Explains the impact of each parameter on performance/memory.

### 🛡️ Dataset Validation
*   Uploads and scans your `.jsonl` file before training.
*   Checks for:
    *   Valid JSON format.
    *   Required fields (`prompt`/`completion` or `instruction`/`output`).
    *   Duplicate entries.
    *   Empty data.
*   Provides a "Health Report" with estimated Train/Val splits.

### 🚀 Real-Time Monitoring
*   Live graph of Training Loss.
*   Streaming logs from the backend.
*   Progress bar and step counter.

---

## 🚀 How to Run

The project includes a unified startup script that launches both the Backend and Frontend.

1.  **Open Terminal** in the project root:
    ```bash
    cd /Users/f.nuno/Desktop/chatbot_2.0
    ```

2.  **Run the Startup Script:**
    ```bash
    ./start_app.sh
    ```

3.  **Access the App:**
    *   The browser should open automatically at `http://localhost:5173`.
    *   Backend API runs at `http://localhost:8000`.

---

## 🛠️ Technical Notes for Future Devs

*   **Environment:** The app uses a specific Python environment (`mlx_finetuning_env`) configured in `start_app.sh`. Ensure this environment has `mlx`, `fastapi`, `uvicorn`, and `psutil` installed.
*   **Fallback Mode:** If MLX is not found (e.g., running on a non-Mac), the backend switches to a "Mock Mode" to allow UI testing without crashing.
*   **State Management:** `App.jsx` holds the global state (`config`) and passes it down to steps. `SystemCheck` initializes the config using backend recommendations.

---

**Created by:** Antigravity (Google DeepMind) & User
**Date:** November 2025
