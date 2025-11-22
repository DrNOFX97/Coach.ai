# 🤖 Inferência Durante Treino

Enquanto o modelo está em treinamento, você pode fazer inferências com o modelo actual (incluindo checkpoints já salvos).

## 📋 Opções Disponíveis

### 1. **Inferência Interativa (RECOMENDADO)**
Console interativo onde você pode fazer várias perguntas seguidas.

```bash
# Em outro terminal:
python3 scripts/interactive_inference.py
```

**Exemplo de uso:**
```
📝 Você: Qual foi a melhor classificação do Farense?
🤔 Processando...
🤖 Farense: O Farense teve a sua melhor classificação em...

📝 Você: Quem foi Hassan Nader?
🤔 Processando...
🤖 Farense: Hassan Nader foi um jogador...

📝 Você: sair
👋 Até logo! (2 conversas)
```

### 2. **Inferência Única (CLI)**
Para fazer uma pergunta individual via command line.

```bash
# Uma pergunta simples:
python3 scripts/inference_during_training.py "Qual foi a melhor classificação do Farense?"

# Com output em JSON:
python3 scripts/inference_during_training.py "Quando foi fundado o Farense?" --json

# Com custom adapter path:
python3 scripts/inference_during_training.py "Pergunta" --adapter-path checkpoints_qlora/adapters

# Com mais tokens na resposta:
python3 scripts/inference_during_training.py "Conte a história do Farense" --max-tokens 500
```

### 3. **Inferência Original**
Script original do projeto.

```bash
python3 scripts/inference_qlora.py "Pergunta aqui"
```

---

## 🔄 Como Funciona Durante Treino

Durante o treinamento:

1. **Modelo base carrega** uma vez (2-3 minutos)
2. **Adapters (LoRA) carregam** do checkpoint actual em `checkpoints_qlora/adapters/`
3. Você pode fazer **múltiplas inferências** sem recarregar o modelo
4. A qualidade das respostas **melhora conforme o treino avança**

### Estados Possíveis:

```
Antes do 1º checkpoint:
  ⚠️  "Adapter não encontrado"
  └─ Usa modelo base (sem fine-tuning)
  └─ Respostas genéricas sobre Mistral

Após 1º checkpoint (~200 steps):
  ✅ "Adapter encontrado"
  └─ Usa modelo + LoRA adapters
  └─ Respostas começam a specialized no Farense

Após N checkpoints:
  ✅ "Adapter encontrado"
  └─ Usa modelo + LoRA adapters mais treinados
  └─ Respostas cada vez melhores
```

---

## 📊 Monitorizar Treino em Paralelo

### Terminal 1: Treino
```bash
python3 scripts/train_qlora.py
```

### Terminal 2: Monitor
```bash
python3 scripts/monitor.py --output-dir checkpoints_qlora --refresh 5
```

### Terminal 3: Inferência Interativa
```bash
python3 scripts/interactive_inference.py
```

---

## 🎯 Exemplos de Perguntas

```
# Sobre história do Farense:
"Qual foi a melhor classificação do Farense?"
"Quando foi fundado o Farense?"
"Quantos campeonatos venceu o Farense?"

# Sobre jogadores:
"Quem foi Hassan Nader?"
"Qual era a posição de Zé Rodrigues?"
"Qual foi o melhor avançado da história do Farense?"

# Sobre resultados:
"Qual foi o resultado contra Benfica em 1950?"
"Qual foi o maior golo marcado pelo Farense?"

# Teste de competência:
"Conte a história completa do Farense"
"Qual foi o impacto de Hassan Nader no Farense?"
```

---

## 🔧 Troubleshooting

### "Adapter não encontrado"
Isto é **normal** até que o primeiro checkpoint seja salvo (~5-10 minutos após início do treino).

### Respostas genéricas/não sobre Farense
O modelo ainda está no início do treino. Espere mais epochs.

### Lentidão nas respostas
- Verifique se o treino está usando GPU: `python3 -c "import mlx.core as mx; print(mx.default_device())"`
- Reduza `--max-tokens` para menos tokens gerados

### Erro "Adapter path não exists"
Use o `--adapter-path` correto:
```bash
python3 scripts/interactive_inference.py --adapter-path checkpoints_qlora/adapters
```

---

## 📈 O Que Esperar

| Fase | Adapter | Qualidade |
|------|---------|-----------|
| Início (0-200 steps) | ❌ Não existe | ⚠️ Genérico (Mistral base) |
| Après 1º checkpoint (200 steps) | ✅ Existe | 🟡 Começa especializar |
| Meio treino (1000+ steps) | ✅ Existe | 🟢 Muito melhor |
| Fim treino (2000+ steps) | ✅ Existe | 🟢🟢 Excelente |

---

## 💡 Dicas

1. **Guarde boas respostas** numa nota enquanto testa
2. **Compare respostas** do mesmo prompt em diferentes checkpoints
3. **Teste pergunta simples** (Ex: "Qual foi a melhor classificação do Farense?") para monitorizar evolução
4. **Use JSON output** para integrar com outras ferramentas

```bash
python3 scripts/inference_during_training.py "Qual foi a melhor classificação?" --json | jq .response
```

---

## 🚀 Quick Start

```bash
# Terminal 1: Start training
python3 scripts/train_qlora.py

# Espere ~5 minutos para primeiro checkpoint

# Terminal 2 (ou 3): Interactive inference
python3 scripts/interactive_inference.py

# Comece a fazer perguntas!
```

---

Bom treino! 🎯
