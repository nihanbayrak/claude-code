# NotebookLM Podcast Pack — Yoshua Bengio: Agents & Security

**Goal:** Learn the core AI terms, and learn how to build safer agents, through Bengio's papers, his Berlin Science Week talk (6 Nov 2026), and current research on AI models that cheat, lie and collude.

## Files
- `01_Bengio_Source_Pack.pdf` — Bengio's papers by era (45 entries), deep dive on agents and security, Berlin talk preview, enterprise controls table, glossary of about 100 terms with Turkish equivalents.
- `02_Why_AI_Cheats_Builders_Guide.pdf` — Five questions: why AIs cheat, lie and collude; the real statistics for Claude, ChatGPT and other models; Bengio's solution; a builder's checklist of 12 rules (PoC vs enterprise) with an action-gate code sketch; one question to ask Bengio.
- `.md` versions of both, if you prefer Markdown uploads.

## Setup (3 steps)
1. notebooklm.google.com → **New notebook** → upload both PDFs.
2. Optional: **Add source → Website** to add primary sources:
   - https://arxiv.org/abs/2502.15657 (Scientist AI)
   - https://arxiv.org/abs/2606.29657 (Safety from Honesty)
   - https://arxiv.org/pdf/2510.05179 (Agentic Misalignment)
   - https://arxiv.org/pdf/2509.15541v1 (Anti-scheming stress test)
3. **Audio Overview → Customize** → paste one prompt below → length **Longer**. For Turkish audio: **Settings → Output language → Türkçe**. Tip: for episodes 4–6, tick only source 02 in the source list so the episode stays focused.

## Podcast prompts (one episode each)

**Episode 1 — AI Terms 101 (Deep Dive) · source 01**
```text
Deep Dive for an AI specialist who builds enterprise AI agents. Use Parts 0-2 and the glossary. Walk through Bengio's papers in time order and explain every AI term in plain language with a short everyday analogy: gradient, embedding, language model, attention, Transformer, GAN, fine-tuning, RAG. Always link old ideas to today's LLMs. End with a quick recap of the 10 most important terms.
```

**Episode 2 — Agents & Security (Deep Dive) · source 01**
```text
Deep Dive on Bengio's view of AI agents and security, using Era 5 of Part 2, Part 3 and Part 5. Explain agency, affordances, deception, self-preservation, reward hacking, prompt injection, jailbreaks, guardrails, defence-in-depth and Scientist AI in simple terms. Separate facts from interpretation. Finish with concrete proof-of-concept vs enterprise controls for a company deploying AI agents.
```

**Episode 3 — Berlin Talk Preview (Debate) · source 01**
```text
Debate format. Preview Bengio's Berlin Science Week talk on trust and responsibility in AI (Part 4). One host argues Scientist AI can make AI agents trustworthy; the other challenges the assumptions in "Safety from Honesty in a Disinterested AI Predictor". Use the listening checklist. Make clear this is a preview based on his recent work, not a transcript.
```

**Episode 4 — Why AI Cheats: Builder's Edition (Deep Dive) · source 02**
```text
Deep Dive for an AI engineer who builds web apps with AI agents. Answer in order: 1) why AIs cheat, lie and seem to collude; 2) what the Claude and ChatGPT statistics really show, and why they are stress tests, not everyday failure rates; 3) Bengio's solution; 4) proof-of-concept vs enterprise actions I can take this week; 5) end with the one question to ask Bengio. Explain every term simply.
```

**Episode 5 — Alarming or Overhyped? (Debate) · source 02**
```text
Debate format. Host A argues the statistics and the July 2026 Hugging Face incident show agents are already dangerous and builders must slow down. Host B argues the numbers come from extreme, artificial tests and good engineering controls are enough. Both must use the table in Question 2. End by agreeing on the top 3 safeguards for a web app with AI agents.
```

**Episode 6 — Builder's Checklist (Brief) · source 02**
```text
Brief format. Read the 12 builder rules from Question 4 as a checklist, one or two sentences each, with the proof-of-concept version first. Then give the one question to ask Bengio and why it works.
```

## Extras
- Use **Flashcards / Quiz** on the glossaries (Part 6 of source 01, glossary of source 02).
- After the talk, add the recording or transcript as a new source and regenerate Episode 3.

## Note
This session's network policy blocked direct access to arXiv, LawZero and other primary sites, so the content was compiled from web search results and known literature. Sections marked "interpretation" are expectations, not quotes. Some 2026 incident details (agent counts, dates) differ across news sources.
