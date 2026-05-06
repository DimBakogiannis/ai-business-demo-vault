const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json({ limit: '5mb' }));

const PORT = process.env.PORT || 5679;
const VAULT_PATH = process.env.VAULT_PATH || process.cwd();

const NEWS_DIR = path.join(VAULT_PATH, '10-News');
const ARTICLES_DIR = path.join(VAULT_PATH, '30-Articles');

function safeFilename(s) {
  return String(s).replace(/[\/\\:*?"<>|]/g, '-').trim();
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

app.post('/news', (req, res) => {
  console.log('[POST /news] payload:', JSON.stringify(req.body, null, 2));
  try {
    const {
      title,
      slug,
      date,
      source_url,
      tldr,
      concepts = [],
      entities = [],
      summary_body,
      why_it_matters,
      tags = [],
    } = req.body;

    if (!title || !slug || !date) {
      return res.status(400).json({ success: false, error: 'title, slug, and date are required' });
    }

    const conceptLinks = concepts.map((c) => `[[${c}]]`).join(', ');
    const entityList = entities.map((e) => `- ${e}`).join('\n');
    const tagList = ['tech-news', ...tags].join(', ');

    const md = `---
date: ${date}
source: ${source_url || ''}
title: "${String(title).replace(/"/g, '\\"')}"
tags: [${tagList}]
---

# ${title}

> [!summary] TL;DR
> ${tldr || ''}

## Key Concepts
${conceptLinks}

## Summary
${summary_body || ''}

## Why It Matters
${why_it_matters || ''}

## Entities
${entityList}

---
*[Source](${source_url || ''}) · Auto-generated ${date}*
`;

    ensureDir(NEWS_DIR);
    const filename = `${safeFilename(date)} ${safeFilename(slug)}.md`;
    const filepath = path.join(NEWS_DIR, filename);
    fs.writeFileSync(filepath, md, 'utf8');
    console.log(`[POST /news] wrote: ${filepath}`);
    return res.json({ success: true, file: filename });
  } catch (err) {
    console.error('[POST /news] error:', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

app.post('/article', (req, res) => {
  console.log('[POST /article] payload:', JSON.stringify(req.body, null, 2));
  try {
    const { title, slug, date, content } = req.body;

    if (!slug || !date || typeof content !== 'string') {
      return res.status(400).json({ success: false, error: 'slug, date, and content are required' });
    }

    ensureDir(ARTICLES_DIR);
    const filename = `${safeFilename(date)} ${safeFilename(slug)}.md`;
    const filepath = path.join(ARTICLES_DIR, filename);
    fs.writeFileSync(filepath, content, 'utf8');
    console.log(`[POST /article] wrote: ${filepath} (title: ${title || '(none)'})`);
    return res.json({ success: true, file: filename });
  } catch (err) {
    console.error('[POST /article] error:', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

app.get('/health', (_req, res) => {
  res.json({ ok: true, vault: VAULT_PATH });
});

app.listen(PORT, () => {
  console.log(`Webhook server listening on http://localhost:${PORT}`);
  console.log(`VAULT_PATH = ${VAULT_PATH}`);
  console.log(`Routes: POST /news -> ${NEWS_DIR}`);
  console.log(`        POST /article -> ${ARTICLES_DIR}`);
});
