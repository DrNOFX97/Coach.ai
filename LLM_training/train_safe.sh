#!/bin/bash

################################################################################
# SAFE TRAIN - Wrapper Seguro para Treino de LLM
#
# Executa:
# 1. Preflight check (diagnóstico do sistema)
# 2. Recomenda configuração otimizada
# 3. Oferece opção de abrir notebook com config aplicada
################################################################################

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$BASE_DIR/scripts"
NOTEBOOKS_DIR="$BASE_DIR/notebooks"
CHECKPOINTS_DIR="$BASE_DIR/checkpoints_qlora"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNÇÕES
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}=================================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}=================================================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}→ $1${NC}"
}

print_step() {
    echo ""
    echo -e "${BLUE}>>> $1${NC}"
    echo "───────────────────────────────────────────────────────────────────────────────"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    print_header "SAFE TRAIN - Treino Seguro de LLM"

    # Step 1: Verificar se está no diretório correto
    if [ ! -f "$SCRIPTS_DIR/preflight_check.py" ]; then
        print_error "Script preflight_check.py não encontrado em $SCRIPTS_DIR"
        exit 1
    fi

    # Step 2: Executar preflight check
    print_step "1. DIAGNÓSTICO DE SISTEMA (Preflight Check)"
    echo "Isso pode levar 1-2 minutos na primeira vez..."
    echo ""

    if python3 "$SCRIPTS_DIR/preflight_check.py"; then
        print_success "Preflight check concluído com sucesso!"
    else
        print_error "Preflight check falhou!"
        print_warning "Resolva os problemas indicados acima antes de tentar treinar"
        exit 1
    fi

    # Step 3: Verificar ficheiros gerados
    if [ ! -f "$CHECKPOINTS_DIR/recommended_config.json" ]; then
        print_error "Ficheiro de config não foi gerado"
        exit 1
    fi

    # Step 4: Mostrar config recomendada
    print_step "2. CONFIGURAÇÃO RECOMENDADA"
    echo ""
    echo "Basado no seu hardware, eis a configuração otimizada:"
    echo ""
    python3 << 'EOF'
import json
config_file = "/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/checkpoints_qlora/recommended_config.json"
with open(config_file) as f:
    config = json.load(f)

for key, value in config.items():
    if not key.startswith("_"):
        print(f"  {key}: {value}")
EOF
    echo ""

    # Step 5: Oferecer opções
    print_step "3. PRÓXIMOS PASSOS"
    echo ""
    echo "Escolha uma opção:"
    echo ""
    echo "  1) Abrir Notebook (RECOMENDADO)"
    echo "     → Facilita editar config e visualizar progresso"
    echo ""
    echo "  2) Executar Script Python"
    echo "     → Para treino automatizado sem interface"
    echo ""
    echo "  3) Apenas Mostrar Instruções"
    echo "     → Ver como configurar manualmente"
    echo ""
    echo "  0) Sair"
    echo ""

    read -p "Escolha (0-3): " choice

    case $choice in
        1)
            open_notebook
            ;;
        2)
            run_script
            ;;
        3)
            show_instructions
            ;;
        0)
            echo "Abortado pelo utilizador"
            exit 0
            ;;
        *)
            print_error "Opção inválida"
            exit 1
            ;;
    esac
}

open_notebook() {
    print_step "ABRIR NOTEBOOK"

    NOTEBOOK="$NOTEBOOKS_DIR/mistral_qlora_training.ipynb"

    if [ ! -f "$NOTEBOOK" ]; then
        print_error "Notebook não encontrado: $NOTEBOOK"
        exit 1
    fi

    echo ""
    print_info "Abrindo notebook em Jupyter..."
    echo ""

    # Tentar abrir com jupyter
    if command -v jupyter &> /dev/null; then
        cd "$BASE_DIR"
        jupyter notebook "$NOTEBOOK"
    else
        print_error "Jupyter não está instalado"
        echo ""
        print_info "Para instalar: pip install jupyter"
        exit 1
    fi

    print_success "Notebook encerrado"

    # Mostrar próximas instruções
    show_post_training_instructions
}

run_script() {
    print_step "EXECUTAR SCRIPT DE TREINO"

    TRAIN_SCRIPT="$SCRIPTS_DIR/train_qlora.py"

    if [ ! -f "$TRAIN_SCRIPT" ]; then
        print_error "Script não encontrado: $TRAIN_SCRIPT"
        exit 1
    fi

    echo ""
    print_warning "Antes de executar, certifique-se de que:"
    echo "  1. Atualizou os parâmetros em $TRAIN_SCRIPT"
    echo "     com os valores de checkpoints_qlora/recommended_config.json"
    echo "  2. Tem terminal separada aberta para monitorar:"
    echo "     python3 scripts/monitor.py --refresh 5"
    echo ""

    read -p "Continuar? (s/n) " confirm
    if [[ $confirm != [sS] ]]; then
        echo "Abortado"
        exit 0
    fi

    echo ""
    print_info "Iniciando treino..."
    echo ""

    cd "$BASE_DIR"
    python3 "$TRAIN_SCRIPT"

    show_post_training_instructions
}

show_instructions() {
    print_step "INSTRUÇÕES MANUAIS"

    echo ""
    echo "1. ATUALIZAR CONFIGURAÇÃO"
    echo "   ──────────────────────"
    echo "   Abra: $NOTEBOOKS_DIR/mistral_qlora_training.ipynb"
    echo "   Procure a seção 'Configuração do Treino'"
    echo "   Atualize com valores de:"
    echo "   → cat $CHECKPOINTS_DIR/recommended_config.json"
    echo ""

    echo "2. INICIAR TREINO"
    echo "   ───────────────"
    echo "   No Jupyter, execute as células normalmente"
    echo "   Ou corra: python3 $SCRIPTS_DIR/train_qlora.py"
    echo ""

    echo "3. MONITORAR (TERMINAL SEPARADA)"
    echo "   ──────────────────────────────"
    echo "   python3 $SCRIPTS_DIR/monitor.py --refresh 5"
    echo ""

    echo "4. APÓS TREINO"
    echo "   ────────────"
    echo "   Visualizar: python3 $SCRIPTS_DIR/visualization.py --report"
    echo "   Testar:     python3 $SCRIPTS_DIR/inference_qlora.py \"pergunta\""
    echo ""
}

show_post_training_instructions() {
    print_step "APÓS TREINO"

    echo ""
    echo "Quando o treino terminar, execute:"
    echo ""
    echo "  # Ver gráficos de progresso"
    echo "  python3 $SCRIPTS_DIR/visualization.py --report"
    echo ""
    echo "  # Testar modelo treinado"
    echo "  python3 $SCRIPTS_DIR/inference_qlora.py \"Qual foi a melhor classificação?\""
    echo ""
    echo "Checkpoints salvos em: $CHECKPOINTS_DIR/"
    echo ""
}

# ============================================================================
# EXECUTAR
# ============================================================================

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não encontrado!"
    exit 1
fi

# Executar main
main

print_success "Concluído!"
