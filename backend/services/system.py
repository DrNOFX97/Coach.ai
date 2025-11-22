import platform
import psutil
try:
    import torch
except ImportError:
    torch = None

def get_hardware_info():
    """Detects system hardware and recommends framework"""
    system = platform.system()
    processor = platform.processor()
    
    accelerator = "CPU"
    device_name = "Unknown"
    framework = "PyTorch" # Default
    has_gpu = False
    
    # Check for Apple Silicon (Metal)
    if system == "Darwin" and "arm" in processor.lower():
        accelerator = "Metal (MPS)"
        device_name = f"Apple {processor}"
        framework = "MLX" # Preferred on Mac
        has_gpu = True
    
    # Check for CUDA
    elif torch and torch.cuda.is_available():
        accelerator = "CUDA"
        device_name = torch.cuda.get_device_name(0)
        framework = "PyTorch"
        has_gpu = True

    # RAM Detection
    ram_gb = 8.0
    if psutil:
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        available_ram_gb = psutil.virtual_memory().available / (1024 ** 3)
    else:
        available_ram_gb = 4.0 # Fallback

    # Recommendation Logic (Three Levels)
    presets = {
        "conservative": {},
        "balanced": {},
        "aggressive": {}
    }
    
    # Base logic based on RAM
    if available_ram_gb < 8:
        # Low RAM (<8GB)
        presets["conservative"] = { 'batch_size': 1, 'gradient_accumulation': 8, 'max_seq_length': 128, 'learning_rate': 0.00005, 'num_epochs': 1 }
        presets["balanced"] =     { 'batch_size': 1, 'gradient_accumulation': 4, 'max_seq_length': 256, 'learning_rate': 0.0001,  'num_epochs': 1 }
        presets["aggressive"] =   { 'batch_size': 2, 'gradient_accumulation': 2, 'max_seq_length': 256, 'learning_rate': 0.0002,  'num_epochs': 2 }
    elif available_ram_gb < 16:
        # Medium RAM (<16GB)
        presets["conservative"] = { 'batch_size': 1, 'gradient_accumulation': 4, 'max_seq_length': 256, 'learning_rate': 0.0001, 'num_epochs': 1 }
        presets["balanced"] =     { 'batch_size': 2, 'gradient_accumulation': 4, 'max_seq_length': 512, 'learning_rate': 0.0002, 'num_epochs': 3 }
        presets["aggressive"] =   { 'batch_size': 4, 'gradient_accumulation': 2, 'max_seq_length': 512, 'learning_rate': 0.0003, 'num_epochs': 3 }
    else:
        # High RAM (>16GB)
        presets["conservative"] = { 'batch_size': 2, 'gradient_accumulation': 4, 'max_seq_length': 512, 'learning_rate': 0.0001, 'num_epochs': 2 }
        presets["balanced"] =     { 'batch_size': 4, 'gradient_accumulation': 2, 'max_seq_length': 1024, 'learning_rate': 0.0002, 'num_epochs': 3 }
        presets["aggressive"] =   { 'batch_size': 8, 'gradient_accumulation': 1, 'max_seq_length': 2048, 'learning_rate': 0.0003, 'num_epochs': 3 }

    # Adjust for GPU
    if has_gpu:
        for key in presets:
            presets[key]['learning_rate'] *= 1.5

    return {
        "os": system,
        "processor": processor,
        "accelerator": accelerator,
        "device_name": device_name,
        "framework": framework,
        "ram_total": ram_gb,
        "ram_available": available_ram_gb,
        "presets": presets,
        "reason": f"Presets generated for {available_ram_gb:.1f}GB RAM"
    }
