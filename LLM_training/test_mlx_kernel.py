#!/usr/bin/env python3
"""
Script para testar se o kernel MLX está configurado corretamente
Executa antes de usar o notebook
"""

import sys
import json
from pathlib import Path

print("\n" + "="*80)
print("🔍 TESTE DO KERNEL MLX PARA JUPYTER")
print("="*80 + "\n")

# 1. Verificar Python
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"✅ Python:              {python_version}")
print(f"   └─ Localização:     {sys.executable}")

if sys.version_info < (3, 10):
    print(f"   ⚠️  Aviso: Python 3.10+ recomendado")

# 2. Verificar MLX
print(f"\n Verificando MLX...")
try:
    import mlx
    mlx_version = mlx.__version__ if hasattr(mlx, '__version__') else "desconhecido"
    print(f"✅ MLX:                 {mlx_version}")

    import mlx.core as mx
    device = mx.default_device()
    print(f"✅ Device:              {device}")

    if "gpu" in str(device).lower():
        print(f"   └─ 🎮 GPU Metal ativo (aceleração Apple Silicon)")
    else:
        print(f"   └─ ⚠️  CPU apenas (sem GPU)")
except ImportError as e:
    print(f"❌ MLX:                 NÃO INSTALADO")
    print(f"   └─ Erro: {e}")
    print(f"\n   Para instalar:")
    print(f"   source mlx_kernel_env/bin/activate")
    print(f"   pip install mlx --upgrade")

# 3. Verificar dependências
print(f"\n 📦 Dependências adicionais...")
dependencies = {
    'transformers': 'Tokenizadores e modelos',
    'numpy': 'Cálculos numéricos',
    'pandas': 'Processamento de dados',
    'matplotlib': 'Visualização',
    'seaborn': 'Gráficos avançados',
    'ipykernel': 'Kernel Jupyter'
}

missing = []
for pkg, description in dependencies.items():
    try:
        __import__(pkg)
        print(f"✅ {pkg:.<20} {description}")
    except ImportError:
        print(f"❌ {pkg:.<20} {description}")
        missing.append(pkg)

if missing:
    print(f"\n   ⚠️  Pacotes em falta: {', '.join(missing)}")
    print(f"   Para instalar:")
    print(f"   source mlx_kernel_env/bin/activate")
    print(f"   pip install {' '.join(missing)}")

# 4. Verificar ficheiros de dados
print(f"\n 📁 Ficheiros de dados...")
data_dir = Path("data")
if data_dir.exists():
    files = list(data_dir.glob("*.jsonl"))
    print(f"✅ Diretório data/     {len(files)} ficheiros JSONL")
    for f in files[:3]:
        size = f.stat().st_size / (1024**2)
        print(f"   └─ {f.name:.<30} {size:.1f} MB")
    if len(files) > 3:
        print(f"   └─ ... e {len(files)-3} mais")
else:
    print(f"⚠️  Diretório data/     NÃO ENCONTRADO")

# 5. Verificar modelo base
print(f"\n 🧠 Modelo base...")
models_dir = Path("models/mistral-7b-4bit")
if models_dir.exists():
    model_files = list(models_dir.glob("*"))
    print(f"✅ Modelo Mistral-7B   Encontrado")
    for f in model_files:
        size = f.stat().st_size / (1024**3)
        print(f"   └─ {f.name:.<30} {size:.1f} GB")
else:
    print(f"⚠️  Modelo Mistral-7B   NÃO ENCONTRADO")
    print(f"   └─ Procurado em: {models_dir}")

# 6. Resumo
print(f"\n" + "="*80)
print("✅ STATUS GERAL: PRONTO PARA USO" if not missing else "⚠️  STATUS: COM AVISOS")
print("="*80)

print(f"""
📋 Próximos passos:

1. No Jupyter Lab/Notebook:
   - Clica no kernel (canto superior direito)
   - Seleciona "MLX + PyTorch (Python 3.13)"
   - Executa as células do notebook

2. Se algo não funcionou:
   - Verifica os avisos acima
   - Executa: source mlx_kernel_env/bin/activate
   - Reinstala: pip install mlx --upgrade

3. Para debugar:
   - Executa este script novamente
   - Verifica se MLX e Device estão ✅

Boa sorte com o treino! 🚀
""")

print("="*80 + "\n")
