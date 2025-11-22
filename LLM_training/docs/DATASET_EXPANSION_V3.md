# Dataset Expansion - Version 3 (V3)

## Resumo Executivo

O Dataset V3 é a terceira versão do dataset de treino para o chatbot Farense. Esta versão representa uma expansão significativa baseada em fontes históricas de alto valor, focando exclusivamente em conteúdo relacionado com o Sporting Clube Farense.

**Data de criação**: Novembro 2024
**Total de exemplos**: 1.048 (953 + 95 novos)
**Aumento**: 95 exemplos (10% de crescimento)
**Fontes**: 2 documentos históricos em PT-PT

---

## Composição do Dataset

### Distribuição de Dados

| Componente | Exemplos | Percentagem | Notas |
|------------|----------|-------------|-------|
| Dataset V2 (original + biografias) | 953 | 90.9% | Base existente |
| Livro: Sporting Clube Farense Historia | 65 | 6.2% | livro_scf_1.txt |
| DOCX: 50 Anos de História do Futebol em Faro | 30 | 2.9% | 1900-1950 |
| **TOTAL V3** | **1.048** | **100%** | **Pronto para treino** |

### Breakdown por Fonte

#### Livro 1: Sporting Clube Farense (TXT)
**Ficheiro**: `dados/outros/livro_scf_1.txt` (1.108 linhas)
**Exemplos extraídos**: 65 pares Q&A

**Categorias cobertas**:
- Fundação e primeiros anos
- Primeiras equipas e jogadores
- Sedes (headquarters) históricas
- Campos de jogo
- Treinadores e administração
- Crises e transformações institucionais

#### Livro 2: 50 Anos de História do Futebol em Faro (DOCX)
**Ficheiro**: `dados/outros/50 anos de História do Futebol em Faro.docx` (3.637 parágrafos)
**Exemplos extraídos**: 30 pares Q&A

**Categorias cobertas**:
- Fundação e história inicial (1900-1910)
- João de Jesus Gralho e primeiros líderes
- Carlos Lyster Franco - introdutor das regras
- Partidas históricas (1914-1920)
- Campeonatos e competições
- Contexto regional e militar
- Associações académicas
- Jogadores memoráveis

---

## Scripts de Extração

### 1. extract_books_qa_comprehensive.py
**Propósito**: Extração de 40 pares do livro_scf_1.txt
**Categorias**: Fundação, equipas, personalidades, rivalidades, competições

```bash
python3 scripts/extract_books_qa_comprehensive.py
```

**Saída**: `data/livros_qa_comprehensive.jsonl` (40 linhas)

### 2. extract_books_qa_mega.py
**Propósito**: Extração de 25 pares do livro_scf_1.txt (seções específicas)
**Categorias**: Sedes, campos, história institucional

```bash
python3 scripts/extract_books_qa_mega.py
```

**Saída**: `data/livros_qa_mega.jsonl` (25 linhas)

### 3. extract_docx_50anos.py
**Propósito**: Extração de 30 pares do DOCX "50 Anos de História"
**Categorias**: Fundação, partidas, competições, contexto regional

```bash
python3 scripts/extract_docx_50anos.py
```

**Saída**: `data/livros_qa_docx_50anos.jsonl` (30 linhas)

### 4. combine_datasets.py (ATUALIZADO)
**Propósito**: Consolidar V2 com todos os 95 novos exemplos
**Funcionalidades**:
- Carrega Dataset V2 (953 exemplos)
- Carrega Dataset Livros Consolidado (95 exemplos)
- Combina em Dataset V3 (1.048 exemplos)
- Cria split train/validation 90/10
- Análise de distribuição de tipos

```bash
python3 scripts/combine_datasets.py
```

**Saídas**:
- `data/farense_dataset_v3.jsonl` (1.048 linhas)
- `data/train_v3.jsonl` (943 linhas - 90%)
- `data/valid_v3.jsonl` (105 linhas - 10%)

