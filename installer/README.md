# devto-cli-skills

Installer that copies the [devto-cli](https://github.com/alchemicduncan/devto-cli) agent skills into your project so Claude Code (and other compatible agents) can discover them.

## Usage

In your project root:

```bash
npx devto-cli-skills install
```

This copies the bundled `SKILL.md` files into `.claude/skills/`:

- `devto-get-article` — fetch a single article by ID or `username/slug`
- `devto-list-articles` — list / filter articles by author, including your drafts
- `devto-publish-article` — upload or update an article from a markdown file

### Options

```bash
npx devto-cli-skills install --target .cursor/skills   # custom target dir
npx devto-cli-skills install --force                   # overwrite existing
npx devto-cli-skills list                              # list bundled skills
```

## Prerequisite

The skills shell out to the `devto` Python CLI. Install it from the parent repo:

```bash
git clone https://github.com/alchemicduncan/devto-cli && cd devto-cli && uv sync
```

Set `DEVTO_API_KEY` in your environment for any write or `articles me` commands.
