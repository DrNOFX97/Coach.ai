# Guia Completo: Fine-Tuning de LLM com MLX no MacBook Pro M1

## 📋 Índice
1. [Introdução e Limitações do M1](#introdução)
2. [Preparação do Ambiente](#preparação)
3. [Preparação dos Dados](#dados)
4. [Escolha e Download do Modelo](#modelo)
5. [Processo de Fine-Tuning](#fine-tuning)
6. [Otimizações e Boas Práticas](#otimizações)
7. [Testes e Validação](#testes)
8. [Troubleshooting](#troubleshooting)

---

## 1. Introdução e Limitações do M1 {#introdução}

### Limitações do MacBook Pro M1 (16GB RAM)
- **Memória Unificada**: 16GB (partilhada entre CPU e GPU)
- **Modelos Recomendados para 16GB**: 
  - ✅ 7B parâmetros: IDEAL (ex: Mistral-7B, Llama-3.1-8B)
  - ✅ 3B parâmetros: muito confortável, mas subutilizado
  - ⚠️ 13B+: possível com 4-bit, mas arriscado
- **Tempo de Treino**: 
  - 7B model: ~2-5 horas para 1000 iterações
  - Com os teus dados: estima 3-6 horas total
- **Quantização**: 4-bit recomendado, 8-bit também viável

### Vantagens do MLX
- Otimizado para chips Apple Silicon
- Gestão eficiente de memória unificada
- Suporte nativo para quantização
- API similar ao PyTorch

---

## 2. Preparação do Ambiente {#preparação}

### Instalação do Python e Dependências

```bash
# Verificar versão do Python (recomendado: 3.9+)
python3 --version

# Criar ambiente virtual
python3 -m venv mlx_env
source mlx_env/bin/activate

# Instalar MLX e dependências
pip install mlx mlx-lm
pip install numpy pandas transformers datasets
pip install huggingface-hub
pip install tqdm

# Verificar instalação
python -c "import mlx.core as mx; print(mx.metal.is_available())"
```

### Estrutura de Pastas

```bash
mkdir -p ~/mlx-finetuning/{data,models,outputs,logs}
cd ~/mlx-finetuning
```

---

## 3. Preparação dos Dados {#dados}

### Formato dos Dados de Treino

Para o seu caso (livros + quadro de resultados + biografias), organize assim:

```python
# prepare_data.py
import json
import pandas as pd

# Estrutura de cada exemplo de treino
training_examples = []

# Exemplo 1: Conteúdo dos livros
book_example = {
    "text": "## Capítulo sobre [Tema]\n\n[Conteúdo do livro...]\n\n### Contexto\n[Informação relevante...]"
}

# Exemplo 2: Quadro de resultados
results_example = {
    "text": "Classificação da temporada 2023:\n1. Equipa A - 85 pontos\n2. Equipa B - 78 pontos\n[...]"
}

# Exemplo 3: Biografias
bio_example = {
    "text": "## Biografia de [Nome]\n\nNascido em [data], [Nome] é conhecido por [...]\n\n### Carreira\n[Detalhes...]"
}

training_examples.extend([book_example, results_example, bio_example])

# Guardar em formato JSONL (recomendado)
with open('data/train.jsonl', 'w', encoding='utf-8') as f:
    for example in training_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')
```

### Processamento de Texto dos Livros

```python
# process_books.py
def process_book(book_path):
    with open(book_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dividir em chunks (importante para memória limitada)
    chunk_size = 2048  # tokens aproximados
    chunks = []
    
    paragraphs = content.split('\n\n')
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size * 4:  # ~4 chars por token
            current_chunk += para + "\n\n"
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append({"text": current_chunk.strip()})
    
    return chunks

# Processar ambos os livros
book1_chunks = process_book('data/livro1.txt')
book2_chunks = process_book('data/livro2.txt')
```

### Formato Ideal para Instrução + Resposta

```python
# Para treino tipo instruction-following
def create_instruction_format(text, instruction_type):
    formats = {
        "resumo": {
            "instruction": "Resume o seguinte texto:",
            "input": text[:500],  # Primeiros 500 chars
            "output": text  # Texto completo
        },
        "pergunta": {
            "instruction": "Com base nas informações fornecidas, responde:",
            "input": f"Informação: {text}\n\nPergunta: [gerar perguntas relevantes]",
            "output": "[resposta baseada no texto]"
        }
    }
    
    return {
        "text": f"### Instrução:\n{formats[instruction_type]['instruction']}\n\n### Contexto:\n{formats[instruction_type]['input']}\n\n### Resposta:\n{formats[instruction_type]['output']}"
    }
```

---

## 4. Escolha e Download do Modelo {#modelo}

### Modelos Recomendados para M1 com 16GB RAM

**Opção 1 (RECOMENDADA): Modelos 7B-8B em 4-bit**
- ✅ `mlx-community/Mistral-7B-Instruct-v0.3-4bit` - Excelente para português
- ✅ `mlx-community/Llama-3.1-8B-Instruct-4bit` - Muito bom overall
- ✅ `mlx-community/Qwen2.5-7B-Instruct-4bit` - Ótimo para multilingual

**Opção 2: Modelos 7B em 8-bit (mais qualidade, mais lento)**
- `mlx-community/Mistral-7B-Instruct-v0.3` (sem quantização)
- Usa ~12-14GB, deixa pouca margem

**Opção 3: Modelos maiores 13B (experimental)**
- ⚠️ `mlx-community/Llama-3.1-13B-4bit` - Possível mas no limite
- Não recomendado para fine-tuning, apenas inferência

### Download do Modelo

```bash
# Usando MLX (recomendado)
mlx_lm.convert --hf-path mlx-community/Mistral-7B-Instruct-v0.3-4bit \
               --mlx-path models/mistral-7b-4bit

# Ou via Python
python -c "
from mlx_lm import load
model, tokenizer = load('mlx-community/Mistral-7B-Instruct-v0.3-4bit')
"
```

---

## 5. Processo de Fine-Tuning {#fine-tuning}

### Script de Fine-Tuning Básico

```python
# finetune.py
import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from mlx_lm import load, generate
from mlx_lm.tuner import train
import json

# Configurações para M1
CONFIG = {
    "model": "mlx-community/Mistral-7B-Instruct-v0.3-4bit",
    "train_data": "data/train.jsonl",
    "val_data": "data/val.jsonl",
    "adapter_file": "outputs/adapters.npz",
    
    # Parâmetros otimizados para M1
    "batch_size": 1,  # Crítico para memória limitada
    "iters": 1000,
    "learning_rate": 1e-5,
    "steps_per_report": 10,
    "steps_per_eval": 100,
    "val_batches": 10,
    "save_every": 100,
    
    # LoRA settings (eficiente em memória)
    "lora_layers": 16,
    "lora_rank": 8,
    "lora_alpha": 16,
    "lora_dropout": 0.0,
}

def load_data(path):
    """Carrega dados JSONL"""
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def main():
    print("🚀 Iniciando fine-tuning...")
    print(f"📊 Memória disponível: {mx.metal.get_active_memory() / 1e9:.2f} GB")
    
    # Carregar modelo
    print("📥 Carregando modelo...")
    model, tokenizer = load(CONFIG["model"])
    
    # Carregar dados
    train_data = load_data(CONFIG["train_data"])
    val_data = load_data(CONFIG["val_data"])
    
    print(f"📚 Dados de treino: {len(train_data)} exemplos")
    print(f"📚 Dados de validação: {len(val_data)} exemplos")
    
    # Treinar com LoRA
    print("🔧 Iniciando treino com LoRA...")
    train(
        model=model,
        tokenizer=tokenizer,
        data=train_data,
        val_data=val_data,
        **CONFIG
    )
    
    print("✅ Fine-tuning concluído!")

if __name__ == "__main__":
    main()
```

### Usar o Script MLX-LM (Mais Simples)

```bash
# Método mais direto usando mlx_lm
mlx_lm.lora \
    --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
    --train \
    --data data \
    --batch-size 1 \
    --iters 1000 \
    --learning-rate 1e-5 \
    --lora-layers 16 \
    --adapter-path outputs/adapters
```

---

## 6. Otimizações e Boas Práticas para 16GB RAM {#otimizações}

### Vantagens de Ter 16GB

Com 16GB tens espaço confortável para:
- ✅ Batch size de 2-4 (treino mais rápido)
- ✅ LoRA rank maior (melhor qualidade)
- ✅ Sequências até 2048 tokens
- ✅ Modelos 7B-8B sem stress
- ✅ Testar modelo durante treino sem crashar

### Gestão de Memória

```python
# monitor_memory.py
import mlx.core as mx
import psutil
import os

def print_memory_stats():
    """Monitoriza uso de memória"""
    # Memória Metal (GPU)
    metal_mem = mx.metal.get_active_memory() / 1e9
    metal_peak = mx.metal.get_peak_memory() / 1e9
    
    # Memória sistema
    process = psutil.Process(os.getpid())
    system_mem = process.memory_info().rss / 1e9
    
    print(f"""
    📊 Estatísticas de Memória:
    ├─ Metal (GPU): {metal_mem:.2f} GB (pico: {metal_peak:.2f} GB)
    └─ Sistema: {system_mem:.2f} GB
    """)

# Chamar periodicamente durante treino
print_memory_stats()
```

### Técnicas de Otimização

```python
# optimization_tips.py

# 1. Gradient Checkpointing (reduz memória)
CONFIG["grad_checkpoint"] = True

# 2. Gradient Accumulation (simula batches maiores)
CONFIG["gradient_accumulation_steps"] = 4

# 3. Mixed Precision (já incluído no 4bit)
# Modelos 4bit já usam quantização

# 4. Truncar sequências longas
def truncate_text(text, max_length=2048):
    tokens = tokenizer.encode(text)
    if len(tokens) > max_length:
        tokens = tokens[:max_length]
    return tokenizer.decode(tokens)

# 5. Liberar memória entre batches
def clear_memory():
    mx.metal.clear_cache()
    import gc
    gc.collect()
```

### Configurações Recomendadas para 16GB RAM

```python
# Configuração OTIMIZADA para M1 16GB
CONFIG_16GB_OPTIMIZED = {
    # Modelo e dados
    "model": "mlx-community/Mistral-7B-Instruct-v0.3-4bit",
    "train_data": "data/train.jsonl",
    "val_data": "data/val.jsonl",
    
    # Fine-tuning parameters (aproveitando os 16GB)
    "batch_size": 2,  # Podes usar 2 confortavelmente!
    "iters": 2000,  # Mais iterações = melhor resultado
    "learning_rate": 2e-5,
    "steps_per_report": 20,
    "steps_per_eval": 200,
    "val_batches": 25,
    "save_every": 200,
    
    # LoRA settings (otimizado para 16GB)
    "lora_layers": 32,  # Mais layers = melhor aprendizagem
    "lora_rank": 16,  # Maior rank = mais capacidade
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    
    # Sequence length
    "max_seq_length": 2048,  # Sequências mais longas OK
    
    # Memory optimization
    "grad_checkpoint": True,
    "gradient_accumulation_steps": 2,  # Simula batch_size=4
}

# Configuração CONSERVADORA (se tiveres problemas)
CONFIG_16GB_SAFE = {
    "batch_size": 1,
    "lora_rank": 8,
    "lora_layers": 16,
    "max_seq_length": 1536,
    "gradient_accumulation_steps": 4,
}

# Configuração AGRESSIVA (máximo desempenho)
CONFIG_16GB_AGGRESSIVE = {
    "batch_size": 4,  # Arriscado mas possível
    "lora_rank": 32,
    "lora_layers": 48,  # Quase todas as layers
    "max_seq_length": 2048,
    "gradient_accumulation_steps": 1,
}
```

---

## 7. Testes e Validação {#testes}

### Script de Teste

```python
# test_model.py
from mlx_lm import load, generate

# Carregar modelo base + adaptadores
model, tokenizer = load(
    "mlx-community/Mistral-7B-Instruct-v0.3-4bit",
    adapter_path="outputs/adapters"
)

# Exemplos de teste
test_prompts = [
    "Resume o capítulo 3 do primeiro livro:",
    "Quais foram os resultados da temporada 2023?",
    "Fala-me sobre a biografia de [Nome]:",
]

for prompt in test_prompts:
    print(f"\n{'='*60}")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}")
    
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=500,
        temp=0.7,
    )
    
    print(f"Resposta: {response}")
```

### Métricas de Avaliação

```python
# evaluate.py
from sklearn.metrics import accuracy_score
import numpy as np

def evaluate_model(model, tokenizer, test_data):
    predictions = []
    references = []
    
    for example in test_data:
        pred = generate(model, tokenizer, example["input"])
        predictions.append(pred)
        references.append(example["output"])
    
    # Calcular perplexidade (opcional)
    perplexity = calculate_perplexity(model, test_data)
    
    print(f"Perplexidade: {perplexity:.2f}")
    
    return predictions, references
```

---

## 8. Troubleshooting {#troubleshooting}

### Problemas Comuns

#### 1. Erro de Memória Insuficiente

```bash
# Soluções:
# - Reduzir batch_size para 1
# - Reduzir lora_rank para 4
# - Reduzir max_seq_length para 512-1024
# - Usar modelo menor (3B em vez de 7B)
# - Fechar todas as outras aplicações
```

#### 2. Treino Muito Lento

```python
# Otimizações:
# - Reduzir número de exemplos de treino
# - Aumentar steps_per_report
# - Usar dados pré-processados
# - Ativar Activity Monitor para verificar uso de recursos
```

#### 3. Modelo Não Aprende

```python
# Verificações:
# - Learning rate muito baixo/alto (testar 1e-4 a 1e-6)
# - Dados insuficientes (mínimo 100-500 exemplos)
# - Formato de dados incorreto
# - LoRA layers muito poucas (aumentar para 16-32)
```

#### 4. Respostas Inconsistentes

```python
# Soluções:
# - Aumentar número de iterações (iters)
# - Melhorar qualidade dos dados
# - Usar exemplos mais diversos
# - Ajustar temperatura durante inferência (0.5-0.9)
```

---

## 📌 Checklist Final

Antes de começar:
- [ ] Python 3.9+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] MLX e dependências instaladas
- [ ] Dados preparados em formato JSONL
- [ ] Modelo escolhido e baixado
- [ ] Pelo menos 50% de memória livre no sistema
- [ ] Backup dos dados originais

Durante o treino:
- [ ] Monitorizar uso de memória
- [ ] Verificar loss está a diminuir
- [ ] Guardar checkpoints regularmente
- [ ] Testar modelo periodicamente

Após o treino:
- [ ] Validar com exemplos reais
- [ ] Comparar com modelo base
- [ ] Guardar adaptadores finais
- [ ] Documentar hiperparâmetros usados

---

## 🔗 Recursos Úteis

- [MLX Documentation](https://ml-explore.github.io/mlx/)
- [MLX Examples](https://github.com/ml-explore/mlx-examples)
- [Hugging Face MLX Community](https://huggingface.co/mlx-community)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

---

## 💡 Dicas Finais

1. **Comece pequeno**: Teste com 10-20 exemplos primeiro
2. **Documente tudo**: Guarde notas sobre cada experiência
3. **Seja paciente**: Fine-tuning no M1 leva tempo (horas/dias)
4. **Valide frequentemente**: Teste o modelo a cada 100 passos
5. **Use quantização**: 4-bit é essencial para M1
6. **Prepare dados com cuidado**: Qualidade > Quantidade
7. **Monitorize temperatura**: Use Activity Monitor para evitar throttling
8. **Backups**: Guarde versões dos adaptadores regularmente

Boa sorte com o seu fine-tuning! 🚀