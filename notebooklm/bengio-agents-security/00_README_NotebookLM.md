# NotebookLM Podcast Paketi — Yoshua Bengio: Ajanlar & Güvenlik

**Amaç:** Bengio'nun makaleleri + Berlin Science Week konuşması üzerinden tüm temel YZ terimlerini podcast (Audio Overview) ile öğrenmek.

## Dosyalar
- `01_Bengio_Source_Pack.md` / `.pdf` — Ana kaynak (İngilizce, B2). 44 makale/olay, ajan & güvenlik derin analizi, Berlin konuşması önizlemesi, kurumsal kontrol tablosu, ~100 terimlik sözlük (Türkçe karşılıklarıyla).
- `00_README_NotebookLM.md` — Bu dosya.

## Kurulum (3 adım)
1. notebooklm.google.com → **New notebook** → `01_Bengio_Source_Pack.pdf` dosyasını yükle.
2. (Opsiyonel) **Add source → Website** ile birincil kaynakları ekle:
   - https://arxiv.org/abs/2502.15657
   - https://arxiv.org/abs/2606.29657
   - https://lawzero.org/en/research
   - https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026
3. Türkçe ses için: **Settings → Output language → Türkçe**. Sonra **Audio Overview → Customize** ile aşağıdaki promptlardan birini yapıştır, uzunluk: **Longer**.

## Podcast promptları (her biri ayrı bölüm)

**Bölüm 1 — AI Terms 101 (Deep Dive)**
```text
Deep Dive for an AI specialist who builds enterprise AI agents. Use Parts 0-2 and the glossary. Walk through Bengio's papers in time order and explain every AI term in plain language with a short everyday analogy: gradient, embedding, language model, attention, Transformer, GAN, fine-tuning, RAG. Always link old ideas to today's LLMs. End with a quick recap of the 10 most important terms.
```

**Bölüm 2 — Agents & Security (Deep Dive)**
```text
Deep Dive on Bengio's view of AI agents and security, using Era 5 of Part 2, Part 3 and Part 5. Explain agency, affordances, deception, self-preservation, reward hacking, prompt injection, jailbreaks, guardrails, defence-in-depth and Scientist AI in simple terms. Separate facts from interpretation. Finish with concrete proof-of-concept vs enterprise controls for a company deploying AI agents.
```

**Bölüm 3 — Berlin Talk Preview (Debate)**
```text
Debate format. Preview Bengio's Berlin Science Week talk on trust and responsibility in AI (Part 4). One host argues Scientist AI can make AI agents trustworthy; the other challenges the assumptions in "Safety from Honesty in a Disinterested AI Predictor". Use the listening checklist. Make clear this is a preview based on his recent work, not a transcript.
```

## Ekstra
- Sözlük çalışması için NotebookLM **Flashcards / Quiz** özelliğini Part 6 üzerinde kullan.
- Konuşmanın kaydı/transkripti yayınlanınca onu yeni kaynak olarak ekle ve Bölüm 3'ü yeniden üret.

## Not
Oturumdaki ağ kısıtı yüzünden birincil sayfalar (arXiv, LawZero, IASR) doğrudan okunamadı; içerik web arama sonuçları + bilinen literatürden derlendi. "Interpretation" olarak işaretli kısımlar tahmindir.
