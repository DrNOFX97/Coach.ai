#!/usr/bin/env python
# coding: utf-8

# # QLoRA Training - Versão Simplificada (Corrigida)
# 
# Esta versão foi reescrita para garantir que o ficheiro é um JSON válido e pode ser aberto no Jupyter. Contém o código de treino simplificado que não bloqueia.

# In[1]:


import os, json, time, gc
from pathlib import Path
print('Imports básicos OK')


# In[2]:


import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from mlx.utils import tree_flatten
from mlx_lm import load, generate
print('MLX OK')
try:
    mx.set_default_device(mx.gpu)
    print('Metal GPU OK')
except:
    print('CPU mode')


# In[3]:


PROJECT_ROOT = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training")
DATA_DIR = PROJECT_ROOT / "data"
train_file = DATA_DIR / "train_data.jsonl"
with open(train_file, 'r') as f:
    train_data = [json.loads(line) for line in f]
print(f'Dados de treino carregados: {len(train_data)} exemplos')


# In[4]:


print('A carregar o modelo base...')
model, tokenizer = load("mistralai/Mistral-7B-v0.1")
print('Modelo carregado.')


# In[ ]:


def train_simple():
    optimizer = optim.Adam(learning_rate=1e-5)
    epochs = 3
    
    print('--- INÍCIO DO TREINO SIMPLIFICADO ---')
    start_time = time.time()
    
    for epoch in range(epochs):
        total_loss = 0
        num_steps = 0
        print(f'Época {epoch + 1}/{epochs}')
        
        for i, item in enumerate(train_data):
            try:
                text = item.get('prompt', '') + item.get('completion', '')
                tokens = tokenizer.encode(text)
                if len(tokens) < 8 or len(tokens) > 256: continue

                input_ids = mx.array([tokens])
                labels = input_ids

                def loss_fn(model):
                    logits = model(input_ids)
                    return nn.losses.cross_entropy(logits[:, :-1, :], labels[:, 1:], reduction="mean")

                loss_val, grads = mx.value_and_grad(loss_fn)(model)
                optimizer.update(model, grads)
                mx.eval(model.parameters(), optimizer.state)

                total_loss += loss_val.item()
                num_steps += 1

                if num_steps > 0 and num_steps % 20 == 0:
                    print(f'  Passo {num_steps} - Loss: {total_loss / num_steps:.4f}')
            except Exception as e:
                print(f'Erro no passo {i}: {e}')
    
    print(f'--- TREINO COMPLETO --- ({time.time() - start_time:.1f}s)')

train_simple()

