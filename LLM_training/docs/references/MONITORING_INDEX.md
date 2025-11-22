# 📚 Índice de Monitorização - Guia de Navegação

## 🎯 Comece Aqui

Você tem 3 ficheiros principais para ler, dependendo do seu objetivo:

### ⚡ Apenas 5 Minutos? Leia Isto:
📄 **[MONITORING_SUMMARY.txt](MONITORING_SUMMARY.txt)**
- Visão geral completa em formato de texto
- Checklist pré-treinamento
- Troubleshooting rápido
- Exemplos de comando

### 🚀 Quer Começar Já? Leia Isto:
📖 **[MONITORING_README.md](MONITORING_README.md)**
- Quick start em 3 passos
- Exemplos práticos
- Comandos essenciais
- Próximos passos claros

### 📚 Quer Entender Tudo? Leia Isto:
📘 **[MONITORING_GUIDE.md](MONITORING_GUIDE.md)**
- Guia completo e detalhado
- Todos os componentes explicados
- Exemplos avançados
- Troubleshooting detalhado
- Interpretação de resultados

---

## 📊 Estrutura de Ficheiros

```
LLM_training/
│
├─ 📚 DOCUMENTAÇÃO (LEIA PRIMEIRO)
│  ├─ MONITORING_INDEX.md          ← Você está aqui
│  ├─ MONITORING_SUMMARY.txt       ← Resumo (5 min)
│  ├─ MONITORING_README.md         ← Quick start (15 min)
│  ├─ MONITORING_GUIDE.md          ← Guia completo (30 min)
│  └─ SETUP_MONITORING.md          ← Detalhes de setup (10 min)
│
├─ 🐍 MÓDULOS PYTHON (scripts/)
│  ├─ metrics.py                   ← Rastreador de métricas
│  ├─ visualization.py             ← Gráficos e dashboards
│  ├─ monitor.py                   ← Monitor em tempo real
│  ├─ test_monitoring.py           ← Teste do sistema
│  └─ train_with_monitoring.py     ← Exemplo de integração
│
├─ 📓 NOTEBOOKS (notebooks/)
│  └─ mistral_qlora_training_monitored.ipynb  ← Treinamento com monitoring
│
└─ 📊 OUTPUT (gerado durante treino)
   └─ checkpoints/
      ├─ training_metrics.csv       ← Métricas em CSV
      ├─ training_metrics.json      ← Métricas em JSON
      ├─ training_summary.json      ← Sumário
      └─ plots/
         ├─ loss_curves.png
         ├─ memory_usage.png
         └─ dashboard.png
```

---

## 🗺️ Mapa de Decisão

```
┌─ Qual é o seu objetivo?
│
├─ "Apenas quero começar logo!"
│  └─→ MONITORING_README.md (15 min)
│      └─→ Abra: mistral_qlora_training_monitored.ipynb
│
├─ "Quero entender como funciona"
│  └─→ MONITORING_GUIDE.md (30 min)
│      └─→ SETUP_MONITORING.md (10 min)
│
├─ "Tenho 5 minutos, querme resumo"
│  └─→ MONITORING_SUMMARY.txt (5 min)
│
├─ "Quero integrar no meu código"
│  └─→ MONITORING_GUIDE.md → Seção "Opção 2"
│      └─→ Ver: scripts/train_with_monitoring.py
│
├─ "Algo está errado"
│  └─→ MONITORING_GUIDE.md → Seção "Troubleshooting"
│      └─→ MONITORING_SUMMARY.txt → Seção "❓ TROUBLESHOOTING"
│
└─ "Preciso de exemplos"
   └─→ MONITORING_README.md → Seção "Exemplos Práticos"
       └─→ scripts/train_with_monitoring.py
```

---

## 📖 Conteúdo de Cada Ficheiro

### MONITORING_SUMMARY.txt (5 min)
```
✓ Resumo visual do sistema
✓ O que foi criado
✓ Quick start em 3 passos
✓ Principais funcionalidades
✓ Resultados de testes
✓ Exemplos de uso
✓ Checklist pré-treinamento
✓ Troubleshooting rápido
```

### MONITORING_README.md (15 min)
```
✓ Quick start
✓ O que você tem
✓ Exemplos de uso
✓ Integrar no seu código
✓ Ler métricas em Python
✓ Gerar gráficos manualmente
✓ Entender os gráficos
✓ Configuração
✓ Próximos passos
```

### MONITORING_GUIDE.md (30 min)
```
✓ Visão geral completa
✓ Componentes do sistema (detalhado)
✓ Como usar (3 opções)
✓ Exemplos práticos
✓ Interpretando resultados
✓ FAQ (perguntas frequentes)
✓ Resumo de comandos
✓ Troubleshooting detalhado
```

### SETUP_MONITORING.md (10 min)
```
✓ Checklist pré-treinamento
✓ Durante o treinamento
✓ Depois do treinamento
✓ Confirmação de setup
✓ Notas importantes
✓ Resources adicionais
```

---

## 🚀 Sequência Recomendada (15 minutos total)

```
1. MONITORING_README.md (ler)              5 min
   └─ Entender o conceito

2. python scripts/test_monitoring.py       2 min
   └─ Confirmar que funciona

3. MONITORING_SUMMARY.txt (revisar)        3 min
   └─ Ver checklist

4. jupyter notebook (abrir)                5 min
   └─ Selecionar mistral_qlora_training_monitored.ipynb

5. Começar treino!
```

---

## 🎯 Casos de Uso Específicos

