import nbformat as nbf

# Create a new notebook object
nb = nbf.v4.new_notebook()


# Create a new notebook object
b = nbf.v4.new_notebook()

# --- Cell 1: Title (Markdown) ---
cell1_text = """
# Treinamento Monitorado com MLX LoRA
"""
b['cells'].append(nbf.v4.new_markdown_cell(cell1_text))

# --- Cell 2: System Info (Markdown) ---
cell2_text = """
## 1. Informações do Sistema

Esta célula exibe informações sobre o sistema e as principais bibliotecas para garantir a reprodutibilidade.
"""
b['cells'].append(nbf.v4.new_markdown_cell(cell2_text))

# --- Cell 3: System Info (Code) ---
cell3_code = """
import sys
import platform
import subprocess

def get_python_version():
    return sys.version.split()[0]

def get_pip_version():
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True, check=True)
        return result.stdout.split()[1]
    except Exception:
        return 'N/A'

print("="*30)
print("INFORMAÇÕES DO SISTEMA")
print("="*30)
print(f"Sistema Operacional: {platform.system()} {platform.release()}")
print(f"Arquitetura: {platform.machine()}")
print(f"Versão do Python: {get_python_version()}")
print(f"Versão do Pip: {get_pip_version()}")
print("="*30)
"""
b['cells'].append(nbf.v4.new_code_cell(cell3_code))

# --- Cell 4: Config (Markdown) ---
cell4_text = """
## 2. Configuração dos Parâmetros de Treinamento

Nesta célula, definimos todos os parâmetros para o treinamento, como caminhos de diretórios, hiperparâmetros do modelo e configurações do LoRA.
"""
b['cells'].append(nbf.v4.new_markdown_cell(cell4_text))

# --- Cell 5: Config (Code) ---
cell5_code = """
from pathlib import Path

project_root = Path("/Users/f.nuno/Desktop/chatbot_2.0/LLM_training")
data_dir = project_root / "data"
checkpoint_dir = project_root / "checkpoints"
checkpoint_dir.mkdir(exist_ok=True)

model_path = project_root / "models/mistral-7b-4bit"

# Parâmetros de Treinamento
batch_size = 4
iters = 100
learning_rate = 1e-5
lora_layers = 4
max_seq_length = 2100
adapter_path = str(checkpoint_dir / "adapters")
val_batches = 25
val_interval = 100
save_every = 100
seed = 0

print("Parâmetros de Configuração:")
print(f"  - Diretório de dados: {data_dir}")
print(f"  - Diretório de checkpoints: {checkpoint_dir}")
print(f"  - Caminho do modelo: {model_path}")
print(f"  - Tamanho do batch: {batch_size}")
print(f"  - Iterações: {iters}")
print(f"  - Taxa de aprendizado: {learning_rate}")
"""
b['cells'].append(nbf.v4.new_code_cell(cell5_code))

# --- Cell 6: Command Build (Markdown) ---
cell6_text = """
## 3. Construção do Comando de Treinamento

Aqui, montamos o comando que será executado no terminal para iniciar o treinamento com `mlx_lm.lora`.
"""
b['cells'].append(nbf.v4.new_markdown_cell(cell6_text))

# --- Cell 7: Command Build (Code) ---
cell7_code = """
command = [
    "python", "-u", "-m", "mlx_lm", "lora",
    "--model", str(model_path),
    "--train",
    "--data", str(data_dir),
    "--batch-size", str(batch_size),
    "--iters", str(iters),
    "--learning-rate", str(learning_rate),
    "--num-layers", str(lora_layers),
    "--max-seq-length", str(max_seq_length),
    "--adapter-path", adapter_path,
    "--val-batches", str(val_batches),
    "--steps-per-eval", str(val_interval),
    "--save-every", str(save_every),
    "--seed", str(seed),
]

print("Comando a ser executado:")
print(" ".join(command))
"""
b['cells'].append(nbf.v4.new_code_cell(cell7_code))

# --- Cell 8: Execution (Markdown) ---
cell8_text = """
## 4. Execução do Treinamento

Esta célula executa o comando de treinamento e exibe a saída em tempo real.
"""
b['cells'].append(nbf.v4.new_markdown_cell(cell8_text))

# --- Cell 9: Execution (Code) ---
cell9_code = """
import subprocess
import sys

print("\n" + "="*70)
print("INICIANDO TREINAMENTO MLX_LM CLI")
print("="*70)

try:
    with subprocess.Popen(
        command, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True, 
        bufsize=1, 
        universal_newlines=True
    ) as p:
        for line in p.stdout:
            print(line, end='')

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)

    print("\n" + "="*70)
    print("TREINAMENTO MLX_LM CLI CONCLUÍDO")
    print("="*70)

except subprocess.CalledProcessError as e:
    print(f"\n\n❌ Erro durante o treinamento: {e}")
except Exception as e:
    print(f"\n\n❌ Ocorreu um erro inesperado: {e}")

print("\n✓ Processo finalizado!")
print(f"\nMétricas e adaptadores salvos em: {adapter_path}")
"""
b['cells'].append(nbf.v4.new_code_cell(cell9_code))


# --- Write the notebook to a file ---
with open('notebooks/train_with_monitoring_v2.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook 'notebooks/train_with_monitoring_v2.ipynb' created successfully.")
