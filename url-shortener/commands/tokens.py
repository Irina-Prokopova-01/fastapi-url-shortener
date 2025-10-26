from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens

app = typer.Typer(
    name="token",
    help="Tokens management",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def chek(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
):
    """
    Chek if the passed token is valid - exists or not.
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists[/green]"
            if tokens.token_exists(token)
            else "[red]dosen't exists[/red]"
        ),
    )


@app.command(
    name="list",
)
def list_tokens():
    """
    List all tokens.
    """
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join(([""] + tokens.get_tokens()))))
    print()


@app.command(
    name="rm",
)
def delete_token(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
):
    """
    Delete a token from DB.
    """
    if not tokens.token_exists(token):
        print(f"[bold]{token} [red]doesn't exist[/red][/bold]")

    tokens.delete_token(token)
    print(f"Token [bold]{token}[/bold] removed from DB")


@app.command()
def create():
    """
    Create a new token.
    """
    new_token = tokens.generate_and_save_token()
    print(f"New token [bold]{new_token}[/bold] saved to DB")


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to add",
        ),
    ],
):
    """
    Add a new token.
    """
    tokens.add_token(token)
    print(f"New token [bold]{token}[/bold] added to DB")
