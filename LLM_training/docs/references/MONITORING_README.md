# 🎯 Sistema de Monitorização - Quick Start

Seu novo sistema de monitorização em 3 passos simples!

## ⚡ Quick Start (5 minutos)

### 1️⃣ Usar o Notebook Pronto

```bash
jupyter notebook notebooks/mistral_qlora_training_monitored.ipynb
```

Este notebook já tem tudo integrado:
- ✅ Carregamento de dados
- ✅ Treinamento com LoRA
- ✅ Rastreamento automático de métricas
- ✅ Gráficos e dashboards ao final

### 2️⃣ Monitor em Tempo Real (Opcional)

Enquanto o notebook treina, abra outro terminal:

```bash
python scripts/monitor.py
```

Saída em tempo real:
- Epoch e step atual
- Loss atual vs melhor loss
- Memória disponível
- Tempo decorrido
- Estimativa de tempo restante

### 3️⃣ Gerar Relatórios Finais

Após treino completar:

```bash
python scripts/monitor.py --report
```

Gera automaticamente:
- 📊 Gráfico de loss
- 💾 Gráfico de memória
- 📈 Dashboard consolidado
- 📝 Relatório formatado

---

## 📦 O Que Você Tem

### Módulos Python

| Arquivo | Função |
|---------|--------|
| `scripts/metrics.py` | Rastreia todas as métricas (CSV + JSON) |
| `scripts/visualization.py` | Cria gráficos e dashboards |
| `scripts/monitor.py` | Monitor em tempo real |
| `scripts/test_monitoring.py` | Testa o sistema |

### Notebooks

| Arquivo | Descrição |
|---------|-----------|
| `notebooks/mistral_qlora_training_monitored.ipynb` | **RECOMENDADO**: Notebook completo com monitorização integrada |
| `notebooks/mistral_qlora_training_simple.ipynb` | Versão simples (sem monitorização) |

### Documentação

| Arquivo | Conteúdo |
|---------|----------|
| `MONITORING_GUIDE.md` | Guia detalhado com exemplos |
| `MONITORING_README.md` | Este ficheiro (quick start) |

---

## 📊 O Que Você Obtém

### Ficheiros de Métrica
```
checkpoints/
├── training_metrics.csv      ← Todas as métricas em CSV (Excel-compatible)
├── training_metrics.json     ← Dados estruturados
└── training_summary.json     ← Sumário com estatísticas
```

### Gráficos
```
checkpoints/plots/
├── loss_curves.png          ← Treino vs Validação
├── memory_usage.png         ← Consumo de memória
└── dashboard.png            ← Todas as métricas juntas
```

---

## 🚀 Exemplos de Uso

### Exemplo 1: Verificar Progresso

```bash
# Terminal 1: Treino em progresso
python scripts/train.py

# Terminal 2: Monitor
python scripts/monitor.py --refresh 5
```

Output:
```
📊 CURRENT STATUS
  Epoch: 2  |  Step: 450  |  Elapsed: 2.3h
  Current Loss: 1.2345  |  Best Loss: 0.9876
  Memory Available: 8500MB
```

### Exemplo 2: Integrar no Seu Código

```python
from scripts.metrics import MetricsTracker

tracker = MetricsTracker('checkpoints')

for epoch in range(num_epochs):
    for step, batch in enumerate(train_loader):
        # ... seu treinamento ...

        # Log a cada 50 steps
        if step % 50 == 0:
            tracker.log_step(
                epoch=epoch,
                step=step,
                loss=loss_value
            )

    # Log fim de época
    tracker.log_epoch(
        epoch=epoch,
        avg_loss=avg_loss
    )

# Sumário final
tracker.save_summary(
    total_time=elapsed_time,
    total_samples=len(dataset)
)
```

### Exemplo 3: Ler Métricas em Python

```python
import pandas as pd

# Ler como DataFrame
df = pd.read_csv('checkpoints/training_metrics.csv')
print(df.tail(10))  # Últimos 10 steps
print(f"Loss média: {df['loss'].mean()}")
```

### Exemplo 4: Gerar Gráficos Manualmente

```python
from scripts.visualization import TrainingVisualizer

viz = TrainingVisualizer('checkpoints')
viz.plot_loss_curves()
viz.plot_memory_usage()
viz.create_dashboard()
viz.print_training_report()
```

---

## ✅ Checklist - O Que Monitorizar

