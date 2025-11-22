import sys
import time
from pathlib import Path
from ..models import TrainingConfig

# Try to import training scripts
try:
    sys.path.append(str(Path(__file__).parent.parent.parent / "LLM_training" / "scripts"))
    import train_qlora
except ImportError:
    train_qlora = None

try:
    import train_pytorch
except ImportError:
    train_pytorch = None

training_active = False

def run_mock_training(config: TrainingConfig):
    """Simulates training for testing purposes"""
    print(f"Starting Mock Training with {config}")
    metrics_path = Path(__file__).parent.parent.parent / "LLM_training" / "checkpoints_qlora" / "training_metrics.json"
    metrics_path.parent.mkdir(exist_ok=True)
    
    import json
    metrics = {"loss": [], "val_loss": [], "logs": []}
    
    for epoch in range(config.epochs):
        for step in range(10):
            if not training_active: return
            
            loss = 2.0 - (epoch * 0.5) - (step * 0.1) + (0.05 * (step % 2))
            metrics["loss"].append({"step": step + (epoch * 10), "value": max(0.1, loss)})
            metrics["logs"].append(f"Epoch {epoch+1}, Step {step+1}: Loss {loss:.4f}")
            
            with open(metrics_path, "w") as f:
                json.dump(metrics, f)
            
            time.sleep(1) # Simulate work

def start_training_process(config: TrainingConfig):
    global training_active
    training_active = True
    try:
        # Redirect stdout/stderr to log file
        log_path = Path(__file__).parent.parent.parent / "backend_debug.log"
        class TeeLogger:
            def __init__(self, filename):
                self.terminal = sys.stdout
                self.log = open(filename, "a", encoding="utf-8")
            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)
                self.log.flush()
            def flush(self):
                self.terminal.flush()
                self.log.flush()
                
        sys.stdout = TeeLogger(str(log_path))
        sys.stderr = TeeLogger(str(log_path))
        
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting training process...")
        print(f"Config: {config}")

        custom_training_config = {
            "batch_size": config.batchSize,
            "num_epochs": config.epochs,
            "gradient_accumulation": config.gradientAccumulation,
            "learning_rate": config.learningRate,
            "max_seq_length": config.maxSeqLength
        }
        
        custom_qlora_config = {}
        if config.quantization == "4-bit":
            custom_qlora_config["bits"] = 4
        elif config.quantization == "8-bit":
            custom_qlora_config["bits"] = 8
            
        if config.framework == "MLX":
            if train_qlora:
                print("Invoking train_qlora.train()...")
                train_qlora.train(custom_training_config, custom_qlora_config)
            else:
                print("train_qlora module not found, falling back to mock.")
                run_mock_training(config)
        elif config.framework == "PyTorch":
            if train_pytorch:
                train_pytorch.train(custom_training_config, custom_qlora_config)
            else:
                print("PyTorch script not found")
                run_mock_training(config)
                
    except Exception as e:
        print(f"Training failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        training_active = False

def stop_training_process():
    global training_active
    training_active = False
