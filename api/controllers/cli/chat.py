import asyncio
import json
from typing import Optional

import typer
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from services.chat_service import ChatService

app = typer.Typer(help="Interactive CLI chat with LLM")
console = Console()


@app.command()
def chat(
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="LLM model to use (overrides LLM_DEFAULT_MODEL from config)",
    ),
    stream: bool = typer.Option(
        True,
        "--stream/--no-stream",
        help="Enable streaming output (default: True)",
    ),
):
    """
    Start an interactive chat session with the LLM.

    Type your messages and press Enter. Type 'exit', 'quit', or press Ctrl+C to quit.
    Type 'clear' to reset conversation history.
    """
    console.print(
        Panel.fit(
            "[bold cyan]SaRa CLI Chat[/bold cyan]\n"
            "Commands: [yellow]exit[/yellow], [yellow]quit[/yellow], [yellow]clear[/yellow]\n"
            f"Streaming: [green]{'ON' if stream else 'OFF'}[/green]",
            border_style="cyan",
        )
    )

    conversation_history: list[dict[str, str]] = []

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]You[/bold green]")

            if not user_input.strip():
                continue

            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if user_input.lower() == "clear":
                conversation_history.clear()
                console.print("[yellow]Conversation history cleared.[/yellow]")
                continue

            conversation_history.append({"role": "user", "content": user_input})

            console.print("\n[bold blue]Assistant[/bold blue]:")

            if stream:
                asyncio.run(_handle_streaming_response(conversation_history, model))
            else:
                asyncio.run(_handle_non_streaming_response(conversation_history, model))

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
            break
        except Exception as exc:
            console.print(f"[red]Error: {exc}[/red]")


async def _handle_streaming_response(
    conversation_history: list[dict[str, str]],
    model: Optional[str],
):
    full_response = ""

    try:
        with Live("", console=console, refresh_per_second=10) as live:
            async for chunk in ChatService.chat_stream(conversation_history, model=model):
                if chunk.startswith("data: "):
                    data_str = chunk[6:].strip()
                    try:
                        data = json.loads(data_str)
                        if data.get("done"):
                            break
                        content = data.get("content", "")
                        full_response += content
                        live.update(Markdown(full_response))
                    except json.JSONDecodeError:
                        continue

        console.print()

        if full_response:
            conversation_history.append({"role": "assistant", "content": full_response})

    except Exception as exc:
        console.print(f"[red]Streaming error: {exc}[/red]")


async def _handle_non_streaming_response(
    conversation_history: list[dict[str, str]],
    model: Optional[str],
):
    try:
        response = await ChatService.chat(conversation_history, model=model)
        console.print(Markdown(response))
        conversation_history.append({"role": "assistant", "content": response})
    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")


@app.command()
def once(
    message: str = typer.Argument(..., help="Message to send to the LLM"),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="LLM model to use",
    ),
    stream: bool = typer.Option(
        False,
        "--stream/--no-stream",
        help="Enable streaming output (default: False for one-shot)",
    ),
):
    """
    Send a single message to the LLM and print the response.

    Example:
        uv run python -m controllers.cli.chat once "What is 2+2?"
    """
    messages = [{"role": "user", "content": message}]

    if stream:
        asyncio.run(_once_streaming(messages, model))
    else:
        asyncio.run(_once_non_streaming(messages, model))


async def _once_streaming(messages: list[dict[str, str]], model: Optional[str]):
    full_response = ""
    try:
        with Live("", console=console, refresh_per_second=10) as live:
            async for chunk in ChatService.chat_stream(messages, model=model):
                if chunk.startswith("data: "):
                    data_str = chunk[6:].strip()
                    try:
                        data = json.loads(data_str)
                        if data.get("done"):
                            break
                        content = data.get("content", "")
                        full_response += content
                        live.update(Markdown(full_response))
                    except json.JSONDecodeError:
                        continue
        console.print()
    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(code=1)


async def _once_non_streaming(messages: list[dict[str, str]], model: Optional[str]):
    try:
        response = await ChatService.chat(messages, model=model)
        console.print(Markdown(response))
    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
