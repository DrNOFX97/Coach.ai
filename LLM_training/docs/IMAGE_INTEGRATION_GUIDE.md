# Guia de Integração de Imagens - Opções 1 e 2

## Visão Geral

Criou com sucesso suporte para **respostas com imagens** em duas abordagens complementares:

1. **OPÇÃO 2**: Dataset Híbrido com Referências a Imagens
2. **OPÇÃO 1**: Modelos de Visão (Vision Language Models)

---

## OPÇÃO 2: Dataset Híbrido com Referências a Imagens

### O que é?

Dataset JSONL expandido que inclui referências a caminhos de imagem. O modelo continua a treinar apenas com texto, mas o frontend pode exibir imagens associadas.

### Característica

✅ **Simples de implementar**
✅ **Não requer retenção de modelo**
✅ **Compatível com qualquer modelo de texto**
✅ **Ideal para UX rica**

### Ficheiros Gerados

```
data/farense_dataset_hybrid.jsonl
  └─ 1.112 pares Q&A
     ├─ 152 pares com imagens (13.7%)
     └─ 960 pares apenas texto
```

### Formato do Dataset

```json
{
  "prompt": "Como era a equipa do Farense em 1982?",
  "completion": "A equipa de 1982 foi campeã...",
  "metadata": {
    "tipo": "equipa_historica",
    "periodo": "1982",
    "imagem": "dados/fotografias/equipas/1980-1989/1982-83 campeão.jpeg"
  }
}
```

### Como Usar

#### 1. **Backend - Treinar o Modelo**

O modelo treina apenas com texto (sem mudanças):

```python
from your_model import train_model

# Usar farense_dataset_v3_expanded.jsonl ou
# farense_dataset_hybrid.jsonl (ignorar campo 'imagem')
train_model(
    train_file="data/train_v3_expanded.jsonl",
    val_file="data/valid_v3_expanded.jsonl"
)
```

#### 2. **Frontend - Exibir Imagem + Resposta**

```python
import json
from pathlib import Path

def get_response_with_image(query: str, model):
    """Get response and associated image if available."""

    # Get response from model
    response = model.generate(query)

    # Load dataset to find matching image
    with open("data/farense_dataset_hybrid.jsonl") as f:
        for line in f:
            pair = json.loads(line)
            if pair['prompt'].lower() in query.lower():
                imagem = pair.get('metadata', {}).get('imagem')
                if imagem:
                    return {
                        "response": response,
                        "image_path": str(Path.cwd() / imagem),
                        "metadata": pair.get('metadata', {})
                    }

    return {"response": response, "image_path": None}
```

#### 3. **Web Interface - Exibir Resultado**

```html
<div class="response-container">
  <div class="text-response">
    <p id="answer"></p>
  </div>

  <div class="image-container" id="imageContainer" style="display:none;">
    <img id="responseImage" alt="Equipa histórica" />
    <p class="metadata" id="imageMeta"></p>
  </div>
</div>

<script>
async function submitQuery(query) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({query: query})
  });

  const data = await response.json();

  // Display text
  document.getElementById('answer').textContent = data.response;

  // Display image if available
  if (data.image_path) {
    document.getElementById('responseImage').src = data.image_path;
    document.getElementById('imageMeta').textContent =
      `${data.metadata.periodo} - ${data.metadata.tipo}`;
    document.getElementById('imageContainer').style.display = 'block';
  }
}
</script>
```

### Estatísticas de Cobertura

| Aspecto | Valor |
|---------|-------|
| Pares totais | 1.112 |
| Pares com imagem | 152 (13.7%) |
| Décadas cobertas | 14 |
| Tipos de conteúdo com imagem | 31 |

### Cobertura por Tipo

```
partido_historico:        21 pares (13.8%)
historia_sedes:           14 pares (9.2%)
historia_campos:          14 pares (9.2%)
figura_historica:         13 pares (8.6%)
competicao_historica:      7 pares (4.6%)
```

### Vantagens

✅ Rápido de implementar
✅ Sem overhead no modelo
✅ Melhor UX para utilizadores
✅ Fácil de manter e atualizar
✅ Compatible com qualquer framework

### Implementação Rápida

```bash
# 1. Gerar dataset híbrido
python3 scripts/create_hybrid_dataset.py

# 2. Usar como antes, mas com suporte a imagens
# O frontend verifica metadata['imagem'] e exibe

# 3. Treinar modelo (sem mudanças)
python3 scripts/train_lora.py \
    --train_data data/train_v3_expanded.jsonl \
    --val_data data/valid_v3_expanded.jsonl
```

---

## OPÇÃO 1: Vision Language Models

### O que é?

Modelos de IA que processam **simultaneamente** texto e imagem. O modelo retorna análises baseadas tanto na pergunta como na imagem.