---

## Ficheiros de Dados Consolidados

### Ficheiros Intermédios
```
data/
├── livros_qa_comprehensive.jsonl    (40 pares - livro_scf_1.txt)
├── livros_qa_mega.jsonl             (25 pares - livro_scf_1.txt seções)
├── livros_qa_all.jsonl              (65 pares - consolidado TXT)
├── livros_qa_docx_50anos.jsonl      (30 pares - DOCX)
└── livros_qa_consolidated.jsonl     (95 pares - CONSOLIDADO FINAL)
```

### Ficheiros Finais (Dataset V3)
```
data/
├── farense_dataset_v3.jsonl         (1.048 exemplos - COMPLETO)
├── train_v3.jsonl                   (943 exemplos - TREINO 90%)
└── valid_v3.jsonl                   (105 exemplos - VALIDAÇÃO 10%)
```

---

## Distribuição de Tipos de Dados (Dataset V3)

### Top 5 Categorias

| Tipo | Exemplos | % |
|------|----------|-----|
| resultado_especifico | 494 | 47.14% |
| vencedor | 406 | 38.74% |
| historico_adversario | 18 | 1.72% |
| golos_adversario | 18 | 1.72% |
| partido_historico | 18 | 1.72% |

### Distribuição Histórica (Nova)

Os 95 novos exemplos adicionam conteúdo sobre:
- **Historia Fundacao**: Contexto da fundação (1900-1910)
- **Historia Sedes**: 9 exemplos sobre sedes históricas
- **Historia Campos**: 8 exemplos sobre campos de jogo
- **Figura Historica**: 8 exemplos sobre personalidades-chave
- **Partido Historico**: 18 exemplos sobre partidas memoráveis
- **Contexto**: Militar, académico, regional, social

---

## Processo de Extração

### Fluxo de Trabalho

```
Livro TXT (1.108 linhas)
    ↓
extract_books_qa_comprehensive.py (40 pares)
extract_books_qa_mega.py (25 pares)
    ↓
livros_qa_all.jsonl (65 pares)
    ↓
┌─────────────────────────────────────────┐
│                                         │
│    DOCX (3.637 parágrafos)             │
│       ↓                                │
│  extract_docx_50anos.py                │
│       ↓                                │
│  livros_qa_docx_50anos.jsonl (30)     │
│                                         │
└─────────────────────────────────────────┘
    ↓
livros_qa_consolidated.jsonl (95 pares)
    ↓
Dataset V2 (953 exemplos)
    ↓
combine_datasets.py
    ↓
farense_dataset_v3.jsonl (1.048 exemplos)
    ↓
┌──────────────────────────────┐
│   train_v3.jsonl (943)       │  90%
│   valid_v3.jsonl (105)       │  10%
└──────────────────────────────┘
```

---

## Características da Extração

### Qualidade de Conteúdo

✅ **Autêntico**: Todo o conteúdo é direto dos documentos históricos
✅ **Foco Farense**: 100% do conteúdo é exclusivamente sobre Sporting Clube Farense
✅ **Linguagem PT-PT**: Mantém a linguagem portuguesa portuguesa original
✅ **Contexto Histórico**: Preserva datas, nomes e contextos originais
✅ **Metadata Rica**: Cada exemplo inclui tipo, período, fonte, pessoa (quando relevante)

### Estrutura de Metadata

Cada exemplo Q&A segue esta estrutura:

```json
{
  "prompt": "Pergunta em português",
  "completion": "Resposta elaborada em português",
  "metadata": {
    "tipo": "categoria_conteudo",
    "periodo": "1910-1920 ou 1910 ou 1910-04",
    "fonte": "livro_scf_1.txt ou 50 anos de História do Futebol em Faro.docx",
    "pessoa": "Nome (opcional)",
    "local": "Localização (opcional)"
  }
}
```

---

## Estatísticas de Validação

### Integridade do Dataset

