# 📚 Índice de Documentação - LLM Training

> **Este é o ponto de partida para toda a documentação!**

---

## 🚀 COMEÇAR AQUI

Se é a primeira vez, **comece por aqui** (5 minutos):

### 1️⃣ Para Treinamento QLoRA (Recomendado em Mac M1)
```
👉 docs/quickstart/QUICKSTART_QLORA.md
   ↓ (depois)
👉 docs/quickstart/START_HERE.md
```

### 2️⃣ Para Treinamento LoRA (Legacy/Antigo)
```
👉 docs/references/README.md
```

### 3️⃣ Se Está Preso (Troubleshooting)
```
👉 docs/troubleshooting/QLORA_TROUBLESHOOTING.md
```

---

## 📂 Estrutura de Pastas

```
docs/
├── quickstart/              ⭐ COMECE AQUI
│   ├── QUICKSTART_QLORA.md     (5 min) - QLoRA rápido
│   ├── START_HERE.md           (10 min) - Setup completo
│   └── USE_SIMPLE_NOTEBOOK.md  (referência)
│
├── guides/                  📖 GUIAS TÉCNICOS
│   ├── QLORA_GUIDE.md              (30 min) - QLoRA em detalhe
│   ├── QLORA_VS_LORA.md            (20 min) - Comparação
│   ├── FINETUNE_MLX_QLORA.md       (referência)
│   ├── mlx_finetuning_guide.md     (técnico)
│   └── MONITORING_GUIDE.md         (monitoramento)
│
├── references/              📋 REFERÊNCIA RÁPIDA
│   ├── INDEX.md                    (mapa geral)
│   ├── README.md                   (visão geral)
│   ├── README_QLORA_REFACTOR.md    (sumário)
│   ├── CHECKLIST.md                (verificação)
│   ├── MONITORING_INDEX.md         (índice monitoramento)
│   └── MONITORING_README.md        (monitoramento)
│
├── troubleshooting/         🔧 AJUDA
│   └── QLORA_TROUBLESHOOTING.md    (problemas e soluções)
│
└── legacy/                  📦 ANTIGO (manter para referência)
    ├── CELL_EXECUTION_ORDER.md
    ├── CLEANUP_COMPLETE.md
    ├── FIX_SUMMARY.md
    ├── QLORA_TRAINING_FIX.md
    ├── QLORA_TRAINING_FIXED.md
    ├── QLORA_FIX_COMPARISON.md
    ├── TRAINING_FIXES.md
    ├── ORGANIZATION_SUMMARY.md
    └── GEMINI.md
```

---

## 🎯 Fluxo por Objetivo

### Cenário 1: Quero Treinar Agora
```
1. Ler: docs/quickstart/QUICKSTART_QLORA.md (5 min)
2. Executar: jupyter notebook notebooks/mistral_qlora_training.ipynb
3. Pronto! ✅
```
**Tempo total: 2-3 horas**

---

### Cenário 2: Quero Entender QLoRA
```
1. Ler: docs/quickstart/QUICKSTART_QLORA.md (5 min)
2. Ler: docs/guides/QLORA_GUIDE.md (30 min)
3. Comparar: docs/guides/QLORA_VS_LORA.md (20 min)
4. Referenciar: docs/references/ conforme necessário
```
**Tempo total: ~55 minutos**

---

### Cenário 3: Tenho um Problema
```
1. Procurar em: docs/troubleshooting/QLORA_TROUBLESHOOTING.md
2. Se não encontrar, ver: docs/quickstart/QUICKSTART_QLORA.md (seção FAQ)
3. Último recurso: docs/guides/QLORA_GUIDE.md (seção troubleshooting)
```

---

### Cenário 4: Quero Comparar LoRA vs QLoRA
```
1. Ler: docs/guides/QLORA_VS_LORA.md
2. Executar: python scripts/compare_models.py
3. Analisar resultados em: output/comparison_results.json
```

---

### Cenário 5: Quero Monitorar o Treinamento
```
1. Ler: docs/guides/MONITORING_GUIDE.md
2. Referenciar: docs/references/MONITORING_README.md
3. Ver índice: docs/references/MONITORING_INDEX.md
```

---

## ✅ Checklist Rápido

### Antes de Treinar
- [ ] Ler `docs/quickstart/QUICKSTART_QLORA.md`
- [ ] Instalar: `pip install mlx mlx-lm mlx-data`
- [ ] Verificar dados em `data/`
- [ ] Fechar apps pesadas (Chrome, Spotify, etc)

### Durante o Treino
- [ ] Monitorar memória
- [ ] Deixar rodando
- [ ] Checkpoints salvam automaticamente

### Depois do Treino
- [ ] Testar: `python scripts/inference_qlora.py "pergunta"`
- [ ] Validar qualidade
- [ ] Integrar no backend (se necessário)

---

## 📊 Resumo das Versões

| Aspecto | LoRA (Legacy) | QLoRA (Recomendado) |
|---------|---------------|-------------------|
| Tamanho Modelo | 14GB | 3.5GB ✓ |
| Memória Necessária | 8-10GB | 4-6GB ✓ |
| Tempo Treino | 135 min | 96 min ✓ |
| Qualidade | 100% | 99%+ ✓ |
| Mac M1 Base | ✗ | ✓ |
| Recomendado | Não | **SIM** ✓ |

---

## 🔗 Links Diretos por Uso

### Iniciar Treino
- [QUICKSTART QLoRA](./quickstart/QUICKSTART_QLORA.md) ⭐ COMECE AQUI

