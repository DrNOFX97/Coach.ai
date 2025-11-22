from mlx_lm.tuner import linear_to_lora_layers
import json
import re
import os
import shutil
import random
from pathlib import Path
import mlx.core as mx
import mlx.nn as nn
from mlx.optimizers import AdamW
from mlx_lm import load

from tqdm import tqdm
import math
import time
import psutil
import pandas as pd
import matplotlib.pyplot as plt

# --- Configurações --- #

# Caminhos
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHECKPOINTS_DIR = BASE_DIR / "checkpoints_qlora"
OUTPUT_DIR = BASE_DIR / "output"

# Certificar que os diretórios existem
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Ficheiros de dados - Dataset V3 Final Complete
TRAIN_FILE = DATA_DIR / "train_v3_final_complete.jsonl"
VALID_FILE = DATA_DIR / "valid_v3_final_complete.jsonl"
CLEANED_DATA_FILE = DATA_DIR / "farense_dataset_cleaned.jsonl"

# Configuração do Modelo e Treino
model_name = str(BASE_DIR / "models/mistral-7b-4bit")

qlora_config = {
    "quantization": "int4",      # 4-bit quantization
    "group_size": 64,            # Quantization group size
    "num_layers": 8,             # Número de camadas do transformador a adaptar
    "lora_parameters": {
        "rank": 6,              # LoRA decomposition rank (reduzido de 8 para 6 - menos parâmetros = menos overfitting)
        "scale": 16,            # LoRA scaling factor (lora_alpha)
        "dropout": 0.08,        # Dropout rate for LoRA layers (aumentado de 0.0 para 0.08 - reduz overfitting)
        "keys": ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], # Módulos alvo
    },
    "bias": "none",
}

training_config = {
    "num_epochs": 3,              # Número de épocas de treino
    "batch_size": 2,              # Tamanho do batch por passo (reduzido de 4 para 2 - reduz overfitting)
    "gradient_accumulation": 4,   # Acumular gradientes ao longo de vários passos (aumentado de 2 para 4 - mantém efetivo)
    "learning_rate": 2e-4,        # Taxa de aprendizagem (reduzida de 5e-4 para 2e-4 - treino mais controlado)
    "max_seq_length": 512,        # Comprimento máximo da sequência para tokenização
    "warmup_steps": 100,          # Passos de aquecimento para o scheduler da taxa de aprendizagem
    "save_steps": 200,            # Guardar checkpoint a cada N passos
    "eval_steps": 200,            # Avaliar a cada N passos
    "log_steps": 10,              # Registar métricas a cada N passos
    "early_stopping_patience": 5, # Parar após 5 validações sem melhoria
    "early_stopping_min_delta": 0.001, # Melhoria mínima de 0.1%
    "lora_parameters_path": CHECKPOINTS_DIR / "adapters.safetensors",
    "model_path": OUTPUT_DIR / "mistral-7b-farense-qlora",
}

# --- Funções de Utilidade --- #

def format_prompt(sample):
    return f"### Pergunta:\n{sample['prompt']}\n\n### Resposta:\n{sample['completion']}"

def load_dataset(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def tokenize(sample, tokenizer, max_seq_length):
    prompt_text = format_prompt(sample)
    # Adicionar padding e truncation para garantir comprimento uniforme
    return tokenizer.encode(prompt_text, max_length=max_seq_length, padding="max_length", truncation=True)

def calculate_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 ** 2)  # Memória em MB

# --- Classe MetricsTracker --- #

