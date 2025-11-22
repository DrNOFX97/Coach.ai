#!/usr/bin/env python3
"""
Diagnóstico QLoRA - Identifica problemas com treino
"""

import sys
import json
from pathlib import Path

print("=" * 70)
print("DIAGNÓSTICO QLORA - Identificar Problemas")
print("=" * 70)

# 1. Verificar Python
print("\n1. Verificando Python...")
print(f"   Versão: {sys.version}")
if sys.version_info < (3, 11):
    print("   ⚠ Aviso: Python 3.11+ recomendado")
else:
    print("   ✓ OK")

# 2. Verificar MLX
print("\n2. Verificando MLX...")
try:
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    from mlx_lm import load, generate
    print("   ✓ MLX carregado")
except ImportError as e:
    print(f"   ✗ Erro: {e}")
    print("   Solução: pip install mlx mlx-lm mlx-data")
    sys.exit(1)

# 3. Verificar M1 Mac
print("\n3. Verificando Hardware...")
import platform
machine = platform.machine()
if machine == "arm64":
    print("   ✓ Mac M1/M2/M3 detectado")
else:
    print(f"   ⚠ Aviso: {machine} (não é M1)")

# 4. Verificar Metal GPU
print("\n4. Verificando Metal GPU...")
try:
    mx.set_default_device(mx.gpu)
    print("   ✓ Metal GPU ativado")
except:
    print("   ⚠ Metal GPU não disponível (usará CPU)")

# 5. Verificar dados
print("\n5. Verificando dados...")
data_dir = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/data")
train_file = data_dir / "train_data.jsonl"
val_file = data_dir / "val_data.jsonl"

if train_file.exists():
    with open(train_file) as f:
        train_count = sum(1 for _ in f)
    print(f"   ✓ train_data.jsonl: {train_count} exemplos")
else:
    print("   ✗ train_data.jsonl não encontrado")

if val_file.exists():
    with open(val_file) as f:
        val_count = sum(1 for _ in f)
    print(f"   ✓ val_data.jsonl: {val_count} exemplos")
else:
    print("   ✗ val_data.jsonl não encontrado")

# 6. Testar carregamento de modelo
print("\n6. Testando carregamento de modelo...")
print("   Isto pode levar alguns minutos na primeira vez...")

try:
    print("   Carregando Mistral-7B...")
    model, tokenizer = load(
        "mistralai/Mistral-7B-v0.1",
        adapter_path=None,
        quantization="int4"
    )
    print("   ✓ Modelo carregado com sucesso")

    # Testar forward pass
    print("   Testando forward pass...")
    import mlx.core as mx
    test_ids = mx.array([[1, 2, 3, 4, 5]])
    output = model(test_ids)
    print(f"   ✓ Output shape: {output.shape}")

except Exception as e:
    print(f"   ✗ Erro: {e}")
    print("   Possíveis soluções:")
    print("   - Verificar internet (primeira vez baixa 4GB)")
    print("   - Verificar espaço em disco (~5GB)")
    print("   - Aguardar download completar")

# 7. Verificar memória
print("\n7. Verificando memória...")
import psutil
mem = psutil.virtual_memory()
print(f"   Total: {mem.total / (1024**3):.1f} GB")
print(f"   Disponível: {mem.available / (1024**3):.1f} GB")
print(f"   Usado: {mem.percent}%")

if mem.available / (1024**3) < 4:
    print("   ⚠ Aviso: Menos de 4GB disponível")
else:
    print("   ✓ OK")

# 8. Testar treino básico
print("\n8. Testando treino básico...")
try:
    print("   Executando 1 step de treino...")

    optimizer = optim.Adam(learning_rate=1e-4)

    # Dados simples
    test_input = mx.array([[1, 2, 3, 4, 5, 6, 7, 8]])

    def loss_fn(model):
        logits = model(test_input)
        if logits.size > 0:
            return mx.mean(logits)
        return mx.array(0.0)

    loss_val, grads = mx.value_and_grad(loss_fn)(model)
    optimizer.update(model, grads)
    mx.eval(model)

    print(f"   ✓ Treino funciona! Loss: {float(loss_val):.4f}")

except Exception as e:
    print(f"   ✗ Erro no treino: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNÓSTICO COMPLETO")
print("=" * 70)

print("\nRecomendações:")
print("1. Se tudo está ✓ verde: execute o notebook normalmente")
print("2. Se há ✗ erros: verifique as soluções acima")
print("3. Se treino não inicia: veja a seção 'Testar treino básico'")

print("\nSe ainda tiver problemas:")
print("- Reduza batch_size para 1 no notebook")
print("- Reduza max_seq_length para 256")
print("- Aumente warmup_steps para 200")
