# Como Aplicar a Configuração Recomendada ao Notebook

Após executar `python3 scripts/preflight_check.py`, você receberá uma configuração otimizada em `checkpoints_qlora/recommended_config.json`.

Este guia explica como aplicar essas configurações ao notebook.

---

## Passo 1: Ver a Configuração Recomendada

```bash
cat checkpoints_qlora/recommended_config.json
```

Exemplo de output:
```json
{
  "batch_size": 1,
  "gradient_accumulation": 4,
  "max_seq_length": 256,
  "learning_rate": 0.0002,
  "num_epochs": 3,
  "warmup_steps": 50,
  "save_steps": 100,
  "eval_steps": 100,
  "log_steps": 10,
  "reason": "Memória limitada (6-8 GB) - config reduzida"
}
```

---

## Passo 2: Abrir o Notebook

```bash
jupyter notebook notebooks/mistral_qlora_training.ipynb
```

---

## Passo 3: Localizar a Seção de Configuração

No notebook, procure pela célula que começa com:

```python
# Configuração do Treino
training_config = {
    ...
}
```

Esta célula deve estar perto do início, após o carregamento de dependências.

---

## Passo 4: Atualizar os Valores

Substitua os valores **antigos** pelos valores **recomendados**.

### ANTES:
```python
training_config = {
    "num_epochs": 3,
    "batch_size": 4,                    # ← Valor antigo
    "gradient_accumulation": 2,         # ← Valor antigo
    "learning_rate": 5e-4,              # ← Valor antigo
    "max_seq_length": 512,              # ← Valor antigo
    "warmup_steps": 100,                # ← Valor antigo
    "save_steps": 200,
    "eval_steps": 200,
    "log_steps": 10,
    "lora_parameters_path": CHECKPOINTS_DIR / "adapters.safetensors",
    "model_path": OUTPUT_DIR / "mistral-7b-farense-qlora",
}
```

### DEPOIS (com valores recomendados):
```python
training_config = {
    "num_epochs": 3,
    "batch_size": 1,                    # ← NOVO VALOR
    "gradient_accumulation": 4,         # ← NOVO VALOR
    "learning_rate": 0.0002,            # ← NOVO VALOR (ou 2e-4)
    "max_seq_length": 256,              # ← NOVO VALOR
    "warmup_steps": 50,                 # ← NOVO VALOR
    "save_steps": 100,
    "eval_steps": 100,
    "log_steps": 10,
    "lora_parameters_path": CHECKPOINTS_DIR / "adapters.safetensors",
    "model_path": OUTPUT_DIR / "mistral-7b-farense-qlora",
}
```

---

## Mapeamento de Valores

Se o `learning_rate` está em notação científica no recomendado:

| Notação | Decimal |
|---------|---------|
| `1e-4` | `0.0001` |
| `2e-4` | `0.0002` |
| `3e-4` | `0.0003` |
| `5e-4` | `0.0005` |

Ambas as formas funcionam no Python! Escolha a que preferir.

---

## Passo 5: Executar o Notebook

Depois de atualizar a configuração:

1. **Clicar em "Run All"** (executar todas as células)
   ou
2. **Executar célula a célula** pressionando `Shift + Enter`

---

## Passo 6: Monitorar Progresso (Terminal Separada)

Enquanto o notebook está executando, abra **uma terminal DIFERENTE**:

```bash
python3 scripts/monitor.py --refresh 5
```

Isto mostra em tempo real:
- Loss de treino e validação
- Uso de memória
- Checkpoint atual
- ETA até conclusão

---

## Dicas Importantes

### ✓ O Que Deve Fazer

- ✓ Atualizar APENAS os valores indicados
- ✓ Deixar os outros parâmetros como estão
- ✓ Salvar o notebook após editar (Ctrl+S ou Cmd+S)
- ✓ Executar o notebook de cima para baixo (order importa)
- ✓ Monitorar em terminal separada durante treino

### ✗ O Que NÃO Deve Fazer

- ✗ Editar outras seções do notebook
- ✗ Mudar ordem das células
- ✗ Remover células
- ✗ Editar as seções de MLX ou modelo
- ✗ Executar células fora de ordem

---

## Se Der Erro

### Erro: "NameError: name 'training_config' is not defined"

**Causa:** Célula de configuração não foi executada.

**Solução:**
1. Voltar para a célula de configuração
2. Pressionar `Shift + Enter` para executar
3. Tentar novamente

### Erro: "Out of Memory"

**Causa:** Configuração ainda está muito pesada.

**Solução:**
1. Reduzir `batch_size` mais: `1 → 1`
2. Aumentar `gradient_accumulation`: `4 → 8`
3. Reduzir `max_seq_length`: `256 → 128`
4. Executar novamente

### Erro: "Module not found"

**Causa:** Dependências não estão instaladas.

**Solução:**
```bash
pip install mlx mlx-lm transformers
```

---

## Exemplo Prático Completo

### Seu Preflight Check retornou:

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

### Seu Notebook Antes:

```python
training_config = {
    "num_epochs": 3,
    "batch_size": 4,
    "gradient_accumulation": 2,
    "learning_rate": 5e-4,
    "max_seq_length": 512,
    "warmup_steps": 100,
    ...
}
```

### Seu Notebook Depois:

```python
training_config = {
    "num_epochs": 3,
    "batch_size": 2,                    # ← MUDOU
    "gradient_accumulation": 2,         # ← OK (igual)
    "learning_rate": 0.0003,            # ← MUDOU (era 5e-4)
    "max_seq_length": 512,              # ← OK (igual)
    "warmup_steps": 50,                 # ← MUDOU
    ...
}
```

---

## Checklist Antes de Executar

- [ ] Executei `python3 scripts/preflight_check.py`
- [ ] Abri `checkpoints_qlora/recommended_config.json`
- [ ] Abri o notebook `notebooks/mistral_qlora_training.ipynb`
- [ ] Encontrei a seção "Configuração do Treino"
- [ ] Atualizei todos os valores com os recomendados
- [ ] Verifiquei que os valores estão corretos
- [ ] Salvei o notebook (Cmd+S)
- [ ] Tenho terminal separada pronta para monitorar
- [ ] Fechei outras aplicações pesadas
- [ ] Tenho internet estável

---

## Próximos Passos

1. ✅ Atualizar configuração (este documento)
2. ⬜ Executar notebook (Shift+Enter ou "Run All")
3. ⬜ Monitorar em terminal separada (`python3 scripts/monitor.py`)
4. ⬜ Aguardar conclusão (2-3 horas)
5. ⬜ Visualizar resultados (`python3 scripts/visualization.py --report`)
6. ⬜ Testar modelo (`python3 scripts/inference_qlora.py "pergunta"`)

---

## Suporte

Se tiver dúvidas:

1. Ver `README_PREFLIGHT.md` para explicação dos parâmetros
2. Ver `SAFE_TRAIN_QUICK_START.md` para workflow completo
3. Consultar `docs/troubleshooting/QLORA_TROUBLESHOOTING.md` para problemas comuns
4. Executar `python3 scripts/diagnose_qlora.py` para diagnóstico detalhado

---

**Boa sorte com o treino!** 🚀
