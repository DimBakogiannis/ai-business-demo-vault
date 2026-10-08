# Voice-Driven Demo Extension — Talk to Your Vault

A second-act demo on top of `DEMO.md` that turns the Obsidian vault into a **voice-queryable knowledge base** using Wisprflow + Claude Code. This is the "wow moment" piece — most of the audience won't have seen voice → file-grounded AI before.

**Total runtime: 5–10 minutes (after the main demo).**

---

## What the audience sees

You're on stage with Obsidian's Graph view filling the screen. You press a hotkey on your keyboard. You ask, out loud:

> *"What did Nvidia announce at GTC this year, and how does it connect to OpenAI?"*

The text appears in a terminal window. Claude Code starts working: greps the vault, reads two news notes, traces the wikilinks, returns a grounded answer with citations. Then you ask it to draft a tweet about it. Then the tweet.

It feels like sci-fi. It's actually three off-the-shelf tools wired together in 30 minutes.

---

## The stack

| Layer | Tool | What it does |
|---|---|---|
| **Voice** | Wisprflow ([wisprflow.ai](https://wisprflow.ai)) | Hotkey-triggered speech-to-text that types into ANY input field, anywhere on macOS. ~$12/mo. |
| **Reasoning** | Claude Code (CLI) | Runs locally, can `Read`/`Grep`/`Glob` files in the current directory, holds a conversation. |
| **Knowledge** | Your Obsidian vault | The auto-populated AI-news vault from the main demo. |

**Free alternative to Wisprflow:** macOS built-in Dictation (Fn Fn) is free and decent, or [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) (one-time purchase) for offline transcription. Wisprflow is the smoothest because it has a global hotkey and inserts text faster than typing.

---

## One-time setup (~15 minutes)

### 1. Install Wisprflow

1. Download from https://wisprflow.ai → install the .dmg → launch.
2. Sign up; the free trial covers a demo.
3. **Grant Accessibility permission** when prompted (System Settings → Privacy & Security → Accessibility) — this is what lets Wisprflow type into other apps.
4. **Grant Microphone permission**.
5. **Set the hotkey**: Wisprflow → Settings → Shortcut. Default is Fn (the function key on Mac keyboards). Pick something you can hit one-handed — I recommend leaving it on Fn.
6. Test in any text field: hold Fn, speak, release. Text should appear.

### 2. Make sure Claude Code is installed

```bash
# check
which claude

# install if missing
npm install -g @anthropic-ai/claude-code
```

You also need an `ANTHROPIC_API_KEY` set (Claude Code prompts you on first run; key from https://console.anthropic.com/).

### 3. Verify the vault context loads

```bash
cd path/to/ai-business-demo-vault
claude
```

Claude Code auto-loads `CLAUDE.md` from the working directory — that file briefs it on the vault structure. Confirm by asking once: *"What folders are in this vault?"* — the answer should match what's in `CLAUDE.md`.

### 4. Practice the loop

The full loop is:
1. Window/cursor focus is in the Claude Code prompt
2. Hold Fn, speak, release
3. Wisprflow types the question
4. Press Enter
5. Watch Claude work

Run through 3–4 of the sample prompts below before going live so the rhythm feels natural.

---

## Pre-demo checklist (the morning of)

- [ ] Vault is freshly pulled — `git pull` in the vault dir
- [ ] `claude` runs and acknowledges the vault structure
- [ ] Wisprflow is in the menu bar, mic icon shows green when you press the hotkey
- [ ] Audio levels OK (no overhead AC fan noise drowning the mic)
- [ ] Terminal font is bumped to 18–20pt (audience needs to read it)
- [ ] Obsidian Graph view is open in another window/desktop, ready to switch to
- [ ] You've done one warm-up voice query that morning so Wisprflow's models are loaded

---

## Live demo flow (5–10 min)

### Setup the moment

After the main demo (DEMO.md), say:

> "OK, so far we've built the pipeline. The vault is filling itself up daily. But here's the question — what do you actually *do* with all this knowledge?"

### Step 1 — Switch to terminal, launch Claude Code

```bash
cd path/to/ai-business-demo-vault
claude
```

> "I'm starting Claude Code in the vault directory. There's a `CLAUDE.md` file here that tells it the layout of the vault — folder by folder, what each note looks like."

### Step 2 — Ask the first voice question

Cursor in Claude prompt → hold Fn → speak → release → Enter.

**Q1:** *"Summarize the most important AI news from the past week in five bullets."*

Narrate while it runs:
> "Watch the bottom of the screen. It's calling Glob to list news files, then Grep, then reading the most recent ones. This isn't a model regurgitating training data — it's a search of MY vault."

### Step 3 — A relationship question (the graph payoff)

**Q2:** *"What's the connection between the EU AI Act and Anthropic? Cite the notes you used."*

This shows off the wikilink graph indirectly — Claude follows `[[Anthropic]]` references across multiple notes and synthesizes.

### Step 4 — A comparative question

**Q3:** *"Compare how OpenAI and Meta have approached open source over the past month."*

Forces Claude to read multiple notes from different clusters and synthesize a contrast. Audience can verify by switching back to the Graph view and seeing both clusters.

### Step 5 — A creative ask (the closer)

**Q4:** *"Pick the most important article from this week and draft a 280-character tweet about it. Make it punchy."*

When Claude returns the tweet, say:

> "And that's the loop. From a daily n8n run to a tweet I could publish, voice-prompted, all grounded in original analysis written by an AI agent against today's news. The vault is the asset. The graph is the navigation. The voice query is the interface."

### Step 6 — Optional: switch back to Graph view

> "And the cool thing — every note Claude just cited is a node in this graph. I can open any of them and follow the trail by hand."

Click one of the cited notes in Obsidian → show the local graph → wrap.

---

## Sample voice prompts (cheat sheet)

Practice these. The bold ones are the ones I recommend for the actual demo.

**Recall**
- **"Summarize the most important AI news from this week."**
- "What did Nvidia announce in their latest earnings?"
- "List every article that mentions the EU AI Act."

**Relationship**
- **"What's the connection between Anthropic and AI Safety?"**
- "Which companies are mentioned across the most articles?"
- "What links Sam Altman, Microsoft, and the AI safety debate?"

**Comparison**
- **"Compare OpenAI's and Meta's approach to open source."**
- "How does Mistral's strategy differ from Llama's?"
- "Who's leading on reasoning models — OpenAI, Anthropic, or Google DeepMind?"

**Generation**
- **"Draft a 280-char tweet about today's most important story."**
- "Write a one-paragraph intro for a Medium article tying together this week's regulation news."
- "Suggest five questions a journalist should ask about the Nvidia earnings story."

**Meta**
- "Which concept stub has the most inbound links?"
- "Are there any articles that don't link to any concepts? List them."
- "Suggest three concept stubs I should add to make the graph denser."

---

## Why this is awesome (talking points for Q&A)

**"Isn't this just ChatGPT?"**
> No — ChatGPT answers from training data. This answers from MY notes, written this week, about events that happened yesterday. The grounding is the whole point.

**"What if the vault is wrong?"**
> Every answer ends with a citation — filenames I can open and verify. Hallucination becomes auditable.

**"Why voice instead of typing?"**
> Demo polish, but also: hands-free means I can keep the visual focus on the graph or the terminal output, not on my keyboard. And it changes the relationship — talking *to* a knowledge base feels different from searching it.

**"What's the cost?"**
> Wisprflow ~$12/mo, Claude Code uses your Anthropic API key (each conversation ~$0.05–$0.20 depending on how much context Claude reads). Trivial.

**"Could I do this on my own notes (research, journal, code)?"**
> That's the takeaway. This pattern — auto-populated structured notes + Claude Code + voice — generalizes to any knowledge work. Switch out the n8n input source and you have a research assistant for whatever domain matters to you.

---

## Backup plan

| Failure | Fallback |
|---|---|
| Wisprflow won't trigger | Type the questions manually — same effect, slightly less wow |
| Mic noise / can't be understood | Type — and joke about it |
| Claude Code connection fails | Show pre-recorded terminal output (record once with `script -t`) |
| API rate limit | Switch to a smaller model for the demo: `claude --model claude-haiku-4-5-20251001` |
| Vault out of date | The 12 hand-written news notes always work; n8n's outputs are bonus |

---

## Beyond the demo (if asked "what's next?")

1. **Add an Obsidian MCP server** — there are community projects (e.g., obsidian-mcp) that let Claude Code create/edit notes directly. The next demo would be voice-prompted note creation.
2. **A weekly digest workflow** — schedule Claude Code with cron to pick the week's top story, draft a Medium post, and commit it.
3. **Voice-triggered summaries via Slack** — Wisprflow → Slackbot → Claude Code with vault context → response in DM. Useful when you're not at your desk.
4. **Multi-vault Q&A** — point Claude Code at a parent folder containing multiple vaults (research, journal, projects). Same pattern, broader corpus.

---

*See `DEMO.md` for the main pipeline demo. This file is the second-act extension.*
