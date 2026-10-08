# Demo Script — n8n + Obsidian AI News Pipeline

A live demo for the **AI in Business** course showing how to build a fully-automated tech news intelligence pipeline that produces a navigable, graph-rich knowledge vault.

**Total runtime: 15–20 minutes.**

---

## 1. Elevator Pitch (30 seconds)

> "Every morning at 8 AM, an n8n workflow scans tech RSS feeds and the NewsAPI, picks the most important AI story of the past 24 hours, has Claude write a structured analysis of it, and commits the result straight to a private GitHub repo that my Obsidian vault auto-syncs from. The result: a daily-growing knowledge graph of AI news, ready for me to publish to Medium or build a course around — without me writing a single word."

---

## 2. The Architecture (1 slide)

```
┌──────────────┐     ┌──────────────────────────────┐     ┌─────────────────┐
│  Daily 8 AM  │ ──▶ │ Fetch RSS + NewsAPI          │ ──▶ │ Normalize +     │
│  trigger     │     │ (BBC Tech, Verge, Ars,       │     │ filter (24h,    │
│              │     │  TechCrunch, NewsAPI)        │     │  top 15)        │
└──────────────┘     └──────────────────────────────┘     └────────┬────────┘
                                                                    │
                            ┌───────────────────────────────────────┘
                            ▼
                   ┌────────────────────┐     ┌────────────────────────┐
                   │ Claude AI Agent    │ ──▶ │ Parse AI Output (JS)   │
                   │ writes the article │     │ → title, slug, content │
                   └────────────────────┘     └─────────┬──────────────┘
                                                        │
                            ┌───────────────────────────┼─────────────────────┐
                            ▼                           ▼                     ▼
                   ┌────────────────┐         ┌──────────────────┐    ┌──────────────┐
                   │ Send Email     │         │ Create Medium    │    │ Commit to    │
                   │ (Gmail)        │         │ Post (draft)     │    │ GitHub repo  │
                   └────────────────┘         └──────────────────┘    └──────┬───────┘
                                                                              │
                                                                              ▼
                                                                  ┌────────────────────┐
                                                                  │ Obsidian Git plugin│
                                                                  │ pulls every 24h    │
                                                                  │ (or on startup)    │
                                                                  └──────────┬─────────┘
                                                                              │
                                                                              ▼
                                                                  ┌────────────────────┐
                                                                  │ Graph view in      │
                                                                  │ Obsidian           │
                                                                  └────────────────────┘
```

**Why GitHub as the middleware?** n8n Cloud blocks direct localhost calls (SSRF protection). GitHub gives us free version control, off-machine backup, and works with any device that has the Obsidian Git plugin.

---

## 3. Pre-Demo Checklist

Run through these the night before:

- [ ] Webhook server NOT needed — using the GitHub path. (`webhook-server.js` is in the repo for reference but not running in production.)
- [ ] In Obsidian, the active vault is `ai-business-demo-vault` (not the parent folder).
- [ ] `Cmd-P → Git: Pull` works without errors.
- [ ] Run a local pull from terminal as a backup: `cd path/to/ai-business-demo-vault && git pull`.
- [ ] Open the n8n workflow in a browser tab and confirm credentials are valid (GitHub PAT, Anthropic, Gmail, Medium).
- [ ] Disable Do Not Disturb / mute Slack.
- [ ] Have one new test article cued up by triggering n8n manually 5 minutes before the demo so the Obsidian view feels "fresh" without waiting for the AI to run live.

---

## 4. Live Demo Walkthrough (15 minutes)

### Screen layout

Split horizontally:
- **Left half**: n8n workflow canvas
- **Right half**: Obsidian (start on the README, switch to Graph view later)
- **Bottom strip**: Terminal in `ai-business-demo-vault/` ready for manual `git pull` if needed

### Step-by-step

**[0:00] Open the n8n workflow.**
> "Here's the daily pipeline. It runs every morning at 8 AM. The trigger is on the left."

**[1:00] Walk through Section 1 — Fetch news sources.**
Point to the RSS nodes and NewsAPI fetch in parallel.
> "We pull from four RSS feeds plus the NewsAPI's tech category in parallel. About 50–100 articles a day."

**[2:00] Walk through Section 2 — Normalize and filter.**
> "Different sources, different field names. We normalize them, filter to the last 24 hours, sort by date, and take the top 15 articles."

**[3:30] Walk through Section 3 — AI writes the article.**
> "This is the interesting part. We aggregate the 15 headlines into a single digest, then hand it to a Claude-powered AI Agent. The agent has a Fetch Article tool — it reads the article it considers most important and writes an original analysis. Original, not copy-paste."

Click into the AI Write News Article node to show the system prompt.

**[5:00] Walk through Section 4 — Distribute the article.**
> "Three destinations in parallel: an email to me, a Medium draft, and a commit to my Obsidian vault on GitHub."

