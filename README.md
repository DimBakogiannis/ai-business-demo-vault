# AI in Business — Demo Vault

This Obsidian vault is populated automatically by an n8n workflow via a localhost webhook.
A Node.js server (`webhook-server.js`) receives JSON payloads from n8n and writes markdown
files into the appropriate folders.

## Folder Structure

- **00-Inbox/** — scratchpad for manual notes and unsorted captures.
- **10-News/** — one markdown note per fetched article. The webhook server writes here.
  Each note links to concept hubs in `20-Concepts/` via `[[wikilinks]]`, which gives the
  Obsidian graph view its density.
- **20-Concepts/** — pre-seeded concept hub stubs (companies, models, themes, domains).
  News notes link into these so the graph clusters around topics.
- **30-Articles/** — aggregated, Medium-ready drafts written by n8n's AI Agent. The
  webhook server writes these as-is (the content field is already formatted markdown).
- **99-Archive/** — archived notes.
  - **n8n-workflows/** — exported `.json` workflow definitions for reproducibility.

## How the Pipeline Works

1. An n8n workflow runs daily.
2. It fetches tech news, then uses an AI Agent to summarize and structure each article.
3. n8n POSTs each article to `http://localhost:5679/news` (per-article notes).
4. n8n POSTs an aggregated Medium draft to `http://localhost:5679/article`.
5. `webhook-server.js` writes each payload as a markdown file in the right folder.
6. The Obsidian Git plugin (set to auto-pull every 2 minutes) picks up new files,
   so the vault stays in sync with the filesystem.

## Running the Webhook Server

```bash
sh start.sh
```

This script:
- Loads `.env` if it exists (so `VAULT_PATH` and `PORT` are set).
- Runs `npm install` if `node_modules/` is missing.
- Starts the Express server with `node webhook-server.js`.

Copy `.env.example` to `.env` and set `VAULT_PATH` to the absolute path of this vault
before first run.

## Webhook Endpoints

- `POST /news`    — per-article summary notes → `10-News/`
- `POST /article` — aggregated Medium drafts  → `30-Articles/`

See `webhook-server.js` for the JSON schema each endpoint expects.
