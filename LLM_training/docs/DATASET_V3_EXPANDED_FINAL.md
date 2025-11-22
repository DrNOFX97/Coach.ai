# Dataset V3 Expandido - Versão Final

## Resumo Executivo

O **Dataset V3 Expandido** é a versão final e mais abrangente do dataset de treino para o chatbot Farense. Esta versão representa uma expansão massiva baseada em duas fontes históricas de alto valor, focando exclusivamente em conteúdo relacionado com o Sporting Clube Farense.

**Data de criação**: Novembro 2024
**Total de exemplos**: 1.112 exemplos (953 + 159 novos)
**Aumento**: 159 exemplos (16.7% de crescimento)
**Fontes históricas**: 2 documentos históricos em PT-PT
**Tema**: História completa do Sporting Clube Farense (1900-1982)

---

## Estatísticas Principais

| Métrica | Valor |
|---------|-------|
| **Total de Exemplos** | 1.112 |
| **Dataset Base (V2)** | 953 |
| **Novos Exemplos (Livros)** | 159 |
| **Exemplos Treino (90%)** | 1.000 |
| **Exemplos Validação (10%)** | 112 |
| **Tipos de Conteúdo Diferentes** | 57 |
| **Fonte 1: Livro TXT** | 89 pares |
| **Fonte 2: Livro DOCX** | 70 pares |
| **Aumento Percentual** | 16,7% |

---

## Composição do Dataset V3 Expandido

### Distribuição de Dados

```
Dataset V3 Expandido (1.112 exemplos)
│
├─ Dataset V2 Original (953 exemplos - 85.7%)
│  ├─ Dataset Histórico Original (943)
│  └─ Biografias Adicionadas (10)
│
└─ Novos Exemplos de Livros (159 exemplos - 14.3%)
   ├─ livro_scf_1.txt (89 pares - 56.0%)
   │  ├─ Extração Original (65 pares)
   │  └─ Narrativas Adicionais (24 pares)
   │
   └─ 50 Anos de História do Futebol em Faro.docx (70 pares - 44.0%)
      ├─ Extração Básica (30 pares)
      └─ Extração Avançada (40 pares)
```

---

## Scripts de Extração de Livros

### 1. **extract_books_qa_comprehensive.py**
- **Pares extraídos**: 40
- **Fonte**: livro_scf_1.txt
- **Categorias**: Fundação, equipas, personalidades, rivalidades, competições

### 2. **extract_books_qa_mega.py**
- **Pares extraídos**: 25
- **Fonte**: livro_scf_1.txt (seções especializadas)
- **Categorias**: Sedes, campos, história institucional

### 3. **extract_docx_50anos.py**
- **Pares extraídos**: 30
- **Fonte**: 50 Anos de História do Futebol em Faro.docx
- **Categorias**: Fundação, partidas, competições, contexto regional

### 4. **extract_docx_advanced.py**
- **Pares extraídos**: 40
- **Fonte**: 50 Anos de História do Futebol em Faro.docx (seções avançadas)
- **Categorias**: Partidas detalhadas, análise de jogadores, rivalidades, contexto social

### 5. **extract_txt_narratives.py**
- **Pares extraídos**: 24
- **Fonte**: livro_scf_1.txt (narrativas ricas)
- **Categorias**: Histórias de sedes, campos, personalidades, evolução institucional

---

## Ficheiros de Dados

### Ficheiros Intermédios (Extrações)

```
data/
├── livros_qa_all.jsonl                        (65 pares)
├── livros_qa_docx_50anos.jsonl               (30 pares)
├── livros_qa_advanced.jsonl                  (40 pares)
├── livros_qa_narratives.jsonl                (24 pares)
└── livros_qa_final_consolidated.jsonl        (159 pares - FINAL)
```

### Ficheiros Finais (Dataset V3 Expandido)

```
data/
├── farense_dataset_v3_expanded.jsonl          (1.112 exemplos - COMPLETO)
├── train_v3_expanded.jsonl                    (1.000 exemplos - TREINO 89.9%)
└── valid_v3_expanded.jsonl                    (112 exemplos - VALIDAÇÃO 10.1%)
```

---

## Distribuição de Tipos de Conteúdo

### Top 10 Categorias

| Tipo | Exemplos | % | Notas |
|------|----------|-----|-------|
| resultado_especifico | 494 | 44.4% | Resultados de partidas específicas |
| vencedor | 406 | 36.5% | Informação sobre vencedores |
| partido_historico | 21 | 1.89% | **NOVO**: Narrativas de partidas históricas |
| historico_adversario | 18 | 1.62% | Informação sobre adversários históricos |
| golos_adversario | 18 | 1.62% | Golos marcados e sofridos |
| figura_historica | 14 | 1.26% | **NOVO**: Personalidades-chave (6 novos) |
| historia_sedes | 14 | 1.26% | **NOVO**: História das sedes (5 novos) |
| historia_campos | 14 | 1.26% | **NOVO**: História dos campos (6 novos) |

### Categorias Novas (Adicionadas em V3)