| Verificação | Resultado | Status |
|-------------|-----------|--------|
| Total de exemplos | 1.048 | ✅ |
| Validação JSON | 1.048/1.048 | ✅ |
| Campo 'prompt' | 1.048/1.048 | ✅ |
| Campo 'completion' | 1.048/1.048 | ✅ |
| Campo 'metadata' | 1.048/1.048 | ✅ |
| Train/Valid split | 943/105 (90/10) | ✅ |

### Distribuição de Tipos

O dataset V3 inclui **56 tipos diferentes** de conteúdo:

- **Resultados de partidas**: 47.14% (resultado_especifico + vencedor)
- **História**: 11.19% (partido_historico, sedes, campos, etc.)
- **Contexto**: 1.91% (regional, social, militar, académico)
- **Outros**: 39.76% (golos, rivalidades, análises)

---

## Comparação de Versões

| Aspecto | V1 | V2 | V3 | Δ |
|--------|-----|------|------|------|
| Dataset Original | 943 | 943 | 943 | - |
| Biografias | - | 10 | 10 | - |
| Livros Históricos | - | - | 95 | **+95** |
| **Total** | **943** | **953** | **1.048** | **+95** |
| Fontes | 1 | 1 | 3 | +2 |
| Tipos de Conteúdo | 45+ | 45+ | 56 | +11 |

---

## Recomendações de Uso

### Para Treino

Use os ficheiros V3 para novo treino do modelo:

```bash
# Treino completo
python3 scripts/train_lora.py \
    --train_data data/train_v3.jsonl \
    --val_data data/valid_v3.jsonl \
    --output_dir checkpoints_v3

# Fine-tuning incremental
python3 scripts/train_lora_incremental.py \
    --base_checkpoint checkpoints_v2 \
    --train_data data/train_v3.jsonl \
    --output_dir checkpoints_v3_incremental
```

### Para Avaliação

Comparar desempenho entre versões:

```bash
# Avaliar V2 vs V3
python3 scripts/compare_models.py \
    --model_v2 checkpoints_v2 \
    --model_v3 checkpoints_v3 \
    --test_data test_queries.txt
```

---

## Próximos Passos

### Fase 4 (Proposta)

1. **Treinar novo modelo** com Dataset V3
2. **Avaliar melhorias** em histórico vs. resultados
3. **Análise de cobertura** de tópicos
4. **Extração adicional** de outras fontes (se disponível)

### Potenciais Expansões

- Digitalização de mais capítulos dos livros
- Integração de registos de partidas/estatísticas
- Entrevistas ou testemunhos históricos
- Registos de jornais da época

---

## Referência Técnica

### Configuração de Reproducibilidade

- **Seed**: 42 (para split train/validation)
- **Formato**: JSONL (UTF-8)
- **Encoding**: UTF-8 (com preserve_ascii=False)
- **Python**: 3.8+
- **Dependências**: python-docx, json

### Localização dos Ficheiros

```
/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/
├── data/
│   ├── farense_dataset_v3.jsonl
│   ├── train_v3.jsonl
│   ├── valid_v3.jsonl
│   └── livros_qa_consolidated.jsonl
├── scripts/
│   ├── extract_books_qa_comprehensive.py
│   ├── extract_books_qa_mega.py
│   ├── extract_docx_50anos.py
│   └── combine_datasets.py
└── dados/outros/
    ├── livro_scf_1.txt
    └── 50 anos de História do Futebol em Faro.docx
```

---

## Conclusão

O Dataset V3 representa um aumento significativo na qualidade e quantidade de dados de treino, com foco em conteúdo histórico autêntico sobre o Sporting Clube Farense. A adição de 95 exemplos de duas fontes históricas distintas enriquece o modelo com contexto histórico, informações institucionais e narrativas detalhadas que melhoram a capacidade do chatbot responder sobre a história do clube.

**Status**: ✅ Pronto para utilização
**Data**: Novembro 2024
**Versão**: 3.0
