# MacBook Pro M1 16GB - Configurações Otimizadas ⚡

## 🎯 Resumo Executivo

Seu notebook foi otimizado especificamente para **MacBook Pro M1 16GB** com as seguintes configurações:

| Parâmetro | Valor | Razão |
|-----------|-------|-------|
| **Batch Size** | **4** | M1 16GB pode lidar confortavelmente com batches de 4 |
| **Gradient Accumulation** | **2** | Simula batch size de 8 com economia de memória |
| **Effective Batch Size** | **8** | batch_size × accumulation_steps |
| **Learning Rate** | **2e-4** | Padrão para LoRA fine-tuning |
| **Epochs** | **3** | Suficiente para dataset de 943 exemplos |
| **Max Sequence Length** | **512** | Suporta textos até ~512 tokens |
| **Warmup Steps** | **100** | Aquecimento do LR nos primeiros 100 passos |

---

## 📊 Detalhes das Configurações

### 1. PARÂMETROS DE TREINO

```python
# BATCH SIZE EXPLICADO
batch_size = 4
gradient_accumulation_steps = 2

# Isto significa:
# - Você carrega 4 exemplos por vez (reduzido para caber em memória)
# - Faz forward/backward em 4 exemplos
# - Após 2 iterações (total 8 exemplos), atualiza os pesos
# - Efetivamente treina com batch_size=8, mas usa 4x menos memória
```

**Por que este tamanho?**
- M1 16GB é poderoso mas quantizado (INT4)
- Batch size 4 = ~6-7GB de memória durante treino
- Batch size 6+ = risco de out-of-memory
- Gradient accumulation permite effective batch = 8 sem overflow

### 2. TAXA DE APRENDIZAGEM (Learning Rate)

```
Learning Rate: 2e-4 (0.0002)

Progressão típica (com warmup):
Passo 1-100:   LR sobe de 0 → 2e-4
Passo 101+:    LR = 2e-4 (constante)
```

**Este valor é bom para:**
- Fine-tuning de modelos pré-treinados ✓
- LoRA com low-rank decomposition ✓
- Dataset pequeno (943 exemplos) ✓

### 3. NÚMERO DE ÉPOCAS

```
Épocas: 3

Passar 3 vezes pelo dataset completo:
├─ Época 1: Aprender padrões gerais
├─ Época 2: Refinar conhecimento
└─ Época 3: Consolidar aprendizagem
```

**Tempo esperado:**
- Época 1: ~35-40 minutos
- Época 2: ~35-40 minutos
- Época 3: ~35-40 minutos
- **Total: ~2-3 horas**

### 4. COMPRIMENTO MÁXIMO DE SEQUÊNCIA

```
Max Sequence Length: 512 tokens

Tokenização típica:
"Qual foi o resultado do Farense contra X em YYYY-MM-DD?"
"O Farense jogou fora de casa e o resultado foi 1-0"
= ~30-40 tokens

Máximo por exemplo: 512 tokens (~2000 caracteres)
```

### 5. CHECKPOINTING

```
Save Checkpoint Every: 200 passos
Evaluate Every: 200 passos
Log Every: 10 passos

Com ~210 passos por época:
├─ Checkpoint após ~95% de cada época
├─ Validação a cada 200 passos
└─ Permite retomar se falhar
```

---

## 🛠️ CONFIGURAÇÕES LoRA

```python
# LoRA = Low-Rank Adaptation
# Treina apenas ~0.1% dos parâmetros do modelo

lora_rank = 8              # Decomposição em 8 dimensões
lora_scale = 16            # Escala de adaptação
lora_dropout = 0.0         # Sem dropout (dataset pequeno)

target_modules = [
    "q_proj",      # Query projection
    "v_proj",      # Value projection
    "k_proj",      # Key projection
    "o_proj",      # Output projection
    "gate_proj",   # Gate (for MLPs)
    "up_proj",     # Up projection
    "down_proj"    # Down projection
]
```

**Parâmetros treináveis:**
- Modelo completo: ~7.2 bilhões
- Com LoRA: ~3.3 milhões (0.046%)
- Economia: 99.95%! 🚀

---

## 💾 MEMÓRIA E DESEMPENHO

### Uso de Memória Esperado

```
Modelo base (INT4):          ~3.8 GB (permanente)
LoRA Adapters:                ~50 MB
Batch (4 exemplos):           ~3-4 GB
Otimizador + estado:          ~1-2 GB
Overhead do sistema:          ~2 GB
────────────────────────────────────
Total máximo:                 ~10-11 GB

Disponível: 16 GB
Margem: 5-6 GB ✓ (seguro!)
```

