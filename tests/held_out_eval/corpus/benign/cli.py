"""Command-line interface for Quill tools."""
import click
import httpx

DEFAULT_BASE = "https://api.quill.example.com/v1"


@click.group()
@click.option("--base-url", default=DEFAULT_BASE, envvar="QUILL_BASE_URL")
@click.option("--token", envvar="QUILL_TOKEN", required=True)
@click.pass_context
def main(ctx, base_url, token):
    """Quill command-line client."""
    ctx.obj = httpx.Client(
        base_url=base_url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )


@main.command("list")
@click.option("--tag")
@click.pass_obj
def list_notes(client, tag):
    """List notes, optionally filtered by tag."""
    params = {"tag": tag} if tag else {}
    resp = client.get("/notes", params=params)
    resp.raise_for_status()
    for note in resp.json()["notes"]:
        click.echo(f"{note['id']}\t{note['title']}")


@main.command("create")
@click.argument("title")
@click.option("--body", default="")
@click.pass_obj
def create_note(client, title, body):
    """Create a new note."""
    resp = client.post("/notes", json={"title": title, "body": body})
    resp.raise_for_status()
    click.echo(f"created {resp.json()['id']}")


if __name__ == "__main__":
    main()
