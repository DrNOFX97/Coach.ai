# 📚 Índice Completo - Sistema Safe Train

## ⚡ Comece Aqui (30 segundos)

- **[START.txt](START.txt)** - Guia ultra-simples, 30 segundos

## 🚀 Próximos Passos (5-10 minutos)

- **[SAFE_TRAIN_START_HERE.md](SAFE_TRAIN_START_HERE.md)** - Quick start com índice
- **[SAFE_TRAIN_MAP.txt](SAFE_TRAIN_MAP.txt)** - Mapa visual com 3 opções
- **[SISTEMA_SAFE_TRAIN_SUMMARY.txt](SISTEMA_SAFE_TRAIN_SUMMARY.txt)** - Resumo técnico

## 📖 Documentação Completa

### Para Iniciantes
- **[README_PREFLIGHT.md](README_PREFLIGHT.md)** - Guia detalhado (15-20 min)
  - O que é preflight check?
  - O que cada parâmetro faz
  - Troubleshooting completo
  - Exemplos por hardware

### Para Aplicar Configuração
- **[APPLY_RECOMMENDED_CONFIG.md](APPLY_RECOMMENDED_CONFIG.md)** - Como atualizar notebook (10 min)
  - Passo a passo com exemplos
  - Mapeamento de valores
  - Checklist antes de executar

### Para Workflow Completo
- **[SAFE_TRAIN_QUICK_START.md](SAFE_TRAIN_QUICK_START.md)** - Guia passo a passo (20-30 min)
  - Workflow visual completo
  - Recomendações por hardware
  - Troubleshooting avançado

### Contexto do Projeto
- **[CLAUDE.md](CLAUDE.md)** - Documentação técnica do projeto
  - Visão geral
  - Arquitetura do sistema
  - Como estender

## 🔧 Scripts Python

### Sistema Automático
- **[scripts/preflight_check.py](scripts/preflight_check.py)** - ⭐ Diagnóstico completo
  - Verifica Python, MLX, GPU, dados, modelo
  - Recomenda configuração otimizada
  - Gera: `recommended_config.json`

- **[scripts/safe_train.py](scripts/safe_train.py)** - Menu Python interativo
  - Executa preflight_check
  - Oferece opções (notebook, script, instruções)

### Treino e Monitoramento
- **scripts/train_qlora.py** - Pipeline de treino principal
- **scripts/monitor.py** - Monitorar em tempo real (loss, memória, ETA)
- **scripts/inference_qlora.py** - Testar modelo treinado
- **scripts/visualization.py** - Gerar gráficos de resultados

### Utilidades
- **scripts/validate_jsonl.py** - Validar dados
- **scripts/clean_dataset.py** - Limpar e normalizar dados
- **scripts/split_data.py** - Dividir treino/validação (90/10)

## 🐚 Script Bash

- **[train_safe.sh](train_safe.sh)** - ⭐ Wrapper bash super fácil
  - `./train_safe.sh`
  - Menu colorido com opções

## 📊 Ficheiros Gerados

### Após Executar `preflight_check.py`
```
checkpoints_qlora/
├── preflight_report.json       ← Relatório técnico completo
└── recommended_config.json     ← ⭐ COPIAR VALORES DAQUI
```

### Durante/Após Treino
```
checkpoints_qlora/
├── checkpoint_epoch_0_step_*/  ← Checkpoints intermediários
├── checkpoint_epoch_1_step_*/
├── checkpoint_epoch_2_step_*/
├── adapters/                   ← Melhor modelo encontrado
├── training_metrics.json       ← Métricas em JSON
├── training_metrics.csv        ← Métricas em CSV
├── training_summary.json       ← Resumo final
├── training_state.json         ← Para resume se interromper
└── plots/                      ← Gráficos gerados
    ├── loss.png
    ├── learning_rate.png
    └── memory_usage.png
```

## 📋 Sequência Recomendada de Leitura

### Primeira Vez (30 minutos)
1. [START.txt](START.txt) - 1 min
2. [SAFE_TRAIN_START_HERE.md](SAFE_TRAIN_START_HERE.md) - 5 min
3. [SAFE_TRAIN_MAP.txt](SAFE_TRAIN_MAP.txt) - 5 min
4. [APPLY_RECOMMENDED_CONFIG.md](APPLY_RECOMMENDED_CONFIG.md) - 10 min
5. Correr sistema: `./train_safe.sh` - 10 min

### Se Tiver Problemas
1. [README_PREFLIGHT.md](README_PREFLIGHT.md) → Troubleshooting
2. [SAFE_TRAIN_QUICK_START.md](SAFE_TRAIN_QUICK_START.md) → FAQ
3. [CLAUDE.md](CLAUDE.md) → Contexto técnico

### Para Entender Tudo
1. [README_PREFLIGHT.md](README_PREFLIGHT.md) - Conceitos
2. [SAFE_TRAIN_QUICK_START.md](SAFE_TRAIN_QUICK_START.md) - Workflow
3. [CLAUDE.md](CLAUDE.md) - Arquitetura
4. Ver código: `scripts/preflight_check.py` - Implementação

## 🎯 Decisão Rápida