### Características

✅ **Análise visual inteligente**
✅ **Respostas contextualizadas com imagem**
✅ **Descreve fotos automaticamente**
✅ **Interação mais natural**
⚠️ **Requer APIs ou GPU potente**

### Modelos Suportados

```
1. Claude 3/3.5 Vision (Anthropic)
   - Melhor qualidade
   - Requer API key
   - Pago por token

2. GPT-4V (OpenAI)
   - Muito capaz
   - Requer API key
   - Pago por token

3. LLaVA (Open-source)
   - Local, grátis
   - Requer 13B+ VRAM
   - Qualidade boa

4. Gemini Vision (Google)
   - Capaz
   - Requer API key
   - Pago por token
```

### Ficheiros Gerados

```
data/farense_dataset_vision_claude-3-vision.jsonl
data/farense_dataset_vision_gpt-4-vision.jsonl
data/farense_dataset_vision_llava.jsonl
data/farense_dataset_multimodal.jsonl (universal)

Cada contém 152 pares com imagens formatados para o modelo específico
```

### Formato para Claude 3 Vision

```json
{
  "role": "user",
  "content": [
    {
      "type": "image",
      "source": {
        "type": "file",
        "path": "dados/fotografias/equipas/1980-1989/1982-83 campeão.jpeg"
      }
    },
    {
      "type": "text",
      "text": "Como era a equipa do Farense em 1982?"
    }
  ],
  "metadata": {...},
  "expected_response": "A equipa de 1982..."
}
```

### Implementação com Claude 3 Vision

#### 1. **Setup**

```bash
# Instalar SDK
pip install anthropic

# Setup API key
export ANTHROPIC_API_KEY='sua-chave-aqui'
```

#### 2. **Usar no Código**

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic()

def analyze_with_vision(question: str, image_path: str) -> str:
    """Analyze image with Claude 3 Vision."""

    image_data = Path(image_path).read_bytes()

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64.b64encode(image_data).decode(),
                        },
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ],
            }
        ],
    )

    return message.content[0].text

# Example
response = analyze_with_vision(
    "Describa os jogadores visíveis nesta foto",
    "dados/fotografias/equipas/1982-83 campeão.jpeg"
)
print(response)
```

### Implementação com GPT-4V

```python
import openai
from pathlib import Path

client = openai.OpenAI()

def analyze_with_gpt4v(question: str, image_path: str) -> str:
    """Analyze image with GPT-4V."""

    image_data = Path(image_path).read_bytes()
    base64_image = base64.b64encode(image_data).decode()

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ],
        max_tokens=1024,
    )

    return response.choices[0].message.content

# Example
response = analyze_with_gpt4v(
    "Identifique os jogadores nesta foto",
    "dados/fotografias/equipas/1982-83 campeão.jpeg"
)
```

### Implementação com LLaVA (Local)

```python
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import torch

