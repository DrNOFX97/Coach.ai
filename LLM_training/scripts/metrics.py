"""
Sistema de Rastreamento de Métricas para Treinamento MLX
Captura e persiste métricas em tempo real
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np


class MetricsTracker:
    """Rastreia métricas de treinamento e as persiste em CSV e JSON"""

    def __init__(self, output_dir: Path = None):
        """
        Inicializa o rastreador de métricas.

        Args:
            output_dir: Diretório para salvar métricas (default: checkpoints/)
        """
        if output_dir is None:
            output_dir = Path("checkpoints")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.csv_file = self.output_dir / "training_metrics.csv"
        self.json_file = self.output_dir / "training_metrics.json"
        self.summary_file = self.output_dir / "training_summary.json"

        # Métricas por step
        self.step_metrics: List[Dict] = []

        # Métricas por época
        self.epoch_metrics: List[Dict] = []

        # Melhor métrica encontrada
        self.best_loss = float('inf')
        self.best_epoch = -1
        self.best_step = -1

        # Configuração inicial
        self._initialize_csv()
        self._load_existing_metrics()

    def _initialize_csv(self):
        """Inicializa o arquivo CSV com headers"""
        if not self.csv_file.exists():
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'timestamp', 'epoch', 'step', 'phase', 'loss', 'val_loss',
                    'learning_rate', 'memory_mb', 'elapsed_time_s'
                ])
                writer.writeheader()

    def _load_existing_metrics(self):
        """Carrega métricas existentes do CSV"""
        if self.csv_file.exists():
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        if row['loss']:
                            loss = float(row['loss'])
                            if loss < self.best_loss:
                                self.best_loss = loss
                                self.best_epoch = int(row['epoch']) if row['epoch'] else -1
                                self.best_step = int(row['step']) if row['step'] else -1
                    except (ValueError, KeyError):
                        continue

    def log_step(self, epoch: int, step: int, loss: float,
                 val_loss: Optional[float] = None, learning_rate: float = 1e-5,
                 memory_mb: Optional[float] = None, elapsed_time: float = 0):
        """
        Registra métrica de um step de treinamento.

        Args:
            epoch: Número da época (0-indexed)
            step: Número do step dentro da época
            loss: Valor da loss
            val_loss: Loss de validação (opcional)
            learning_rate: Taxa de aprendizado atual
            memory_mb: Memória RAM disponível em MB
            elapsed_time: Tempo decorrido desde o início do treinamento
        """
        timestamp = datetime.now().isoformat()

        metric = {
            'timestamp': timestamp,
            'epoch': epoch,
            'step': step,
            'phase': 'train',
            'loss': loss,
            'val_loss': val_loss,
            'learning_rate': learning_rate,
            'memory_mb': memory_mb,
            'elapsed_time_s': elapsed_time
        }

        self.step_metrics.append(metric)

        # Atualiza melhor loss
        if loss < self.best_loss:
            self.best_loss = loss
            self.best_epoch = epoch
            self.best_step = step

        # Persiste no CSV
        self._append_to_csv(metric)

    def log_epoch(self, epoch: int, avg_loss: float, val_loss: Optional[float] = None,
                  learning_rate: float = 1e-5, elapsed_time: float = 0):
        """
        Registra métricas de fim de época.

        Args:
            epoch: Número da época
            avg_loss: Loss média da época
            val_loss: Loss de validação após a época
            learning_rate: Taxa de aprendizado
            elapsed_time: Tempo total decorrido
        """
        timestamp = datetime.now().isoformat()

        metric = {
            'timestamp': timestamp,
            'epoch': epoch,
            'step': None,
            'phase': 'epoch',
            'loss': avg_loss,
            'val_loss': val_loss,
            'learning_rate': learning_rate,
            'memory_mb': None,
            'elapsed_time_s': elapsed_time
        }

        self.epoch_metrics.append(metric)
        self._append_to_csv(metric)

    def _append_to_csv(self, metric: Dict):
        """Adiciona uma métrica ao CSV"""
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'epoch', 'step', 'phase', 'loss', 'val_loss',
                'learning_rate', 'memory_mb', 'elapsed_time_s'
            ])
            writer.writerow(metric)

    def save_json(self):
        """Salva todas as métricas em formato JSON"""
        data = {
            'step_metrics': self.step_metrics,
            'epoch_metrics': self.epoch_metrics,
            'best_loss': self.best_loss,
            'best_epoch': self.best_epoch,
            'best_step': self.best_step,
            'total_steps': len(self.step_metrics),
            'total_epochs': len(self.epoch_metrics)
        }

        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)

    def save_summary(self, total_time: float, total_samples: int,
                    training_config: Optional[Dict] = None):
        """
        Salva sumário final do treinamento.

        Args:
            total_time: Tempo total de treinamento em segundos
            total_samples: Número total de amostras processadas
            training_config: Configuração do treinamento
        """
        # Calcula estatísticas
        losses = [m['loss'] for m in self.step_metrics if m['loss'] is not None]
        val_losses = [m['val_loss'] for m in self.step_metrics + self.epoch_metrics
                      if m['val_loss'] is not None]

        summary = {
            'training_date': datetime.now().isoformat(),
            'total_time_seconds': total_time,
            'total_time_hours': round(total_time / 3600, 2),
            'total_steps': len(self.step_metrics),
            'total_epochs': len(self.epoch_metrics),
            'total_samples_processed': total_samples,
            'best_train_loss': min(losses) if losses else None,
            'final_train_loss': losses[-1] if losses else None,
            'best_val_loss': min(val_losses) if val_losses else None,
            'final_val_loss': val_losses[-1] if val_losses else None,
            'avg_loss_per_step': np.mean(losses) if losses else None,
            'loss_improvement': (losses[0] - losses[-1]) if losses and len(losses) > 1 else None,
            'loss_improvement_pct': ((losses[0] - losses[-1]) / losses[0] * 100)
                                   if losses and len(losses) > 1 and losses[0] > 0 else None,
            'samples_per_second': total_samples / total_time if total_time > 0 else 0,
            'best_checkpoint': {
                'epoch': self.best_epoch,
                'step': self.best_step,
                'loss': self.best_loss
            },
            'training_config': training_config or {}
        }

        with open(self.summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        return summary

    def get_current_status(self) -> Dict:
        """Retorna status atual do treinamento"""
        if not self.step_metrics:
            return {
                'status': 'not_started',
                'total_steps': 0,
                'best_loss': None
            }

        latest = self.step_metrics[-1]

        return {
            'status': 'running',
            'epoch': latest['epoch'],
            'step': latest['step'],
            'current_loss': latest['loss'],
            'best_loss': self.best_loss,
            'total_steps': len(self.step_metrics),
            'best_at': f"epoch {self.best_epoch}, step {self.best_step}"
        }

    def print_status(self):
        """Imprime status formatado"""
        status = self.get_current_status()
        print("\n" + "="*60)
        print("TRAINING STATUS")
        print("="*60)
        if status['status'] == 'not_started':
            print("Training not started yet")
        else:
            print(f"Epoch: {status['epoch']}")
            print(f"Step: {status['step']}")
            print(f"Current Loss: {status['current_loss']:.4f}")
            print(f"Best Loss: {status['best_loss']:.4f} ({status['best_at']})")
            print(f"Total Steps: {status['total_steps']}")
        print("="*60 + "\n")


class PerformanceMonitor:
    """Monitora performance do sistema durante treinamento"""

    def __init__(self):
        self.memory_readings = []
        self.min_memory = float('inf')
        self.max_memory = 0

    def record_memory(self, available_mb: float):
        """Registra leitura de memória"""
        self.memory_readings.append(available_mb)
        self.min_memory = min(self.min_memory, available_mb)
        self.max_memory = max(self.max_memory, available_mb)

    def get_stats(self) -> Dict:
        """Retorna estatísticas de performance"""
        if not self.memory_readings:
            return {}

        return {
            'min_memory_mb': self.min_memory,
            'max_memory_mb': self.max_memory,
            'avg_memory_mb': np.mean(self.memory_readings),
            'memory_readings_count': len(self.memory_readings)
        }
