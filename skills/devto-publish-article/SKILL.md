---
name: devto-publish-article
description: Upload a markdown file as a new dev.to article, or update an existing one by ID. Use when the user has written a markdown post locally and wants to publish it (or save it as a draft) on dev.to.
---

# Publish or update a dev.to article from a markdown file

Use the `devto` CLI to create or update articles. Both operations require `DEVTO_API_KEY` to be set in the environment.

## When to use this skill

- The user has a `.md` file and wants to push it to dev.to (as draft or published).
- The user wants to update an existing dev.to post from a local markdown file.
- A workflow generated a blog post and needs to ship it.

## Prerequisite

```bash
export DEVTO_API_KEY=...   # generate at https://dev.to/settings/extensions
```

If the user hasn't set this, ask them to before running the commands — don't try to invent or guess a key.

## Create a new article

Default to `--draft` unless the user explicitly asks to publish — drafts are reversible, accidental live posts aren't.

```bash
uv run devto articles create <FILE>.md \
  --title "..." \
  --description "..." \
  --tag <tag1> --tag <tag2> \
  --draft
```

To publish immediately:
```bash
uv run devto articles create <FILE>.md --title "..." --tag python --published
```

Other flags: `--canonical-url`, `--main-image`, `--series`, `--organization-id`.

## Update an existing article

Get the article ID first (via the `devto-list-articles` or `devto-get-article` skill), then:

```bash
uv run devto articles update <ARTICLE_ID> <FILE>.md --published
```

The same metadata flags apply. Omitting a flag leaves that field as it was on the server (or as set by frontmatter in the markdown).

## Frontmatter

If the markdown file already has dev.to-style YAML frontmatter, you can omit the corresponding flags — dev.to parses them server-side from `body_markdown`. Example:

```markdown
---
title: My post
published: false
tags: python, cli
description: A short hook
---

Body goes here.
```

CLI flags override frontmatter when both are present.

## After publishing

The CLI prints the full article JSON. Surface the `url` field to the user so they can open the post:

```bash
uv run devto articles create post.md --title "..." --draft | jq -r '.url'
```

## Notes

- A 401/403 means `DEVTO_API_KEY` is missing or invalid — don't retry blindly.
- A 422 usually means a missing `title` (in flags or frontmatter) or duplicate title; surface the error body to the user verbatim.
- There is no delete endpoint in this CLI; if the user needs to retract a draft, do it in the dev.to web UI.