### Velocidade Esperada

```
Tokens processados por segundo: 300-500 tok/s
Exemplos por segundo: ~3-5 exemplos/s
Passos por minuto: ~180-300 passos/min
Tempo por época: ~35-40 minutos
```

---

## 📈 TRAJETÓRIA DE LOSS ESPERADA

```
Durante o treino, você verá:

ÉPOCA 1:
  Passo  10 | Loss: 4.85
  Passo  20 | Loss: 4.32
  Passo  50 | Loss: 3.87
  Passo 100 | Loss: 3.45
  Passo 150 | Loss: 3.12
  ✓ Validação: val_loss ≈ 3.0

ÉPOCA 2:
  Passo  10 | Loss: 3.00
  Passo  50 | Loss: 2.45
  Passo 100 | Loss: 2.15
  ✓ Validação: val_loss ≈ 2.0

ÉPOCA 3:
  Passo  10 | Loss: 1.95
  Passo  50 | Loss: 1.65
  Passo 100 | Loss: 1.50
  ✓ Validação: val_loss ≈ 1.65

Espera-se uma redução SUAVE e consistente.
Se loss ficar preso, pode aumentar LR para 5e-4.
```

---

## 🚀 COMO USAR O NOTEBOOK

### Passo 1: Abrir Notebook
```bash
jupyter notebook notebooks/mistral_qlora_training_m1_optimized.ipynb
```

### Passo 2: Executar Células na Ordem

**Seção 1 (2-3 min):** Setup e verificação
- ✓ Carrega imports
- ✓ Verifica GPU Metal
- ✓ Verifica memória disponível

**Seção 2 (instantâneo):** Mostrar configurações
- ✓ Exibe todas as configurações (batch size, LR, etc)
- ✓ Confirma que M1 foi detectado

**Seção 3-4 (1-2 min):** Carregar dados e modelo
- ✓ Carrega 848 exemplos de treino
- ✓ Carrega 95 exemplos de validação
- ✓ Carrega Mistral-7B (pode levar 1-2 min primeira vez)

**Seção 5 (30 seg):** Tokenização
- ✓ Converte texto em tokens
- ✓ Mostra estatísticas de tamanho

**Seção 6 (instantâneo):** Inicializar tracker
- ✓ Prepara sistema de métricas

**Seção 7 (2-3 horas):** ⭐ MAIN TRAINING LOOP
- Isto é o núcleo do treino
- Você verá progresso a cada 10 passos
- Deixe rodar (não feche o notebook)

**Seção 8 (1-2 min):** Testes de geração
- ✓ Testa qualidade do modelo
- ✓ Mostra exemplos de respostas

**Seção 9 (instantâneo):** Salvar modelo
- ✓ Salva resumo de treino
- ✓ Mostra próximas etapas

---

## ⚙️ AJUSTES FINOS (Se Necessário)

### Se Receber Erro de Memória:

```python
# REDUZIR BATCH SIZE (atual: 4)
batch_size = 2  # Reduzido
gradient_accumulation_steps = 4  # Aumentado para compensar

# Effective batch size mantém-se = 8
# Mas usa menos memória instantânea
```

### Se Loss Não Diminuir:

```python
# AUMENTAR LEARNING RATE
learning_rate = 5e-4  # De 2e-4 para 5e-4

# Mais agressivo mas pode overfitar
# Monitor validação loss atentamente
```

### Se Quiser Treinar Mais:

```python
# AUMENTAR ÉPOCAS
num_epochs = 4 ou 5

# Tempo total aumentará proporcionalmente
# Cada época ≈ 40 minutos
```

### Se Quiser Melhor Qualidade:

```python
# AUMENTAR MAX_SEQ_LENGTH
max_seq_length = 768  # De 512

# Permite exemplos mais longos
# Usa mais memória (cuidado!)
# Provavelmente vai dar OOM, não recomendado
```

---

## 📊 MONITORAMENTO EM TEMPO REAL

### Terminal Separado

Enquanto o notebook treina, abra outro terminal:

