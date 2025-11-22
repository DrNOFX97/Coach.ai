#  Troubleshooting - Guia de Resolução de Problemas

Este documento descreve erros comuns encontrados durante a configuração e execução dos scripts de treino, juntamente com as suas respetivas soluções.

---

### 1. Erro: `SyntaxError: f-string: unmatched '['`

Este erro ocorre quando se tenta aceder a um dicionário com chaves de string (ex: `config["key"]`) dentro de uma f-string que também usa aspas duplas.

**Exemplo do Erro:**

```python
# Erro: Aspas duplas dentro de aspas duplas
print(f"O valor é {my_dict["key"]}") 
```

**Causa:**
O interpretador Python confunde as aspas duplas da chave do dicionário com o final da f-string, resultando num erro de sintaxe.

**Solução:**
Utilize aspas simples para a chave do dicionário se a f-string estiver a usar aspas duplas (ou vice-versa).

**Exemplo da Correção:**

```python
# Correto: Usar aspas simples dentro da f-string
print(f"O valor é {my_dict['key']}")

# Alternativa: Guardar numa variável antes
key_value = my_dict["key"]
print(f"O valor é {key_value}")
```

---


### 2. Erro: `SyntaxError: invalid syntax` (com `::` no final da linha)

Este é um erro de digitação simples que pode ocorrer no final de uma declaração de `for`, `if`, `def`, ou `class`.

**Exemplo do Erro:**

```python
for i in range(10)::  # Erro: Dois-pontos a mais
    print(i)
```

**Causa:**
A sintaxe do Python exige apenas um único dois-pontos (`:`) para iniciar um bloco de código.

**Solução:**
Remova o dois-pontos extra.

**Exemplo da Correção:**

```python
for i in range(10):  # Correto: Apenas um dois-pontos
    print(i)
```

---


### 3. Erro: `ImportError: cannot import name 'LoRA' from 'mlx_lm.lora'`

Este erro indica que a estrutura da biblioteca `mlx-lm` mudou e a classe `LoRA` (ou outras) já não se encontra no caminho de importação especificado.

**Causa:**
As bibliotecas evoluem e as suas APIs podem mudar entre versões. Na versão `0.28.3` do `mlx-lm`, as classes como `LoRA` e `Model` foram movidas para dentro de `mlx_lm.models`.

**Solução:**
Atualize os caminhos de importação para refletir a estrutura da versão instalada da biblioteca.

**Exemplo da Correção:**

```python
# Antigo (e incorreto para a v0.28.3)
# from mlx_lm.lora import LoRA, Model, KVCache

# Novo (e correto para a v0.28.3)
from mlx_lm.models.lora import LoRA
from mlx_lm.models.model import Model, KVCache
```

---


### 4. Erro: `TypeError: load() got an unexpected keyword argument 'q_config'`

Este erro é o mais crítico e indica uma mudança fundamental no fluxo de trabalho para aplicar QLoRA na versão `0.28.3` do `mlx-lm`.

**Causa:**
A função `mlx_lm.load()` já não aceita o argumento `q_config` para realizar a quantização e o carregamento do modelo num único passo. O processo foi dividido em duas fases distintas: pré-quantização e treino.

**Solução:**
O fluxo de trabalho deve ser ajustado da seguinte forma:

**Passo 1: Pré-Quantizar o Modelo (uma única vez, via terminal)**
Antes de executar o script de treino, converta e quantize o modelo base do Hugging Face para o formato MLX.

```bash
# Exemplo de comando para quantizar o Mistral-7B
python -m mlx_lm.convert \
    --hf-path mistralai/Mistral-7B-v0.1 \
    --q-bits 4 \
    --q-group-size 64 \
    --output-path models/mistral-7b-v0.1-4bit-mlx
```

**Passo 2: Atualizar o Script de Treino**
Modifique o script para:
a. Apontar para o diretório do modelo local pré-quantizado.
b. Carregar o modelo sem o argumento `q_config`.
c. Aplicar a configuração LoRA programaticamente após o carregamento.

**Exemplo da Correção no Script:**

```python
# 1. Atualizar o nome do modelo para o caminho local
model_name = "models/mistral-7b-v0.1-4bit-mlx" # Aponta para o modelo pré-quantizado

# ... (resto da configuração)

def train():
    # ...

    # 2. Carregar o modelo sem q_config
    model, tokenizer = load(model_name)
    
    # 3. Aplicar a configuração LoRA ao modelo já carregado
    model = LoRA.from_model(model, **qlora_config)
    
    print("Modelo pré-quantizado carregado e LoRA aplicado.")
    
    # ... (continuar com o resto do script de treino)
```

---


### 5. Erros: `ImportError` e `TypeError` com `linear_to_lora_layers`

Após corrigir o fluxo de QLoRA, uma série de erros pode surgir ao tentar aplicar os adaptadores LoRA ao modelo. Isto deve-se a mudanças na API da função `linear_to_lora_layers` na versão `0.28.3` do `mlx-lm`.

**Sintomas:**
- `ImportError: cannot import name 'LoRA' from 'mlx_lm.tuner.lora'`
- `AttributeError: module 'mlx_lm.tuner.lora' has no attribute 'LoRA'`
- `TypeError: linear_to_lora_layers() got an unexpected keyword argument 'quantization'`
- `TypeError: linear_to_lora_layers() got an unexpected keyword argument 'lora_rank'`
- `TypeError: linear_to_lora_layers() got an unexpected keyword argument 'bias'`

**Causa:**
A investigação (usando `grep` e pesquisa web) revelou que a abordagem `LoRA.from_model` está incorreta para esta versão. A função correta é `mlx_lm.tuner.linear_to_lora_layers`, mas a sua assinatura não é trivial. Ela espera uma estrutura de configuração específica e não aceita argumentos de quantização ou `bias` diretamente.

**Solução:**
A solução envolve duas etapas: reestruturar a configuração do LoRA e chamar a função com os argumentos corretos.

**1. Reestruturar a Configuração:**
O dicionário de configuração deve ter uma chave `num_layers` e um sub-dicionário `lora_parameters` que contém `rank`, `scale` (em vez de `lora_alpha`), `dropout` e `keys` (em vez de `target_modules`).

```python
# Estrutura de configuração CORRETA
qlora_config = {
    "quantization": "int4",
    "group_size": 64,
    "num_layers": 8,  # Número de camadas a adaptar
    "lora_parameters": {
        "rank": 8,
        "scale": 16,      # Equivalente a lora_alpha
        "dropout": 0.0,
        "keys": ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    },
    "bias": "none", # O bias é mantido aqui mas não é passado para a função
}
```

**2. Chamar a Função Corretamente:**
A função `linear_to_lora_layers` espera o modelo, o número de camadas e o dicionário de parâmetros LoRA.

```python
from mlx_lm.tuner import linear_to_lora_layers

# ...

# Criar uma config apenas com os parâmetros relevantes
lora_only_config = {
    k: v for k, v in qlora_config.items() 
    if k not in ["quantization", "group_size"]
}

# Chamar a função com a assinatura correta
model = linear_to_lora_layers(
    model,
    lora_only_config["num_layers"],
    lora_only_config["lora_parameters"],
)
```

Ao seguir este guia, deverá ser capaz de diagnosticar e resolver os problemas mais comuns relacionados com a configuração do ambiente e as atualizações da biblioteca `mlx-lm`.