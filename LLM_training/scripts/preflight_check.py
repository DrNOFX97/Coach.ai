#!/usr/bin/env python3
"""
PREFLIGHT CHECK - Sistema de Diagnóstico e Recomendação de Configuração
Executa antes do treino para evitar crashes e recomendar config otimizada
"""

import sys
import os
import json
import platform
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
import time

# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHECKPOINTS_DIR = BASE_DIR / "checkpoints_qlora"
OUTPUT_DIR = BASE_DIR / "output"

PREFLIGHT_REPORT = CHECKPOINTS_DIR / "preflight_report.json"
RECOMMENDED_CONFIG = CHECKPOINTS_DIR / "recommended_config.json"

# ============================================================================
# ESTRUTURA DE DADOS
# ============================================================================

@dataclass
class HardwareInfo:
    """Informações de hardware detectadas"""
    machine: str
    python_version: str
    python_full_version: str
    os_name: str
    os_version: str
    cpu_cores: int
    total_memory_gb: float
    available_memory_gb: float
    memory_usage_percent: float
    disk_space_gb: float

@dataclass
class DependencyStatus:
    """Status das dependências"""
    mlx: bool
    mlx_lm: bool
    transformers: bool
    torch: bool
    psutil: bool
    pandas: bool
    tqdm: bool

@dataclass
class DataInfo:
    """Informações sobre dados"""
    train_file: str
    valid_file: str
    train_samples: int
    valid_samples: int
    total_samples: int
    avg_sample_size_bytes: float

@dataclass
class GPUInfo:
    """Informações de GPU"""
    metal_available: bool
    gpu_memory_available: bool
    device_type: str

@dataclass
class RecommendedConfig:
    """Configuração recomendada"""
    batch_size: int
    gradient_accumulation: int
    max_seq_length: int
    learning_rate: float
    num_epochs: int
    warmup_steps: int
    save_steps: int
    eval_steps: int
    log_steps: int
    reason: str

# ============================================================================
# FUNÇÕES DE DIAGNÓSTICO
# ============================================================================

