import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

try:
    from langchain_openai import AzureChatOpenAI
    from langchain.prompts import ChatPromptTemplate
except Exception:
    AzureChatOpenAI = None
    ChatPromptTemplate = None


from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

load_dotenv()

@dataclass
class LLMConfig:
    endpoint: str
    api_key: str
    api_version: str
    deployment: str

    @staticmethod
    def from_env() -> "LLMConfig":
        return LLMConfig(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        )

class TestGenAgent:
    def __init__(self, llm_config: Optional[LLMConfig] = None, dry_run: bool = False):
        self.llm_config = llm_config or LLMConfig.from_env()
        self.dry_run = dry_run or (os.getenv("DRY_RUN", "false").lower() == "true")

        if not self.dry_run:
            if AzureChatOpenAI is None or ChatPromptTemplate is None:
                raise RuntimeError("Dependências LangChain/LangChain-OpenAI não disponíveis.")
            if not (self.llm_config.endpoint and self.llm_config.api_key and self.llm_config.deployment):
                raise RuntimeError("Variáveis de ambiente Azure OpenAI ausentes. Verifique o .env.")

            self.llm = AzureChatOpenAI(
                azure_endpoint=self.llm_config.endpoint,
                api_key=self.llm_config.api_key,
                api_version=self.llm_config.api_version,
                azure_deployment=self.llm_config.deployment,
                temperature=0.2,
            )
            self.prompt = ChatPromptTemplate.from_messages(
                [("system", SYSTEM_PROMPT), ("user", USER_PROMPT_TEMPLATE)]
            )

    def generate_tests(self, code_text: str, module_name: str) -> str:
        if self.dry_run:
            return self._fallback_tests(code_text, module_name)

        messages = self.prompt.format_messages(code=code_text, module_name=module_name)
        res = self.llm.invoke(messages)
        # Garantir que só venha código puro
        content = res.content.strip()
        # Remove cercas de markdown se o modelo incluir por engano
        if content.startswith("```"):
            content = content.strip("`")
            content = content.replace("python", "", 1).strip()
        return content

    def _fallback_tests(self, code_text: str, module_name: str) -> str:
        # Fallback simples (sem LLM) para desenvolvimento local
        header = "import pytest\n"
        body = f"""
def test_placeholder_success():
    # TODO: Substituir por casos reais após configurar Azure OpenAI.
    assert True

def test_placeholder_failure():
    with pytest.raises(AssertionError):
        assert False, "Exemplo de falha proposital"

def test_skip_if_no_functions():
    pytest.skip("Modo DRY_RUN: configure Azure OpenAI para gerar casos reais para {module_name}.")
"""
        return header + body.strip() + "\n"