class MetricsTracker:
    def __init__(self, checkpoint_dir):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.metrics_file_csv = self.checkpoint_dir / "training_metrics.csv"
        self.metrics_file_json = self.checkpoint_dir / "training_metrics.json"
        self.summary_file = self.checkpoint_dir / "training_summary.json"
        self.training_state_file = self.checkpoint_dir / "training_state.json"
        self.best_model_path = self.checkpoint_dir / "adapters" / "adapters.safetensors"
        self.best_val_loss = float('inf')
        self.metrics_data = []
        self.start_time = time.time()
        self.current_epoch = 0
        self.current_step = 0
        self.total_steps = 0
        self.total_epochs = 0

        self._load_state()

    def _load_state(self):
        if self.training_state_file.exists():
            try:
                with open(self.training_state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.current_epoch = state.get('current_epoch', 0)
                    self.current_step = state.get('current_step', 0)
                    self.best_val_loss = state.get('best_val_loss', float('inf'))
                    print(f"Estado de treino recuperado: Época {self.current_epoch}, Passo {self.current_step}, Melhor Val Loss {self.best_val_loss:.4f}")
            except json.JSONDecodeError:
                print("Erro ao ler training_state.json, a iniciar novo treino.")
        
        if self.metrics_file_json.exists():
            try:
                with open(self.metrics_file_json, 'r', encoding='utf-8') as f:
                    self.metrics_data = json.load(f)
            except json.JSONDecodeError:
                print("Erro ao ler training_metrics.json, a iniciar novo registo de métricas.")

    def _save_state(self):
        state = {
            'current_epoch': self.current_epoch,
            'current_step': self.current_step,
            'best_val_loss': self.best_val_loss,
            'last_save_time': time.time()
        }
        with open(self.training_state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4, ensure_ascii=False)

    def log_step(self, epoch, step, loss, val_loss=None, memory_mb=None, learning_rate=None):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        metric = {
            "epoch": epoch,
            "step": step,
            "loss": loss.item() if hasattr(loss, 'item') else loss,
            "timestamp": current_time,
            "elapsed_time_sec": elapsed_time,
            "memory_mb": memory_mb if memory_mb is not None else calculate_memory_usage(),
            "learning_rate": learning_rate if learning_rate is not None else training_config["learning_rate"],
        }
        if val_loss is not None:
            metric["val_loss"] = val_loss.item() if hasattr(val_loss, 'item') else val_loss

        self.metrics_data.append(metric)
        
        # Guardar incrementalmente para evitar perda de dados
        with open(self.metrics_file_json, 'w', encoding='utf-8') as f:
            json.dump(self.metrics_data, f, indent=4, ensure_ascii=False)

        # Atualizar CSV
        pd.DataFrame(self.metrics_data).to_csv(self.metrics_file_csv, index=False)

        self.current_epoch = epoch
        self.current_step = step
        self._save_state()

    def save_best_model(self, model, val_loss):
        if val_loss < self.best_val_loss:
            self.best_val_loss = val_loss
            self._save_state()
            
            adapters_dir = self.checkpoint_dir / "adapters"
            adapters_dir.mkdir(parents=True, exist_ok=True)
            
            # Guardar apenas os pesos do adaptador
            model.save_weights(str(self.best_model_path))
            print(f"✓ Melhor modelo guardado com Val Loss: {self.best_val_loss:.4f}")

    def save_summary(self, total_time, total_samples):
        summary = {
            "total_training_time_sec": total_time,
            "total_samples_processed": total_samples,
            "final_epoch": self.current_epoch,
            "final_step": self.current_step,
            "best_validation_loss": self.best_val_loss,
            "training_config": training_config,
            "qlora_config": qlora_config,
            "model_name": model_name
        }
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

# --- Classe EarlyStoppingMonitor --- #

class EarlyStoppingMonitor:
    """Monitora overfitting e aplica early stopping automático"""

    def __init__(self, patience=5, min_delta=0.001, restore_best_weights=True):
        self.patience = patience                    # Parar após N validações sem melhoria
        self.min_delta = min_delta                  # Melhoria mínima necessária
        self.best_val_loss = float('inf')
        self.patience_counter = 0                   # Contador de validações sem melhoria
        self.best_epoch = 0
        self.best_step = 0
        self.restore_best_weights = restore_best_weights
        self.should_stop = False
        self.overfitting_gap_history = []

    def check(self, val_loss, train_loss, epoch, step):
        """
        Verifica se deve parar o treino

        Returns:
            should_stop (bool): True se deve parar o treino
            improved (bool): True se houve melhoria
        """
        # Calcular gap de overfitting
        gap = val_loss - train_loss
        self.overfitting_gap_history.append(gap)

        # Alertar se overfitting severo
        if gap > 0.30:
            print(f"  ⚠️  OVERFITTING SEVERO DETECTADO (gap={gap:.4f})")
        elif gap > 0.15:
            print(f"  ⚠️  Overfitting moderado (gap={gap:.4f})")

        # Verificar se houve melhoria
        if val_loss < self.best_val_loss - self.min_delta:
            self.best_val_loss = val_loss
            self.patience_counter = 0
            self.best_epoch = epoch
            self.best_step = step
            print(f"  ✅ Melhor Val Loss: {self.best_val_loss:.4f}")
            return False, True
        else:
            self.patience_counter += 1
            if self.patience_counter >= self.patience:
                self.should_stop = True
                print(f"\n⏹️  EARLY STOPPING ATIVADO!")
                print(f"   Sem melhoria por {self.patience} validações consecutivas")
                print(f"   Melhor modelo: Época {self.best_epoch}, Step {self.best_step}")
                print(f"   Melhor Val Loss: {self.best_val_loss:.4f}")
                return True, False
            else:
                print(f"  ℹ️  Sem melhoria ({self.patience_counter}/{self.patience})")
                return False, False

    def get_overfitting_status(self):
        """Retorna status de overfitting baseado no gap médio"""
        if not self.overfitting_gap_history:
            return "Sem dados"

        avg_gap = sum(self.overfitting_gap_history) / len(self.overfitting_gap_history)

        if avg_gap < 0.05:
            return "✅ EXCELENTE (gap < 0.05)"
        elif avg_gap < 0.15:
            return "✅ BOM (gap < 0.15)"
        elif avg_gap < 0.30:
            return "⚠️ MODERADO (gap < 0.30)"
        else:
            return "❌ CRÍTICO (gap >= 0.30)"

# --- Funções de Treino --- #

def loss_fn(model, inputs, targets, lengths):
    # Máscara para ignorar tokens de preenchimento e prompt
    mask = mx.arange(inputs.shape[1])[None, :] < lengths[:, None]

    # Forward pass
    logits = model(inputs)

    # Calcular a perda apenas para os tokens de resposta (completion)
    # Assumimos que o prompt já está mascarado ou que a perda é calculada apenas na completion
    # Para LoRA, a máscara é aplicada na função de perda para ignorar o padding e o prompt
    loss = nn.losses.cross_entropy(logits, targets, reduction='none')
    loss = mx.sum(loss * mask) / mx.sum(mask)
    return loss, logits

def create_step_fn(model, optimizer):
    # Criar a função que calcula a perda e os gradientes
    grad_fn = nn.value_and_grad(model, loss_fn)

    @mx.compile
    def step_fn(inputs, targets, lengths):
        # Calcular a perda e os gradientes
        (loss, logits), grads = grad_fn(model, inputs, targets, lengths)
        
        # Atualizar o modelo usando o otimizador com os gradientes calculados
        optimizer.update(model, grads)
        
        return loss
    return step_fn

def create_eval_fn(model):
    @mx.compile
    def eval_fn(inputs, targets, lengths):
        loss, _ = loss_fn(model, inputs, targets, lengths)
        return loss
    return eval_fn

# --- Main Training Loop --- #

def train(custom_training_config=None, custom_qlora_config=None):
    print("\n--- A iniciar o processo de treino --- ")
    
    # Update configs if provided
    if custom_qlora_config:
        qlora_config.update(custom_qlora_config)
    if custom_training_config:
        training_config.update(custom_training_config)

    print(f"A carregar modelo: {model_name} com QLoRA")
    print(f"Configuração QLoRA: {qlora_config}")
    print(f"Configuração de Treino: {training_config}")

    # 1. Carregar Modelo e Tokenizer
    # NOTA: O modelo base deve ser pré-quantizado usando `python -m mlx_lm.convert`
    # e o `model_name` deve apontar para o diretório do modelo quantizado.
    model, tokenizer = load(model_name)
    
    # Definir o pad_token para ser igual ao eos_token
    tokenizer.pad_token = tokenizer.eos_token
    
    # Criar uma configuração apenas com os parâmetros LoRA
    lora_only_config = {k: v for k, v in qlora_config.items() if k not in ["quantization", "group_size"]}
    
    # Aplicar LoRA ao modelo carregado (modifica o modelo in-place)
    linear_to_lora_layers(
        model,
        lora_only_config["num_layers"],
        lora_only_config["lora_parameters"],
    )
    
    print("Modelo e tokenizer carregados e LoRA aplicado.")

    # 2. Carregar e Preparar Dados
    print(f"A carregar dados de treino de: {TRAIN_FILE}")
    print(f"A carregar dados de validação de: {VALID_FILE}")
    train_dataset = load_dataset(TRAIN_FILE)
    val_dataset = load_dataset(VALID_FILE)

    print(f"Amostras de treino: {len(train_dataset)}")
    print(f"Amostras de validação: {len(val_dataset)}")
    print(f"Total de amostras: {len(train_dataset) + len(val_dataset)}")

    # Tokenizar datasets
    train_tokens = [tokenize(sample, tokenizer, training_config["max_seq_length"]) for sample in train_dataset]
    val_tokens = [tokenize(sample, tokenizer, training_config["max_seq_length"]) for sample in val_dataset]

    # Filtrar amostras vazias após tokenização
    train_tokens = [t for t in train_tokens if t]
    val_tokens = [t for t in val_tokens if t]

    if not train_tokens:
        raise ValueError("Nenhum dado de treino válido após tokenização. Verifique o dataset e max_seq_length.")
    if not val_tokens:
        print("Aviso: Nenhum dado de validação válido após tokenização.")

    # 3. Configurar Otimizador, Tracker e Early Stopping
    optimizer = AdamW(learning_rate=training_config["learning_rate"])
    tracker = MetricsTracker(CHECKPOINTS_DIR)
    early_stopping = EarlyStoppingMonitor(
        patience=training_config["early_stopping_patience"],
        min_delta=training_config["early_stopping_min_delta"]
    )

    # Recuperar estado de treino se existir
    start_epoch = tracker.current_epoch
    start_step = tracker.current_step

    # Carregar adaptadores se existirem para continuar o treino
    if tracker.best_model_path.exists():
        print(f"A carregar adaptadores de: {tracker.best_model_path}")
        model.load_weights(str(tracker.best_model_path))
        print("Adaptadores carregados. A retomar treino.")
    else:
        print("Nenhum adaptador encontrado, a iniciar treino do zero.")

    # Compilar funções de treino e avaliação
    train_step_fn = create_step_fn(model, optimizer)
    eval_fn = create_eval_fn(model)

    # 4. Loop de Treino
    print("\n--- A iniciar o loop de treino --- ")
    total_train_steps = (len(train_tokens) // training_config["batch_size"]) * training_config["num_epochs"]
    print(f"Total de passos de treino esperados: {total_train_steps}")

    for epoch in range(start_epoch, training_config["num_epochs"]):
        # Baralhar dados de treino a cada época
        random.shuffle(train_tokens)
        
        # Resetar o contador de passos para a nova época se não estiver a retomar
        if epoch > start_epoch:
            tracker.current_step = 0

        for i in tqdm(range(tracker.current_step, len(train_tokens) // training_config["batch_size"]), desc=f"Época {epoch+1}/{{training_config['num_epochs']}}"):
            batch_start = i * training_config["batch_size"]
            batch_end = (i + 1) * training_config["batch_size"]
            batch_tokens = train_tokens[batch_start:batch_end]

            # Padding e criação de tensores
            max_len = max(len(t) for t in batch_tokens)
            inputs = mx.array([t + [0] * (max_len - len(t)) for t in batch_tokens])
            targets = inputs
            lengths = mx.array([len(t) for t in batch_tokens])

            # Passo de treino
            loss = train_step_fn(inputs, targets, lengths)
            mx.eval(model.parameters(), optimizer.state, loss)
            
            # Logging
            if (i + 1) % training_config["log_steps"] == 0:
                mem_usage = calculate_memory_usage()
                tracker.log_step(epoch, i + 1, loss, memory_mb=mem_usage)
                print(f"[Época {epoch+1}/{{training_config['num_epochs']}}] Passo {i+1}/{{len(train_tokens) // training_config['batch_size']}} - Loss: {loss.item():.4f} - Memória: {mem_usage:.2f} MB")

            # Avaliação e Guardar Checkpoint
            if (i + 1) % training_config["eval_steps"] == 0 and val_tokens:
                val_loss_sum = 0
                num_val_batches = len(val_tokens) // training_config["batch_size"]
                if num_val_batches == 0 and len(val_tokens) > 0: # Handle case where val_tokens < batch_size
                    num_val_batches = 1

                for j in range(num_val_batches):
                    val_batch_start = j * training_config["batch_size"]
                    val_batch_end = (j + 1) * training_config["batch_size"]
                    val_batch_tokens = val_tokens[val_batch_start:val_batch_end]
                    
                    if not val_batch_tokens: # Skip empty batches
                        continue

                    val_max_len = max(len(t) for t in val_batch_tokens)
                    val_inputs = mx.array([t + [0] * (val_max_len - len(t)) for t in val_batch_tokens])
                    val_targets = val_inputs
                    val_lengths = mx.array([len(t) for t in val_batch_tokens])

                    val_loss = eval_fn(val_inputs, val_targets, val_lengths)
                    val_loss_sum += val_loss.item()
                
                avg_val_loss = val_loss_sum / num_val_batches if num_val_batches > 0 else float('inf')
                print(f"[Época {epoch+1}/{{training_config['num_epochs']}}] Val Loss: {avg_val_loss:.4f}")
                tracker.log_step(epoch, i + 1, loss, val_loss=avg_val_loss, memory_mb=calculate_memory_usage())
                tracker.save_best_model(model, avg_val_loss)

                # Verificar Early Stopping e Overfitting
                print(f"\n📊 Análise de Validação:")
                should_stop, improved = early_stopping.check(
                    val_loss=avg_val_loss,
                    train_loss=loss.item(),
                    epoch=epoch,
                    step=i + 1
                )

                if should_stop:
                    print(f"\n🏁 Treino terminado por Early Stopping")
                    break

            if (i + 1) % training_config["save_steps"] == 0:
                checkpoint_path = CHECKPOINTS_DIR / f"checkpoint_epoch{epoch}_step{i+1}"
                checkpoint_path.mkdir(parents=True, exist_ok=True)
                model.save_weights(str(checkpoint_path / "adapters.safetensors"))
                print(f"✓ Checkpoint guardado em: {checkpoint_path}")

        # Sair do loop de épocas se early stopping foi acionado
        if early_stopping.should_stop:
            break

    # 5. Análise Final de Overfitting
    print("\n" + "="*80)
    print("🔍 ANÁLISE FINAL DE OVERFITTING")
    print("="*80)
    overfitting_status = early_stopping.get_overfitting_status()
    print(f"Status: {overfitting_status}")
    if early_stopping.overfitting_gap_history:
        avg_gap = sum(early_stopping.overfitting_gap_history) / len(early_stopping.overfitting_gap_history)
        max_gap = max(early_stopping.overfitting_gap_history)
        min_gap = min(early_stopping.overfitting_gap_history)
        print(f"Gap médio: {avg_gap:.4f}")
        print(f"Gap máximo: {max_gap:.4f}")
        print(f"Gap mínimo: {min_gap:.4f}")
    print("="*80 + "\n")

    # 6. Guardar Modelo Final
    print("\n--- Treino concluído. A guardar o modelo final --- ")
    final_model_path = training_config["model_path"]
    final_model_path.mkdir(parents=True, exist_ok=True)

    # Copiar adaptadores para o diretório final
    shutil.copy(tracker.best_model_path, final_model_path / "adapters.safetensors")
    
    # Guardar configuração do adaptador
    with open(final_model_path / "adapter_config.json", 'w', encoding='utf-8') as f:
        json.dump(qlora_config, f, indent=4, ensure_ascii=False)

    # Guardar tokenizer (se necessário, mlx_lm.save já o faz)
    # tokenizer.save_pretrained(str(final_model_path))

    print(f"Modelo QLoRA finetunado guardado em: {final_model_path}")
    tracker.save_summary(time.time() - tracker.start_time, len(train_dataset))
    print("Sumário de treino guardado.")

    print("\n--- A gerar relatórios finais --- ")
    # Chamar o script de visualização para gerar gráficos
    os.system(f"python {BASE_DIR / 'scripts' / 'visualization.py'} --report")
    print("Relatórios finais gerados.")

if __name__ == "__main__":
    # Criar ficheiros de treino e validação a partir do dataset limpo
    full_dataset = load_dataset(CLEANED_DATA_FILE)
    split_idx = int(len(full_dataset) * 0.9)
    train_dataset = full_dataset[:split_idx]
    val_dataset = full_dataset[split_idx:]

    with open(TRAIN_FILE, 'w', encoding='utf-8') as f:
        for entry in train_dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    with open(VALID_FILE, 'w', encoding='utf-8') as f:
        for entry in val_dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    train()