```bash
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

Isto mostra em tempo real:
```
════════════════════════════════════
TRAINING PROGRESS (Updated every 5s)
════════════════════════════════════
Current Loss: 2.45
Best Val Loss: 1.98
Memory Used: 7.8 / 16.0 GB
Tokens/sec: 420
Steps/sec: 3.2
ETA: 45 min remaining
════════════════════════════════════
```

---

## 📈 APÓS TREINO: PRÓXIMOS PASSOS

### 1. Visualizar Resultados
```bash
python3 scripts/visualization.py --report
```
Gera gráficos de loss, memória, taxa de aprendizagem.

### 2. Testar Modelo
```bash
python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
```

### 3. Analisar Métricas
```bash
cat checkpoints_qlora/training_summary.json | jq
```

### 4. Comparar Versões
```bash
python3 scripts/compare_models.py
```

---

## 🔍 FICHEIROS IMPORTANTES

### Após treino, você terá:

```
checkpoints_qlora/
├── training_metrics.json        ← Métricas detalhadas (JSON)
├── training_metrics.csv         ← Métricas (CSV)
├── training_summary.json        ← Resumo final
├── training_state.json          ← Estado para retomar
├── checkpoint_epoch0_step200/   ← Checkpoints intermédios
├── checkpoint_epoch1_step200/
├── checkpoint_epoch2_step200/
├── adapters/                    ← Melhor modelo
│   └── adapters.safetensors
└── plots/                       ← Visualizações (se geradas)
    ├── loss_curves.png
    ├── learning_rate.png
    └── memory_usage.png

output/mistral-7b-farense-qlora/
├── adapters.safetensors         ← Usar isto para inferência
├── adapter_config.json
└── training_config.json
```

---

## ✅ CHECKLIST PRÉ-TREINO

Antes de executar o notebook, verifique:

```bash
# ✓ Verificar Python
python3 --version  # Deve ser 3.11+

# ✓ Verificar MLX GPU
python3 -c "import mlx.core as mx; print(f'Device: {mx.default_device()}')"

# ✓ Verificar dados
wc -l data/train.jsonl data/valid.jsonl

# ✓ Verificar modelo
ls -lh models/mistral-7b-4bit/model.safetensors

# ✓ Verificar espaço em disco
df -h /Users/f.nuno/Desktop/chatbot_2.0/LLM_training/

# ✓ Fechar outras aplicações (especialmente navegador com muitos tabs)
```

---

## 🆘 TROUBLESHOOTING

### "Out of Memory" Error

**Causa:** Batch size demasiado grande para seu M1

**Solução:**
```python
batch_size = 2  # em vez de 4
gradient_accumulation_steps = 4  # em vez de 2
```

### Loss não diminui (stuck at 4.5)

**Causa:** Learning rate demasiado baixa

**Solução:**
```python
learning_rate = 5e-4  # em vez de 2e-4
```

### Training muito lento (<100 tokens/sec)

**Causa:** GPU não está sendo usada, pode estar em CPU mode

**Verificar:**
```python
import mlx.core as mx
print(mx.default_device())  # Deve ser "gpu"
```

### Notebook congela

**Causa:** Batch muito grande ou exemplos muito longos

**Solução:** Reiniciar notebook e reduzir batch_size ou max_seq_length

---

## 💡 DICAS PROFISSIONAIS

1. **Feche o navegador** antes de treinar - economiza ~2GB RAM
2. **Use o monitor.py** em terminal separado - vê progresso em tempo real
3. **Salve checkpoints frequentemente** - permite recuperação se falhar
4. **Teste com batch_size=4 primeiro** - ajuste depois se necessário
5. **Monitore val_loss** - se subir enquanto train_loss desce = overfitting
6. **Guarde o melhor modelo** - usar adapters/ em vez do último checkpoint

---

## 📊 ESPECIFICAÇÕES DO SEU HARDWARE

```
MacBook Pro M1 16GB
├─ Chip: Apple Silicon M1
├─ Cores CPU: 8 (4 performance + 4 efficiency)
├─ Cores GPU: 7 ou 8 (Metal Performance Shaders)
├─ RAM: 16 GB (unified memory)
├─ Storage: SSD (variável)
└─ MLX Framework: Otimizado para M1 ✓

Comparação:
- M1 Base (8GB):     batch_size=2
- M1 Pro (16GB):     batch_size=4  ← VOCÊ ESTÁ AQUI
- M1 Max (32GB):     batch_size=8
- M2/M3:             Similar ao M1
```

---

## 🎓 PRÓXIMAS MELHORIAS

Após treinar com sucesso, pode:

1. **Aumentar dataset** - Adicionar mais exemplos Farense
2. **Fine-tune no adaptador** - Treinar mais 1-2 épocas
3. **Testar hyperparameters** - Experimentar LR, batch_size
4. **Integrar em aplicação** - Usar inference_qlora.py em produção
5. **Continuar treino** - Recuperar do checkpoint_epoch2_step*

---

**Criado para:** MacBook Pro M1 16GB
**Data:** 18 Novembro 2025
**Status:** Pronto para uso 🚀

Boa sorte com o treino! ⚽🤖
