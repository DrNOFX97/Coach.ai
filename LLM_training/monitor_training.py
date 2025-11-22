#!/usr/bin/env python3
"""
Monitor LoRA Training in Real-Time
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

def monitor_training():
    """Monitor training progress and display metrics."""
    
    log_file = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/training_log.txt")
    metrics_file = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/checkpoints_qlora/training_metrics.json")
    
    print("\n" + "="*80)
    print("🚀 QLORA TRAINING MONITOR - REAL-TIME METRICS")
    print("="*80 + "\n")
    
    start_time = time.time()
    
    while True:
        try:
            # Check if log file exists and has content
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"\n⏱️  Time Elapsed: {(time.time() - start_time)/60:.1f} minutes")
                        print("\n📊 Latest Output from Training:")
                        print("-" * 80)
                        # Show last 20 lines
                        for line in lines[-20:]:
                            print(line.rstrip())
                        print("-" * 80)
            
            # Check if metrics file exists
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    metrics = json.load(f)
                    print("\n📈 TRAINING METRICS:")
                    for key, value in metrics.items():
                        if isinstance(value, float):
                            print(f"   {key}: {value:.4f}")
                        else:
                            print(f"   {key}: {value}")
            
            print(f"\n🔄 Next update in 10 seconds... (Press Ctrl+C to stop monitoring)")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n\n✋ Monitoring stopped by user")
            break
        except Exception as e:
            print(f"⚠️  Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_training()