def analyze_with_llava(question: str, image_path: str) -> str:
    """Analyze image with LLaVA locally."""

    # Load model (first run downloads ~16GB)
    processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
    model = LlavaForConditionalGeneration.from_pretrained(
        "llava-hf/llava-1.5-7b-hf",
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load image
    image = Image.open(image_path)

    # Process
    inputs = processor(text=question, images=image, return_tensors="pt")

    # Generate response
    output = model.generate(**inputs, max_new_tokens=200)
    response = processor.decode(output[0], skip_special_tokens=True)

    return response

# Example
response = analyze_with_llava(
    "Descreva os jogadores visíveis",
    "dados/fotografias/equipas/1982-83 campeão.jpeg"
)
```

### Fluxo de Chat Completo

```python
class VisionChatbot:
    def __init__(self, model_type="claude-3-vision"):
        self.model_type = model_type
        if model_type == "claude-3-vision":
            self.client = anthropic.Anthropic()
        elif model_type == "gpt-4-vision":
            self.client = openai.OpenAI()

    def chat_with_image(self, question: str, image_path: str) -> Dict[str, str]:
        """Chat using vision model."""

        if self.model_type == "claude-3-vision":
            return self._claude_chat(question, image_path)
        elif self.model_type == "gpt-4-vision":
            return self._gpt4v_chat(question, image_path)

    def _claude_chat(self, question: str, image_path: str) -> Dict[str, str]:
        """Claude 3 Vision chat."""
        # ... implementation
        pass

    def _gpt4v_chat(self, question: str, image_path: str) -> Dict[str, str]:
        """GPT-4V chat."""
        # ... implementation
        pass

# Usage
bot = VisionChatbot(model_type="claude-3-vision")
result = bot.chat_with_image(
    "Qual é a formação tática desta equipa?",
    "dados/fotografias/equipas/1982-83 campeão.jpeg"
)
print(result)
```

### Requisitos

| Modelo | Requisito | Custo |
|--------|-----------|-------|
| Claude 3 Vision | API key | €0.03-0.15 por imagem |
| GPT-4V | API key | €0.01-0.03 por imagem |
| LLaVA | GPU 13GB+ VRAM | Grátis |
| Gemini Vision | API key | €0.0025-0.025 por imagem |

---

## Comparação: Opção 1 vs Opção 2

| Aspecto | Opção 2 (Híbrido) | Opção 1 (Vision) |
|--------|-------------------|-------------------|
| **Implementação** | Muito fácil | Moderada |
| **Custo** | Grátis | €0.01-0.15/imagem |
| **Latência** | Baixa | Média a alta |
| **Análise visual** | Não | Sim, inteligente |
| **Requer retenção** | Não | Não |
| **UX** | Simples | Avançada |
| **Escalabilidade** | Excelente | Boa |
| **Manutenção** | Simples | Moderada |

---

## Recomendação de Arquitetura

### Abordagem Híbrida Completa

```
┌──────────────────────────────────────────────────────────┐
│                        User Query                         │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Check if Image      │
    │  Related Query?      │
    └─────┬──────────┬─────┘
          │          │
        YES         NO
          │          │
    ┌─────▼──┐  ┌────▼──────┐
    │Vision  │  │Text Model  │
    │Model   │  │(Hybrid DS) │
    │Claude  │  │            │
    │3/GPT4V │  └─────┬──────┘
    └─────┬──┘        │
          │           │
          └─────┬─────┘
                │
                ▼
    ┌──────────────────────┐
    │Frontend Response:    │
    │• Text Answer         │
    │• Image (if available)│
    │• Metadata            │
    └──────────────────────┘
```

### Implementação

```python
class HybridChatbot:
    def __init__(self):
        self.text_model = load_text_model()
        self.vision_client = anthropic.Anthropic()
        self.hybrid_dataset = load_hybrid_dataset()

    def chat(self, query: str) -> Dict[str, Any]:
        # Check if image-related query
        if self._is_image_query(query):
            # Use Vision Model
            image_path = self._find_relevant_image(query)
            if image_path:
                return self._vision_response(query, image_path)

        # Use Text Model (Hybrid Dataset)
        response = self.text_model.generate(query)
        image = self._find_associated_image(query)

        return {
            "response": response,
            "image": image,
            "model_used": "hybrid"
        }

    def _is_image_query(self, query: str) -> bool:
        """Detect if query needs visual analysis."""
        keywords = ["mostrar", "describa", "vejo", "foto", "equipa",
                   "uniforme", "camisa", "visual"]
        return any(kw in query.lower() for kw in keywords)

    def _vision_response(self, query: str, image_path: str) -> Dict[str, Any]:
        """Get response from Vision Model."""
        # Use Claude 3 Vision
        message = self.vision_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "file", "path": image_path}
                    },
                    {"type": "text", "text": query}
                ]
            }]
        )

        return {
            "response": message.content[0].text,
            "image": image_path,
            "model_used": "vision"
        }
```

---

## Próximos Passos

### Curto Prazo (Esta semana)

1. **Implementar Opção 2 (Híbrido)**
   - Usar dataset `farense_dataset_hybrid.jsonl`
   - Frontend carrega imagem se existir em metadata
   - Treinar modelo normalmente

### Médio Prazo (Próximas semanas)

2. **Adicionar Opção 1 (Vision)**
   - Setup Claude 3 Vision (mais fácil)
   - Ou LLaVA se preferir local
   - Integrar com arquitetura híbrida

### Longo Prazo (Próximas meses)

3. **Expansão**
   - Fine-tune Vision Model com dataset
   - Aumentar cobertura de imagens (agora 13.7%)
   - Integração completa no frontend

---

## Ficheiros Criados

```
scripts/
├── create_hybrid_dataset.py          (Dataset Híbrido)
├── vision_model_integration.py       (Vision Models)
└── vision_chat_demo.py               (Demo)

data/
├── farense_dataset_hybrid.jsonl      (1.112 pares, 152 com imagem)
├── farense_dataset_multimodal.jsonl  (Universal format)
├── farense_dataset_vision_claude-3-vision.jsonl
├── farense_dataset_vision_gpt-4-vision.jsonl
└── farense_dataset_vision_llava.jsonl
```

---

## Status Atual

✅ Dataset Híbrido (Opção 2): **Pronto**
✅ Vision Models (Opção 1): **Pronto**
✅ Exemplo de Integração: **Pronto**
✅ Documentação: **Completa**

**Próximo Passo**: Escolher qual implementar primeiro ou começar com Opção 2 (mais simples).