### Entender Tecnologia
- [Guia QLoRA](./guides/QLORA_GUIDE.md)
- [Comparação LoRA vs QLoRA](./guides/QLORA_VS_LORA.md)
- [Guia MLX Finetuning](./guides/mlx_finetuning_guide.md)

### Referência Rápida
- [Índice Principal](./references/INDEX.md)
- [README](./references/README.md)
- [Checklist](./references/CHECKLIST.md)

### Troubleshooting
- [QLoRA Troubleshooting](./troubleshooting/QLORA_TROUBLESHOOTING.md)

### Monitoramento
- [Guia de Monitoramento](./guides/MONITORING_GUIDE.md)
- [README Monitoramento](./references/MONITORING_README.md)

---

## 📁 Arquivos Importantes do Projeto

```
LLM_training/
├── DOCS_INDEX.md ........................... VOCÊ ESTÁ AQUI! 👈
├── docs/ .................................. Documentação organizada
│
├── notebooks/
│   ├── mistral_qlora_training.ipynb ........ Novo (QLoRA) ✓ USE ESTE
│   └── mistral_lora_training.ipynb ........ Antigo (LoRA legacy)
│
├── scripts/
│   ├── inference_qlora.py ................. Novo (QLoRA) ✓ USE ESTE
│   ├── compare_models.py .................. Benchmark
│   └── inference.py ....................... Antigo (LoRA legacy)
│
├── data/
│   ├── train_data.jsonl ................... Treino
│   └── val_data.jsonl ..................... Validação
│
├── checkpoints_qlora/ ..................... Novos (durante treino)
├── checkpoints/ ........................... Antigos (legacy)
│
└── output/
    ├── mistral-7b-farense-qlora/ ......... Novo modelo (use)
    └── mistral-7b-farense-lora/ .......... Antigo modelo (legacy)
```

---

## 🚨 Importante: Qual Versão Usar?

### ✅ USE QLORA (Novo - Recomendado)
- Notebooks: `mistral_qlora_training.ipynb`
- Scripts: `inference_qlora.py`
- Checkpoints: `checkpoints_qlora/`
- Output: `mistral-7b-farense-qlora/`

### ⚠️ NÃO USE (Legacy/Antigo)
- Notebooks: `mistral_lora_training.ipynb`
- Scripts: `inference.py`
- Checkpoints: `checkpoints/`
- Output: `mistral-7b-farense-lora/`

---

## 🎓 Tempo de Leitura Estimado

| Documento | Tempo | Para Quem |
|-----------|-------|----------|
| QUICKSTART_QLORA.md | 5 min | Todos |
| START_HERE.md | 10 min | Iniciantes |
| QLORA_GUIDE.md | 30 min | Técnicos |
| QLORA_VS_LORA.md | 20 min | Comparação |
| MONITORING_GUIDE.md | 15 min | Avançados |
| README.md | 10 min | Overview |

**Total recomendado antes de treinar: 15-20 minutos**

---

## 💡 Dicas Importantes

1. **Comece pequeno**: Sempre comece com QUICKSTART
2. **Não pule**: Leia na ordem recomendada
3. **Salve bookmarks**: Guarde links dos docs mais usados
4. **Monitore**: Acompanhe o treino (pode levar 2-3 horas)
5. **Checkpoint**: Sistema salva automaticamente a cada 200 passos

---

## ❓ FAQ Rápido

**P: Por onde começo?**
A: [QUICKSTART_QLORA.md](./quickstart/QUICKSTART_QLORA.md) - 5 minutos!

**P: Qual notebook usar?**
A: `mistral_qlora_training.ipynb` (novo/recomendado)

**P: Quanto tempo leva?**
A: ~2-3 horas de treino + 5-20 min leitura

**P: Posso parar e resumir?**
A: Sim! Checkpoints salvam automaticamente

**P: Qual script de inferência usar?**
A: `scripts/inference_qlora.py` (novo/recomendado)

---

## 🔄 Fluxo Recomendado

```
START
  ↓
[1] Ler QUICKSTART_QLORA.md (5 min) .......... docs/quickstart/
  ↓
[2] Ler START_HERE.md (10 min) .............. docs/quickstart/
  ↓
[3] Abrir Jupyter e carregar notebook ....... notebooks/
  ↓
[4] Executar células (2-3 horas) ............ Deixe rodando
  ↓
[5] Testar modelo novo ...................... scripts/inference_qlora.py
  ↓
[6] Integrar no backend (opcional) .......... Ver INTEGRATION_GUIDE
  ↓
[7] Deploy em produção ...................... Pronto!
  ↓
END ✅
```

---

## 🆘 Precisa de Ajuda?

1. **Problema comum?** → `docs/troubleshooting/QLORA_TROUBLESHOOTING.md`
2. **Entender QLoRA?** → `docs/guides/QLORA_GUIDE.md`
3. **Primeira vez?** → `docs/quickstart/QUICKSTART_QLORA.md`
4. **Comparar?** → `docs/guides/QLORA_VS_LORA.md`

---

## 📊 Estatísticas da Documentação

- **Total de documentos**: 27 ficheiros markdown
- **Documentação ativa**: 15 ficheiros
- **Documentação legacy**: 9 ficheiros
- **Tempo total de leitura**: ~120 minutos (apenas guias ativos)
- **Setup + Treino**: ~3.5 horas

---

## ✨ Estado da Documentação

```
✅ Organizada por categoria
✅ Acessível via índice central
✅ Links diretos para cada seção
✅ Documentação legacy preservada
✅ Pronta para uso imediato
```

---

**Última atualização**: 2025-11-17
**Status**: ✅ Pronto para Uso
**Próximo passo**: Abra `docs/quickstart/QUICKSTART_QLORA.md` e comece! 🚀
