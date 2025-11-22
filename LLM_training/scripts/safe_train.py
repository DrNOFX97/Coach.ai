#!/usr/bin/env python3
"""
SAFE TRAIN - Wrapper que executa preflight check antes do treino
Previne crashes ao validar sistema e recomendar configuração otimizada
"""

import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CHECKPOINTS_DIR = BASE_DIR / "checkpoints_qlora"
RECOMMENDED_CONFIG = CHECKPOINTS_DIR / "recommended_config.json"


def run_preflight_check():
    """Executa preflight check"""
    print("\n" + "=" * 80)
    print("  EXECUTANDO PREFLIGHT CHECK...")
    print("=" * 80 + "\n")

    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "preflight_check.py")],
        cwd=str(BASE_DIR)
    )

    if result.returncode != 0:
        print("\n" + "=" * 80)
        print("  ✗ PREFLIGHT CHECK FALHOU")
        print("  Resolva os problemas acima antes de tentar treinar")
        print("=" * 80)
        return False

    return True


def load_recommended_config():
    """Carrega configuração recomendada"""
    if not RECOMMENDED_CONFIG.exists():
        print("⚠ Config recomendada não encontrada")
        return None

    with open(RECOMMENDED_CONFIG) as f:
        return json.load(f)


def print_recommendations():
    """Imprime recomendações para o usuário"""
    config = load_recommended_config()
    if not config:
        return

    print("\n" + "=" * 80)
    print("  PRÓXIMOS PASSOS")
    print("=" * 80)
    print("\n1. USAR CONFIGURAÇÃO RECOMENDADA")
    print(f"   Os seguintes valores foram recomendados para seu sistema:")
    print(f"   • batch_size: {config['batch_size']}")
    print(f"   • gradient_accumulation: {config['gradient_accumulation']}")
    print(f"   • max_seq_length: {config['max_seq_length']}")
    print(f"   • learning_rate: {config['learning_rate']}")
    print(f"\n   OPÇÃO A: Usar Notebook (RECOMENDADO)")
    print(f"   $ jupyter notebook notebooks/mistral_qlora_training.ipynb")
    print(f"   → Abra a seção 'Configuração' e atualize os valores acima")
    print(f"\n   OPÇÃO B: Usar Script Python")
    print(f"   $ python3 scripts/train_qlora.py")
    print(f"   → Edite scripts/train_qlora.py antes de correr")

    print(f"\n2. MONITORAR TREINO EM TEMPO REAL")
    print(f"   Numa segunda terminal, corra:")
    print(f"   $ python3 scripts/monitor.py --refresh 5")

    print(f"\n3. APÓS TREINO")
    print(f"   • Checkpoints salvos em: {BASE_DIR}/checkpoints_qlora/")
    print(f"   • Visualizar resultados: python3 scripts/visualization.py --report")
    print(f"   • Testar modelo: python3 scripts/inference_qlora.py \"sua pergunta\"")

    print("\n" + "=" * 80)


def main():
    """Main entry point"""
    # 1. Executar preflight check
    if not run_preflight_check():
        sys.exit(1)

    # 2. Mostrar próximos passos
    print_recommendations()

    print("\n✓ Sistema validado e pronto para treino!")
    print("  Execute os comandos acima para começar o treino.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelado pelo utilizador")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
