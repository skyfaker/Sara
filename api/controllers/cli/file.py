from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.rag.file_indexer import FileIndexer
from core.rag.file_loader.docling_loader import DoclingLoader
from services.file_service import (
    FileService,
    FileTooLargeError,
    UnsupportedFileTypeError,
)

console = Console()


def upload(
    file_path: str = typer.Argument(..., help="Path to DOCX file to upload"),
    user_id: str = typer.Option(
        "cli_user",
        "--user-id",
        "-u",
        help="User ID for the upload",
    ),
):
    path = Path(file_path)

    if not path.exists():
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(code=1)

    if not path.is_file():
        console.print(f"[red]Error: Path is not a file: {file_path}[/red]")
        raise typer.Exit(code=1)

    if path.suffix.lower() != ".docx":
        console.print(
            f"[red]Error: Only DOCX files are supported. Got: {path.suffix}[/red]"
        )
        raise typer.Exit(code=1)

    console.print(
        Panel.fit(
            f"[bold cyan]Uploading File[/bold cyan]\n"
            f"File: [yellow]{path.name}[/yellow]\n"
            f"Size: [yellow]{path.stat().st_size / 1024:.2f} KB[/yellow]\n"
            f"User: [yellow]{user_id}[/yellow]",
            border_style="cyan",
        )
    )

    try:
        from extensions.ext_storage import storage
        from extensions.storage.local_storage import LocalStorage
        
        if storage.storage_runner is None:
            storage.storage_runner = LocalStorage()
        
        with open(path, "rb") as f:
            content = f.read()

        with console.status("[bold green]Uploading file..."):
            file_info = FileService.upload_file(
                filename=path.name, content=content, user_id=user_id
            )

        console.print("[green]✓[/green] File uploaded successfully")

        table = Table(title="Upload Details", show_header=False, box=None)
        table.add_row("[cyan]File UUID[/cyan]", file_info["file_uuid"])
        table.add_row("[cyan]Filename[/cyan]", file_info["filename"])
        table.add_row("[cyan]Size[/cyan]", f"{file_info['size'] / 1024:.2f} KB")
        console.print(table)

        indexed = False
        if file_info["extension"] == "docx":
            try:
                console.print("\n[bold yellow]Starting automatic indexing...[/bold yellow]")

                with console.status("[bold green]Loading document..."):
                    import os
                    from configs import app_config
                    
                    file_full_path = os.path.join(
                        app_config.LOCAL_STORAGE_PATH,
                        file_info["file_key"]
                    )
                    loader = DoclingLoader()
                    documents = loader.load_file(file_full_path)

                console.print(
                    f"[green]✓[/green] Loaded {len(documents)} document chunks"
                )

                with console.status("[bold green]Indexing with LLM..."):
                    indexer = FileIndexer()
                    index_path = indexer.index_documents_sync(
                        documents=documents,
                        source_file=file_info["filename"],
                        file_id=file_info["file_uuid"],
                    )

                console.print("[green]✓[/green] Indexed successfully")
                console.print(f"[dim]Index saved to: {index_path}[/dim]")
                indexed = True

            except Exception as e:
                console.print(f"[red]✗ Indexing failed: {e}[/red]")
                console.print(
                    "[yellow]Note: File was uploaded but not indexed.[/yellow]"
                )

        console.print(
            "\n[bold green]✓ Upload and indexing complete![/bold green]" if indexed else "\n[bold green]✓ Upload complete![/bold green]"
        )

    except FileTooLargeError as e:
        console.print(f"[red]Error: {e.message}[/red]")
        raise typer.Exit(code=1)
    except UnsupportedFileTypeError as e:
        console.print(f"[red]Error: {e.message}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
