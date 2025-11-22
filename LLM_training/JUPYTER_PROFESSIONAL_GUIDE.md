# 📓 Jupyter Lab Professional Training Guide

## 🎯 Visão Geral

Este guia descreve como usar o **notebook profissional** (`mistral_qlora_professional.ipynb`) para treinar um modelo Mistral-7B com QLoRA em Jupyter Lab de forma segura e com seleção automática de configurações.

---

## 📁 Ficheiros Principais Criados

### 1. **`notebooks/mistral_qlora_professional.ipynb`** ⭐ PRINCIPAL
   - **Tipo:** Jupyter Notebook
   - **Tamanho:** ~100KB
   - **Duração:** 2-3 horas (treino completo)
   - **Estrutura:** 10 células temáticas

### 2. **`scripts/visualization_professional.py`** 📊
   - **Tipo:** Script Python standalone
   - **Função:** Gera gráficos matplotlib profissionais
   - **Uso:** `python3 scripts/visualization_professional.py`
   - **Output:**
     - `checkpoints_qlora/training_dashboard.png` (4 gráficos principais)
     - `checkpoints_qlora/training_detailed_analysis.png` (6 gráficos detalhados)

---

## 🚀 Como Usar o Notebook

### Pré-requisitos
```bash
# Instale as dependências
pip install jupyter-lab matplotlib seaborn pandas numpy scipy

# Verifique MLX
python3 -c "import mlx.core as mx; print(mx.default_device())"
```

### Abrir o Notebook
```bash
cd /Users/f.nuno/Desktop/chatbot_2.0/LLM_training

# Opção 1: Jupyter Lab
jupyter lab notebooks/mistral_qlora_professional.ipynb

# Opção 2: Jupyter Notebook
jupyter notebook notebooks/mistral_qlora_professional.ipynb
```

---

## 📋 Estrutura das Células (10 Blocos)

### **[SETUP] 1️⃣ Importações e Configurações Iniciais**

```
O que faz:
✅ Importa bibliotecas (MLX, pandas, matplotlib, etc)
✅ Configura variáveis globais (diretórios)
✅ Define funções utilitárias
✅ Suprime avisos

Tempo: ~2 segundos
Pode correr isoladamente: ✅ SIM
```

**Executar primeiro!** Todas as outras células dependem disto.

---

### **[SYSTEM CHECK] 2️⃣ Diagnóstico do Hardware**

```
O que faz:
✅ Verifica Python, MLX, transformers
✅ Detecta GPU/Metal disponível
✅ Mede RAM e espaço em disco
✅ Valida arquivos de dados
✅ Verifica modelo base

Saída:
📊 Relatório completo do sistema
⚠️  Avisos se algo faltar

Tempo: ~3-5 segundos
Pode correr isoladamente: ✅ SIM
```

**Informações que mostra:**
- Python version
- MLX version + GPU Metal disponível
- RAM total e disponível
- Disco livre (GB)
- Ficheiros de dados válidos
- Modelo base presente

---

### **[RECOMMENDATIONS] 2.5️⃣ Recomendação Automática de Config**

```
O que faz:
✅ Analisa RAM disponível
✅ Detecta presença de GPU
✅ Recomenda 3 níveis de configuração:
   1. SAFE       - Mínimo seguro (sem crash)
   2. BALANCED   - Recomendado (maioria dos casos)
   3. PERFORMANCE - Para hardware superior

Tempo: ~1 segundo
Pode correr isoladamente: ✅ SIM
```

**Configurações Recomendadas:**

| Config | batch_size | learning_rate | Situação |
|--------|-----------|---|----------|
| SAFE | 1 | 0.0001 | RAM <6GB ou teste |
| BALANCED | 2 | 0.0002 | RAM 8-10GB ⭐ |
| PERFORMANCE | 4 | 0.0003 | RAM >12GB + GPU |

---

### **[CONFIG WIZARD] 3️⃣ Seleção Interativa**

