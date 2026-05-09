from __future__ import annotations

import json
import sys

import click

from devto_cli.client import API_KEY_ENV, DevToClient, DevToError


def _emit(payload: object) -> None:
    click.echo(json.dumps(payload, indent=2, sort_keys=False))


def _run(ctx: click.Context, fn):
    try:
        result = fn(ctx.obj["client"])
    except DevToError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)
    _emit(result)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--api-key",
    envvar=API_KEY_ENV,
    help=f"dev.to API key (or set ${API_KEY_ENV}).",
)
@click.pass_context
def cli(ctx: click.Context, api_key: str | None) -> None:
    """Interact with the dev.to API."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = DevToClient(api_key=api_key)
    ctx.call_on_close(ctx.obj["client"].__exit__)


@cli.group()
def articles() -> None:
    """Read articles from dev.to."""


@articles.command("list")
@click.option("--username", "-u", help="Filter by author username.")
@click.option("--page", type=int, help="Pagination page number.")
@click.option("--per-page", type=int, help="Articles per page.")
@click.pass_context
def articles_list(ctx, username, page, per_page):
    """List articles, optionally filtered by username."""
    _run(ctx, lambda c: c.list_articles(username=username, page=page, per_page=per_page))


@articles.command("get")
@click.argument("article_id", type=int)
@click.pass_context
def articles_get(ctx, article_id):
    """Get a single article by numeric ID."""
    _run(ctx, lambda c: c.get_article(article_id))


@articles.command("by-slug")
@click.argument("username")
@click.argument("slug")
@click.pass_context
def articles_by_slug(ctx, username, slug):
    """Get an article by USERNAME and SLUG."""
    _run(ctx, lambda c: c.get_article_by_slug(username, slug))


@articles.command("me")
@click.option("--page", type=int)
@click.option("--per-page", type=int)
@click.pass_context
def articles_me(ctx, page, per_page):
    """List your own articles (requires API key)."""
    _run(ctx, lambda c: c.list_my_articles(page=page, per_page=per_page))


@cli.group()
def users() -> None:
    """Look up users on dev.to."""


@users.command("get")
@click.argument("user_id", type=int)
@click.pass_context
def users_get(ctx, user_id):
    """Get a user by numeric ID."""
    _run(ctx, lambda c: c.get_user(user_id))


@users.command("by-username")
@click.argument("username")
@click.pass_context
def users_by_username(ctx, username):
    """Get a user by USERNAME."""
    _run(ctx, lambda c: c.get_user_by_username(username))


if __name__ == "__main__":
    cli()
