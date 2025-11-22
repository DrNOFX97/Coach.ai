# Project Overview

This project is designed for fine-tuning a Mistral-7B model with LoRA (Low-Rank Adaptation) on Apple Silicon using the MLX framework. The goal is to create a specialized model for a Farense Bot.

The project includes:
- A Jupyter notebook for training the model (`notebooks/mistral_qlora_training_monitored.ipynb`).
- A Python script for running inference on the trained model (`scripts/inference.py`).
- Documentation on how to get started, technical details of the implementation, and how to integrate the model.

# Building and Running

## Training

To train the model, open and run the Jupyter notebook:
```bash
jupyter notebook /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/notebooks/mistral_qlora_training_monitored.ipynb
```
Execute the cells sequentially. The notebook is configured to automatically save checkpoints and the final trained model.

## Inference

To run inference on the trained model, use the `scripts/inference.py` script:
```bash
python3 /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/scripts/inference.py "Your prompt here"
```

# Development Conventions

- The project uses the MLX framework, which is optimized for Apple Silicon.
- The training process is managed through a Jupyter notebook, which allows for interactive experimentation and monitoring.
- The inference script is designed to be used in a production environment and outputs JSON.
- The project includes a checkpointing and recovery system to resume training from the last saved state.
- The `prepare_data.py` script is responsible for loading and preparing the data for training.
- The `visualization.py` script is used for creating post-training reports.