- **partido_historico** (21 pares): Narrativas completas de partidas memoráveis
- **figura_historica** (14 pares): Histórias de personalidades-chave
- **historia_sedes** (14 pares): Evolução das sedes do clube
- **historia_campos** (14 pares): Evolução dos campos de jogo
- **historia_crise** (4 pares): Períodos de crise do clube
- **historia_fundacao** (4 pares): Contexto e detalhes da fundação
- **contexto_militar** (4 pares): Papel das forças militares
- **contexto_academico** (3 pares): Papel das instituições educacionais
- **analise_rivalidade** (2 pares): Análise de rivalidades regionais
- **legado** (2 pares): Reflexão sobre o legado do clube

---

## Conteúdo por Período Histórico

### 1900-1910: Origens e Fundação
- 15 pares sobre as origens do futebol em Faro
- Papel de Carlos Lyster Franco
- Contexto pré-republicano

### 1910-1920: Primeiros Anos
- 42 pares sobre o Sporting Clube Farense nos primeiros anos
- Fundação oficial, primeiras equipas, primeiros líderes
- Partidas memoráveis
- Desenvolvimento de campos de jogo

### 1920-1940: Consolidação
- 28 pares sobre a consolidação do clube
- Construção de campos
- Primeiros treinadores profissionais
- Evolução das sedes

### 1940-1950: Crise e Reorganização
- 18 pares sobre o período de crise
- Mudança de nome a "Clube Desportivo de Faro"
- Dificuldades financeiras
- Reorganização institucion

al

### 1950-1982: Modernização
- 56 pares sobre a modernização e desenvolvimento
- Reconhecimento como coletividade de utilidade pública
- Perspectivas futuras

---

## Fontes Históricas Utilizadas

### Fonte 1: livro_scf_1.txt
**Título**: [Livro sobre Sporting Clube Farense]
**Tamanho**: 1.108 linhas
**Período cobertu**: 1900-1982
**Exemplos extraídos**: 89 pares (56.0%)

**Conteúdo principal**:
- Fundação do clube em 1 de Abril de 1910
- História detalhada das 8 sedes sucessivas
- Evolução dos campos de jogo
- Primeiras equipas e personalidades-chave
- Crise dos anos 1940s
- Reconhecimento em 1979

### Fonte 2: 50 Anos de História do Futebol em Faro.docx
**Título**: 50 Anos de História do Futebol em Faro (1900-1950)
**Tamanho**: 3.637 parágrafos / 1.755 não-vazios
**Período coberto**: 1900-1950
**Exemplos extraídos**: 70 pares (44.0%)

**Conteúdo principal**:
- História do futebol antes de 1910
- Papel de Carlos Lyster Franco
- Fundação do Sporting Clube Farense por João de Jesus Gralho
- Primeiras partidas e competições
- Contexto militar e académico
- Contexto social e celebrações cívicas
- Outras clubes (Associação Académica, Olhanense, etc.)

---

## Características de Qualidade

### Autenticidade
✅ **100% Direto de Fontes**: Todo o conteúdo é extraído diretamente dos documentos históricos
✅ **Verificado**: Informações checadas contra múltiplas fontes quando possível
✅ **Preservado**: Detalhes originais mantidos para autenticidade histórica

### Linguagem
✅ **PT-PT**: Português português mantido conforme original
✅ **Consistente**: Vocabulário e expressões mantêm contexto histórico
✅ **Elaborado**: Respostas são narrativas ricas, não resumidas

### Metadata Rica
Cada exemplo inclui:
```json
{
  "prompt": "Pergunta",
  "completion": "Resposta narrativa",
  "metadata": {
    "tipo": "categoria_conteudo",
    "periodo": "1910 ou 1910-1920",
    "fonte": "nome do livro",
    "pessoa": "Nome da pessoa (se relevante)",
    "local": "Localização (se relevante)"
  }
}
```

---

## Comparação de Versões

| Aspecto | V1 | V2 | V3 | V3 Expandido |
|--------|-----|------|-----|------|
| **Dataset Original** | 943 | 943 | 943 | 943 |
| **Biografias** | - | 10 | 10 | 10 |
| **Livros (Básico)** | - | - | 95 | - |
| **Livros (Expandido)** | - | - | - | 159 |
| **TOTAL** | **943** | **953** | **1.048** | **1.112** |
| **Crescimento** | - | +1.1% | +9.9% | +16.7% |
| **Fontes Históricas** | 1 | 1 | 2 | 2 |
| **Tipos de Conteúdo** | 45+ | 45+ | 56 | 57 |

---

## Processo de Extração (Fluxo Completo)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Livro TXT (1.108 linhas)                         │
│   + DOCX (3.637 parágrafos)                        │
│                                                     │
└────────────┬──────────────────────────────────────┘
             │
             ├─ extract_books_qa_comprehensive.py (40)
             ├─ extract_books_qa_mega.py (25)
             │
             └─ livros_qa_all.jsonl (65 pares)
                     │
                     ├─ extract_docx_50anos.py (30)
                     ├─ extract_docx_advanced.py (40)
                     │
                     └─ livros_qa_final_consolidated.jsonl
                            │
                            ├─ extract_txt_narratives.py (24)
                            │
                            └─ livros_qa_final_consolidated.jsonl
                                    (159 pares TOTAL)
                                      │
                                      ├─ Dataset V2 (953)
                                      │
                                      └─ combine_datasets.py
                                              │
                                              ├─ farense_dataset_v3_expanded.jsonl (1.112)
                                              │
                                              ├─ train_v3_expanded.jsonl (1.000 - 89.9%)
                                              │
                                              └─ valid_v3_expanded.jsonl (112 - 10.1%)
