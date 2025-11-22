"""
Visualização de Métricas de Treinamento
Cria gráficos e dashboards para monitorizar treinamento
"""

import json
from pathlib import Path
from datetime import datetime
import numpy as np
from typing import Optional, Dict, List

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class TrainingVisualizer:
    """Cria visualizações dos dados de treinamento"""

    def __init__(self, output_dir: Path = None):
        """
        Inicializa o visualizador.

        Args:
            output_dir: Diretório para salvar gráficos
        """
        if output_dir is None:
            output_dir = Path("checkpoints")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.metrics_file = self.output_dir / "training_metrics.json"
        self.plots_dir = self.output_dir / "plots"
        self.plots_dir.mkdir(exist_ok=True)

    def load_metrics(self) -> Dict:
        """Carrega métricas do arquivo JSON"""
        if not self.metrics_file.exists():
            return None

        with open(self.metrics_file, 'r') as f:
            return json.load(f)

    def plot_loss_curves(self, save=True) -> Optional[str]:
        """
        Cria gráfico de curvas de loss (treino vs validação).

        Args:
            save: Se True, salva o gráfico

        Returns:
            Caminho do arquivo salvo (se save=True)
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️  matplotlib não disponível. Instale com: pip install matplotlib")
            return None

        metrics = self.load_metrics()
        if not metrics or not metrics.get('step_metrics'):
            print("Nenhuma métrica disponível para plotar")
            return None

        # Extrai dados
        step_metrics = metrics['step_metrics']

        steps = []
        train_losses = []
        val_losses = []
        epochs = []

        for m in step_metrics:
            if m['loss'] is not None:
                steps.append(m['step'])
                train_losses.append(m['loss'])
                epochs.append(m['epoch'])

            if m['val_loss'] is not None:
                val_losses.append(m['val_loss'])

        # Cria figura com 2 subgráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Gráfico 1: Loss ao longo dos steps
        if train_losses:
            ax1.plot(steps, train_losses, 'b-', label='Train Loss', linewidth=2)
            ax1.fill_between(steps, train_losses, alpha=0.3)
            ax1.set_xlabel('Step', fontsize=12)
            ax1.set_ylabel('Loss', fontsize=12)
            ax1.set_title('Training Loss Over Steps', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend()

            # Marca melhor loss
            best_idx = np.argmin(train_losses)
            ax1.scatter([steps[best_idx]], [train_losses[best_idx]],
                       color='red', s=100, marker='*', zorder=5, label='Best')

        # Gráfico 2: Comparação treino vs validação
        if train_losses and val_losses:
            epochs_train = sorted(set(epochs))

            # Calcula loss médio por época
            epoch_train_losses = []
            epoch_val_losses = []

            for epoch in epochs_train:
                epoch_train = [train_losses[i] for i in range(len(epochs)) if epochs[i] == epoch]
                if epoch_train:
                    epoch_train_losses.append(np.mean(epoch_train))

            epoch_val_losses = val_losses[:len(epoch_train_losses)]

            x = np.arange(len(epochs_train))
            width = 0.35

            ax2.bar(x - width/2, epoch_train_losses, width, label='Train Loss', alpha=0.8)
            ax2.bar(x + width/2, epoch_val_losses, width, label='Val Loss', alpha=0.8)
            ax2.set_xlabel('Epoch', fontsize=12)
            ax2.set_ylabel('Loss', fontsize=12)
            ax2.set_title('Train vs Validation Loss per Epoch', fontsize=14, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(epochs_train)
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save:
            save_path = self.plots_dir / "loss_curves.png"
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Gráfico salvo: {save_path}")
            plt.close()
            return str(save_path)
        else:
            plt.show()
            return None

    def plot_memory_usage(self, save=True) -> Optional[str]:
        """
        Cria gráfico de uso de memória ao longo do tempo.

        Args:
            save: Se True, salva o gráfico

        Returns:
            Caminho do arquivo salvo (se save=True)
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️  matplotlib não disponível")
            return None

        metrics = self.load_metrics()
        if not metrics or not metrics.get('step_metrics'):
            return None

        step_metrics = metrics['step_metrics']

        # Extrai dados de memória
        memory_data = [(m['step'], m['memory_mb']) for m in step_metrics
                       if m['memory_mb'] is not None]

        if not memory_data:
            print("Nenhum dado de memória disponível")
            return None

        steps, memory_mb = zip(*memory_data)

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(steps, memory_mb, 'g-', linewidth=2, label='Available Memory')
        ax.fill_between(steps, memory_mb, alpha=0.3, color='green')

        # Adiciona linhas de threshold
        ax.axhline(y=1000, color='red', linestyle='--', linewidth=2, label='Critical (1GB)')
        ax.axhline(y=5000, color='orange', linestyle='--', linewidth=2, label='Warning (5GB)')

        ax.set_xlabel('Step', fontsize=12)
        ax.set_ylabel('Available Memory (MB)', fontsize=12)
        ax.set_title('Memory Usage During Training', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.tight_layout()

        if save:
            save_path = self.plots_dir / "memory_usage.png"
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Gráfico salvo: {save_path}")
            plt.close()
            return str(save_path)
        else:
            plt.show()
            return None

    def plot_learning_rate_schedule(self, learning_rates: List[float],
                                   save=True) -> Optional[str]:
        """
        Cria gráfico do schedule de learning rate.

        Args:
            learning_rates: Lista de learning rates por step
            save: Se True, salva o gráfico

        Returns:
            Caminho do arquivo salvo (se save=True)
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(learning_rates, 'purple', linewidth=2)
        ax.fill_between(range(len(learning_rates)), learning_rates, alpha=0.3, color='purple')
        ax.set_xlabel('Step', fontsize=12)
        ax.set_ylabel('Learning Rate', fontsize=12)
        ax.set_title('Learning Rate Schedule', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save:
            save_path = self.plots_dir / "learning_rate.png"
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Gráfico salvo: {save_path}")
            plt.close()
            return str(save_path)
        else:
            plt.show()
            return None

    def create_dashboard(self, save=True) -> Optional[str]:
        """
        Cria dashboard consolidado com todas as métricas.

        Args:
            save: Se True, salva o dashboard

        Returns:
            Caminho do arquivo salvo (se save=True)
        """
        if not MATPLOTLIB_AVAILABLE:
            print("⚠️  matplotlib não disponível")
            return None

        metrics = self.load_metrics()
        summary_file = self.output_dir / "training_summary.json"

        if not metrics:
            print("Nenhuma métrica disponível")
            return None

        summary = {}
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                summary = json.load(f)

        # Cria figura com 4 subgráficos
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        step_metrics = metrics.get('step_metrics', [])
        epoch_metrics = metrics.get('epoch_metrics', [])

        # 1. Loss ao longo dos steps
        ax1 = fig.add_subplot(gs[0, 0])
        if step_metrics:
            steps = [m['step'] for m in step_metrics if m['loss']]
            losses = [m['loss'] for m in step_metrics if m['loss']]
            ax1.plot(steps, losses, 'b-', linewidth=2)
            ax1.fill_between(steps, losses, alpha=0.3)
            ax1.set_title('Training Loss', fontweight='bold')
            ax1.set_xlabel('Step')
            ax1.set_ylabel('Loss')
            ax1.grid(True, alpha=0.3)

        # 2. Validation Loss
        ax2 = fig.add_subplot(gs[0, 1])
        if epoch_metrics:
            epochs = [m['epoch'] for m in epoch_metrics if m['val_loss']]
            val_losses = [m['val_loss'] for m in epoch_metrics if m['val_loss']]
            ax2.plot(epochs, val_losses, 'r-', marker='o', linewidth=2)
            ax2.set_title('Validation Loss', fontweight='bold')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Val Loss')
            ax2.grid(True, alpha=0.3)

        # 3. Memória
        ax3 = fig.add_subplot(gs[1, 0])
        memory_data = [(m['step'], m['memory_mb']) for m in step_metrics
                       if m['memory_mb'] is not None]
        if memory_data:
            steps, memory_mb = zip(*memory_data)
            ax3.plot(steps, memory_mb, 'g-', linewidth=2)
            ax3.axhline(y=1000, color='red', linestyle='--', linewidth=1)
            ax3.set_title('Memory Usage', fontweight='bold')
            ax3.set_xlabel('Step')
            ax3.set_ylabel('Available (MB)')
            ax3.grid(True, alpha=0.3)

        # 4. Resumo de texto (estatísticas)
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')

        summary_text = "TRAINING SUMMARY\n" + "="*30 + "\n"
        if summary:
            summary_text += f"Total Time: {summary.get('total_time_hours', 0):.2f}h\n"
            summary_text += f"Total Steps: {summary.get('total_steps', 0)}\n"
            summary_text += f"Total Epochs: {summary.get('total_epochs', 0)}\n"
            summary_text += f"Samples/sec: {summary.get('samples_per_second', 0):.2f}\n"
            summary_text += f"\nBest Loss: {summary.get('best_train_loss', 0):.4f}\n"
            summary_text += f"Final Loss: {summary.get('final_train_loss', 0):.4f}\n"
            if summary.get('loss_improvement_pct'):
                summary_text += f"Improvement: {summary['loss_improvement_pct']:.1f}%\n"

        ax4.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # 5. Loss Improvement ao longo de épocas
        ax5 = fig.add_subplot(gs[2, :])
        if step_metrics:
            epochs_list = sorted(set(m['epoch'] for m in step_metrics if m['loss']))
            epoch_losses = []
            for epoch in epochs_list:
                epoch_steps = [m['loss'] for m in step_metrics if m['epoch'] == epoch]
                if epoch_steps:
                    epoch_losses.append(np.mean(epoch_steps))

            ax5.bar(epochs_list, epoch_losses, color='steelblue', alpha=0.7, edgecolor='black')
            ax5.set_title('Average Loss per Epoch', fontweight='bold')
            ax5.set_xlabel('Epoch')
            ax5.set_ylabel('Average Loss')
            ax5.grid(True, alpha=0.3, axis='y')

        plt.suptitle('Training Dashboard', fontsize=16, fontweight='bold', y=0.995)

        if save:
            save_path = self.plots_dir / "dashboard.png"
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Dashboard salvo: {save_path}")
            plt.close()
            return str(save_path)
        else:
            plt.show()
            return None

    def print_training_report(self):
        """Imprime relatório de treinamento formatado"""
        summary_file = self.output_dir / "training_summary.json"

        if not summary_file.exists():
            print("Nenhum sumário de treinamento encontrado")
            return

        with open(summary_file, 'r') as f:
            summary = json.load(f)

        print("\n" + "="*70)
        print(" "*20 + "TRAINING REPORT")
        print("="*70)

        print(f"\n📊 TIMING")
        print(f"  Total Time: {summary.get('total_time_hours', 0):.2f} hours ({summary.get('total_time_seconds', 0):.0f}s)")
        print(f"  Samples/second: {summary.get('samples_per_second', 0):.2f}")

        print(f"\n📈 ITERATIONS")
        print(f"  Total Steps: {summary.get('total_steps', 0)}")
        print(f"  Total Epochs: {summary.get('total_epochs', 0)}")
        print(f"  Total Samples: {summary.get('total_samples_processed', 0)}")

        print(f"\n📉 LOSS METRICS")
        print(f"  Best Train Loss: {summary.get('best_train_loss', 0):.4f}")
        print(f"  Final Train Loss: {summary.get('final_train_loss', 0):.4f}")
        if summary.get('loss_improvement'):
            improvement = summary['loss_improvement']
            improvement_pct = summary.get('loss_improvement_pct', 0)
            print(f"  Loss Improvement: {improvement:.4f} ({improvement_pct:.1f}%)")

        if summary.get('best_val_loss'):
            print(f"  Best Val Loss: {summary['best_val_loss']:.4f}")
            print(f"  Final Val Loss: {summary.get('final_val_loss', 0):.4f}")

        print(f"\n🎯 BEST CHECKPOINT")
        best = summary.get('best_checkpoint', {})
        print(f"  Epoch: {best.get('epoch', 'N/A')}")
        print(f"  Step: {best.get('step', 'N/A')}")
        print(f"  Loss: {best.get('loss', 'N/A'):.4f}" if best.get('loss') else "  Loss: N/A")

        print(f"\n⚙️  CONFIGURATION")
        config = summary.get('training_config', {})
        for key, value in config.items():
            print(f"  {key}: {value}")

        print("\n" + "="*70 + "\n")