```
O que faz:
✅ Oferece menu interativo (escolher 1-4)
✅ Permite customização manual
✅ Valida valores
✅ Salva configuração em JSON

Tempo: ~5-10 segundos (interativo)
Pode correr isoladamente: ✅ SIM

Opções:
1 = Use SAFE config
2 = Use BALANCED config (recomendado)
3 = Use PERFORMANCE config
4 = Customize manualmente cada parâmetro
```

**Customização Manual (Opção 4):**
- batch_size
- gradient_accumulation
- max_seq_length
- learning_rate
- num_epochs

---

### **[DATA PREP] 4️⃣ Validação de Dados**

```
O que faz:
✅ Valida formato JSONL
✅ Verifica campos obrigatórios (prompt, completion)
✅ Conta exemplos em train/valid
✅ Detecta problemas (JSON inválido, campos vazios)
✅ Mostra estatísticas

Tempo: ~5 segundos
Pode correr isoladamente: ✅ SIM

Requerimentos:
- data/train.jsonl
- data/valid.jsonl
```

**Output esperado:**
```
✅ train.jsonl - 850 exemplos válidos
✅ valid.jsonl - 95 exemplos válidos
```

---

### **[MODEL SETUP] 5️⃣ Carregamento do Modelo**

```
O que faz:
✅ Carrega tokenizador (Mistral-7B)
✅ Localiza modelo base quantizado (4-bit)
✅ Configura LoRA adapters
✅ Prepara para treino

Tempo: ~2-3 minutos
Pode correr isoladamente: ✅ SIM

Requerimentos:
- models/mistral-7b-4bit/model.safetensors (3.8GB)
```

**Configuração LoRA:**
- Rank: 8
- Alpha: 16
- Target modules: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- Dropout: 0.0

---

### **[TRAINING] 6️⃣ Loop de Treino**

```
O que faz:
✅ Treino principal (forward → loss → backward → update)
✅ Salva checkpoints a cada N steps
✅ Avalia em dados de validação
✅ Registra métricas em JSON Lines
✅ Mostra progresso em barra

Tempo: ~2-3 horas (3 epochs)
Pode correr isoladamente: ❌ NÃO (depende de células anteriores)

Dependências:
- training_config (de [CONFIG WIZARD])
- tokenizer (de [MODEL SETUP])
```

**Output:**
- `checkpoints_qlora/training_metrics.json` (atualizado a cada step)
- `checkpoints_qlora/checkpoint_epochX_stepY/` (modelo em checkpoint)

---

### **[MONITORING] 7️⃣ Visualização em Tempo Real**

```
O que faz:
✅ Lê métricas em tempo real
✅ Mostra gráficos dinâmicos (loss, val_loss)
✅ Atualiza gráficos enquanto treino roda

Tempo: ~5 segundos
Pode correr isoladamente: ✅ SIM (durante/após treino)
```

**Gráficos mostrados:**
- Plot 1: Loss Training vs Validation
- Plot 2: Loss médio por Época

---

### **[VISUALIZATION] 8️⃣ Análise Detalhada (Gráficos Profissionais)**

```
O que faz:
✅ Gera 6 gráficos profissionais:
   1. Loss por Época (linhas)
   2. Volatilidade de Loss (rolling std)
   3. Taxa de Melhoria (derivada)
   4. Loss Acumulado por Época
   5. Learning Curve (com smoothing)
   6. Box Plot (distribuição)

✅ Salva como PNG (150 DPI)
✅ Pronto para apresentações

Tempo: ~3-5 segundos
Pode correr isoladamente: ✅ SIM

Output:
- training_detailed_analysis.png
```

**Alternativa: Usar script Python**
```bash
python3 scripts/visualization_professional.py
# Gera 2 ficheiros PNG:
# - training_dashboard.png (4 gráficos principais)
# - training_detailed_analysis.png (6 gráficos detalhados)
```

---

### **[INFERENCE] 9️⃣ Teste do Modelo**

