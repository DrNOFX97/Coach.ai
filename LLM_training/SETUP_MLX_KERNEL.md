# Setup MLX Kernel para Jupyter

## ✅ O que foi feito

1. **Criado venv novo** com Python 3.13
2. **Instalado MLX 0.29.4** (versão mais recente)
3. **Registado kernel Jupyter** chamado `mlx_pytorch`

## 🎯 Como usar

### Opção 1: No Jupyter Lab (Recomendado)

1. Abre o notebook no Jupyter
2. No canto superior direito, clica no seletor de kernel
3. Seleciona **"MLX + PyTorch (Python 3.13)"**
4. Clica em "Select"
5. Pronto! O notebook agora vai usar MLX

### Opção 2: Na linha de comando

```bash
# Entrar no venv
source mlx_kernel_env/bin/activate

# Verificar MLX
python3 -c "import mlx.core as mx; print(f'Device: {mx.default_device()}')"

# Lancar Jupyter com este kernel
jupyter notebook --ip=127.0.0.1
```

## 🔍 Verificação

O erro que tinhas era:
```
✅ Python:        3.10.14
✅ MLX:           unknown
```

**Causa:** O kernel do Jupyter era da versão antiga (3.10.14) que não tinha MLX

**Solução:** Agora tens um kernel novo (3.13) com MLX 0.29.4 instalado

## 📋 Informações do Kernel

```
Nome no Jupyter:     MLX + PyTorch (Python 3.13)
Nome interno:        mlx_pytorch
Localização:         /Users/f.nuno/Library/Jupyter/kernels/mlx_pytorch
Python:              3.13.5
MLX:                 0.29.4
Device:              GPU (Apple Silicon Metal)
```

## 🛠️ Se precisares reinstalar

```bash
# Ativar venv
source mlx_kernel_env/bin/activate

# Reinstalar MLX
pip install --upgrade mlx

# Verificar
python3 -c "import mlx; print(mlx.__version__)"
```

## ✨ Próximo passo

No Jupyter, vai ver que agora:
- ✅ Python versão correta (3.13)
- ✅ MLX reconhecido e funcional
- ✅ GPU Metal disponível e ativo
- ✅ Pronto para treino!