Durante o treinamento, verifique:

- [ ] **Loss diminuindo?** (principal indicador)
- [ ] **Checkpoints criados?** (a cada 200 steps)
- [ ] **Memória estável?** (não deve descer muito)
- [ ] **Sem erros no console?**
- [ ] **Velocidade razoável?** (5-10 samples/segundo)

Após o treinamento:

- [ ] **Gráficos gerados?**
- [ ] **Loss final melhor que inicial?** (>50% improvement)
- [ ] **Validação segue treino?** (não há overfitting)
- [ ] **Relatório completo?**

---

## 🧪 Testar o Sistema

Antes de usar com seu treinamento, teste:

```bash
python scripts/test_monitoring.py
```

Isto vai:
1. ✅ Simular um treinamento
2. ✅ Gerar métricas
3. ✅ Criar gráficos
4. ✅ Verificar todos os ficheiros

Se vê "✅ All tests passed!" - está pronto para usar!

---

## 🎨 Entender os Gráficos

### Loss Curves
- **Azul (Train)**: Deve descer consistentemente
- **Vermelho (Val)**: Deve seguir azul, sem estar muito acima
- **Melhor ponto**: Marcado com estrela vermelha

**Bom:** Loss desce regularmente
**Problemático:** Loss sobe ou fica constante

### Memory Usage
- **Verde (Available)**: Quantidade de RAM livre
- **Linha vermelha (crítica)**: 1GB (perigo!)
- **Linha laranja (aviso)**: 5GB

**Bom:** Memória estável em 8-10GB
**Problemático:** Memória descendo progressivamente

### Dashboard
Consolidação de:
- Gráfico de loss por step
- Loss de validação
- Consumo de memória
- Estatísticas resumidas

---

## ⚙️ Configuração

### Valores Padrão (no notebook)

```python
config = {
    "num_epochs": 3,              # Épocas de treino
    "batch_size": 1,              # Batch size
    "learning_rate": 1e-5,        # Taxa de aprendizado
    "gradient_accumulation": 4,   # Acumulação de gradientes
    "max_seq_length": 256,        # Comprimento máximo
    "logging_steps": 50,          # Log a cada N steps
    "save_steps": 200,            # Checkpoint a cada N steps
}
```

### Optimizar para Velocidade

```python
# Aumentar batch_size (se houver memória)
"batch_size": 2

# Diminuir max_seq_length
"max_seq_length": 128

# Aumentar gradient_accumulation (economiza memória)
"gradient_accumulation": 8
```

### Optimizar para Qualidade

```python
# Mais épocas
"num_epochs": 5

# Learning rate menor (mais cuidado)
"learning_rate": 5e-6

# Mais steps de avaliação
"save_steps": 100
```

---

## 📖 Recursos Adicionais

- 📚 **Guia Completo**: Ver `MONITORING_GUIDE.md`
- 🧪 **Ver Exemplo**: Executar `python scripts/test_monitoring.py`
- 💬 **Ajuda**: Ver comentários no código
- 🎓 **Aprender MLX**: https://ml-explore.github.io/mlx/build/html/index.html

---

## 🐛 Problemas Comuns

### "matplotlib não encontrado"
```bash
pip install matplotlib
```

### "Nenhuma métrica registada"
1. Verificar se checkpoint_dir existe
2. Confirmar que treinamento começou
3. Ver se há erros no notebook

### "Loss não melhora"
- Aumentar learning rate para 1e-4
- Ou diminuir para 1e-6
- Verificar qualidade dos dados

### "Memoria cheia"
- Aumentar gradient_accumulation_steps para 8
- Diminuir batch_size para 1
- Diminuir max_seq_length para 128

---

## 📞 Próximos Passos

1. **Testar o sistema**: `python scripts/test_monitoring.py`
2. **Abrir notebook**: `jupyter notebook`
3. **Abrir `mistral_qlora_training_monitored.ipynb`**
4. **Executar célula por célula** e verificar output
5. **Monitorar em tempo real**: `python scripts/monitor.py`
6. **Analisar resultados**: `python scripts/monitor.py --report`

---

## 🎉 Bom Treinamento!

Seu sistema de monitorização está pronto. A partir de agora, você terá visibilidade completa do seu treinamento com:

✅ Métricas em tempo real
✅ Gráficos automáticos
✅ Relatórios detalhados
✅ Recuperação de crashes

Boa sorte! 🚀
