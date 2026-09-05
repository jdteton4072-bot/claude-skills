# RAG Architecture Memo — NFL/CFB Spread & Totals Prediction Service

**Author role:** Retrieval-systems architecture (supporting role to edge research)
**Date:** 2026-09-05

---

## Recommendation

- **Recommend (c), narrowly scoped, and built almost entirely on top of (b):** a classical statistical/ML core (gradient-boosted trees or a hierarchical Bayesian model, consistent with the team's existing HMM/walk-forward-validation competence) **emits every published number**. Retrieval and LLMs appear in exactly two bounded, auditable roles: (1) **offline feature extraction** — turning unstructured injury/beat-reporter/news text into small, versioned numeric/categorical features that are inputs to the stats model, and (2) a **narrow near-real-time monitoring layer** that flags when a late-breaking unstructured signal (a scratch, a weather shift) has occurred *after* the model's last feature refresh and *before* the line has moved to reflect it — surfaced to a human, never auto-emitting a new number. **RAG-as-predictor (option a) is rejected** for the core prediction task. Confidence: Medium-High.
- **Why:** LLMs are demonstrated to be extraction/classification tools, not calibrated numeric forecasters (see §1). The 52.38% breakeven bar means the system needs a *reproducible, backtestable, low-variance* number generator; an LLM reasoning end-to-end to a spread reintroduces non-determinism, cost, and — critically — training-data contamination directly into the one output that decides whether the business survives. A stats model with LLM-derived features keeps the actual number-generation classical and testable, while still letting retrieval do the one thing it's plausibly good for: fast, structured extraction of information the market may not have fully priced.
- **Single biggest risk to this design:** **point-in-time leakage.** Any LLM in the pipeline — even doing "only" feature extraction — was pretrained on a corpus that already contains sports journalism, box scores, and post-game analysis for most historical games used in backtesting. If retrieval and feature extraction are not strictly bound to an as-of-timestamp index (§2), the backtest will look better than the live system ever will, and the team will not find out until real money is down. This is treated as a first-class constraint below, not a caveat.

---

## 1. Resolving the definition

### (a) RAG-as-predictor
**Mechanism:** LLM retrieves stats/injury/news/line context at inference time and reasons directly to a spread, total, or pick.

**Plausible edge:** In principle, an LLM could integrate qualitative signals (a backup QB's specific weaknesses, a beat reporter's off-the-record read on a coach's game plan) that a discretized stats model handles crudely. No evidence found that this integration step, in practice, produces calibrated numeric output rather than plausible-sounding narrative.

**Evidence on numeric calibration:** The best available proxy evidence is LLM forecasting-tournament literature, not point-spread-specific research (that gap is real and is flagged as such — no dedicated study of LLM-generated point spreads or totals calibration was found in this search). ForecastBench (Karger et al., 2024) and subsequent 2025-2026 tournament results show frontier models (GPT-4-class, o3/o4-mini, Claude 3.5) reaching Brier scores around 0.135–0.159 in real-world event forecasting — better than a generic human crowd (~0.149) but well behind expert superforecasters (~0.02), with **persistent overconfidence at high-probability levels** documented across models ([Future Is Unevenly Distributed, arXiv, Nov 2025](https://arxiv.org/html/2511.18394); [KalshiBench / epistemic calibration via prediction markets, arXiv, Dec 2025](https://arxiv.org/html/2512.16030)). This is evidence about *probability* calibration on discrete world events, not about emitting a calibrated *point-spread number* — extrapolating it to "LLM outputs a good spread" is **judgment**, but the direction of the judgment (structurally worse at precise numeric quantities than at classification/extraction) is consistent with everything in this literature and with the general shape of LLM training objectives (next-token prediction over text, not squared-error minimization over a continuous target).

**Failure modes:** (i) training-data contamination — see below and §2, this is not hypothetical, it is close to guaranteed for any backtest touching historical games; (ii) hallucinated stats presented with false confidence; (iii) no native uncertainty quantification a bettor can size a stake against; (iv) non-determinism from model updates and batched-inference floating-point effects breaks the ability to reproduce a backtest at all (§1, determinism below); (v) an LLM asked to "reason to a number" is also the most expensive and highest-latency option per game.

**Cost/latency:** Highest of the three options — long-context retrieval, multi-call self-consistency needed to reduce variance, and the contamination-control machinery in §2 has to wrap the entire prediction path, not just a feature layer.

**Verdict:** Reject as the number-generating mechanism. Low confidence this ever clears 52.38%; no plausible mechanism beyond what a stats model already captures from EPA/success-rate/line data, and it actively adds contamination and reproducibility risk to the one output that matters.

### (b) RAG-as-feed
**Mechanism:** Retrieval assembles and normalizes features. Structured sources (play-by-play, lines, weather) are mostly **plain SQL/feature-store lookups, not retrieval in the RAG sense at all** (see §3 — flagged per-source). Unstructured sources (injury notes, beat reports, depth-chart chatter) are distilled by a classifier/small-LLM step into a bounded set of numeric/categorical features (e.g., `starting_qb_out: bool`, `practice_participation_trend: ordinal(0-3)`, `beat_reporter_severity_score: float[-1,1]` with a confidence field) that join the same feature vector as the structured data. A separate, classical model (GBM, or a hierarchical Bayesian model with team/season random effects — directly analogous to the team's HMM background) does all calibration and number emission, e.g., via isotonic regression or Platt scaling on top of the raw model output.

**Plausible edge:** Whatever edge exists plausibly lives in (i) the stats model's ability to weight and calibrate already-known signals better than the market's simplified consensus, and (ii) the marginal information in unstructured text that is genuinely not yet reflected in structured data or the line — e.g., a beat reporter's report of a limited practice participant trending toward "doubtful" a few hours before the official designation. The LLM's job is bounded to classification/extraction, which is the task class LLMs are actually good at relative to open-ended numeric generation.

**Failure modes:** Contamination is still possible at the feature-extraction step (an LLM summarizing a 2021 injury report may lean on memorized knowledge of how that season turned out); overfitting the stats model to noisy, LLM-derived features if extraction quality isn't independently validated; feature drift if extraction prompts/models change without version pinning.

**Cost/latency:** Low-medium. Feature extraction is batchable (nightly per slate), not a live reasoning call; the stats model itself is near-instant at inference.

**Verdict:** This is the dominant, load-bearing role for retrieval in this system.

### (c) Hybrid
**Mechanism:** Everything in (b), plus one additional, deliberately narrow real-time component: a **line-staleness monitor**. Between the time features were last refreshed and kickoff, an event-driven pipeline watches a small set of high-value unstructured triggers (official injury designation changes, a beat reporter reporting a scratch, a sudden wind-forecast revision) and computes a lightweight severity/direction score. This score does **not** generate a new predicted number; it flags "the model's last output is now stale relative to a real-world change, and the market may not have repriced yet" for human review or a narrow rule-based re-weighting (e.g., "QB out" triggers a pre-computed backup-QB adjustment already validated offline, not a fresh LLM-generated number).

**Plausible edge:** This is the only place in the architecture where *speed* itself is the edge candidate — beating the market's own repricing of a late-breaking event by minutes to hours. This is a timing/latency arbitrage, not a modeling insight, and its existence depends entirely on the market being slow to reprice public information, which the architecture cannot verify (see §6).

**Failure modes:** False triggers from unreliable beat-reporter sourcing; the "narrow rule-based re-weighting" must itself be pre-validated offline (not invented live) or it reintroduces the same calibration and contamination problems as option (a), just at smaller scale and higher frequency.

**Verdict:** Adopt as an *extension* of (b), not as a separate independent architecture. This is what "hybrid" concretely means here: a classical predictor, a batch LLM feature layer, and a bounded, human-gated, non-generative real-time alerting layer. At no point does an LLM emit the published spread or total.

### Training-data contamination — first-class constraint, not a caveat
**Mechanism:** Pretraining corpora for any general-purpose LLM include sports journalism, box scores, post-game recaps, and betting-market commentary through the model's training cutoff. If that LLM is used anywhere in the prediction path — even "only" to extract a feature like "how severe is this injury" — for a **historical** game used in backtesting, its output can be influenced by memorized knowledge of how that game turned out, not just by the as-of-date facts it was given. E.g., asked in 2026 to assess whether a 2022 backup QB start "will hurt performance," the model may lean toward the historically correct answer because it has seen post-game analysis describing the outcome, independent of what was actually knowable before kickoff.

**Severity:** This is not a minor caveat — it is the mechanism most likely to make a backtest look profitable when the live system is not. Recent literature on this exact failure mode: [Temporal Leakage in LLM Backtesting: Measurement, Validation, and Adjusted Scores, arXiv, Aug 2026](https://arxiv.org/html/2608.02985) and [All Leaks Count, Some Count More: Interpretable Temporal Contamination Detection and Mitigation, arXiv, Feb 2026](https://arxiv.org/html/2602.17234) — both establish that the naive check (compare pre-cutoff vs. post-cutoff performance) is *itself* unreliable, because models can fail that check even on questions they provably could not have memorized, meaning contamination detection needs the ablation and canary methods below, not a single before/after split.

**Architectural mitigations (mandatory, not optional):**
1. **Strict as-of-date retrieval** (§2) — the index itself, not a prompt instruction, enforces that only information timestamped before the decision point is retrievable.
2. **Post-cutoff holdout as the only valid backtest window for LLM-touched components.** Any pinned LLM has a public training cutoff; only games occurring after that cutoff can be used to validate the LLM-containing feature-extraction layer under conditions resembling live deployment. Pre-cutoff games can validate the *classical stats model* (which has no memorization channel) but cannot cleanly validate the LLM feature layer.
3. **Ablation testing:** run the identical stats-model backbone with the LLM-derived features present vs. removed, separately for pre-cutoff and post-cutoff games. A performance gain that appears only pre-cutoff and vanishes post-cutoff is the contamination signature.
4. **Canary/counterfactual injection:** insert deliberately fabricated facts (a fictitious injury, a false depth-chart change) into the as-of-date index for real historical games and confirm the LLM's derived feature reflects the injected counterfactual rather than the real, memorized outcome. If the model "corrects" back toward the real-world result, that is direct evidence of memorization overriding retrieved context.

Confidence in the *existence and severity* of this risk: High. Confidence in any specific mitigation being fully sufficient: Medium — this is an active research area (both cited papers are 2026) and the state of the art has not converged.

### Determinism and reproducibility
A backtest that cannot be rerun to the same result is not a backtest. Two distinct sources of non-determinism apply if an LLM is anywhere in the path:
- **Model-version drift.** Hosted model endpoints change silently; a backtest run in month 1 and reproduced in month 6 against "the same model name" may not be the same weights. **Mitigation:** pin exact model versions/checkpoints, and re-run and diff outputs whenever a provider deprecates a pinned version.
- **Batch-size-dependent floating-point non-determinism.** Even at temperature 0, identical prompts can return different completions because dynamic batching changes the internal order of floating-point reductions in GPU kernels ("batch invariance"). Thinking Machines Lab's analysis found up to 9% accuracy swings from GPU-count/batch-size changes alone, and the fix requires batch-invariant kernels, not just temperature=0 ([LMSYS/SGLang, "Towards Deterministic Inference," Sep 22, 2025](https://www.lmsys.org/blog/2025-09-22-sglang-deterministic/); [Defeating nondeterminism in LLM inference in practice, Medium, 2025](https://medium.com/@siddhantg314/defeating-nondeterminism-in-llm-inference-in-practice-38a7dd1e4112)). **Mitigation:** cache every LLM output keyed on (input hash, model version, prompt version); never regenerate a cached historical feature; if self-hosting, use batch-invariant inference kernels for anything that must be exactly reproducible.
- **Practical implication:** treat every LLM call in the pipeline as a **write-once artifact** — logged, hashed, versioned — exactly like a market-data snapshot, not as a function that can be silently recomputed later and assumed equivalent.

---

## 2. Point-in-time correctness — the central engineering constraint

This is where the design lives or dies, per the brief, and it is the section with the least tolerance for hand-waving.

### Bitemporal modeling
Every fact in the system carries **two** timestamps:
- **Event time** — when the fact became true in the world (e.g., a player suffered an injury, a line moved, wind speed at kickoff).
- **Knowledge time** — when the system's ingestion pipeline learned the fact and it became queryable (e.g., when a beat reporter's tweet was scraped, when a sportsbook's API returned the updated line).

A prediction for game G at decision timestamp T must only ever query facts where `knowledge_time <= T`, regardless of `event_time`. This is standard bitemporal data modeling (judgment: this is established practice in financial market-data and clinical-data systems generally, not something specific to this domain that needs a fresh citation — but the specific application to sports retrieval is this memo's judgment call, not a cited external practice).

Concretely: every row in every source table (injury reports, lines, weather, news, depth charts) gets `event_time`, `ingested_at` (knowledge time), and an immutable `source_snapshot_id`. Nothing is ever updated in place; corrections are new rows with a later `ingested_at`, and the original row is retained.

### Why "add a date filter to the prompt" fails
The common shortcut — retrieve broadly, then instruct the LLM "only use information before date X" — fails for two independent reasons:
1. **It relies on the index already excluding future information, and that's exactly the property it doesn't have.** If the underlying vector/document store contains post-game articles and box scores (because they were ingested in one big historical crawl), a semantic query like "QB injury Week 6 2023" can retrieve a chunk from a Week 7 recap that discusses how the injury affected the outcome — the date instruction only tells the model to *ignore* it, and compliance with that instruction is not guaranteed, verifiable, or enforceable at the retrieval layer.
2. **It does nothing about the model's parametric memory.** Even with a perfectly filtered retrieval set, the LLM's weights already encode the outcome if the game is pre-cutoff. Prompt-level date instructions cannot filter what's already baked into the model — only post-cutoff holdout and ablation (§1) address that.

**The correct mechanism is to filter the index itself before retrieval, not the retrieved output after the fact:** every retrieval call is parameterized by the decision timestamp T, and the query against the store is `WHERE ingested_at <= T` (a metadata filter enforced at the database/vector-index level, e.g., a partition key or a mandatory filtered ANN search), so content with a later knowledge-time is structurally unreachable, not merely disrecommended. Practically, this means: partition or index unstructured content by ingestion-time buckets (daily), and generate/maintain **immutable as-of snapshots** of the retrievable corpus for each historical game used in backtesting, built once and frozen, so a backtest run in 2027 sees exactly the same retrievable universe as one run in 2026 for the same game — this is also what makes the backtest reproducible per §1.

### Detecting leakage after the fact
Point-in-time filtering can still fail silently (a mis-tagged ingestion timestamp, a scraper backfilling a "Tuesday" article with a stale timestamp). Detection layer, independent of the prevention layer:
- **Canary tests** (as in §1): inject known-false facts into the as-of index for spot-checked historical games and confirm the pipeline's output reflects the injected fact, not the real outcome.
- **Ablation deltas by recency:** performance uplift from the LLM/retrieval layer should be roughly stable across the backtest period if it's real; a backtest where the uplift is *concentrated in older games* (further from the model's cutoff you'd expect less memorization, not more — actually the opposite pattern, uplift concentrated in games *well before* the cutoff and vanishing in the most recent pre-cutoff games, or vanishing entirely post-cutoff, is the tell) is a symptom, not a coincidence.
- **"Too good" as a red flag, not a result:** if the full pipeline clears 52.38% by a wide, stable margin in backtest but the classical-model-only ablation (no LLM/retrieval features) is close to breakeven, treat the gap as a leakage hypothesis to be disproven, not a discovery to be reported. Genuine, durable sports-betting edges are typically thin (low single-digit points above breakeven) — a large gap attributable to the LLM layer specifically should raise the prior on leakage, not on model quality. (Judgment.)
- **Live/paper-trading confirmation is the only real validator.** Per the contamination literature cited in §1, a benchmark or backtest — however carefully constructed — cannot fully substitute for evaluation on new games generated after any component was frozen; this should be budgeted as a required phase, not treated as optional confirmation of a backtest that already "looks good."

---

## 3. What actually needs retrieving

| Source | What's retrieved | Structured? | Update freq | Latency need | Index/access pattern | Edge plausibility & is retrieval the right pattern? |
|---|---|---|---|---|---|---|
| **Play-by-play, box scores, efficiency metrics (EPA, success rate, DVOA-like)** | Per-play and per-game numeric aggregates | Fully structured | Post-game (final), some near-live in-game | Batch, not real-time for pretrained features | **Plain SQL / feature store, keyed by team-week.** Not a retrieval problem at all. | This is the backbone of any legitimate model here; it's a database query, not RAG. Flag: calling this "RAG" would be architectural fashion — it's a data warehouse. Confidence: High that this is not a retrieval task. |
| **Injury reports & depth charts** | NFL: standardized practice-participation + game-status designations. CFB: no NCAA mandate; CFP requires public availability reports starting 2025-26 season; conference-level policies vary (Big Ten, SEC have their own mandates; many conferences have none). | Structured where mandated (NFL, CFP); unstructured/rumor-based elsewhere (most of CFB) | NFL: Wed/Thu/Fri practice reports by 4pm ET, Friday game-status ([NFL official injury policy, media.nfl.com, 2025](https://media.nfl.com/content/dam/communications/football-communications/2025/news/06%2005%2025%20-%20Important%20Dates.pdf); [profootballnetwork.com, injury policy summary](https://www.profootballnetwork.com/what-is-nfl-injury-policy-rules-and-procedures-for-nfl-teams/)) | NFL structured feed: hourly/on-publish is enough. CFB unstructured: as-fast-as-possible given no official cadence. | NFL: SQL table on standardized designations. CFB non-mandated portion: genuinely unstructured text (beat reporters, team pressers) — this is the one place hybrid dense/sparse retrieval over recent-news chunks is actually warranted. | **NFL/mandated-CFP portion: structured lookup, not retrieval.** **Non-mandated CFB portion is the one place in this table where the NFL-vs-CFB disclosure asymmetry could be a genuine, narrow edge**, because information is more fragmented and slower to consolidate into a single consensus signal for the market to price — but it is also **noisier and less verified** (beat-reporter rumor vs. official designation), so it plausibly cuts both ways: real signal on some slates, false-positive noise on others. This needs its own precision/recall validation before being trusted as a feature. Judgment; not verified here as a real edge. |
| **Weather (forecast + actual), especially wind for totals** | Wind speed/direction, precipitation, temperature at kickoff; forecast at multiple lead times | Structured (numeric API data) | Hourly-to-daily as kickoff approaches; final actuals post-game | Needs to be as-current-as-possible near kickoff for totals models | **API/DB, not retrieval.** No unstructured text involved unless quoting a forecaster's narrative. | Plausible, well-established structured input to totals models (wind materially affects passing/kicking); not a retrieval problem. Flag: no RAG role here at all. |
| **Betting lines (opening, current, closing, multi-book) + movement timestamps** | Numeric line/price time series per book | Fully structured | Real-time/tick-level ideally | Needs precise timestamps to compute CLV at all | **Time-series DB, not retrieval.** This is the ground truth the whole business is graded against. | Not a retrieval problem in any sense — but it is the single most important data feed in the entire architecture, because CLV is measured against it. Misclassifying this as "just another RAG source" would be a serious design error. |
| **News, beat-reporter reporting, social signals** | Free text: articles, press-conference transcripts, social posts | Unstructured | Continuous | Needs to reach the feature layer within hours to be useful, and within minutes for the real-time monitor (§1c) | **This is the legitimate RAG surface area** — hybrid dense/sparse retrieval over recency-partitioned, as-of-timestamped chunks (§2, §4) | Plausible narrow edge only insofar as it surfaces information not yet reflected in the injury/depth-chart structured feed or the line; large false-positive risk from unreliable sourcing. This is exactly the source class option (b)'s feature-extraction layer and option (c)'s monitor are built for. |
| **Coaching/scheme changes, travel, rest days, altitude, surface** | Mostly structured facts (days of rest, distance traveled, stadium altitude, surface type) with occasional unstructured commentary (a coordinator change, a scheme shift reported in the press) | Mostly structured; a thin unstructured layer for scheme/coaching narrative | Low frequency, schedule-driven for the structured part | Batch, well ahead of kickoff | **Structured table (rest days, altitude, surface are static/schedule facts) plus a small text-classification pass for coaching-change narrative** | Mostly a database problem. The unstructured sliver (interpreting a scheme change's likely effect) is a good candidate for feature extraction (b), not for real-time monitoring — these changes are known days-to-weeks ahead, not last-minute. |

**Overall judgment on this table:** the large majority of "what needs retrieving" for this system is a data-engineering problem (structured time-series and relational data), not a RAG problem. RAG has a legitimate, narrow surface area limited to (i) fragmented, non-mandated-disclosure text (mostly CFB injury/availability chatter) and (ii) general news/beat-reporter signal that might move a number before the structured feed or the line catches up. Presenting this as a "RAG system" end-to-end would be over-scoping the architecture to match the project's name rather than its actual data shape.

---

## 4. Retrieval design (only to the depth that matters)

- **Corpus scope:** limited to the two unstructured source classes in §3 (news/beat-reporter text, non-mandated CFB availability chatter) — do not build a vector index over structured data; that is architectural fashion, not a requirement.
- **Chunking:** article/post-level chunking with team+week metadata and the mandatory `ingested_at`/`event_time` bitemporal fields (§2); chunk size driven by typical article length (a few hundred tokens), not a generic RAG default — this corpus is small and short-form relative to, e.g., legal or technical documentation corpora.
- **Indexing/retrieval method:** hybrid dense + sparse (BM25) retrieval with reciprocal rank fusion is the current default best practice for this kind of short, keyword-rich, entity-dense text (player names, team names) — sparse retrieval alone tends to underperform on paraphrase, dense alone underperforms on exact entity/name matches, and RRF fusion of the two is a well-established, low-cost combination step ([Hybrid Search: BM25, Vector & Reranking Reference, digitalapplied.com, 2026](https://www.digitalapplied.com/blog/hybrid-search-bm25-vector-reranking-reference-2026); [Hybrid RAG: Dense and Sparse Retrieval, atlan.com, accessed 2026](https://atlan.com/know/hybrid-rag/)). Confidence: Medium — these are engineering-blog-level sources, not peer-reviewed benchmarks specific to this domain; treated as reasonable industry practice, not proven optimal for sports text specifically.
- **Reranking:** a cross-encoder reranking pass on top-100-to-top-1000 fused candidates is standard practice as of 2025-2026 and worth including given how cheap it is relative to the rest of the pipeline; instruction-following rerankers (e.g., Voyage rerank-2.5, Aug 2025) are a recent capability if entity-specific filtering ("only injury-relevant passages," not general team news) is needed. Confidence: Medium.
- **Vector database vs. Postgres/pgvector:** **at this data volume (a news/injury corpus for two sports, realistically low millions of chunks at most over many seasons), pgvector — or even pgvectorscale for headroom — is sufficient and is the right default.** Benchmarks from May 2025 show pgvectorscale reaching 471 QPS at 99% recall on 50M vectors, competitive with or beating Qdrant/Pinecone-class systems at that scale, and pgvector alone already matches dedicated vector DBs below ~10M vectors ([Tiger Data, pgvector vs Qdrant, 2025](https://www.tigerdata.com/blog/pgvector-vs-qdrant); [zenvanriel.com, pgvector vs dedicated vector DBs, accessed 2026](https://zenvanriel.com/ai-engineer-blog/pgvector-vs-dedicated-vector-db/)). This system's corpus will not approach 10M vectors for a long time. **A dedicated vector database (Pinecone/Weaviate/Milvus) is not warranted at this scale and would be architectural fashion, not a requirement** — its main justification (massive scale, distributed sharding, thousands of concurrent users) does not apply to an internal feature-extraction pipeline serving a small paying customer base. Confidence: High on the "not warranted at this scale" conclusion; Medium on which specific tool to use, since the field moves fast.
- **Embedding model choice:** out of scope to recommend a specific commercial model given how quickly this changes, but the criterion should be: strong short-text/entity retrieval performance and low latency for batch nightly runs — not multimodal or long-context capability, which this corpus doesn't need. Judgment.
- **Fashion flag, explicit:** anything resembling "agentic multi-hop retrieval," multi-vector/late-interaction indexes, or a knowledge-graph layer over this corpus is disproportionate to the actual data shape and volume here and should be treated as premature complexity, not as required infrastructure. Judgment.

---

## 5. Reference architecture

```mermaid
flowchart TB
    subgraph Ingestion["Ingestion (bitemporal, immutable)"]
        A1[Play-by-play / box scores feed]
        A2[NFL official injury feed]
        A3[CFB availability: CFP mandated + conference + scraped beat reports]
        A4[Weather API]
        A5[Multi-book line feed, tick-level]
        A6[News / beat reporter / social scraper]
        A7[Schedule facts: rest, travel, altitude, surface]
    end

    Ingestion --> Snap[Immutable as-of snapshot store\n(event_time, ingested_at, source_snapshot_id)]

    Snap --> Struct[(Structured feature store\nPostgres: EPA/success-rate,\nlines, weather, schedule)]
    Snap --> Unstruct[(Unstructured corpus\nPostgres+pgvector, chunked,\nbitemporal-partitioned)]

    Unstruct --> Retr[Hybrid retrieval\nBM25 + dense + RRF fusion\n+ cross-encoder rerank\nfiltered by as-of timestamp]
    Retr --> Extract[LLM/classifier feature extraction\n(pinned model version, temp=0,\ncached, versioned prompts)]
    Extract --> FeatStore[(Derived feature store\ninjury_severity, sentiment,\nconfidence fields)]

    Struct --> FeatJoin[Feature join / as-of point-in-time join]
    FeatStore --> FeatJoin

    FeatJoin --> Model[Classical predictor\nGBM / hierarchical Bayesian\n+ isotonic/Platt calibration]
    Model --> Pub[Published spread/total]

    Retr -.narrow, bounded.-> Monitor[Near-real-time line-staleness monitor\n(rule-based re-weighting only,\nno LLM-generated number)]
    Monitor -.flags.-> HumanGate[Human review / gated trigger]
    HumanGate -.optional override.-> Pub

    Pub --> Backtest[Backtest / evaluation harness]
    Snap --> Backtest
    Backtest --> Ablation[Ablation: with/without LLM features,\npre-cutoff vs post-cutoff split,\ncanary injection tests]
    Ablation --> Report[CLV-vs-close report, leakage report]
```

**Data flow narrative:** ingestion writes immutable, bitemporally-tagged records for every source. The structured feature store and the unstructured corpus are both derived from the same immutable snapshot layer, never from a live "current state" table, so that any historical prediction can be exactly replayed against the corpus as it existed at that decision time. The LLM feature-extraction step runs in batch against the as-of-filtered retrieval layer, writes versioned features, and those join the structured features on team-week keys. The classical model is the only component that emits the published number. The real-time monitor is a separate, narrow, human-gated path that never bypasses the model.

**Evaluation/backtest harness as a first-class component:** the harness is not a downstream reporting script; it is a component with its own required inputs: (1) the frozen as-of snapshot corresponding to each historical game's actual decision timestamp, (2) the pinned model/prompt versions used for that period, (3) mandatory ablation runs (with/without LLM features), (4) mandatory pre-cutoff/post-cutoff split reporting, (5) canary-injection test results, and (6) CLV computed against the multi-book line feed, not just against a single closing number. No backtest result should be reported to the manager without items 3-5 attached.

---

## 6. Where this conflicts with the edge research

This design is built to be **agnostic** about whether an edge exists — its job is to make the edge question cheaply testable, not to answer it. But several concrete recommendations only make sense under specific, unverified assumptions about market inefficiency, and those should be surfaced rather than smoothed over:

1. **The entire justification for the real-time monitor (§1c) depends on the assumption that sportsbooks are measurably slow to reprice public, unstructured information** (a scratch, a beat-reporter report) relative to how fast this pipeline can ingest and act on it. If books reprice within seconds using their own scraping/modeling infrastructure — which is plausible given how well-capitalized modern books are — this entire component contributes zero CLV and is pure engineering cost. This assumption is **not verified by this memo** and belongs to the edge-research workstream; the architecture is built so it can be A/B tested cheaply (run with/without the monitor, measure CLV delta) rather than assumed.
2. **The CFB non-mandated-disclosure asymmetry (§3) is presented as "could be a genuine, narrow edge" — this requires the assumption that CFB betting markets are less efficient at pricing fragmented injury information than NFL markets.** This is a plausible-sounding market-structure argument (thinner CFB market depth, more books relying on shared, laggy injury aggregators) but it is exactly the kind of thing that sounds compelling and turns out to be already priced by professional bettors and syndicate-informed lines. This memo takes no position on whether it's real; it only argues the feature is cheap enough to build and test in isolation (ablate it specifically) rather than bundle it into an unfalsifiable "the model works" claim.
3. **Recommending (b)/(c) over (a) implicitly assumes the marginal edge, if any, is a few percentage points at most** — consistent with efficient-market priors for a widely bet, heavily modeled market like NFL/CFB spreads. If the true state of the world is that there is a large, exploitable inefficiency in how markets price unstructured qualitative information (which would make option (a)'s "LLM reasons holistically" approach more attractive because the qualitative synthesis itself is the edge, not just a feature), then this architecture under-invests in the reasoning layer. This memo's recommendation is **conditional on the edge research not finding evidence of a large, qualitative-synthesis-shaped inefficiency** — if it does, the recommendation in §1 should be revisited, not treated as settled.
4. **The entire "detect leakage after the fact" methodology (§2) assumes that a stable, non-contamination-explained backtest margin over 52.38% is achievable and observable at all** within a reasonable evaluation window (a season or two of post-cutoff games). If the true edge (if any) is thin enough to be statistically indistinguishable from noise over that sample size, the ablation methodology in §2 may not have the power to separate "small real edge" from "no edge" from "residual leakage" — that is a sample-size/statistical-power problem that belongs to whoever owns backtest methodology validation, not to this architecture memo, but it directly limits how much confidence this design can produce even if built correctly.

---

## Open questions

1. What historical depth of unstructured news/injury data is actually available and scrapeable for CFB going back far enough to build a meaningful post-cutoff-excluded backtest sample, given CFB's disclosure asymmetry is recent (CFP mandate starts 2025-26 season)?
2. Which pinned LLM/classifier will be used for feature extraction, and what is its actual public training cutoff — this directly determines how many historical seasons are backtest-usable for the LLM-feature-layer ablation versus contaminated?
3. Does the business want the real-time line-staleness monitor at all in v1, given §6 flags its value as unverified and its engineering cost is nontrivial (event-driven ingestion, human-gating workflow)?
4. What is the actual expected query/write volume for the unstructured corpus over a multi-season horizon — needed to confirm the pgvector-suffices judgment in §4 stays valid rather than needing to be revisited if CFB's now-broader disclosure surface generates much more volume than assumed?
5. Who validates precision/recall of the LLM feature-extraction step against ground truth (e.g., human-labeled injury severity), and how often — this is the main lever against "garbage-in" feature noise flagged in §1(b)?

---

## Source table

| Source | Date | What it supports | URL |
|---|---|---|---|
| Karger et al., ForecastBench (referenced via 2025-2026 tournament summaries) | 2024, ongoing | LLM forecasting Brier scores vs. human crowd/superforecasters; basis for numeric-calibration skepticism | (referenced via secondary summaries in search results; no single stable URL retrieved) |
| Future Is Unevenly Distributed: Forecasting Ability of LLMs Depends on What We're Asking | Nov 2025 | LLM forecasting Brier scores by domain, overconfidence patterns | https://arxiv.org/html/2511.18394 |
| Do Large Language Models Know What They Don't Know? Evaluating Epistemic Calibration via Prediction Markets (KalshiBench) | Dec 2025 | LLM overconfidence at high-probability levels | https://arxiv.org/html/2512.16030 |
| Temporal Leakage in LLM Backtesting: Measurement, Validation, and Adjusted Scores | Aug 2026 | Contamination mechanism and detection methodology for LLM backtests | https://arxiv.org/html/2608.02985 |
| All Leaks Count, Some Count More: Interpretable Temporal Contamination Detection and Mitigation in LLM Backtesting | Feb 2026 | Naive before/after-cutoff check is unreliable; ablation-based detection needed | https://arxiv.org/html/2602.17234 |
| LMSYS/SGLang, "Towards Deterministic Inference in SGLang and Reproducible RL Training" | Sep 22, 2025 | Batch-invariance nondeterminism at temperature 0; mitigation via batch-invariant kernels | https://www.lmsys.org/blog/2025-09-22-sglang-deterministic/ |
| Defeating nondeterminism in LLM inference, in practice (Medium) | 2025 | Practical summary of batch-invariance nondeterminism findings | https://medium.com/@siddhantg314/defeating-nondeterminism-in-llm-inference-in-practice-38a7dd1e4112 |
| NFL Important Dates 2025-2026 (official PDF) | Jun 5, 2025 | NFL injury-report cadence context | https://media.nfl.com/content/dam/communications/football-communications/2025/news/06%2005%2025%20-%20Important%20Dates.pdf |
| Pro Football Network, "What Is the NFL Injury Policy?" | accessed 2026 | NFL Wed/Thu/Fri practice-report and Friday game-status designation rules | https://www.profootballnetwork.com/what-is-nfl-injury-policy-rules-and-procedures-for-nfl-teams/ |
| Sportshandle, "NCAA Doesn't Plan To Mandate College Football Injury Reports" | referencing 2019 NCAA stance, article accessed 2025-2026 | No NCAA-wide mandate; decision pushed to conferences — older underlying stance (2019) but still the operative status as of 2025-2026 per this and related articles | https://sportshandle.com/ncaa-college-football-injury-report-discussions/ |
| CBS Sports, "College Football Playoff will require teams to provide player availability reports beginning with 2025 season" | 2025 | CFP-specific mandated disclosure starting 2025-26 season | https://www.cbssports.com/college-football/news/college-football-playoff-will-require-teams-to-provide-player-availability-reports-beginning-with-2025-season/ |
| College Football Playoff, "2025-26 CFP Student-Athlete Availability Reporting" | Nov 12, 2025 | Specifics of CFP availability-report cadence | https://collegefootballplayoff.com/sports/2025/11/12/reports.aspx |
| Sportshandle, "College Football Injury Report Mandates Up To Conferences" | accessed 2025-2026 | Confirms Big Ten/SEC conference-level mandates vs. no mandate elsewhere | https://sportshandle.com/college-football-injury-reporting-conference-decision/ |
| Tiger Data, "Pgvector vs. Qdrant" | 2025 | pgvectorscale QPS/recall benchmarks at 10M-100M vector scale | https://www.tigerdata.com/blog/pgvector-vs-qdrant |
| zenvanriel.com, "pgvector vs Dedicated Vector Databases: When PostgreSQL Is Enough" | accessed 2026 | pgvector sufficiency threshold (~10M vectors) vs. dedicated vector DB use cases | https://zenvanriel.com/ai-engineer-blog/pgvector-vs-dedicated-vector-db/ |
| digitalapplied.com, "Hybrid Search: BM25, Vector & Reranking Reference 2026" | 2026 | Hybrid dense/sparse + RRF + cross-encoder reranking as current default practice | https://www.digitalapplied.com/blog/hybrid-search-bm25-vector-reranking-reference-2026 |
| atlan.com, "Hybrid RAG: Dense and Sparse Retrieval for Better AI Answers" | accessed 2026 | Rationale for hybrid retrieval on entity-dense, short-form text | https://atlan.com/know/hybrid-rag/ |

**Notes on sourcing gaps (explicit):** No dedicated, peer-reviewed study of LLM-generated point-spread or totals calibration specifically (as opposed to general-event probability forecasting) was found in this search; the numeric-calibration argument in §1 extrapolates from general forecasting-calibration literature and is labeled as judgment where it does so. The ForecastBench Brier-score figures were obtained via secondary summaries during search rather than a single stable primary URL; treat those specific numbers as indicative, not exact, and re-verify against the primary ForecastBench source before citing externally.
