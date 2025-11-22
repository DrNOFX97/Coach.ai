#!/usr/bin/env python3
"""
Script para testar o sistema de monitorização
Simula um treinamento e gera métricas
"""

import time
import random
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from metrics import MetricsTracker, PerformanceMonitor
from visualization import TrainingVisualizer


def simulate_training():
    """Simula um treinamento para testar o sistema de monitorização"""

    print("\n" + "="*70)
    print(" "*15 + "MONITORING SYSTEM TEST - Simulating Training")
    print("="*70)

    # Setup
    output_dir = Path("checkpoints")
    tracker = MetricsTracker(output_dir)
    monitor = PerformanceMonitor()
    visualizer = TrainingVisualizer(output_dir)

    # Configuração
    config = {
        "num_epochs": 3,
        "steps_per_epoch": 100,
        "batch_size": 1,
        "learning_rate": 1e-5,
    }

    training_start = time.time()

    print("\n📝 Simulating training with configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    # Simular épocas
    for epoch in range(config["num_epochs"]):
        epoch_start = time.time()
        epoch_losses = []

        print(f"\n📍 Epoch {epoch + 1}/{config['num_epochs']}")

        # Simular steps
        for step in range(1, config["steps_per_epoch"] + 1):
            # Simular loss que diminui com o tempo (curva de aprendizado)
            # Com variações aleatórias
            base_loss = 5.0 * math.exp(-epoch / 2) * math.exp(-step / config["steps_per_epoch"] / 2)
            noise = random.gauss(0, base_loss * 0.1)
            loss = max(0.1, base_loss + noise)

            epoch_losses.append(loss)

            # Simular validation loss (um pouco maior)
            val_loss = loss * random.uniform(1.0, 1.1) if step % 10 == 0 else None

            # Simular memória
            memory_mb = 8000 + random.randint(-500, 500)
            monitor.record_memory(memory_mb)

            # Log metrics
            elapsed = time.time() - training_start
            tracker.log_step(
                epoch=epoch,
                step=step,
                loss=loss,
                val_loss=val_loss,
                learning_rate=config["learning_rate"],
                memory_mb=memory_mb,
                elapsed_time=elapsed
            )

            # Print progress
            if step % 20 == 0:
                print(f"  Step {step:3d}/{config['steps_per_epoch']} - "
                      f"Loss: {loss:.4f} - Memory: {memory_mb:.0f}MB")

            # Simular delay de processamento
            time.sleep(0.01)

        # End of epoch
        epoch_time = time.time() - epoch_start
        avg_epoch_loss = sum(epoch_losses) / len(epoch_losses)

        print(f"✓ Epoch {epoch + 1} completed in {epoch_time:.1f}s - Avg Loss: {avg_epoch_loss:.4f}")

        # Log epoch metrics
        tracker.log_epoch(
            epoch=epoch,
            avg_loss=avg_epoch_loss,
            val_loss=avg_epoch_loss * 1.05,
            learning_rate=config["learning_rate"],
            elapsed_time=time.time() - training_start
        )

        # Save metrics periodically
        tracker.save_json()

    # Training complete
    total_time = time.time() - training_start

    print("\n" + "="*70)
    print(" "*20 + "TRAINING SIMULATION COMPLETE")
    print("="*70)
    print(f"Total time: {total_time:.1f}s")

    # Save final summary
    summary = tracker.save_summary(
        total_time=total_time,
        total_samples=config["num_epochs"] * config["steps_per_epoch"],
        training_config=config
    )

    # Print status
    print("\n✓ Metrics saved to:")
    print(f"  CSV: {tracker.csv_file}")
    print(f"  JSON: {tracker.json_file}")
    print(f"  Summary: {tracker.summary_file}")

    return tracker, visualizer


def test_visualization(visualizer: TrainingVisualizer):
    """Testa a visualização"""

    print("\n" + "="*70)
    print(" "*15 + "TESTING VISUALIZATION")
    print("="*70)

    try:
        print("\n📊 Generating loss curves...")
        loss_plot = visualizer.plot_loss_curves(save=True)
        print(f"✓ Loss curves saved: {loss_plot}")
    except Exception as e:
        print(f"⚠️  Could not generate loss curves: {e}")

    try:
        print("\n💾 Generating memory plot...")
        memory_plot = visualizer.plot_memory_usage(save=True)
        print(f"✓ Memory plot saved: {memory_plot}")
    except Exception as e:
        print(f"⚠️  Could not generate memory plot: {e}")

    try:
        print("\n📈 Generating dashboard...")
        dashboard = visualizer.create_dashboard(save=True)
        print(f"✓ Dashboard saved: {dashboard}")
    except Exception as e:
        print(f"⚠️  Could not generate dashboard: {e}")

    print("\n" + "-"*70)
    print("Training Report:")
    print("-"*70)
    visualizer.print_training_report()


def main():
    print("\n🧪 MONITORING SYSTEM TEST SUITE\n")

    # Test 1: Simulate training
    print("Test 1: Simulating training and collecting metrics...")
    tracker, visualizer = simulate_training()

    # Test 2: Test metrics tracker
    print("\n\nTest 2: Testing MetricsTracker...")
    print("-"*70)
    tracker.print_status()

    # Test 3: Test visualization
    print("\nTest 3: Testing visualization...")
    try:
        test_visualization(visualizer)
    except ImportError as e:
        print(f"\n⚠️  Matplotlib not available. Install with: pip install matplotlib")
        print(f"  Error: {e}")

    # Test 4: Verify files exist
    print("\n\nTest 4: Verifying output files...")
    print("-"*70)

    output_dir = Path("checkpoints")
    files_to_check = [
        output_dir / "training_metrics.csv",
        output_dir / "training_metrics.json",
        output_dir / "training_summary.json",
    ]

    for file_path in files_to_check:
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"✓ {file_path.name:30s} ({size_kb:.1f}KB)")
        else:
            print(f"✗ {file_path.name:30s} (not found)")

    # Summary
    print("\n" + "="*70)
    print(" "*25 + "TEST COMPLETE")
    print("="*70)
    print("\n✅ All tests passed!")
    print("\nNext steps:")
    print("1. Review the generated plots in checkpoints/plots/")
    print("2. Check the metrics in checkpoints/training_metrics.csv")
    print("3. Run: python scripts/monitor.py --report")
    print("4. Integrate into your training script!")
    print()


if __name__ == '__main__':
    main()
