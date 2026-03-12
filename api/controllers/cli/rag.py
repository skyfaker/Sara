import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from core.rag.retriever import Retriever
from services.chat_service import ChatService

console = Console()


def query(
    top_k: int = typer.Option(
        3,
        "--top-k",
        "-k",
        help="Number of documents to retrieve (default: 3)",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="LLM model to use (overrides LLM_DEFAULT_MODEL from config)",
    ),
):
    console.print(
        Panel.fit(
            "[bold cyan]SaRa RAG Query[/bold cyan]\n"
            "Commands: [yellow]exit[/yellow], [yellow]quit[/yellow], [yellow]sources[/yellow]\n"
            f"Top-K: [green]{top_k}[/green]",
            border_style="cyan",
        )
    )

    retriever = Retriever()
    last_sources = []

    while True:
        try:
            user_query = Prompt.ask("\n[bold green]Question[/bold green]")

            if not user_query.strip():
                continue

            if user_query.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if user_query.lower() == "sources":
                if last_sources:
                    _display_sources(last_sources)
                else:
                    console.print("[yellow]No sources available. Ask a question first.[/yellow]")
                continue

            with console.status("[bold green]Retrieving documents...[/bold green]"):
                documents = retriever.retrieve_sync(user_query, top_k=top_k)

            if not documents:
                console.print("[yellow]No relevant documents found.[/yellow]")
                continue

            last_sources = documents
            _display_sources(documents)

            context = _build_context(documents)
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的问答助手。根据提供的文档内容回答用户问题。如果文档中没有相关信息，请明确说明。"
                },
                {
                    "role": "user",
                    "content": f"文档内容：\n{context}\n\n用户问题：{user_query}"
                }
            ]

            console.print("\n[bold blue]Answer[/bold blue]:")
            asyncio.run(_handle_rag_response(messages, model))

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
            break
        except Exception as exc:
            console.print(f"[red]Error: {exc}[/red]")


def ask(
    question: str = typer.Argument(..., help="Question to ask based on indexed documents"),
    top_k: int = typer.Option(
        3,
        "--top-k",
        "-k",
        help="Number of documents to retrieve (default: 3)",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="LLM model to use",
    ),
    show_sources: bool = typer.Option(
        False,
        "--show-sources",
        "-s",
        help="Display source documents",
    ),
):
    try:
        with console.status("[bold green]Retrieving documents...[/bold green]"):
            retriever = Retriever()
            documents = retriever.retrieve_sync(question, top_k=top_k)

        if not documents:
            console.print("[yellow]No relevant documents found.[/yellow]")
            raise typer.Exit(code=0)

        if show_sources:
            _display_sources(documents)

        context = _build_context(documents)
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的问答助手。根据提供的文档内容回答用户问题。如果文档中没有相关信息，请明确说明。"
            },
            {
                "role": "user",
                "content": f"文档内容：\n{context}\n\n用户问题：{question}"
            }
        ]

        asyncio.run(_handle_rag_response(messages, model))

    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(code=1)


async def _handle_rag_response(messages: list[dict[str, str]], model: Optional[str]):
    try:
        response = await ChatService.chat(messages, model=model)
        console.print(Markdown(response))
    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")


def _display_sources(documents: list):
    table = Table(title="Retrieved Sources")
    table.add_column("Source File", style="cyan")
    table.add_column("Relevance Score", style="yellow", justify="right")

    for doc in documents:
        table.add_row(
            doc.source_file,
            f"{doc.relevance_score:.2f}"
        )

    console.print(table)


def _build_context(documents: list) -> str:
    context_parts = []
    for idx, doc in enumerate(documents, 1):
        context_parts.append(f"--- 文档 {idx}: {doc.source_file} ---")
        context_parts.append(doc.content)
        context_parts.append("")
    return "\n".join(context_parts)
