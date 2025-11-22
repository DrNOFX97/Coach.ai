#!/usr/bin/env python3
# ============================================================================
# PROFESSIONAL VISUALIZATION - Generate Beautiful Matplotlib Plots
# ============================================================================
"""
Generate professional matplotlib visualizations for training metrics.

Usage:
    python3 scripts/visualization_professional.py

Output:
    - checkpoints_qlora/training_dashboard.png (2x2 grid)
    - checkpoints_qlora/training_detailed_analysis.png (3x2 grid)
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configure paths
CHECKPOINTS_DIR = Path("checkpoints_qlora")
metrics_file = CHECKPOINTS_DIR / "training_metrics.json"

def load_metrics():
    """Load training metrics from JSON"""
    if not metrics_file.exists():
        print(f"❌ Metrics file not found: {metrics_file}")
        return None

    with open(metrics_file) as f:
        metrics = json.load(f)

    return pd.DataFrame(metrics)

def setup_style():
    """Configure professional matplotlib style"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = '#f8f9fa'
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

def plot_dashboard(df):
    """
    Create main dashboard with 4 subplots:
    - Loss training vs validation with trend
    - Loss by epoch with error bars
    - Loss distribution with KDE
    - Cumulative improvement
    """
    print("\n📊 Gerando Dashboard Principal...\n")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('🚀 Training Dashboard - Análise Completa de Treino',
                  fontsize=18, fontweight='bold', y=0.995)

    # ========== Plot 1: Loss Training vs Validation ==========
    ax1 = axes[0, 0]
    ax1.plot(df['step'], df['loss'], 'o-', linewidth=2.5, markersize=4,
            color='#2E86AB', label='Training Loss', alpha=0.8)

    # Polynomial trend
    if len(df) > 3:
        z = np.polyfit(df['step'], df['loss'], 2)
        p = np.poly1d(z)
        ax1.plot(df['step'], p(df['step']), '--', linewidth=2.5,
                color='#A23B72', label='Tendência (Polynomial)', alpha=0.9)

    # Validation loss
    if 'val_loss' in df.columns:
        val_mask = df['val_loss'].notna()
        ax1.scatter(df[val_mask]['step'], df[val_mask]['val_loss'],
                   color='#F18F01', s=100, label='Validation Loss',
                   edgecolors='black', linewidth=1.5, zorder=5)

    ax1.set_xlabel('Step', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Loss', fontsize=12, fontweight='bold')
    ax1.set_title('📈 Loss Training vs Validation', fontsize=13, fontweight='bold', pad=10)
    ax1.legend(loc='upper right', fontsize=10, framealpha=0.95)
    ax1.grid(True, alpha=0.4, linestyle='--')
    ax1.set_facecolor('#ffffff')

    # ========== Plot 2: Loss by Epoch ==========
    ax2 = axes[0, 1]
    if 'epoch' in df.columns:
        epoch_loss = df.groupby('epoch')['loss'].agg(['mean', 'std', 'min', 'max'])
        epochs_list = epoch_loss.index.tolist()
        means = epoch_loss['mean'].values
        stds = epoch_loss['std'].values

        colors_epoch = ['#06A77D', '#2E86AB', '#A23B72']
        ax2.bar(epochs_list, means, yerr=stds, capsize=8,
               color=colors_epoch[:len(epochs_list)],
               edgecolor='black', linewidth=1.5, alpha=0.8,
               error_kw={'elinewidth': 2, 'capthick': 5})

        # Add values on bars
        for i, (epoch, mean) in enumerate(zip(epochs_list, means)):
            ax2.text(epoch, mean + stds[i] + 0.1, f'{mean:.3f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)

        ax2.set_xlabel('Época', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Loss Médio', fontsize=12, fontweight='bold')
        ax2.set_title('📊 Loss Médio por Época (com desvio padrão)',
                     fontsize=13, fontweight='bold', pad=10)
        ax2.set_xticks(epochs_list)
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax2.set_facecolor('#ffffff')

    # ========== Plot 3: Distribution with KDE ==========
    ax3 = axes[1, 0]
    ax3.hist(df['loss'], bins=35, color='#2E86AB', edgecolor='black',
            alpha=0.7, density=True, label='Distribuição')

    # KDE
    density = stats.gaussian_kde(df['loss'])
    xs = np.linspace(df['loss'].min(), df['loss'].max(), 200)
    ax3.plot(xs, density(xs), 'r-', linewidth=2.5, label='KDE')

    # Mean and median lines
    mean_loss = df['loss'].mean()
    median_loss = df['loss'].median()
    ax3.axvline(mean_loss, color='green', linestyle='--', linewidth=2.5,
               label=f'Média: {mean_loss:.4f}')
    ax3.axvline(median_loss, color='orange', linestyle='--', linewidth=2.5,
               label=f'Mediana: {median_loss:.4f}')

    ax3.set_xlabel('Loss', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Densidade', fontsize=12, fontweight='bold')
    ax3.set_title('📉 Distribuição de Loss (Histogram + KDE)',
                 fontsize=13, fontweight='bold', pad=10)
    ax3.legend(loc='upper right', fontsize=10, framealpha=0.95)
    ax3.set_facecolor('#ffffff')

    # ========== Plot 4: Cumulative Improvement ==========
    ax4 = axes[1, 1]
    cumulative_improvement = np.array([df['loss'].iloc[0] - loss for loss in df['loss']])

    ax4.fill_between(df['step'], cumulative_improvement, alpha=0.4,
                    color='#06A77D', label='Melhoria Cumulativa')
    ax4.plot(df['step'], cumulative_improvement, linewidth=2.5,
            color='#06A77D', marker='o', markersize=3, label='Loss Reduction')

    # Final value
    final_improvement = cumulative_improvement[-1]
    ax4.text(df['step'].iloc[-1], final_improvement,
            f' {final_improvement:.4f}',
            va='center', fontweight='bold', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

    ax4.set_xlabel('Step', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Melhoria Total de Loss', fontsize=12, fontweight='bold')
    ax4.set_title('📈 Progresso Cumulativo de Melhoria',
                 fontsize=13, fontweight='bold', pad=10)
    ax4.legend(loc='upper left', fontsize=10, framealpha=0.95)
    ax4.grid(True, alpha=0.4, linestyle='--')
    ax4.set_facecolor('#ffffff')

    plt.tight_layout()

    plot_path = CHECKPOINTS_DIR / 'training_dashboard.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.show()

    print(f"✅ Dashboard salvo em: {plot_path}\n")
    return plot_path

def plot_detailed_analysis(df):
    """
    Create detailed analysis with 6 subplots:
    - Loss by epoch (line plot)
    - Loss volatility (rolling std)
    - Improvement rate (derivative)
    - Cumulative loss by epoch
    - Learning curve (smoothed)
    - Box plot distribution
    """
    print("📊 Gerando Análise Detalhada...\n")

    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    fig.suptitle('🔬 Análise Detalhada - Métricas e Performance',
                  fontsize=18, fontweight='bold', y=0.995)

    # ========== Plot 1: Loss by Epoch ==========
    ax = axes[0, 0]
    if 'epoch' in df.columns:
        for epoch_num in sorted(df['epoch'].unique()):
            epoch_data = df[df['epoch'] == epoch_num]
            ax.plot(epoch_data['step'], epoch_data['loss'],
                   marker='o', markersize=4, linewidth=2,
                   label=f'Época {epoch_num + 1}', alpha=0.8)
    ax.set_xlabel('Step dentro da Época', fontsize=11, fontweight='bold')
    ax.set_ylabel('Loss', fontsize=11, fontweight='bold')
    ax.set_title('📍 Loss por Época (Detalhe)', fontsize=12, fontweight='bold', pad=10)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#ffffff')

    # ========== Plot 2: Volatility ==========
    ax = axes[0, 1]
    rolling_std = pd.Series(df['loss'].values).rolling(window=5, center=True).std()
    ax.fill_between(df['step'], rolling_std, alpha=0.5, color='#F18F01')
    ax.plot(df['step'], rolling_std, color='#F18F01', linewidth=2.5, label='Variação (Rolling Std)')
    ax.set_xlabel('Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('Desvio Padrão', fontsize=11, fontweight='bold')
    ax.set_title('⚡ Volatilidade de Loss (Rolling Window)', fontsize=12, fontweight='bold', pad=10)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#ffffff')

    # ========== Plot 3: Improvement Rate ==========
    ax = axes[1, 0]
    loss_derivative = -np.gradient(df['loss'].values)
    colors = ['green' if x > 0 else 'red' for x in loss_derivative]
    ax.bar(df['step'], loss_derivative, color=colors, alpha=0.7, edgecolor='black')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('Taxa de Melhoria', fontsize=11, fontweight='bold')
    ax.set_title('🚀 Taxa de Melhoria de Loss (Derivada)', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_facecolor('#ffffff')

    # ========== Plot 4: Cumulative Loss ==========
    ax = axes[1, 1]
    if 'epoch' in df.columns:
        epoch_cumsum = df.groupby('epoch')['loss'].sum().cumsum()
        ax.plot(epoch_cumsum.index + 1, epoch_cumsum.values,
               marker='o', markersize=10, linewidth=3, color='#2E86AB')
        ax.fill_between(epoch_cumsum.index + 1, epoch_cumsum.values, alpha=0.3, color='#2E86AB')
        for epoch, value in epoch_cumsum.items():
            ax.text(epoch + 1, value, f'{value:.1f}', ha='center',
                   va='bottom', fontweight='bold', fontsize=10)
    ax.set_xlabel('Época', fontsize=11, fontweight='bold')
    ax.set_ylabel('Loss Acumulado', fontsize=11, fontweight='bold')
    ax.set_title('📊 Loss Acumulado por Época', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#ffffff')

    # ========== Plot 5: Learning Curve ==========
    ax = axes[2, 0]
    moving_avg = pd.Series(df['loss'].values).rolling(window=10, center=True).mean()
    ax.plot(df['step'], df['loss'], 'o-', alpha=0.3, color='gray', markersize=3, label='Loss Raw')
    ax.plot(df['step'], moving_avg, linewidth=3, color='#A23B72', label='Moving Avg (window=10)')
    ax.set_xlabel('Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('Loss', fontsize=11, fontweight='bold')
    ax.set_title('📈 Learning Curve (com Smoothing)', fontsize=12, fontweight='bold', pad=10)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#ffffff')

    # ========== Plot 6: Box Plot ==========
    ax = axes[2, 1]
    if 'epoch' in df.columns:
        data_by_epoch = [df[df['epoch'] == e]['loss'].values for e in sorted(df['epoch'].unique())]
        bp = ax.boxplot(data_by_epoch, labels=[f'Época {i+1}' for i in range(len(data_by_epoch))],
                        patch_artist=True, widths=0.6)

        colors_box = ['#06A77D', '#2E86AB', '#A23B72']
        for patch, color in zip(bp['boxes'], colors_box[:len(bp['boxes'])]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        for whisker in bp['whiskers']:
            whisker.set(linewidth=1.5)
        for cap in bp['caps']:
            cap.set(linewidth=1.5)

    ax.set_ylabel('Loss', fontsize=11, fontweight='bold')
    ax.set_title('📦 Box Plot - Distribuição por Época', fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_facecolor('#ffffff')

    plt.tight_layout()

    plot_path = CHECKPOINTS_DIR / 'training_detailed_analysis.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.show()

    print(f"✅ Análise Detalhada salva em: {plot_path}\n")
    return plot_path

def print_statistics(df):
    """Print summary statistics"""
    print("\n" + "="*80)
    print("📊 ESTATÍSTICAS DESCRITIVAS")
    print("="*80)

    print(f"\n📈 Loss:")
    print(f"  Inicial:      {df['loss'].iloc[0]:.6f}")
    print(f"  Final:        {df['loss'].iloc[-1]:.6f}")
    print(f"  Mínimo:       {df['loss'].min():.6f}")
    print(f"  Máximo:       {df['loss'].max():.6f}")
    print(f"  Média:        {df['loss'].mean():.6f}")
    print(f"  Mediana:      {df['loss'].median():.6f}")
    print(f"  Desvio Pad:   {df['loss'].std():.6f}")

    improvement = df['loss'].iloc[0] - df['loss'].iloc[-1]
    improvement_pct = (improvement / df['loss'].iloc[0]) * 100
    print(f"\n✨ Melhoria:")
    print(f"  Redução:      {improvement:.6f}")
    print(f"  Percentual:   {improvement_pct:.2f}%")

    if 'val_loss' in df.columns and df['val_loss'].notna().any():
        val_losses = df[df['val_loss'].notna()]['val_loss']
        print(f"\n✅ Validation Loss:")
        print(f"  Mínimo:       {val_losses.min():.6f}")
        print(f"  Máximo:       {val_losses.max():.6f}")
        print(f"  Média:        {val_losses.mean():.6f}")
        print(f"  Desvio Pad:   {val_losses.std():.6f}")

        # Overfitting check
        final_train_loss = df['loss'].iloc[-1]
        final_val_loss = val_losses.iloc[-1]
        gap = final_val_loss - final_train_loss
        print(f"\n🔍 Análise de Overfitting:")
        print(f"  Train Loss Final:     {final_train_loss:.6f}")
        print(f"  Val Loss Final:       {final_val_loss:.6f}")
        print(f"  Gap (Val - Train):    {gap:.6f}")
        if gap < 0.1:
            print(f"  Status:               ✅ Excelente (Sem overfitting)")
        elif gap < 0.3:
            print(f"  Status:               ✅ Bom (Overfitting leve)")
        else:
            print(f"  Status:               ⚠️  Cuidado (Overfitting pronunciado)")

    print(f"\n" + "="*80)

def main():
    """Main function"""
    print("\n" + "="*80)
    print("🎨 PROFESSIONAL TRAINING VISUALIZATION")
    print("="*80 + "\n")

    # Setup
    setup_style()

    # Load metrics
    df = load_metrics()
    if df is None or len(df) == 0:
        print("❌ Sem métricas para visualizar. Execute o treino primeiro.")
        return

    print(f"✅ Carregadas {len(df)} métricas\n")

    # Generate plots
    plot1_path = plot_dashboard(df)
    plot2_path = plot_detailed_analysis(df)

    # Print statistics
    print_statistics(df)

    print("\n✅ Visualização Profissional Completa!")
    print(f"\n📁 Ficheiros gerados:")
    print(f"   - {plot1_path}")
    print(f"   - {plot2_path}")
    print(f"\n💡 Dica: Abra os ficheiros PNG para análise detalhada.\n")

if __name__ == "__main__":
    main()