### Caso 1: "Quero começar agora, sem ler muito"
```
1. python scripts/test_monitoring.py       ← confirmar funciona
2. jupyter notebook                        ← abrir
3. mistral_qlora_training_monitored.ipynb ← treinar
```

### Caso 2: "Tenho um script de treino existente"
```
1. MONITORING_GUIDE.md → "Opção 2"        ← entender integração
2. Copiar código exemplo de integration   ← adaptar ao seu
3. scripts/train_with_monitoring.py       ← referência
```

### Caso 3: "Quero monitorar um treino já em progresso"
```
1. python scripts/monitor.py --refresh 5  ← monitor em tempo real
2. Verificar loss, memória, time estimate ← acompanhar
3. Depois: python scripts/monitor.py --report ← relatório final
```

### Caso 4: "Algo deu errado, preciso de ajuda"
```
1. MONITORING_SUMMARY.txt → "❓ TROUBLESHOOTING"  ← solução rápida
2. MONITORING_GUIDE.md → "Troubleshooting"       ← análise detalhada
3. Verificar console, logs, ficheiros metrics     ← debug
```

### Caso 5: "Quero ler métricas em Python"
```
1. MONITORING_README.md → "Exemplo 3"     ← template
2. import pandas as pd                     ← usar
3. df = pd.read_csv('checkpoints/training_metrics.csv')
```

---

## 📊 Ficheiros Gerados Durante Treino

Após treino, você terá:

```
checkpoints/
├─ training_metrics.csv                   ← Pode abrir no Excel
├─ training_metrics.json                  ← Ler com Python
├─ training_summary.json                  ← Estatísticas finais
└─ plots/
   ├─ loss_curves.png                    ← Gráfico de loss
   ├─ memory_usage.png                   ← Gráfico de memória
   └─ dashboard.png                      ← Dashboard consolidado
```

---

## ⌨️ Comandos Principais

```bash
# Testar sistema
python scripts/test_monitoring.py

# Monitor em tempo real
python scripts/monitor.py
python scripts/monitor.py --refresh 10

# Gerar relatórios finais
python scripts/monitor.py --report

# Ver métricas em CSV
cat checkpoints/training_metrics.csv | head -20

# Ver sumário
cat checkpoints/training_summary.json | jq '.'

# Abrir notebook
jupyter notebook notebooks/mistral_qlora_training_monitored.ipynb
```

---

## 🧩 Módulos Python

```python
# MetricsTracker - Rastrear métricas
from scripts.metrics import MetricsTracker
tracker = MetricsTracker('checkpoints')
tracker.log_step(epoch=0, step=100, loss=2.345)

# PerformanceMonitor - Monitorar memória
from scripts.metrics import PerformanceMonitor
monitor = PerformanceMonitor()
monitor.record_memory(9000)

# TrainingVisualizer - Gerar gráficos
from scripts.visualization import TrainingVisualizer
viz = TrainingVisualizer('checkpoints')
viz.plot_loss_curves()
viz.create_dashboard()
```

---

## ✅ Checklist Rápido

### Antes de Começar
- [ ] Leia MONITORING_README.md (15 min)
- [ ] Execute `python scripts/test_monitoring.py`
- [ ] Veja gráficos em `checkpoints/plots/`
- [ ] Abra o notebook

### Durante Treinamento
- [ ] Monitor loss descendo
- [ ] Checkpoints criados (a cada 200 steps)
- [ ] Memória estável (7-9GB)
- [ ] Usar `python scripts/monitor.py` para live updates

### Depois do Treinamento
- [ ] Execute `python scripts/monitor.py --report`
- [ ] Revise os gráficos em `checkpoints/plots/`
- [ ] Leia o sumário em `checkpoints/training_summary.json`
- [ ] Analise improvement % (deve ser >50%)

---

## 🎓 Aprender Mais

### Dentro deste Projeto
- 📖 MONITORING_GUIDE.md - Guia completo
- 🐍 scripts/train_with_monitoring.py - Exemplo prático
- 📓 notebooks/mistral_qlora_training_monitored.ipynb - Treinamento real

### Biblioteca MLX
- [Documentação MLX](https://ml-explore.github.io/mlx/)
- [MLX Examples](https://github.com/ml-explore/mlx-examples)

### Outras Ferramentas
- Pandas - Análise de dados
- Matplotlib - Visualização
- Jupyter - Notebooks interativos

---

## 🎯 Próximo Passo

Dependendo do tempo que tem:

⏱️ **5 minutos?**
→ Leia: MONITORING_SUMMARY.txt

🚀 **15 minutos?**
→ Leia: MONITORING_README.md
→ Execute: python scripts/test_monitoring.py

📚 **30 minutos?**
→ Leia: MONITORING_README.md + MONITORING_GUIDE.md
→ Explore: scripts/train_with_monitoring.py

---

## 💬 Perguntas Frequentes

**P: Por onde começar?**
R: MONITORING_README.md (15 min)

**P: Quero usar já, sem ler?**
R: `jupyter notebook` → Abra mistral_qlora_training_monitored.ipynb

**P: Como integrar no meu código?**
R: MONITORING_GUIDE.md → Seção "Opção 2"

**P: Algo quebrou!**
R: MONITORING_SUMMARY.txt → Seção "❓ TROUBLESHOOTING"

**P: Como ler os gráficos?**
R: MONITORING_README.md → Seção "Entender os Gráficos"

---

**Status**: ✅ Sistema pronto para usar
**Data**: 9 de Novembro de 2025
**Localização**: `/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/`

---

Bom treinamento! 🚀
