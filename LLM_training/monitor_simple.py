#!/usr/bin/env python3
"""Monitor de Treino Simples"""

import json
import time
from pathlib import Path
from datetime import datetime

CHECKPOINT_DIR = Path("checkpoints_qlora")

def read_metrics():
    metrics_file = CHECKPOINT_DIR / "training_metrics.json"
    if not metrics_file.exists():
        return None
    try:
        with open(metrics_file) as f:
            return json.load(f)
    except:
        return None

def main():
    print("\n" + "="*80)
    print("  MONITOR DE TREINO - SISTEMA SAFE TRAIN")
    print("="*80 + "\n")
    print("Pressione Ctrl+C para parar\n")

    last_len = 0
    start = time.time()

    while True:
        metrics = read_metrics()

        if metrics:
            if isinstance(metrics, list):
                current = metrics[-1] if metrics else {}
            else:
                current = metrics

            current_len = len(metrics) if isinstance(metrics, list) else 1

            # Se houver novos dados
            if current_len != last_len or True:
                elapsed = time.time() - start
                hours, remainder = divmod(int(elapsed), 3600)
                mins, secs = divmod(remainder, 60)

                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Progresso:")
                print(f"  Época:       {current.get('epoch', 'N/A')}")
                print(f"  Step:        {current.get('step', 'N/A')}")
                print(f"  Loss:        {current.get('loss', 'N/A'):.4f}" if isinstance(current.get('loss'), (int, float)) else f"  Loss:        {current.get('loss', 'N/A')}")
                print(f"  Val Loss:    {current.get('val_loss', 'N/A'):.4f}" if isinstance(current.get('val_loss'), (int, float)) else f"  Val Loss:    {current.get('val_loss', 'N/A')}")
                print(f"  Tempo:       {hours}h {mins}m {secs}s")

                last_len = current_len
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Aguardando métricas...")

        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Monitor encerrado")
