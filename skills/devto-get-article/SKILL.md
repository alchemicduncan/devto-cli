---
name: devto-get-article
description: Fetch a single dev.to article by numeric ID or by username+slug, returning the full JSON payload (title, body_markdown, tags, reactions, etc.). Use when the user references a dev.to URL or article ID.
---

# Fetch a dev.to article

Use the `devto` CLI (provided by the `devto-cli` Python package) to read a single article. No API key is needed for public articles.

## When to use this skill

- The user pastes a dev.to URL (e.g. `https://dev.to/<username>/<slug>`) and wants the article content or metadata.
- The user names a dev.to article by ID and wants its body, tags, or stats.
- A workflow needs to inspect an existing post before editing it (pair with `devto-publish-article`).

## Commands

By numeric ID:
```bash
uv run devto articles get <ARTICLE_ID>
```

By username + slug (parse these from the URL — `https://dev.to/<username>/<slug>`):
```bash
uv run devto articles by-slug <USERNAME> <SLUG>
```

## Working with the output

The CLI prints the full JSON response to stdout. Pipe to `jq` to extract specific fields:

```bash
uv run devto articles get 1475746 | jq '{title, tags, body_markdown}'
uv run devto articles by-slug guilhermecheng how-to-use-devto-api-4p65 | jq -r '.body_markdown' > article.md
```

Useful fields: `id`, `title`, `description`, `body_markdown`, `tags`, `published`, `url`, `canonical_url`, `reading_time_minutes`, `public_reactions_count`, `user.username`.

## Notes

- The endpoint is unauthenticated for public articles — no `DEVTO_API_KEY` needed.
- For the user's own *unpublished* drafts, use the `devto-list-articles` skill with `articles me` instead (the public `get` endpoint won't return them).
- If `uv run devto` is not on PATH, the CLI is not installed in this project — fall back to telling the user to run `uv sync` in the devto-cli repo, or `pipx install devto-cli` once published.
