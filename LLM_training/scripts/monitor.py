#!/usr/bin/env python3
"""
Real-time Training Monitor
Monitora métricas de treinamento em tempo real
Uso: python monitor.py [--output-dir CHECKPOINT_DIR] [--refresh SECONDS]
"""

import json
import time
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from visualization import TrainingVisualizer
    from metrics import MetricsTracker
except ImportError:
    print("Error: visualization.py or metrics.py not found in scripts/")
    sys.exit(1)


class TrainingMonitor:
    """Monitor de treinamento em tempo real"""

    def __init__(self, output_dir: Path = None):
        self.output_dir = Path(output_dir or "checkpoints")
        self.tracker = MetricsTracker(self.output_dir)
        self.visualizer = TrainingVisualizer(self.output_dir)
        self.last_step_count = 0

    def clear_screen(self):
        """Limpa a tela do terminal"""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')

    def format_time(self, seconds: float) -> str:
        """Formata segundos em string legível"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.2f}h"

    def print_header(self):
        """Imprime cabeçalho do monitor"""
        print("╔" + "═"*78 + "╗")
        print("║" + " "*15 + "TRAINING MONITOR - " +
              datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " "*26 + "║")
        print("╚" + "═"*78 + "╝")

    def print_metrics(self):
        """Imprime métricas atuais"""
        metrics_file = self.output_dir / "training_metrics.json"

        if not metrics_file.exists():
            print("\n⏳ Awaiting training data...")
            return False

        try:
            with open(metrics_file, 'r') as f:
                data = json.load(f)
        except:
            print("⚠️  Could not read metrics file")
            return False

        step_metrics = data.get('step_metrics', [])
        epoch_metrics = data.get('epoch_metrics', [])

        if not step_metrics:
            print("\n⏳ No training data yet")
            return False

        # Current status
        latest_step = step_metrics[-1]
        epoch = latest_step.get('epoch', 0)
        step = latest_step.get('step', 0)
        current_loss = latest_step.get('loss', 0)
        memory_mb = latest_step.get('memory_mb', 0)
        elapsed = latest_step.get('elapsed_time_s', 0)

        # Historical data
        losses = [m['loss'] for m in step_metrics if m['loss'] is not None]
        best_loss = min(losses) if losses else 0
        val_losses = [m['val_loss'] for m in epoch_metrics if m['val_loss'] is not None]

        # Print status
        print(f"\n📊 CURRENT STATUS")
        print("─" * 80)
        print(f"  Epoch: {epoch + 1}  |  Step: {step}  |  Elapsed: {self.format_time(elapsed)}")
        print(f"  Current Loss: {current_loss:.6f}  |  Best Loss: {best_loss:.6f}")

        if memory_mb:
            print(f"  Memory Available: {memory_mb:.0f}MB")

        # Show progress
        print(f"\n📈 LOSS STATISTICS")
        print("─" * 80)
        print(f"  Steps with data: {len(losses)}")
        print(f"  Loss range: {min(losses):.6f} - {max(losses):.6f}")

        if len(losses) > 1:
            improvement = losses[0] - losses[-1]
            improvement_pct = (improvement / losses[0] * 100) if losses[0] > 0 else 0
            print(f"  Improvement: {improvement:.6f} ({improvement_pct:+.1f}%)")

        # Validation loss
        if val_losses:
            print(f"\n🎯 VALIDATION")
            print("─" * 80)
            print(f"  Best Val Loss: {min(val_losses):.6f}")
            print(f"  Latest Val Loss: {val_losses[-1]:.6f}")
            if len(val_losses) > 1:
                val_improvement = val_losses[0] - val_losses[-1]
                print(f"  Val Improvement: {val_improvement:+.6f}")

        # Best checkpoint
        best_checkpoint = data.get('best_checkpoint', {})
        if best_checkpoint.get('epoch') is not None:
            print(f"\n🏆 BEST CHECKPOINT")
            print("─" * 80)
            print(f"  Epoch: {best_checkpoint.get('epoch')}")
            print(f"  Step: {best_checkpoint.get('step')}")
            print(f"  Loss: {best_checkpoint.get('loss'):.6f}")

        # Tips
        new_steps = len(losses) - self.last_step_count
        self.last_step_count = len(losses)

        if new_steps > 0:
            print(f"\n✓ {new_steps} new step(s) recorded")

        return True

    def show_predictions(self, count: int = 5):
        """Mostra previsões de tempo de treinamento"""
        metrics_file = self.output_dir / "training_metrics.json"

        if not metrics_file.exists():
            return

        try:
            with open(metrics_file, 'r') as f:
                data = json.load(f)
        except:
            return

        step_metrics = data.get('step_metrics', [])
        epoch_metrics = data.get('epoch_metrics', [])

        if not step_metrics or not epoch_metrics:
            return

        # Calcula tempo médio por step
        if len(step_metrics) > 1:
            first_step = step_metrics[0]
            last_step = step_metrics[-1]

            elapsed_total = last_step.get('elapsed_time_s', 0) - first_step.get('elapsed_time_s', 0)
            steps_done = len(step_metrics)

            if elapsed_total > 0 and steps_done > 0:
                time_per_step = elapsed_total / steps_done

                print(f"\n⏱️  TIME ESTIMATES")
                print("─" * 80)
                print(f"  Time per step: {time_per_step:.2f}s")

                # Estima resto do treinamento
                total_steps_estimate = steps_done * 1.5  # estimativa
                remaining_steps = max(0, total_steps_estimate - steps_done)
                remaining_time = remaining_steps * time_per_step

                print(f"  Est. remaining: {self.format_time(remaining_time)}")

    def run(self, refresh_interval: int = 5):
        """Executa monitor continuamente"""
        print(f"Starting training monitor (refresh every {refresh_interval}s)")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                self.clear_screen()
                self.print_header()
                has_data = self.print_metrics()

                if has_data:
                    self.show_predictions()

                print("\n" + "─" * 80)
                print(f"Next update in {refresh_interval}s... (Ctrl+C to exit)")

                time.sleep(refresh_interval)

        except KeyboardInterrupt:
            print("\n\n✓ Monitor stopped")

    def generate_reports(self):
        """Gera relatórios finais"""
        print("\n📊 Generating reports...")

        # Print training report
        self.visualizer.print_training_report()

        # Generate plots
        print("\n🎨 Generating plots...")

        try:
            loss_plot = self.visualizer.plot_loss_curves(save=True)
            print(f"✓ Loss curves saved")
        except Exception as e:
            print(f"⚠️  Could not generate loss curves: {e}")

        try:
            memory_plot = self.visualizer.plot_memory_usage(save=True)
            print(f"✓ Memory usage saved")
        except Exception as e:
            print(f"⚠️  Could not generate memory plot: {e}")

        try:
            dashboard = self.visualizer.create_dashboard(save=True)
            print(f"✓ Dashboard saved")
        except Exception as e:
            print(f"⚠️  Could not generate dashboard: {e}")

        print(f"\n✓ All reports generated in: {self.visualizer.plots_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Real-time training monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monitor.py                          # Monitor default checkpoint dir
  python monitor.py --output-dir ./ckpts     # Monitor specific directory
  python monitor.py --report                 # Generate final report and exit
  python monitor.py --refresh 10             # Refresh every 10 seconds
        """
    )

    parser.add_argument('--output-dir', default='checkpoints',
                       help='Checkpoint directory (default: checkpoints)')
    parser.add_argument('--refresh', type=int, default=5,
                       help='Refresh interval in seconds (default: 5)')
    parser.add_argument('--report', action='store_true',
                       help='Generate final report and exit')

    args = parser.parse_args()

    monitor = TrainingMonitor(output_dir=args.output_dir)

    if args.report:
        monitor.generate_reports()
    else:
        monitor.run(refresh_interval=args.refresh)


if __name__ == '__main__':
    main()