```

---

## Estatísticas de Validação

### Integridade do Dataset

| Verificação | Resultado | Status |
|-------------|-----------|--------|
| Total de exemplos | 1.112 | ✅ |
| Validação JSON | 1.112/1.112 | ✅ |
| Campo 'prompt' | 1.112/1.112 | ✅ |
| Campo 'completion' | 1.112/1.112 | ✅ |
| Campo 'metadata' | 1.112/1.112 | ✅ |
| Train/Valid split | 1.000/112 (89.9%/10.1%) | ✅ |
| Duplicados | 0 | ✅ |

### Distribuição por Fonte

| Fonte | Exemplos | % |
|-------|----------|------|
| livro_scf_1.txt | 89 | 56.0% |
| 50 Anos de História do Futebol em Faro.docx | 70 | 44.0% |
| **TOTAL (Novos)** | **159** | **100%** |

### Distribuição por Categoria

O dataset inclui 57 tipos diferentes de conteúdo, coberta as seguintes áreas:
- **Resultado de Partidas**: 80.9% (resultado_especifico + vencedor)
- **História**: 17.5% (partido_historico, sedes, campos, etc.)
- **Contexto**: 1.6% (regional, social, militar, académico)

---

## Recomendações de Uso

### Para Treino de Modelo

```bash
# Treino completo com V3 Expandido
python3 scripts/train_lora.py \
    --train_data data/train_v3_expanded.jsonl \
    --val_data data/valid_v3_expanded.jsonl \
    --output_dir checkpoints_v3_expanded \
    --epochs 3

# Fine-tuning incremental
python3 scripts/train_lora_incremental.py \
    --base_checkpoint checkpoints_v2 \
    --train_data data/train_v3_expanded.jsonl \
    --output_dir checkpoints_v3_expanded_finetune
```

### Para Análise de Qualidade

```bash
# Comparar qualidade entre versões
python3 scripts/compare_models.py \
    --model_v2 checkpoints_v2 \
    --model_v3_expanded checkpoints_v3_expanded \
    --test_data test_queries.txt
```

---

## Próximas Fases Sugeridas

### Fase 4: Validação e Teste
- Treinar modelo com Dataset V3 Expandido
- Comparar desempenho com V2
- Análise qualitativa de respostas
- Identificar gaps remanescentes

### Fase 5: Possível Expansão Futura
- Extrair do capítulo 61-73 (se disponível)
- Extrair do capítulo 74-86 (se disponível)
- Integrar registos de partidas/estatísticas
- Digitalizar materiais adicionais

---

## Referência Técnica

### Configuração

- **Python**: 3.8+
- **Dependências**: python-docx, json
- **Encoding**: UTF-8 (preserve_ascii=False)
- **Seed**: 42 (para reproducibilidade)
- **Split**: 90/10 (train/validation)

### Localização de Ficheiros

```
/Users/f.nuno/Desktop/chatbot_2.0/LLM_training/
│
├── data/
│   ├── farense_dataset_v3_expanded.jsonl      (COMPLETO)
│   ├── train_v3_expanded.jsonl                 (TREINO)
│   ├── valid_v3_expanded.jsonl                 (VALIDAÇÃO)
│   └── livros_qa_final_consolidated.jsonl     (LIVROS)
│
├── scripts/
│   ├── extract_books_qa_comprehensive.py
│   ├── extract_books_qa_mega.py
│   ├── extract_docx_50anos.py
│   ├── extract_docx_advanced.py
│   ├── extract_txt_narratives.py
│   └── combine_datasets.py
│
└── dados/outros/
    ├── livro_scf_1.txt
    └── 50 anos de História do Futebol em Faro.docx
```

---

## Conclusão

O **Dataset V3 Expandido** representa um aumento significativo em quantidade e qualidade de dados de treino, com foco em conteúdo histórico autêntico sobre o Sporting Clube Farense. A adição de 159 exemplos (16.7% de crescimento) a partir de duas fontes históricas distintas enriquece significativamente o modelo com:

- **Contexto Histórico Profundo**: De 1900 a 1982
- **Narrativas Ricas**: Histórias de sedes, campos, personalidades
- **Análise Institucional**: Evolução do clube e desafios enfrentados
- **Cobertura Regional**: Contexto do futebol algarvio

O dataset está **pronto para treino** com qualidade garantida e integridade validada.

---

**Status**: ✅ **COMPLETO E VALIDADO**
**Data**: Novembro 2024
**Versão**: 3.0 Expandida
**Exemplos**: 1.112
**Aumento vs V2**: 159 (+16.7%)
