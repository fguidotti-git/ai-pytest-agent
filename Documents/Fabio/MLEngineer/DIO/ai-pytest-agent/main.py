import os
import pathlib
import typer

from agent.agent import TestGenAgent, LLMConfig

app = typer.Typer(help="Agente gerador de testes pytest (LangChain + Azure OpenAI)")

def _read_text_or_file(input_path: str | None, text: str | None) -> tuple[str, str]:
    if input_path:
        p = pathlib.Path(input_path)
        if not p.exists() or p.suffix != ".py":
            raise typer.BadParameter("Forneça um caminho válido para um arquivo .py")
        code = p.read_text(encoding="utf-8")
        module_name = p.stem
        return code, module_name
    if text:
        # Nome padrão quando vier texto direto
        return text, "snippet"
    raise typer.BadParameter("Use --file ou --text para fornecer código.")

@app.command()
def generate(
    file: str = typer.Option(None, "--file", "-f", help="Caminho para o arquivo .py a ser testado"),
    text: str = typer.Option(None, "--text", "-t", help="Código Python inline"),
    outdir: str = typer.Option("tests", "--outdir", "-o", help="Diretório de saída dos testes"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Gerar testes placeholders sem chamar Azure"),
):
    """Gera um arquivo de testes pytest com base no código Python fornecido."""
    code, module_name = _read_text_or_file(file, text)

    os.makedirs(outdir, exist_ok=True)

    agent = TestGenAgent(LLMConfig.from_env(), dry_run=dry_run)
    test_code = agent.generate_tests(code, module_name)

    outfile = pathlib.Path(outdir) / f"test_{module_name}.py"
    outfile.write_text(test_code, encoding="utf-8")

    typer.secho(f"✔ Teste gerado: {outfile}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
