import typer

import controllers.cli.chat as chat
import controllers.cli.file as file
import controllers.cli.rag as rag

app = typer.Typer(help="SaRa CLI - RAG knowledge base assistant")

app.command("chat")(chat.chat)
app.command("chat_once")(chat.once)

app.command("upload")(file.upload)

app.command("query")(rag.query)
app.command("ask")(rag.ask)

if __name__ == "__main__":
    app()