```
O que faz:
✅ Carrega modelo treinado com LoRA adapters
✅ Tokeniza queries de teste
✅ Gera respostas
✅ Testa qualidade das saídas

Tempo: ~2-5 segundos (por query)
Pode correr isoladamente: ✅ SIM
```

**Exemplos de teste:**
```python
"Qual foi a melhor classificação do Farense?"
"Quantos campeonatos o Farense ganhou?"
"Quem foi o melhor treinador do Farense?"
```

---

### **[ANALYSIS] 🔟 Resumo Final e Métricas**

```
O que faz:
✅ Gera relatório final
✅ Mostra melhorias alcançadas
✅ Lista checkpoints salvos
✅ Próximos passos (deploy, etc)

Tempo: ~2 segundos
Pode correr isoladamente: ✅ SIM
```

**Informações no relatório:**
- Duração total do treino
- Loss inicial vs final
- Percentual de melhoria
- Validation loss estatísticas
- Análise de overfitting
- Localização de checkpoints

---

## 💡 Fluxo de Uso (Primeira Vez)

### Passo 1: Abrir Jupyter Lab
```bash
jupyter lab
```

### Passo 2: Abrir Notebook
Navegue para `notebooks/mistral_qlora_professional.ipynb`

### Passo 3: Executar em Ordem
```
[SETUP] → [SYSTEM CHECK] → [RECOMMENDATIONS] → [CONFIG WIZARD]
   ↓
[DATA PREP] → [MODEL SETUP] → [TRAINING] (⏱️ 2-3h)
   ↓
[MONITORING] → [VISUALIZATION] → [INFERENCE] → [ANALYSIS]
```

### Passo 4: Acompanhar Progresso (Opcional)
Abra outro terminal:
```bash
python3 scripts/visualization_professional.py  # A qualquer momento
# ou
tail -f checkpoints_qlora/training_metrics.json | python3 -m json.tool
```

---

## ⚡ Dicas Importantes

### Para Evitar Crashes
- ✅ Execute [SYSTEM CHECK] primeiro
- ✅ Use config recomendada ("BALANCED")
- ✅ Se RAM < 8GB, use "SAFE" config
- ✅ Comece com 1 epoch se primeira vez

### Para Melhor Performance
- 🚀 Se RAM > 12GB, use "PERFORMANCE" config
- 🚀 Aumente batch_size incrementalmente
- 🚀 Use GPU Metal (MLX detecta automaticamente)
- 🚀 Reduza max_seq_length se treino lento

### Durante o Treino
- 📊 [MONITORING] mostra progresso em tempo real
- ⏸️ Pode parar com Ctrl+C (checkpoint é salvo)
- 🔄 Retome depois rodando [TRAINING] novamente
- 💾 Estado salvo em `checkpoints_qlora/training_state.json`

### Após o Treino
- 📈 Execute [VISUALIZATION] para gráficos profissionais
- 🔮 Execute [INFERENCE] para testar modelo
- 📋 Execute [ANALYSIS] para relatório final
- 🖼️ Use gráficos PNG para apresentações

---

## 🎛️ Customização de Parâmetros

### Batch Size (Memória)
```
batch_size=1 → ~4-5GB RAM
batch_size=2 → ~6-8GB RAM ⭐
batch_size=4 → ~12GB+ RAM
```

### Learning Rate (Treino)
```
0.0001  → Muito conservador (lento)
0.0002  → Recomendado ⭐
0.0003  → Um pouco agressivo
0.0005  → Agressivo (risco instabilidade)
```

### Max Seq Length (Velocidade)
```
256   → Rápido mas sequências curtas
384   → Bom compromisso
512   → Completo mas mais lento ⭐
```

### Gradient Accumulation (Batch Efetivo)
```
effective_batch = batch_size * gradient_accumulation
Exemplo: batch_size=2, grad_accum=2 → effective=4
```

---

## 📊 Ficheiros Gerados

