# Vault Context for Claude Code

This is an Obsidian vault built for an **AI in Business** course demo. It was populated by an n8n workflow (May 2026) that fetched tech news, had Claude write a summary, and committed it to GitHub; Obsidian pulled from GitHub. The pipeline is no longer running — the vault is a snapshot.

## Folder structure

- **00-Inbox/** — `Course MOC.md` is the central hub note. Start here when navigating.
- **10-News/** — one markdown note per news article. YAML frontmatter (date, source, title, tags), then sections: TL;DR, Key Concepts, Summary, Why It Matters, Entities. Concepts and entities use `[[wikilinks]]` to `20-Concepts/` and `25-People/` notes.
- **20-Concepts/** — short concept hub stubs: companies, models/products, themes, domains. Each is 1–2 sentences with cross-links.
- **25-People/** — short person stubs: CEOs and lead researchers. Each is 1–2 sentences linking to their company and themes.
- **30-Articles/** — web clippings: short excerpts saved with Obsidian Web Clipper, each linking to the original article and to related concept notes.
- **99-Archive/n8n-workflows/** — exported `.json` workflow definitions.
- **`DEMO.md`** — demo walkthrough.
- **`vault_chat.py`** — Streamlit chat app over the vault.
- **`webhook-server.js`** — alternative local webhook (not used in production; GitHub middleware replaced it).

## How to answer questions about the vault

When the user asks about news, trends, people, or relationships:

1. **Use Glob and Grep first.** The vault is small enough that searching is fast. Try `Glob` on `10-News/*.md` or `25-People/*.md`. Use `Grep` for entity/topic names.
2. **Read selectively.** News notes have a structured format — read the TL;DR and Why It Matters sections first; only read full Summary if you need detail.
3. **Cite sources.** Always end answers with the markdown filenames you drew from, formatted as a list. The user will use these to navigate the graph.
4. **Prefer recency.** News filenames start with `YYYY-MM-DD`. When relevance is similar, prefer newer.
5. **Mind the difference between 10-News and 30-Articles.** `10-News/` has clean structured data (best for Q&A). `30-Articles/` only has short excerpts of third-party articles — cite the source link, don't treat them as full coverage.

## Format for answers

- Lead with a 1–3 sentence direct answer.
- Then a short bulleted "Sources" list of the notes you used.
- If asked to "draft" or "write" something (tweet, summary, email), produce it inline and offer to save it to `00-Inbox/` if the user wants.

## What NOT to do

- Don't fabricate news. If a question can't be answered from the vault, say so and suggest related entries.
- Don't dump entire file contents into the response.
- Don't write to `10-News/`, `20-Concepts/`, or `25-People/` without explicit instruction — those are managed by the pipeline and by the user's curation.
