# devto-cli

CLI for interacting with the [dev.to API](https://developers.forem.com/api).

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

For authenticated endpoints, generate an API key from your dev.to account settings and export it:

```bash
export DEVTO_API_KEY=...
```

## Usage

```bash
uv run devto --help
uv run devto articles list --username guilhermecheng --per-page 5
uv run devto articles get 1475746
uv run devto articles by-slug guilhermecheng how-to-use-devto-api-4p65
uv run devto articles me                  # requires DEVTO_API_KEY
uv run devto users by-username ben

# Upload / update markdown articles (requires DEVTO_API_KEY)
uv run devto articles create post.md --title "My post" --tag python --tag cli --draft
uv run devto articles update 1234567 post.md --published
```

Output is JSON on stdout — pipe to `jq` to filter.