### Durante o Treino
```
checkpoints_qlora/
├── training_metrics.json      ← Atualizado a cada step
├── training_metrics.csv       ← Formato CSV
├── training_state.json        ← Para retomar se interromper
├── checkpoint_epoch0_step*/   ← Checkpoints intermediários
└── adapters/                  ← Melhor modelo encontrado
```

### Após Gerar Gráficos
```
checkpoints_qlora/
├── training_dashboard.png              ← 4 gráficos principais
└── training_detailed_analysis.png      ← 6 gráficos detalhados
```

### Configuração Usada
```
checkpoints_qlora/
└── config_selected.json  ← Specs exatos do treino
```

---

## 🔧 Troubleshooting

| Problema | Solução |
|----------|---------|
| **Out of Memory** | Reduzir batch_size (2→1) ou aumentar gradient_accumulation (2→4) |
| **Treino muito lento** | Aumentar batch_size ou max_seq_length |
| **Loss não diminui** | Aumentar learning_rate (0.0002→0.0003) |
| **Modelo não carrega** | Verificar se models/mistral-7b-4bit/model.safetensors existe |
| **Dados inválidos** | Executar [DATA PREP] para validar |
| **Metrics file não atualiza** | Verificar se treino está rodando (ps aux \| grep train) |
| **Gráficos vazios** | Executar treino primeiro (mínimo 10 steps) |

---

## 📚 Referência Rápida - Comandos

```bash
# Ver progresso do treino
tail -5 checkpoints_qlora/training_metrics.json

# Monitor em tempo real
tail -f checkpoints_qlora/training_metrics.json | python3 -m json.tool

# Gerar gráficos profissionais
python3 scripts/visualization_professional.py

# Ver processo de treino
ps aux | grep train

# Verificar tamanho de checkpoints
du -sh checkpoints_qlora/

# Parar treino gracefully
kill -15 <PID>

# Retomar treino depois
# (Jupyter: execute [TRAINING] novamente)
```

---

## 📈 Métricas Esperadas

### Primeira Epoch (esperado)
- Loss inicial: ~4.5-5.0
- Loss final: ~2.5-3.0
- Tendência: ↓ Decrescente ✅

### Segunda Epoch
- Loss inicial: ~2.5-3.0
- Loss final: ~1.5-2.0
- Tendência: ↓ Continua diminuindo ✅

### Terceira Epoch
- Loss inicial: ~1.5-2.0
- Loss final: ~0.8-1.2
- Tendência: ↓ Possível convergência

### Val Loss
- Deve ser ligeiramente maior que training loss
- Se gap < 0.2 → Sem overfitting ✅
- Se gap > 0.5 → Overfitting significativo ⚠️

---

## 🎓 Aprender Mais

**Dentro do notebook:**
- Cada célula tem explicação detalhada
- Comments em código explicam o que faz

**Em português:**
- `README_PREFLIGHT.md` - Guia detalhado de preflight check
- `TRAINING_IN_PROGRESS.md` - Como monitorar durante treino

**Conceitos:**
- MLX framework: https://ml-explore.github.io/mlx/
- QLoRA: https://arxiv.org/abs/2305.14314
- LoRA: https://arxiv.org/abs/2106.09714

---

## ✅ Checklist Antes de Começar

- [ ] Python 3.11+
- [ ] MLX instalado (`python3 -c "import mlx"`)
- [ ] Jupyter Lab instalado
- [ ] Dados em `data/train.jsonl` e `data/valid.jsonl`
- [ ] Modelo em `models/mistral-7b-4bit/model.safetensors`
- [ ] RAM >= 6GB (8GB recomendado)
- [ ] Disco >= 20GB livre

---

**Versão:** 1.0
**Data:** 2025-11-19
**Framework:** MLX (Apple Silicon)
**Modelo:** Mistral-7B-4bit
**Método:** QLoRA

---

**Dúvidas?** Consulte o notebook - cada célula está bem comentada!
