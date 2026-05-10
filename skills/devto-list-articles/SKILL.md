---
name: devto-list-articles
description: List or search dev.to articles — by author username (public) or for the authenticated user's own posts (including drafts). Use to discover article IDs, find a post by title, or audit recent activity before editing.
---

# List and search dev.to articles

Use the `devto` CLI to enumerate articles. The dev.to public API does not expose a free-text search endpoint, so "search" here means listing by author and filtering client-side with `jq`.

## When to use this skill

- The user wants to find an article by partial title, tag, or recency without knowing the ID.
- The user wants to see what they've published or drafted recently.
- A workflow needs an article ID before calling `devto-get-article` or `devto-publish-article` (update path).

## Commands

List a user's public articles (paginated):
```bash
uv run devto articles list --username <USERNAME> --per-page 30 --page 1
```

List the authenticated user's own articles, including drafts (requires `DEVTO_API_KEY` in env):
```bash
uv run devto articles me --per-page 30
```

## Searching / filtering

Pipe the JSON list into `jq`. Examples:

Find by title substring (case-insensitive):
```bash
uv run devto articles list --username <USERNAME> --per-page 100 \
  | jq '[.[] | select(.title | ascii_downcase | contains("zod"))] | map({id, title, url})'
```

Filter by tag:
```bash
uv run devto articles list --username <USERNAME> --per-page 100 \
  | jq '[.[] | select(.tag_list | index("react"))] | map({id, title, tag_list})'
```

Most-recent N with just the fields needed for follow-up:
```bash
uv run devto articles me --per-page 50 \
  | jq 'sort_by(.published_at) | reverse | .[:10] | map({id, title, published, published_at})'
```

## Notes

- `articles list --username` only returns *published* posts. To see drafts, use `articles me` with an API key.
- The list endpoint returns truncated descriptions, not full `body_markdown`. Use `devto-get-article` once you have an ID.
- For very prolific authors, walk pages with `--page` since `--per-page` is capped server-side.