| Situação | Recomendação |
|----------|--------------|
| **Quero começar agora** | `./train_safe.sh` |
| **Quero ler primeiro** | [SAFE_TRAIN_START_HERE.md](SAFE_TRAIN_START_HERE.md) |
| **Preciso atualizar notebook** | [APPLY_RECOMMENDED_CONFIG.md](APPLY_RECOMMENDED_CONFIG.md) |
| **Deu erro no preflight** | [README_PREFLIGHT.md](README_PREFLIGHT.md) |
| **Treino crashed** | [SAFE_TRAIN_QUICK_START.md](SAFE_TRAIN_QUICK_START.md) |
| **Quer entender código** | [CLAUDE.md](CLAUDE.md) |
| **Mapa visual** | [SAFE_TRAIN_MAP.txt](SAFE_TRAIN_MAP.txt) |

## 📞 Suporte Rápido

### Erro no Preflight Check?
→ [README_PREFLIGHT.md](README_PREFLIGHT.md) - Seção "Troubleshooting"

### "Out of Memory" durante treino?
→ [SAFE_TRAIN_QUICK_START.md](SAFE_TRAIN_QUICK_START.md) - Seção "Troubleshooting"

### Como atualizar notebook?
→ [APPLY_RECOMMENDED_CONFIG.md](APPLY_RECOMMENDED_CONFIG.md)

### Qual é a melhor config para meu hardware?
→ [README_PREFLIGHT.md](README_PREFLIGHT.md) - Seção "Exemplos de Configurações por Hardware"

### Como funciona QLoRA?
→ [CLAUDE.md](CLAUDE.md) - Seção "Code Architecture"

## 🗂️ Estrutura de Ficheiros Completa

```
LLM_training/
│
├── 📄 FICHEIROS DE INÍCIO (LEIA ESTES!)
│   ├── START.txt                            ⭐ Comece aqui
│   ├── INDEX.md                             (este ficheiro)
│   ├── SAFE_TRAIN_START_HERE.md            Quick start
│   ├── SAFE_TRAIN_MAP.txt                  Mapa visual
│   └── SISTEMA_SAFE_TRAIN_SUMMARY.txt      Resumo
│
├── 📚 DOCUMENTAÇÃO DETALHADA
│   ├── README_PREFLIGHT.md                 Guia completo
│   ├── SAFE_TRAIN_QUICK_START.md           Workflow
│   ├── APPLY_RECOMMENDED_CONFIG.md         Notebook guide
│   └── CLAUDE.md                           Contexto técnico
│
├── 🔧 SCRIPTS
│   ├── train_safe.sh                       ⭐ Fácil (bash)
│   └── scripts/
│       ├── preflight_check.py              ⭐ Diagnóstico
│       ├── safe_train.py                   Menu Python
│       ├── train_qlora.py                  Treino
│       ├── monitor.py                      Monitor tempo real
│       ├── inference_qlora.py              Tester
│       ├── visualization.py                Gráficos
│       ├── validate_jsonl.py               Validação
│       ├── clean_dataset.py                Limpeza
│       └── split_data.py                   Split train/val
│
├── 📊 DADOS
│   └── data/
│       ├── train_v3_final_complete.jsonl   Treino
│       └── valid_v3_final_complete.jsonl   Validação
│
├── 📓 NOTEBOOKS
│   └── notebooks/
│       └── mistral_qlora_training.ipynb    Principal
│
└── 📂 CHECKPOINTS (GERADO)
    └── checkpoints_qlora/
        ├── preflight_report.json           Diagnóstico
        ├── recommended_config.json         ⭐ Config
        ├── checkpoint_*                    Checkpoints
        ├── adapters/                       Modelo final
        ├── training_metrics.json
        └── plots/
```

## 🚀 Atalhos Úteis

```bash
# Começar rápido
./train_safe.sh

# Diagnóstico manual
python3 scripts/preflight_check.py

# Ver config recomendada
cat checkpoints_qlora/recommended_config.json

# Abrir notebook
jupyter notebook notebooks/mistral_qlora_training.ipynb

# Monitorar treino (terminal separada)
python3 scripts/monitor.py --refresh 5

# Após treino - gráficos
python3 scripts/visualization.py --report

# Testar modelo
python3 scripts/inference_qlora.py "sua pergunta"

# Validar dados
python3 scripts/validate_jsonl.py data/train_v3_final_complete.jsonl

# Diagnóstico detalhado
python3 scripts/diagnose_qlora.py
```

## ✅ Checklist

### Antes de Começar
- [ ] Ler [START.txt](START.txt)
- [ ] Ler [SAFE_TRAIN_START_HERE.md](SAFE_TRAIN_START_HERE.md)
- [ ] Correr `./train_safe.sh`

### Antes de Treinar
- [ ] Executei `python3 scripts/preflight_check.py`
- [ ] Vi valores em `checkpoints_qlora/recommended_config.json`
- [ ] Atualizei notebook com esses valores
- [ ] Salvei notebook
- [ ] Terminal separada pronta para monitor

### Durante Treino
- [ ] Monitor rodando: `python3 scripts/monitor.py`
- [ ] Loss diminuindo
- [ ] Memória OK
- [ ] Nenhum erro visível

### Após Treino
- [ ] `python3 scripts/visualization.py --report`
- [ ] `python3 scripts/inference_qlora.py "pergunta"`
- [ ] Checkpoints salvos em `checkpoints_qlora/`

## 📞 Suporte

- **Erros?** Ver [README_PREFLIGHT.md](README_PREFLIGHT.md)
- **Dúvidas?** Ler documentação relevante acima
- **Mais ajuda?** Consultar [CLAUDE.md](CLAUDE.md)

---

**Versão:** 1.0  
**Data:** 2024-11-18  
**Status:** ✅ Pronto para usar
