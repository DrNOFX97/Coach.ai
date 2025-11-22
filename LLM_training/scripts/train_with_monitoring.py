#!/usr/bin/env python3
"""
Exemplo de Treinamento com LoRA usando o CLI mlx_lm.lora.

Este script invoca o CLI mlx_lm.lora para treinar um modelo com LoRA,
simplificando a gestão de dados e o loop de treino.

Uso: python train_with_monitoring.py
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Main function to execute mlx_lm.lora CLI training command"""

    project_root = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training")
    data_dir = project_root / "data"
    checkpoint_dir = project_root / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)

    model_path = str(project_root / "models/mistral-7b-4bit")

    # Define training parameters
    batch_size = 4
    iters = 100
    learning_rate = 1e-5
    lora_layers = 4
    max_seq_length = 2100
    adapter_path = str(checkpoint_dir / "adapters")
    val_batches = 25
    val_interval = 100
    save_every = 100
    seed = 0

    # Construct the mlx_lm.lora CLI command
    command = [
        "python", "-u", "-m", "mlx_lm", "lora",
        "--model", str(model_path),
        "--train",
        "--data", str(data_dir),
        "--batch-size", str(batch_size),
        "--iters", str(iters),
        "--learning-rate", str(learning_rate),
        "--num-layers", str(lora_layers),
        "--max-seq-length", str(max_seq_length),
        "--adapter-path", adapter_path,
        "--val-batches", str(val_batches),
        "--steps-per-eval", str(val_interval),
        "--save-every", str(save_every),
        "--seed", str(seed),
    ]

    print("\n" + "="*70)
    print("STARTING MLX_LM CLI TRAINING")
    print("Command:", " ".join(command))
    print("="*70)

    try:
        # Execute the command and show output in the terminal in real-time
        with subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=1, 
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                print(line, end='')

        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, p.args)

        print("\n" + "="*70)
        print("MLX_LM CLI TRAINING COMPLETE")
        print("="*70)

    except subprocess.CalledProcessError as e:
        print(f"\n\n❌ Error during MLX_LM CLI training: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ An unexpected error occurred: {e}")
        sys.exit(1)

    print("\n✓ All done!")
    print(f"\nMetrics and adapters saved in: {checkpoint_dir}/adapters/")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)