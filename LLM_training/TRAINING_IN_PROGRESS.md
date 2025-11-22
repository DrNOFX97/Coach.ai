# 🚀 Treino em Progresso - Monitoramento

## ✅ Status Atual

**Treino Iniciado:** Sim  
**Processo PID:** 8681  
**Status:** ✅ RODANDO  
**Hora de Início:** ~22:15 (18 nov 2025)  
**Tempo Decorrido:** ~30-45 minutos  

## 📊 Progresso

```
Época:          1 / 3
Step:           400 / ~1000+
Loss Treino:    1.4453
Loss Validação: 1.2645
Tendência:      ↓ DIMINUINDO ✅
```

## 🔍 Como Monitorar

### Opção 1: Ver Métricas Mais Recentes (Simples)
```bash
tail -5 checkpoints_qlora/training_metrics.json | python3 -m json.tool
```

### Opção 2: Monitorar em Tempo Real (Contínuo)
```bash
tail -f checkpoints_qlora/training_metrics.json | python3 -m json.tool
```

### Opção 3: Usar Script de Monitoramento
```bash
python3 monitor_simple.py
```

### Opção 4: Ver CSV (Excel-friendly)
```bash
tail -10 checkpoints_qlora/training_metrics.csv
```

## 📂 Ficheiros de Monitoramento

```
checkpoints_qlora/
├── training_metrics.json      ← Métricas JSON (atualizado a cada step)
├── training_metrics.csv       ← Métricas CSV (atualizado a cada step)
├── training_state.json        ← Estado para retomar se interromper
├── checkpoint_epoch0_step200/ ← Checkpoint 1
├── checkpoint_epoch0_step400/ ← Checkpoint 2
├── checkpoint_epoch1_step200/ ← Checkpoint 3
├── checkpoint_epoch1_step400/ ← Checkpoint 4 (em progresso)
└── adapters/                  ← Melhor modelo encontrado
```

## ⏱️ Tempo Estimado

- **Tempo decorrido:** ~30-45 minutos
- **Tempo por epoch:** 40-50 minutos (aproximado)
- **Total de epochs:** 3
- **Tempo total estimado:** 2-3 horas
- **Término estimado:** 00:30 - 01:00 (próximas horas)

## 🛑 Se Precisar Parar

1. **Parar o treino gracefully:**
   ```bash
   kill -15 8681  # ou Ctrl+C no terminal onde está rodando
   ```

2. **Sistema salva automaticamente:**
   - Estado em `training_state.json`
   - Checkpoint em `checkpoint_epoch1_step400/`

3. **Para retomar:**
   ```bash
   python3 scripts/train_qlora.py
   # Detecta checkpoint automaticamente e retoma
   ```

## ✅ Sinais de Treino Saudável

- ✅ Loss está diminuindo (1.4453 → mais baixo)
- ✅ Val Loss é menor que Loss (1.2645 < 1.4453)
- ✅ CPU utilização normal (6.5%)
- ✅ Memória estável (907 MB)
- ✅ Checkpoints sendo salvos regularmente

## ⚠️ Sinais de Problemas

Se vir qualquer um destes:
- **Loss aumentando constantemente** → Reduzir learning_rate
- **Out of Memory** → Aumentar gradient_accumulation
- **Processo parou** → Verificar terminal com erro
- **Loss muito alto (>10)** → Problema com dados

## 📈 O Que Esperar

### Época 1
- Loss inicial alto (esperado)
- Loss deve diminuir ao longo dos steps
- Checkpoint salvo a cada 100 steps

### Época 2
- Loss começa mais baixo que época 1 (bom sinal!)
- Continua diminuindo
- Val Loss deve estabilizar

### Época 3
- Loss muito mais baixo
- Pode convergir (deixar de diminuir)
- Modelo final bem mais bom que no início

## 🎯 Após Treino Terminar

1. **Visualizar resultados:**
   ```bash
   python3 scripts/visualization.py --report
   ```
   Gera gráficos de loss, learning rate, etc.

2. **Testar modelo treinado:**
   ```bash
   python3 scripts/inference_qlora.py "Qual foi a melhor classificação do Farense?"
   ```

3. **Analisar métricas finais:**
   ```bash
   python3 << 'EOF'
   import json
   with open('checkpoints_qlora/training_metrics.json') as f:
       metrics = json.load(f)
   
   final = metrics[-1] if isinstance(metrics, list) else metrics
   initial = metrics[0] if isinstance(metrics, list) else metrics
   
   print(f"Loss Inicial: {initial.get('loss')}")
   print(f"Loss Final:  {final.get('loss')}")
   print(f"Melhoramento: {initial.get('loss') - final.get('loss'):.4f}")
   EOF
   ```

## 📝 Configuração Usada

```json
{
  "batch_size": 2,
  "gradient_accumulation": 2,
  "max_seq_length": 512,
  "learning_rate": 0.0003,
  "num_epochs": 3,
  "warmup_steps": 50,
  "save_steps": 100,
  "eval_steps": 100,
  "log_steps": 10,
  "reason": "Memória adequada (8-10 GB) - config conservadora"
}
```

## 🔗 Referências Rápidas

- **Ver treino ao vivo:** `tail -f checkpoints_qlora/training_metrics.json`
- **Ver processo:** `ps aux | grep train_qlora`
- **Matar treino:** `kill -15 8681` ou `pkill -f train_qlora`
- **Espaço em disco:** `du -sh checkpoints_qlora/`

## ❓ Dúvidas?

Consulte:
- `README_PREFLIGHT.md` → Troubleshooting
- `SAFE_TRAIN_QUICK_START.md` → FAQ completo
- `CLAUDE.md` → Contexto técnico

---

**Última atualização:** 2025-11-18 22:15  
**Treino ID:** epoch1_step400  
**Status:** ✅ EM PROGRESSO