class PreflightChecker:
    """Sistema completo de diagnóstico pré-treino"""

    def __init__(self):
        self.checks_passed = []
        self.checks_failed = []
        self.warnings = []
        self.hardware_info = None
        self.dependency_status = None
        self.data_info = None
        self.gpu_info = None
        self.recommended_config = None

    def print_header(self, text: str):
        """Imprime cabeçalho formatado"""
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80)

    def print_section(self, text: str):
        """Imprime título de seção"""
        print(f"\n>>> {text}")
        print("-" * 80)

    def check_ok(self, text: str):
        """Marca como passou"""
        print(f"  ✓ {text}")
        self.checks_passed.append(text)

    def check_fail(self, text: str, error: str = None):
        """Marca como falhou"""
        msg = f"  ✗ {text}"
        if error:
            msg += f" ({error})"
        print(msg)
        self.checks_failed.append(text)

    def check_warn(self, text: str):
        """Marca como aviso"""
        print(f"  ⚠ {text}")
        self.warnings.append(text)

    # ========================================================================
    # CHECK 1: Hardware
    # ========================================================================

    def check_hardware(self) -> HardwareInfo:
        """Detecta configuração de hardware"""
        self.print_section("1. VERIFICAÇÃO DE HARDWARE")

        import psutil

        machine = platform.machine()
        os_name = platform.system()
        os_version = platform.release()
        python_version = platform.python_version()
        python_full = sys.version

        cpu_count = os.cpu_count() or 1

        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024**3)
        available_gb = mem.available / (1024**3)
        mem_percent = mem.percent

        disk = psutil.disk_usage("/")
        disk_gb = disk.free / (1024**3)

        # Exibir informações
        print(f"  • Machine: {machine}")
        print(f"  • OS: {os_name} ({os_version})")
        print(f"  • Python: {python_version}")
        print(f"  • CPU Cores: {cpu_count}")
        print(f"  • Total RAM: {total_gb:.1f} GB")
        print(f"  • Available RAM: {available_gb:.1f} GB ({100-mem_percent:.0f}% livre)")
        print(f"  • Disk Space: {disk_gb:.1f} GB livre")

        # Validações
        if machine == "arm64":
            self.check_ok(f"Apple Silicon (M1/M2/M3) detectado")
        elif machine == "x86_64":
            self.check_warn(f"Intel Mac detectado - projeto otimizado para Apple Silicon")
        else:
            self.check_fail(f"Arquitetura {machine} não suportada")

        if sys.version_info >= (3, 11):
            self.check_ok(f"Python {python_version} (recomendado 3.11+)")
        else:
            self.check_warn(f"Python {python_version} - recomendado atualizar para 3.11+")

        if available_gb >= 8:
            self.check_ok(f"Memória suficiente: {available_gb:.1f} GB disponível")
        elif available_gb >= 4:
            self.check_warn(f"Memória limitada: {available_gb:.1f} GB (recomendado 8+ GB)")
        else:
            self.check_fail(f"Memória insuficiente: {available_gb:.1f} GB (precisa 4+ GB)")

        if disk_gb >= 10:
            self.check_ok(f"Espaço em disco: {disk_gb:.1f} GB livre")
        else:
            self.check_warn(f"Espaço em disco limitado: {disk_gb:.1f} GB (recomendado 20+ GB)")

        self.hardware_info = HardwareInfo(
            machine=machine,
            python_version=python_version,
            python_full_version=python_full,
            os_name=os_name,
            os_version=os_version,
            cpu_cores=cpu_count,
            total_memory_gb=total_gb,
            available_memory_gb=available_gb,
            memory_usage_percent=mem_percent,
            disk_space_gb=disk_gb,
        )

        return self.hardware_info

    # ========================================================================
    # CHECK 2: Dependências Python
    # ========================================================================

    def check_dependencies(self) -> DependencyStatus:
        """Verifica se todas as dependências estão instaladas"""
        self.print_section("2. VERIFICAÇÃO DE DEPENDÊNCIAS")

        deps = {}
        required_packages = {
            'mlx': "MLX (framework principal)",
            'mlx_lm': "MLX-LM (carregamento de modelos)",
            'transformers': "Transformers (tokenizer)",
        }
        optional_packages = {
            'torch': "PyTorch (alternativa para non-Apple)",
            'psutil': "PSUtil (monitorização de sistema)",
            'pandas': "Pandas (análise de dados)",
            'tqdm': "tqdm (barras de progresso)",
        }

        # Verificar pacotes obrigatórios
        for pkg, desc in required_packages.items():
            try:
                __import__(pkg)
                self.check_ok(f"{desc}")
                deps[pkg] = True
            except ImportError:
                self.check_fail(f"{desc}")
                deps[pkg] = False

        # Verificar pacotes opcionais
        for pkg, desc in optional_packages.items():
            try:
                __import__(pkg)
                self.check_ok(f"{desc}")
                deps[pkg] = True
            except ImportError:
                self.check_warn(f"{desc} não instalado")
                deps[pkg] = False

        # Avisos se faltar obrigatórios
        missing_required = [k for k, v in deps.items() if not v and k in required_packages]
        if missing_required:
            print(f"\n  ⚠ INSTALE PACOTES OBRIGATÓRIOS:")
            print(f"     pip install mlx mlx-lm transformers")

        self.dependency_status = DependencyStatus(**deps)

        return self.dependency_status

    # ========================================================================
    # CHECK 3: GPU/Metal
    # ========================================================================

    def check_gpu(self) -> GPUInfo:
        """Verifica disponibilidade de GPU Metal"""
        self.print_section("3. VERIFICAÇÃO DE GPU")

        metal_available = False
        gpu_memory_available = False
        device_type = "CPU"

        try:
            import mlx.core as mx

            # Tentar usar GPU
            try:
                mx.set_default_device(mx.gpu)
                device = mx.default_device()
                if "gpu" in str(device):
                    self.check_ok("Metal GPU detectado e ativado")
                    metal_available = True
                    device_type = "Metal GPU"
                    gpu_memory_available = True
                else:
                    self.check_warn(f"Dispositivo: {device} (esperado GPU)")
                    device_type = str(device)
            except Exception as e:
                self.check_warn(f"Metal GPU não disponível ({str(e)[:50]})")
                device_type = "CPU"

        except ImportError:
            self.check_fail("MLX não importável - não foi possível verificar GPU")

        # Se não há GPU, avisar sobre performance
        if device_type == "CPU":
            self.check_warn("GPU não disponível - treino será muito lento")
            self.check_warn("Verificar: deve estar em Mac M1/M2/M3 com MLX instalado")

        self.gpu_info = GPUInfo(
            metal_available=metal_available,
            gpu_memory_available=gpu_memory_available,
            device_type=device_type,
        )

        return self.gpu_info

    # ========================================================================
    # CHECK 4: Dados
    # ========================================================================

    def check_data(self) -> DataInfo:
        """Verifica disponibilidade e tamanho dos dados"""
        self.print_section("4. VERIFICAÇÃO DE DADOS")

        # Procurar ficheiros de dados
        possible_train_files = [
            DATA_DIR / "train_v3_final_complete.jsonl",
            DATA_DIR / "train_v3.jsonl",
            DATA_DIR / "train.jsonl",
        ]

        possible_valid_files = [
            DATA_DIR / "valid_v3_final_complete.jsonl",
            DATA_DIR / "valid_v3.jsonl",
            DATA_DIR / "valid.jsonl",
        ]

        train_file = None
        valid_file = None
        train_samples = 0
        valid_samples = 0

        # Encontrar ficheiro de treino
        for f in possible_train_files:
            if f.exists():
                train_file = f
                with open(f, encoding='utf-8') as fp:
                    train_samples = sum(1 for _ in fp)
                break

        # Encontrar ficheiro de validação
        for f in possible_valid_files:
            if f.exists():
                valid_file = f
                with open(f, encoding='utf-8') as fp:
                    valid_samples = sum(1 for _ in fp)
                break

        # Validações
        if train_file:
            self.check_ok(f"Ficheiro de treino: {train_file.name} ({train_samples} amostras)")
        else:
            self.check_fail("Ficheiro de treino não encontrado")

        if valid_file:
            self.check_ok(f"Ficheiro de validação: {valid_file.name} ({valid_samples} amostras)")
        else:
            self.check_fail("Ficheiro de validação não encontrado")

        if train_samples < 100:
            self.check_warn(f"Poucas amostras de treino ({train_samples})")
        else:
            self.check_ok(f"Amostras de treino suficientes ({train_samples})")

        if valid_samples < 20:
            self.check_warn(f"Poucas amostras de validação ({valid_samples})")
        else:
            self.check_ok(f"Amostras de validação suficientes ({valid_samples})")

        # Estimar tamanho médio
        avg_size = 0
        if train_file and train_samples > 0:
            file_size = train_file.stat().st_size
            avg_size = file_size / train_samples

        self.data_info = DataInfo(
            train_file=str(train_file) if train_file else "NOT FOUND",
            valid_file=str(valid_file) if valid_file else "NOT FOUND",
            train_samples=train_samples,
            valid_samples=valid_samples,
            total_samples=train_samples + valid_samples,
            avg_sample_size_bytes=avg_size,
        )

        return self.data_info

    # ========================================================================
    # CHECK 5: Modelo
    # ========================================================================

    def check_model(self):
        """Verifica disponibilidade e capacidade de carregamento do modelo"""
        self.print_section("5. VERIFICAÇÃO DE MODELO")

        model_path = BASE_DIR / "models" / "mistral-7b-4bit"

        if model_path.exists():
            size_gb = sum(f.stat().st_size for f in model_path.rglob('*')) / (1024**3)
            self.check_ok(f"Modelo base encontrado: {model_path.name} ({size_gb:.1f} GB)")
        else:
            self.check_warn(f"Modelo base não encontrado em {model_path}")
            self.check_warn("Será baixado na primeira execução (~3.8 GB)")

        # Tentar carregar modelo (sem forward pass)
        try:
            from mlx_lm import load
            print("\n  Testando carregamento de modelo...")
            try:
                # Tentar com parâmetro quantization (versões antigas)
                model, tokenizer = load(
                    "mistralai/Mistral-7B-v0.1",
                    adapter_path=None,
                    quantization="int4"
                )
            except TypeError:
                # Fallback para versões novas (quantization vem automático)
                model, tokenizer = load(
                    "mistralai/Mistral-7B-v0.1",
                    adapter_path=None
                )
            self.check_ok("Modelo carregado com sucesso")
        except Exception as e:
            self.check_warn(f"Erro ao carregar modelo: {str(e)[:80]}")
            self.check_warn("Model será carregado na primeira execução")

    # ========================================================================
    # CHECK 6: Espaço em Disco para Checkpoints
    # ========================================================================

    def check_disk_space(self):
        """Verifica espaço em disco suficiente para checkpoints"""
        self.print_section("6. VERIFICAÇÃO DE ESPAÇO EM DISCO")

        disk = __import__('psutil').disk_usage("/")
        free_gb = disk.free / (1024**3)

        # Estimativa: 3 checkpoints x 500MB cada + modelo + outputs
        estimated_needed = 5  # GB

        print(f"  • Espaço livre: {free_gb:.1f} GB")
        print(f"  • Estimado necessário: ~{estimated_needed} GB")

        if free_gb >= estimated_needed * 2:
            self.check_ok(f"Espaço em disco suficiente")
        elif free_gb >= estimated_needed:
            self.check_warn(f"Espaço em disco limitado")
        else:
            self.check_fail(f"Espaço insuficiente para treino")

    # ========================================================================
    # RECOMENDAÇÃO DE CONFIGURAÇÃO
    # ========================================================================

    def recommend_config(self) -> RecommendedConfig:
        """Recomenda configuração otimizada baseado em hardware detectado"""
        self.print_section("7. RECOMENDAÇÃO DE CONFIGURAÇÃO")

        avail_mem = self.hardware_info.available_memory_gb
        metal_available = self.gpu_info.metal_available
        total_samples = self.data_info.total_samples

        print(f"  • Memória disponível: {avail_mem:.1f} GB")
        print(f"  • GPU disponível: {metal_available}")
        print(f"  • Amostras de dados: {total_samples}")

        # ====== RECOMENDAÇÃO BASEADO EM MEMÓRIA ======

        if avail_mem >= 16:
            # M1 Pro/Max ou máquina com muita memória
            batch_size = 4
            grad_accum = 2
            max_seq_length = 512
            learning_rate = 5e-4
            reason = "Memória alta (16+ GB) - máx performance"

        elif avail_mem >= 10:
            # M1 Pro com configuração decente
            batch_size = 2
            grad_accum = 2
            max_seq_length = 512
            learning_rate = 3e-4
            reason = "Memória média (10-16 GB) - config balanceada"

        elif avail_mem >= 8:
            # M1 base ou M2 com memória suficiente
            batch_size = 2
            grad_accum = 2
            max_seq_length = 512
            learning_rate = 3e-4
            reason = "Memória adequada (8-10 GB) - config conservadora"

        elif avail_mem >= 6:
            # M1 base tight
            batch_size = 1
            grad_accum = 4
            max_seq_length = 256
            learning_rate = 2e-4
            reason = "Memória limitada (6-8 GB) - config reduzida"

        else:
            # Memória muito limitada
            batch_size = 1
            grad_accum = 8
            max_seq_length = 128
            learning_rate = 1e-4
            reason = "Memória crítica (<6 GB) - config mínima"

        # ====== AJUSTES POR GPU ======

        if not metal_available:
            self.check_warn("GPU não disponível - reduzindo batch_size")
            batch_size = max(1, batch_size // 2)
            reason += " | GPU não disponível"

        # ====== OUTRAS CONFIGS DERIVADAS ======

        num_epochs = 3
        warmup_steps = max(50, int(total_samples * num_epochs * batch_size * 0.05 / 100))
        save_steps = max(100, int(total_samples * batch_size / 100))
        eval_steps = save_steps
        log_steps = 10

        config = RecommendedConfig(
            batch_size=batch_size,
            gradient_accumulation=grad_accum,
            max_seq_length=max_seq_length,
            learning_rate=learning_rate,
            num_epochs=num_epochs,
            warmup_steps=warmup_steps,
            save_steps=save_steps,
            eval_steps=eval_steps,
            log_steps=log_steps,
            reason=reason,
        )

        # Exibir recomendação
        print(f"\n  CONFIGURAÇÃO RECOMENDADA:")
        print(f"  • batch_size: {config.batch_size}")
        print(f"  • gradient_accumulation: {config.gradient_accumulation}")
        print(f"  • max_seq_length: {config.max_seq_length}")
        print(f"  • learning_rate: {config.learning_rate}")
        print(f"  • num_epochs: {config.num_epochs}")
        print(f"  • warmup_steps: {config.warmup_steps}")
        print(f"  • save_steps: {config.save_steps}")
        print(f"  • eval_steps: {config.eval_steps}")
        print(f"\n  RAZÃO: {config.reason}")

        self.recommended_config = config

        return config

    # ========================================================================
    # RELATÓRIO FINAL
    # ========================================================================

    def print_summary(self):
        """Imprime resumo final"""
        self.print_header("RESUMO DO PREFLIGHT CHECK")

        total_checks = len(self.checks_passed) + len(self.checks_failed)

        print(f"\n  ✓ Passou: {len(self.checks_passed)}")
        print(f"  ✗ Falhou: {len(self.checks_failed)}")
        print(f"  ⚠ Avisos: {len(self.warnings)}")
        print(f"  Total: {total_checks} verificações")

        if self.checks_failed:
            print(f"\n  PROBLEMAS ENCONTRADOS:")
            for check in self.checks_failed:
                print(f"    - {check}")

        if self.warnings:
            print(f"\n  AVISOS:")
            for warn in self.warnings:
                print(f"    - {warn}")

        # Status final
        print("\n" + "=" * 80)
        if not self.checks_failed:
            print("  ✓ SISTEMA PRONTO PARA TREINO")
            print(f"  Use configuração recomendada para evitar crashes")
        else:
            print("  ⚠ EXISTEM PROBLEMAS - Resolva antes de treinar")
        print("=" * 80)

    # ========================================================================
    # SALVAR RELATÓRIO
    # ========================================================================

    def save_report(self):
        """Salva relatório e config recomendada como JSON"""
        CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "hardware": asdict(self.hardware_info),
            "dependencies": asdict(self.dependency_status),
            "data": asdict(self.data_info),
            "gpu": asdict(self.gpu_info),
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "warnings": self.warnings,
        }

        with open(PREFLIGHT_REPORT, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        config_dict = asdict(self.recommended_config)
        config_dict["_description"] = "Esta configuração é recomendada para seu sistema"
        config_dict["_usage"] = "Copie esses valores para train_qlora.py ou notebook"

        with open(RECOMMENDED_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)

        print(f"\n  ✓ Relatório salvo: {PREFLIGHT_REPORT}")
        print(f"  ✓ Config salva: {RECOMMENDED_CONFIG}")

    # ========================================================================
    # EXECUTAR TODOS OS CHECKS
    # ========================================================================

    def run_all(self):
        """Executa todos os checks"""
        self.print_header("PREFLIGHT CHECK - LLM TRAINING")
        print("Diagnóstico de sistema antes do treino\n")

        # Executar todos os checks
        self.check_hardware()
        self.check_dependencies()
        self.check_gpu()
        self.check_data()
        self.check_model()
        self.check_disk_space()

        # Apenas recomendar se não há falhas críticas
        if len(self.checks_failed) <= 2:  # Allowance para pequenas falhas
            self.recommend_config()
        else:
            print("\n⚠ EXISTEM PROBLEMAS CRÍTICOS - Não é possível recomendar config")

        # Imprimir resumo e salvar
        self.print_summary()
        self.save_report()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        checker = PreflightChecker()
        checker.run_all()

        # Exit code
        if checker.checks_failed:
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"\n✗ ERRO NO PREFLIGHT CHECK: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