**[6:00] Trigger the workflow live.**
Click **Execute Workflow**. Narrate while it runs (~30–60 seconds depending on AI latency).

**[7:00] Show the GitHub commit appearing in real time.**
Switch to the GitHub repo tab — refresh — point at the new commit.
> "There it is. n8n just made a commit to the main branch."

**[8:00] Pull in Obsidian.**
Switch to Obsidian. **Cmd-P → "Git: Pull"**. The new file appears in `30-Articles/`.
> "And now it's in my vault. No copy-paste, no manual import."

**[9:00] Open the new article.**
Click it in the file tree. Walk through the structure.

**[10:00] Open the Graph view (Cmd-G).**
> "But the magic isn't a single article — it's the structure that emerges over time."

Zoom in on a cluster:
- **OpenAI cluster** → point at OpenAI, GPT, ChatGPT, Sam Altman, Microsoft as a tight cluster.
- **Anthropic cluster** → point at Anthropic, Claude, Dario Amodei, AI Safety.
- **Hardware cluster** → Nvidia, Jensen Huang, GPU Compute, AI Infrastructure.
- **Regulation cluster** → EU AI Act, AI Regulation, AI Ethics.

**[12:00] Click a single concept node — e.g., `[[OpenAI]]`.**
Show the local graph (depth 2). Five news articles, three product nodes, one person node, all attached.
> "Two months from now this graph will have hundreds of nodes. It's a knowledge artifact you can navigate, not a search you have to remember to run."

**[13:00] Open `Course MOC`.**
> "And this is the index — a single map-of-content note that links to every concept hub. Anyone joining the course mid-semester has one entry point."

**[14:00] Show the README.**
Tie it all together: folder structure, why it works, how to extend it.

**[15:00] Wrap.**

---

## 5. Talking Points (have ready for Q&A)

**"Why Obsidian instead of Notion or Confluence?"**
> Plain markdown files, local-first, free graph view, no vendor lock-in, Git-friendly. The graph view is the differentiator — it makes the knowledge structure tangible.

**"Why GitHub as middleware? Why not write directly to a server?"**
> n8n Cloud blocks calls to localhost and private IPs (SSRF protection). GitHub solves auth, persistence, sync, and version history in one move. The local webhook server I built originally is in the repo (`webhook-server.js`) for self-hosted n8n setups.

**"What does it cost to run?"**
> Approximately:
> - n8n Cloud Starter: ~€20/month (or self-host for free)
> - Anthropic API: ~$0.05 per daily run (~$1.50/month at one article a day)
> - GitHub: free for private repos
> - Total: well under $25/month for a daily AI-powered intelligence pipeline.

**"Couldn't I just use ChatGPT to summarize a feed manually?"**
> You could, once. Automation pays off when you compound it daily. Two months in, the graph and the article archive become the artifact — not the daily action of generating one.

**"How do I extend it?"**
> Three obvious next steps: (1) add a "weekly digest" workflow that aggregates 7 daily articles into a Medium-ready piece. (2) Add a per-article branch that writes individual news notes to `10-News/` so the graph fills out faster. (3) Wire a Slack notifier so you get a digest in chat.

---

## 6. Backup Plan (if anything fails)

| Failure | Fallback |
|---|---|
| n8n trigger fails | Show a pre-recorded n8n run, or click through node-by-node with pinned data |
| GitHub commit fails | Show an existing commit from the past week |
| Obsidian Git pull fails | Run `git pull` in the terminal pane — the file appears in Obsidian without the plugin |
| Graph view crashes | Show static screenshots in Keynote backup deck |
| Internet drops | Whole demo runs locally — vault is already populated, just walk through Graph view + open notes |

---

## 7. Key Files in This Vault

| File / folder | Purpose |
|---|---|
| `00-Inbox/Course MOC.md` | Hub note. Start every navigation here. |
| `10-News/` | Per-article news notes (currently seeded manually for the demo; the production flow targets this folder) |
| `20-Concepts/` | Cross-linked concept hubs — companies, models, themes, domains |
| `25-People/` | Cross-linked person notes — CEOs, lead researchers |
| `30-Articles/` | Aggregated Medium-ready drafts (where n8n's daily output lands) |
| `99-Archive/n8n-workflows/` | Exported `.json` workflow definitions for reproducibility |
| `webhook-server.js` | Optional local webhook (alternative to GitHub middleware) |

---

## 8. After the Demo

Follow-up improvements you can mention:

1. **Tighten the AI prompt** so daily outputs include `[[wikilinks]]` and YAML frontmatter automatically — the demo content was hand-written for the graph.
2. **Add a separate `/news` branch** that splits aggregated articles back into individual items, so the graph fills out organically each day.
3. **Add an AI-relevance filter** so non-AI tech news (e.g., consumer hardware) doesn't dilute the corpus.
4. **Schedule a weekly digest** that aggregates a week of `30-Articles/` into one Medium publication.

---

*Vault repository: https://github.com/DimBakogiannis/ai-business-demo-vault*
