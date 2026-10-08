# AI in Business — Demo Vault

An Obsidian vault filled automatically every day by an n8n workflow: it pulls tech news,
has Claude write a structured summary, and commits the note straight to this GitHub repo.
Obsidian (with the Obsidian Git plugin) pulls the new notes in. A small Streamlit app,
**Vault Chat**, lets you ask Claude questions about the vault.

## Folder Structure

- **00-Inbox/** — `Course MOC.md` (the central hub note) plus manual notes.
- **10-News/** — one markdown note per daily news digest, committed by n8n. Each note links
  to concept and people hubs via `[[wikilinks]]`, which gives the graph view its density.
- **20-Concepts/** — concept hub stubs (companies, models, themes, domains).
- **25-People/** — person stubs (CEOs, lead researchers).
- **30-Articles/** — older Medium-style drafts from earlier versions of the workflow.
- **99-Archive/n8n-workflows/** — the exported n8n workflow (`AI-Powered Tech news Agent.json`).

## How the Pipeline Works

1. **Daily 8AM trigger** in n8n.
2. Fetches news from RSS (BBC Tech, The Verge, Ars Technica, TechCrunch) and NewsAPI,
   keeps the last 24 hours, and takes the top 15.
3. An AI Agent (Claude via the Anthropic node) writes the digest and fetches full articles
   when it needs them.
4. The result is emailed (Gmail) and formatted as Obsidian markdown.
5. The **GitHub node** commits it to `10-News/YYYY-MM-DD <slug>.md` in this repo.
6. The Obsidian Git plugin auto-pulls, so new notes appear in the vault.

### Importing the workflow

Import `99-Archive/n8n-workflows/AI-Powered Tech news Agent.json` into n8n, then set up
your own credentials: Anthropic API, NewsAPI (header auth), Gmail OAuth2, and GitHub OAuth2.
Change the Gmail `sendTo` address and the GitHub node's owner/repository to your own.
The Medium and "Save to Obsidian" (Local REST API) nodes are disabled alternatives.

## Vault Chat

Ask questions about the vault in a browser. It loads `10-News`, `20-Concepts`, `25-People`
and `00-Inbox` into Claude's context (prompt-cached) and answers with sources.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set ANTHROPIC_API_KEY
streamlit run vault_chat.py
```

## Optional: Local Webhook Server

`webhook-server.js` is an alternative to the GitHub path: n8n POSTs JSON to localhost and
the server writes the markdown files. Not used by the current workflow.

```bash
cp .env.example .env   # set VAULT_PATH to the absolute path of this vault
sh start.sh            # npm install on first run, then node webhook-server.js
```

- `POST /news`    — per-article summary notes → `10-News/`
- `POST /article` — aggregated drafts → `30-Articles/`
- `GET  /health`  — health check

See `webhook-server.js` for the JSON schema each endpoint expects.
