# Agente de IA para Geração Automática de Testes com Pytest (LangChain + Azure OpenAI)

Gere arquivos de teste `pytest` automaticamente a partir de um **arquivo ou trecho de código Python** usando **LangChain** + **Azure OpenAI**.

## ✨ O que este projeto faz

- Recebe um arquivo/trecho Python e devolve `tests/test_<nome>.py`
- Garante:
  - `import pytest` na primeira linha
  - Funções `def test_*` com **casos de sucesso e de falha**
  - Uso de `pytest.raises` quando houver exceções esperadas
- Não usa rede/I/O nos testes — apenas chama as funções do módulo

## 🧱 Estrutura
agent/ # agente + prompts
examples/ # funções simples de exemplo
tests/ # saída gerada
main.py # CLI


## 🚀 Pré-requisitos

- Python 3.10+
- Uma instância/configuração do **Azure OpenAI** com um deployment (ex.: `gpt-4o-mini`)
- Variáveis de ambiente configuradas (ver `.env.example`)

## ⚙️ Instalação

```bash
git clone https://github.com/<seu-usuario>/dio-ai-pytest-agent.git
cd dio-ai-pytest-agent
python -m venv .venv
# Windows:
. .venv/Scripts/activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edite .env e preencha suas credenciais Azure OpenAI
```

## 🔑 Variáveis (.env)
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
# Opcional: DRY_RUN=true para gerar placeholders sem chamar o LLM


### 🧪 Como usar
## 1) Gerar testes a partir de um arquivo
```bash
python main.py generate --file examples/math_ops.py
# Saída: tests/test_math_ops.py
```
## 2) Gerar testes a partir de um trecho inline
```bash
python main.py generate --text "def soma(a,b): return a+b"
# Saída: tests/test_snippet.py
```
## 3) Rodar os testes
```bash
pytest -q
```
## 4) Sem credenciais (modo local)
```bash
python main.py generate --file examples/string_ops.py --dry-run
# Gera um arquivo de teste com TODOs (placeholders)
```
🧰 Exemplos incluídos

examples/math_ops.py: soma, subtrai, divide (raise em divisão por zero)

examples/string_ops.py: slugify (normalização simples)

📝 Como isso atende ao desafio

Código do agente: agent/ + main.py (LangChain + Azure OpenAI).

Exemplos de uso: examples/ com pelo menos duas funções; execução demonstrada acima.

README: este arquivo, com passo a passo e .env.example.

🖼️ (Opcional) Capturas de tela

Crie a pasta /images e adicione prints rodando python main.py e pytest.

📚 Notas sobre LangChain + Azure OpenAI

Este projeto usa langchain-openai e AzureChatOpenAI com temperature=0.2 para respostas determinísticas.

O prompt força formato pytest e a primeira linha import pytest.