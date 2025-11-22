# Sistema de Monitorização de Treinamento

Guia completo para monitorizar o seu treinamento com métricas, gráficos e dashboard em tempo real.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Componentes do Sistema](#componentes-do-sistema)
3. [Como Usar](#como-usar)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Interpretando Resultados](#interpretando-resultados)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O sistema de monitorização fornece:

| Componente | Descrição | Output |
|---|---|---|
| **MetricsTracker** | Captura todas as métricas de treinamento | CSV + JSON |
| **PerformanceMonitor** | Rastreia uso de memória | Stats integradas |
| **TrainingVisualizer** | Cria gráficos e dashboards | PNG + Relatórios |
| **Monitor CLI** | Monitor em tempo real no terminal | Live updates |

---

## 🔧 Componentes do Sistema

### 1. MetricsTracker (`scripts/metrics.py`)

Rastreia e persiste todas as métricas durante o treinamento.

**Funções principais:**

```python
tracker = MetricsTracker(output_dir='checkpoints')

# Log de cada step
tracker.log_step(
    epoch=0,
    step=100,
    loss=2.345,
    val_loss=2.456,
    learning_rate=1e-5,
    memory_mb=9000,
    elapsed_time=120
)

# Log de fim de época
tracker.log_epoch(
    epoch=0,
    avg_loss=2.345,
    val_loss=2.456,
    elapsed_time=3600
)

# Salvar sumário final
tracker.save_summary(
    total_time=7200,
    total_samples=2414,
    training_config={'lr': 1e-5}
)

# Ver status
tracker.print_status()
```

**Output:**
- `training_metrics.csv` - Todas as métricas por linha
- `training_metrics.json` - Dados estruturados
- `training_summary.json` - Sumário final com estatísticas

### 2. PerformanceMonitor

Monitora performance do sistema:

```python
monitor = PerformanceMonitor()
monitor.record_memory(available_mb=9500)
stats = monitor.get_stats()
```

### 3. TrainingVisualizer (`scripts/visualization.py`)

Cria visualizações dos dados:

```python
viz = TrainingVisualizer(output_dir='checkpoints')

# Gráfico de loss
viz.plot_loss_curves(save=True)

# Uso de memória
viz.plot_memory_usage(save=True)

# Dashboard completo
viz.create_dashboard(save=True)

# Relatório formatado
viz.print_training_report()
```

**Output:**
- `checkpoints/plots/loss_curves.png` - Curva de loss treino vs validação
- `checkpoints/plots/memory_usage.png` - Gráfico de memória
- `checkpoints/plots/dashboard.png` - Dashboard consolidado

### 4. Monitor CLI (`scripts/monitor.py`)

Monitor em tempo real:

```bash
# Monitor contínuo
python scripts/monitor.py

# Monitor com intervalo customizado
python scripts/monitor.py --refresh 10

# Gerar relatório final
python scripts/monitor.py --report

# Monitor diretório específico
python scripts/monitor.py --output-dir ./my_checkpoints
```

---

## 📖 Como Usar

### Opção 1: Usar o Notebook Monitorizado

**Arquivo:** `notebooks/mistral_qlora_training_monitored.ipynb`

1. Abrir no Jupyter
2. Executar células sequencialmente
3. Monitorização automática integrada
4. Gráficos e relatórios ao final

### Opção 2: Integrar no Seu Código Atual

No seu script de treinamento:

```python
from scripts.metrics import MetricsTracker, PerformanceMonitor

# Inicializar
tracker = MetricsTracker('checkpoints')
monitor = PerformanceMonitor()

# Durante treinamento
for epoch in range(num_epochs):
    for step, batch in enumerate(train_loader):
        # ... seu código de treinamento ...

        # Log a cada N steps
        if step % 50 == 0:
            tracker.log_step(
                epoch=epoch,
                step=step,
                loss=loss_value,
                memory_mb=get_available_memory(),
                elapsed_time=time.time() - start_time
            )

    # Log ao fim da época
    tracker.log_epoch(
        epoch=epoch,
        avg_loss=avg_loss,
        val_loss=val_loss_value,
        elapsed_time=time.time() - start_time
    )

    # Salvar checkpoint de métricas
    tracker.save_json()

# Final
summary = tracker.save_summary(
    total_time=time.time() - start_time,
    total_samples=len(dataset),
    training_config=config
)
```

### Opção 3: Monitorar Treinamento Existente

Enquanto o notebook está a correr em outro terminal:

```bash
# Terminal 1: Executar treinamento
jupyter notebook

# Terminal 2: Monitorar em tempo real
python scripts/monitor.py

# Terminal 3: Gerar relatório final
python scripts/monitor.py --report
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Verificar Progresso Atual

```bash
# Num terminal diferente
python scripts/monitor.py --refresh 5
```

Output:
```
╔════════════════════════════════════════════════════════════════════════════╗
║                    TRAINING MONITOR - 2025-11-09 14:30:45                 ║
╚════════════════════════════════════════════════════════════════════════════╝

📊 CURRENT STATUS
────────────────────────────────────────────────────────────────────────────
  Epoch: 2  |  Step: 450  |  Elapsed: 2.3h
  Current Loss: 1.2345  |  Best Loss: 0.9876
  Memory Available: 8500MB

📈 LOSS STATISTICS
────────────────────────────────────────────────────────────────────────────
  Steps with data: 450
  Loss range: 0.9876 - 4.5678
  Improvement: 3.2345 (+65.3%)

🎯 VALIDATION
────────────────────────────────────────────────────────────────────────────
  Best Val Loss: 1.0234
  Latest Val Loss: 1.0456

🏆 BEST CHECKPOINT
────────────────────────────────────────────────────────────────────────────
  Epoch: 1
  Step: 250
  Loss: 0.9876
```

### Exemplo 2: Gerar Gráficos ao Final

```python
from scripts.visualization import TrainingVisualizer

viz = TrainingVisualizer('checkpoints')
viz.plot_loss_curves(save=True)
viz.plot_memory_usage(save=True)
viz.create_dashboard(save=True)
viz.print_training_report()
```

Output:
```
======================================================================
                     TRAINING REPORT
======================================================================

📊 TIMING
  Total Time: 2.35 hours (8460s)
  Samples/second: 285.24

📈 ITERATIONS
  Total Steps: 2414
  Total Epochs: 3
  Total Samples: 2414

📉 LOSS METRICS
  Best Train Loss: 0.9876
  Final Train Loss: 1.0234
  Loss Improvement: 3.2345 (65.3%)
  Best Val Loss: 0.9654
  Final Val Loss: 1.0456

🎯 BEST CHECKPOINT
  Epoch: 1
  Step: 250
  Loss: 0.9876

⚙️  CONFIGURATION
  num_epochs: 3
  batch_size: 1
  learning_rate: 0.00001
  max_seq_length: 256
```

### Exemplo 3: Ler Métricas Programaticamente

```python
import json

# Ler CSV
import pandas as pd
df = pd.read_csv('checkpoints/training_metrics.csv')
print(df.tail())

# Ler JSON
with open('checkpoints/training_metrics.json') as f:
    metrics = json.load(f)

# Acessar dados
best_loss = metrics['best_loss']
total_steps = metrics['total_steps']
step_metrics = metrics['step_metrics']

# Análise
print(f"Best loss: {best_loss}")
print(f"Total steps: {total_steps}")
print(f"Loss history: {[m['loss'] for m in step_metrics[-10:]]}")
```

---

## 📊 Interpretando Resultados

### Loss Curves

```
Comportamento Esperado:
- Loss diminui ao longo dos steps (treino aprendendo)
- Validação segue similar ao treino
- Ambas convergem gradualmente

Problemas Comuns:
- Loss constante → Taxa de aprendizado muito baixa
- Loss sobe → Taxa de aprendizado muito alta
- Val loss sobe, train desce → Overfitting
- Picos aleatórios → Dados problemáticos
```

### Memory Usage

```
Esperado:
- Memória estável durante treino
- Pequenas variações normais
- Nunca deve cair abaixo de 1GB

Problemas:
- Memória diminuindo → Memory leak
- Crash em memória → Aumentar gradient accumulation
- Variações grandes → Problemas de batch size
```

### Métricas Chave

| Métrica | Valor Bom | Valor Problemático |
|---------|-----------|-------------------|
| Loss Improvement | >50% | <10% |
| Validation vs Train | Similar | Val >> Train (overfitting) |
| Samples/second | >100 | <50 (lento) |
| Memory Stable | Sim | Trending down |

---

## 🔍 Troubleshooting

### Problema: Nenhuma métrica registada

**Solução:**
1. Verificar se `checkpoints/` existe
2. Confirmar que o treinamento começou
3. Ver se há erros no notebook

```bash
ls -la checkpoints/
cat checkpoints/training_metrics.csv
```

### Problema: Gráficos não aparecem

**Solução:**
1. Instalar matplotlib
2. Usar `%matplotlib inline` no Jupyter

```bash
pip install matplotlib
```

No notebook:
```python
%matplotlib inline
```

### Problema: Memory leak aparente

**Solução:**
1. Adicionar `gc.collect()` no loop
2. Aumentar `gradient_accumulation_steps`
3. Diminuir batch size

### Problema: Loss não melhora

**Possíveis causas:**
- Learning rate muito alto (loss salta)
- Learning rate muito baixo (loss estagnada)
- Dados de qualidade inferior
- Modelo já convergiu

**Soluções:**
- Tente learning rate = 1e-4 ou 1e-6
- Verificar qualidade dos dados
- Aumentar número de épocas

---

## 📁 Estrutura de Ficheiros

```
checkpoints/
├── training_metrics.csv          ← Todas as métricas em CSV
├── training_metrics.json         ← Métricas em JSON
├── training_summary.json         ← Sumário final
└── plots/
    ├── loss_curves.png          ← Gráfico de loss
    ├── memory_usage.png         ← Gráfico de memória
    └── dashboard.png            ← Dashboard completo
```

---

## 🚀 Quick Start

**3 passos para começar:**

1. **Abrir notebook monitorizado:**
   ```bash
   jupyter notebook notebooks/mistral_qlora_training_monitored.ipynb
   ```

2. **Em outro terminal, monitorar:**
   ```bash
   python scripts/monitor.py --refresh 5
   ```

3. **Ao final, gerar relatórios:**
   ```bash
   python scripts/monitor.py --report
   ```

---

## 📞 Perguntas Frequentes

**P: Como saber se o treinamento está funcionando?**
R: Veja se a loss está a descer consistentemente e os checkpoints estão a ser criados.

**P: Quanto tempo leva o treinamento?**
R: Estimado no monitor, tipicamente 2-3 horas para 3 épocas num Mac M1.

**P: Posso parar e retomar?**
R: Sim! O sistema salva checkpoints e pode retomar de onde parou.

**P: Como optimizar a velocidade?**
R: Aumentar `gradient_accumulation_steps` ou reduzir `max_seq_length`.

---

## 📝 Resumo de Comandos

```bash
# Monitorar em tempo real
python scripts/monitor.py

# Gerar gráficos finais
python scripts/monitor.py --report

# Ler CSV com pandas
python -c "import pandas as pd; print(pd.read_csv('checkpoints/training_metrics.csv').tail())"

# Ver resumo JSON
cat checkpoints/training_summary.json | jq '.'

# Ver status
python -c "from scripts.metrics import MetricsTracker; MetricsTracker('checkpoints').print_status()"
```

---

Boa sorte com o seu treinamento! 🚀
