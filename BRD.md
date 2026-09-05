# Business Requirements Document — NFL/CFB Spread & Totals Prediction System

**Version:** 1.0 · **Date:** 2026-09-05
**Audience:** Claude Code, consuming this directly as a build spec in a later session.
**Builder profile:** Solo. Production RAG shipped; PyTorch built from source for a
Blackwell GPU; walk-forward-validated HMM trading model; LangChain and Claude Code
fluent. **Do not explain ML basics, vector stores, or temporal validation.** Sports
data plumbing is the new work.

---

## 0. READ THIS BEFORE WRITING ANY CODE

**This is not a spec for a product. It is a spec for an experiment that will probably
fail, plus a conditional product spec that activates only if it does not.**

The predictive-edge research underlying this document puts **5–7%** on an edge large
enough to be a business on main-market NFL/CFB sides and totals, and **40–45%** on zero
or negative edge. There is **no published evidence that an LLM or RAG system produces
closing-line value on NFL or CFB spreads or totals.**

Therefore:

1. **Phases are gates, not milestones.** Each has a kill-gate. When a kill-gate trips,
   **stop and report — do not proceed to the next phase, and do not weaken the gate.**
2. **Build the evaluation harness before any model.** A model without a trustworthy
   harness is unfalsifiable.
3. **Pre-register before you fit.** Write the hypothesis, the strategy variant count,
   and the acceptance threshold to a file, commit it, and only then run the test. The
   trial count is required to compute the Deflated Sharpe Ratio and PBO; these are not
   post-hoc diagnostics.
4. **Success is CLV, not win rate.** Win rate cannot resolve this question on any
   business-relevant timescale (§3.4).
5. **Do not build the user-facing product, billing, or marketing surface until Phase 1
   passes its gate.** Phases 3+ are conditional and must not be started early.

---

## 1. Problem Statement

Determine, as cheaply and as falsifiably as possible, whether a point-in-time-correct
statistical model — optionally augmented by retrieval-derived features — produces
statistically significant positive closing-line value against NFL and college football
point spreads and totals.

If and only if it does, deliver that model's output as a subscription product with an
auditable performance record built to FTC substantiation standards.

**Breakeven:** standard -110 vigorish implies 110/210 = **52.38%**.
**Primary metric:** mean CLV per bet, in points and in win-probability terms, measured
against a pre-registered closing line.
**Secondary metric:** ATS% / totals hit rate — reported, never used as the gate.

---

## 2. Functional Requirements

### FR-1 Data Ingestion

- **FR-1.1** Ingest, for NFL and CFB FBS, at minimum 2020→present (deeper where free):
  game results and box scores; play-by-play; derived efficiency metrics (EPA, success
  rate); schedule, venue, surface, rest, travel; injury reports and depth charts;
  weather (forecast *and* actual); betting lines for spreads and totals.
- **FR-1.2 — Bitemporal storage is mandatory for every record.** Every row carries
  `valid_time` (when the fact was true of the world) and `recorded_time` (when the
  system learned it). **No downstream code may read a table directly**; all reads go
  through a single `as_of(query, timestamp)` accessor that filters on `recorded_time`.
- **FR-1.3** Odds ingestion must capture **opening line, every material move with a
  timestamp, and the closing line, per book**. Single open/close pairs without
  intraday timestamps are insufficient — they cannot support CLV and must be rejected
  at ingest with a clear error, not silently accepted.
- **FR-1.4** Ingestion is idempotent and replayable. Re-running over the same window
  produces byte-identical state.
- **FR-1.5** Record provenance per row: source, retrieval timestamp, vendor
  record-version where available.
- **FR-1.6** Never overwrite a revised statistic in place. Revisions are appended as new
  `recorded_time` rows. Retroactively corrected stats are a primary leak vector.

### FR-2 Retrieval / RAG Pipeline

**Architecture decision (resolved): hybrid, narrowly scoped. RAG-as-predictor is
rejected.** A classical statistical/ML model emits **every published number.**
Retrieval and LLMs appear in exactly two bounded roles.

- **FR-2.1 — Offline feature extraction (the only LLM role in v1).** An LLM/classifier
  converts unstructured text (injury notes, beat-reporter reports, depth-chart
  chatter) into a **bounded, versioned set of numeric/categorical features** — e.g.
  `starting_qb_out: bool`, `practice_participation_trend: ordinal(0-3)`,
  `beat_reporter_severity: float[-1,1]` with a confidence field. These join the same
  feature vector as structured data.
- **FR-2.2 — Structured sources are NOT retrieval.** Play-by-play, lines, weather, and
  schedule are SQL / feature-store lookups. **Do not put them in a vector index.** At
  this data volume Postgres + pgvector is sufficient for the unstructured slice; a
  dedicated vector database is not warranted and must not be introduced without a
  measured justification.
- **FR-2.3 — As-of-timestamp filtering happens IN the index, not after retrieval.**
  Every indexed document carries a verified publication timestamp; the retriever
  hard-filters on it. Post-filtering retrieved results is not acceptable — it leaks
  through ranking.
- **FR-2.4 — Contamination control.** Any LLM-touched component may only be evaluated on
  games occurring **after** the pinned model version's training cutoff. Pre-cutoff
  backtests of LLM-derived features are uninterpretable and must be labeled as such in
  every report.
- **FR-2.5 — Determinism.** Pin model version and all decoding parameters; cache every
  LLM call keyed by (model version, prompt hash, as-of timestamp). A backtest that
  cannot be reproduced byte-for-byte is not a backtest.
- **FR-2.6 — Ablation is mandatory.** Every evaluation reports the with-LLM-features and
  without-LLM-features variants side by side. **The ablation acceptance criterion is
  stated in CLV terms, not win rate** (see §3.4 — the win-rate version of this test
  cannot return a verdict within the available sample).
- **FR-2.7 — Deferred to v2, explicitly gated.** The near-real-time line-staleness
  monitor (flagging that a late signal has landed before the line moved) is **NOT in
  v1**. The book-repricing-latency inefficiency it targets has **no located
  measurement** — the edge research searched for one and deleted its own estimate.
  Build it only after FR-6 measures that latency and finds it exploitable.

### FR-3 Prediction Model

- **FR-3.1** A classical model emits every number: gradient-boosted trees or a
  hierarchical Bayesian model with team/season random effects.
- **FR-3.2** Output is a calibrated probability and an implied number, with explicit
  uncertainty. Calibrate with isotonic regression or Platt scaling on out-of-sample
  data only.
- **FR-3.3** Predictions are made against a specific book, line, and timestamp — never
  against "the line" in the abstract.
- **FR-3.4** Every prediction is written to an **immutable, append-only pick log**
  before the event: model version, feature vector hash, as-of timestamp, book, line
  taken, stake, and rationale. This log is simultaneously the backtest record and the
  FTC substantiation record. **It is a Phase 0 deliverable, not a launch-day one.**
- **FR-3.5** Model registry: every trained model is versioned with its training window,
  feature set version, hyperparameters, and a pointer to its pre-registration file.

### FR-4 Backtesting & Evaluation Framework

**This is the most important component in the system. Build it first.**

- **FR-4.1** Walk-forward validation, season-by-season or rolling-window. No shuffling.
  No cross-season leakage.
- **FR-4.2** CLV computation per graded bet: `implied_prob(closing_line) −
  implied_prob(bet_line)`, de-vigged, aggregated with confidence intervals. The
  reference close is **pre-registered** — which book, which timestamp (last tick before
  scheduled kickoff) — before any evaluation runs.
- **FR-4.3 — Leakage tests are first-class tests.** Include a test that deliberately
  corrupts a feature with future data and asserts the harness detects and rejects it.
  Cover, at minimum, all six known vectors: retroactively revised statistics; injury
  reports stored as final status rather than as-of status; weather as observed rather
  than forecast; odds snapshots of ambiguous book/timestamp provenance; survivorship in
  the odds archive (postponed/rescheduled games silently absent); and line selection
  ("we'd have gotten +3.5").
- **FR-4.4 — Trivial baselines, implemented before any real model:** always-favorite,
  always-home, and regress-to-market-close. If the harness cannot show these baselines
  producing ~zero CLV, the harness is wrong, not the baselines.
- **FR-4.5 — Overfitting controls.** Record the total number of strategy variants tested.
  Compute Probability of Backtest Overfitting (CSCV) and the Deflated Sharpe Ratio.
  Report Bonferroni-corrected thresholds alongside uncorrected ones. **A backtest
  reported without its trial count is not evidence.**
- **FR-4.6 — The decorrelation test is the cheap kill.** Regress realized margin on
  (closing line, model prediction). If the model's coefficient is not significantly
  non-zero, the model contains no information the close does not already have. This
  runs in an afternoon and most candidate models will fail it. **Run it before
  anything else.**
- **FR-4.7** Report NFL and CFB separately, and spreads and totals separately. They may
  behave differently and pooling hides it.

### FR-5 User-Facing Output — CONDITIONAL, do not build before Phase 1 passes

- **FR-5.1** Web-first delivery. Do not build native apps (app-store policy risk).
- **FR-5.2** Publish the full auditable CLV record — every pick, timestamped, graded,
  including losers. No cherry-picking, no retroactive edits.
- **FR-5.3** Geo-gating enforced at signup **and at content delivery** (IP + billing
  address + attestation), not merely stated in terms.
- **FR-5.4** 21+ attestation gate; responsible-gambling messaging.
- **FR-5.5** Subscription mechanics built to California ARL and the FTC negative-option
  regime: express affirmative consent, clear terms before charge, and cancellation at
  least as easy as signup.
- **FR-5.6** No performance claim may be rendered anywhere in the product or marketing
  unless it is computed directly from the immutable pick log over a stated window with
  its confidence interval displayed. **Hard-code this constraint; do not leave it to
  editorial discipline.**

### FR-6 Instrumentation Probe (cheap, run in parallel with Phase 0)

- **FR-6.1** Passively capture tick-level multi-book odds against a timestamped log of
  official injury/availability announcements, and **measure the actual book-repricing
  latency.** This is the measurement nobody has made; it decides whether FR-2.7 is ever
  built.
- **FR-6.2** Probe capacity: record accepted stake and rejection point per book on CFB
  team totals and alternates at the day/hour a candidate strategy would fire. Capacity
  in these markets has been measured by nobody and is a first-order business
  constraint.

---

## 3. Non-Functional Requirements

### 3.1 Data refresh cadence
| Source | Cadence |
|---|---|
| Odds | ≤5 min in season; tick-level for the FR-6 probe |
| Injuries | Per official report cycle; continuous monitoring Thu–Sun |
| Weather | 6-hourly to T-24h; hourly inside T-24h |
| Play-by-play / results | Post-game, same day |
| News | Continuous ingest, timestamped at retrieval |

### 3.2 Latency
- Backtest: no requirement. Correctness only.
- Live prediction (Phase 3+): minutes, not seconds. **v1 is a scheduled batch job, not
  a persistent low-latency service.** If FR-6.1 later justifies FR-2.7, the always-on
  event-driven variant must be **separately estimated and budgeted** — it is a
  different system and is currently costed by nobody.

### 3.3 Accuracy / evaluation thresholds

**Phase 1 gate (the only gate that matters):**
- ≥150 prospectively timestamped bets (plan for 150–300, not 70 — the 70-bet figure
  assumes cross-bet CLV SD of 1.0pt; at SD 2.0 it is 275).
- Mean CLV significantly > 0 at **p < 0.01, one-sided**, against the pre-registered
  close.
- **AND** a significantly non-zero model coefficient in the FR-4.6 decorrelation
  regression.
- **AND** PBO below a pre-registered threshold given the declared trial count.

**Explicitly NOT a gate:** any ATS% figure. Detecting a true 54% rate against 52.38%
at 80% power needs **5,868 bets** — 12.4 seasons betting selectively, or **34 seasons**
after Bonferroni for 100 variants. Report it; never gate on it.

### 3.4 Reproducibility
Any backtest must be re-runnable from a commit hash + pre-registration file to
byte-identical output.

### 3.5 Auditability
The pick log is append-only, timestamped, and externally verifiable. It is the FTC
substantiation record; treat integrity as a security property.

---

## 4. Data Sources & Integrations

| Need | Recommended | Cost | Status |
|---|---|---|---|
| NFL PBP/stats | nflfastR / nflverse | $0 | MIT-licensed code |
| CFB PBP/stats | CollegeFootballData.com | $0–$300/yr | **Terms reportedly bar redistribution — confirm derived-output use** |
| Weather | NOAA/NWS (hist.), Open-Meteo (live) | $0 / $348/yr | Public domain / commercial tier |
| Odds — MVP | The Odds API Business | $1,188/yr | **Commercial-use and derived-works terms UNREAD — blocking** |
| Odds — true CLV depth | OddsJam / OpticOdds / SportsGameOdds | **$6,000–$18,000/yr est.** | Quote-gated; third-party estimate only |
| News | RSS first | $0 | Avoid paid news APIs until proven necessary |

**BLOCKING PRE-BUILD ACTIONS** (do these before writing ingestion code):
1. Obtain written vendor quotes and readable terms from The Odds API, OddsJam,
   OpticOdds, and SportsGameOdds covering: intraday/tick odds history, multi-book
   attribution, history depth, **and explicit permission for commercial derived
   works in a gambling-adjacent product**.
2. Confirm CFBD permits derived-output commercial use.
3. Note: Sportradar's terms prohibit use "in a betting, gaming, gambling, or wagering
   capacity" without written approval; OpticOdds bars "any revenue-generating
   endeavor" without an upgraded agreement. **The product is a derived work of odds
   data.** `[REQUIRES REVIEW BY LICENSED ATTORNEY]`

---

## 5. Recommended Architecture

```
┌─ Ingestion ──────────────────────────────────────────────┐
│  odds │ pbp/stats │ injuries │ weather │ news            │
│         ↓ all writes stamped (valid_time, recorded_time) │
└──────────────────────────┬───────────────────────────────┘
                           ↓
┌─ Bitemporal store (Postgres + pgvector) ─────────────────┐
│  ALL reads via as_of(query, ts). No direct table reads.  │
└──────────────────────────┬───────────────────────────────┘
                           ↓
┌─ Feature layer ──────────────────────────────────────────┐
│  structured: SQL/feature store  (NOT retrieval)          │
│  unstructured: as-of-filtered index → LLM extractor →    │
│                bounded versioned features (cached)       │
└──────────────────────────┬───────────────────────────────┘
                           ↓
┌─ Model (classical; emits EVERY number) ──────────────────┐
│  GBM or hierarchical Bayesian → calibration              │
└──────────────────────────┬───────────────────────────────┘
                           ↓
┌─ Immutable pick log (append-only)  ← FTC substantiation  │
└──────────────────────────┬───────────────────────────────┘
                           ↓
┌─ Evaluation harness (BUILT FIRST) ───────────────────────┐
│  walk-forward │ CLV │ decorrelation │ leakage tests │    │
│  PBO / DSR / trial count │ ablation (CLV terms)          │
└──────────────────────────┬───────────────────────────────┘
                           ↓
┌─ Delivery (CONDITIONAL — Phase 3+ only) ─────────────────┐
│  web │ geo-gate │ 21+ │ ARL billing │ public CLV record  │
└──────────────────────────────────────────────────────────┘
```

**Stack:** Python; Postgres + pgvector; Parquet for historical snapshots; Prefect or
plain cron for orchestration; MLflow or plain versioned artifacts for tracking;
scikit-learn / LightGBM / PyMC; FastAPI for the eventual thin delivery layer. Bias
toward boring, debuggable, and cheap. The Blackwell GPU is not a bottleneck here and
should not shape the design.

---

## 6. Technical Risks & Open Questions

| Risk | Likelihood | Impact | Early warning | Mitigation |
|---|---|---|---|---|
| First backtest silently contaminated | **Near-certain** | Fatal | Results look good | FR-4.3 leakage suite; six named vectors |
| Overfitting via variant selection | **Near-certain** | Fatal | A 57% variant appears | Pre-register trial count; PBO/DSR (FR-4.5) |
| LLM training-data contamination | High | Fatal to LLM path | Pre-cutoff ≫ post-cutoff | FR-2.4 post-cutoff-only eval; FR-2.6 ablation |
| Timestamped odds unaffordable/unlicensed | High | Blocks CLV entirely | Vendor quotes | §4 blocking pre-build actions |
| Sample too small to conclude | **Certain on win rate** | High | — | CLV-only gating (§3.3) |
| CLV→profit link unvalidated | High | Strategic | — | Acknowledge; treat CLV as necessary-not-sufficient |
| Capacity / account limiting | High | Caps the business | Limits on first real bets | FR-6.2 measures it |
| Data license bars the product | Medium | Fatal | Terms review | §4; attorney review |

**Open questions — answer before or during Phase 0:**
1. What are The Odds API's actual commercial-use and derived-works terms?
2. Does the Business tier actually provide multi-season, intraday-timestamped,
   multi-book history — the exact requirement?
3. **Read Arscott (2023),** *JSE* 24(5):664–689. It is the single strongest affirmative
   evidence in this project and **nobody has read it.** Its sample size, period, and
   whether the >55% was measured against the closing or opening line are all unknown.
   Obtain via institutional library, ILL, or by emailing the author.
4. What is the actual book-repricing latency after injury news? (FR-6.1)
5. What are real accepted stakes on CFB team totals and alternates? (FR-6.2)
6. Confirm the ForecastBench figures at source (arXiv:2409.19839) — two team members
   reported incompatible numbers and neither read the paper.

---

## 7. Suggested Build Phases

> **Effort figures are estimates at 25–30 hrs/week and carry an explicit dependency on
> §4's blocking actions completing first. The adversarial review's objection — that
> these ranges were never audited and are optimistic against the data and compliance
> dependencies — is accepted; treat the upper bound as the planning number.**

### Phase 0 — Harness & probes (3–5 weeks) · *unconditional*
Bitemporal storage + `as_of()`; walk-forward splitter; CLV computation; leakage test
suite; three trivial baselines; **immutable pick log**; FR-6 latency and capacity probes
running in parallel.
**Exit:** baselines run end-to-end on ≥1 full season per league; leakage tests pass;
CLV confidence intervals reported.
**Kill-gate:** if vendor data provides no reliable as-of/revision semantics, or §4's
licensing questions come back prohibitive — **stop.** Building a model on ungoverned or
unlicensed data is not worth doing.

### Phase 1 — Falsify the edge (3–5 weeks) · *unconditional*
Pre-register first. Small deliberately-limited feature set; one well-understood model
class; no ensembling; no large hyperparameter search. Run **FR-4.6 decorrelation first**.
**Exit:** the Phase 1 gate in §3.3, in full.
**Kill-gate:** decorrelation coefficient not significantly non-zero, **or** mean CLV not
significantly > 0 at p<0.01 — **stop and report. Do not proceed. Do not weaken the
gate. Do not add features and retry without incrementing and re-declaring the trial
count.**

### Phase 2 — Prospective validation (1 full season) · *conditional on Phase 1*
Paper or personal-stake only. Zero subscribers, zero marketing, zero claims. Accumulate
≥150 prospectively timestamped bets against the pre-registered close. Run the FR-2.6
ablation in CLV terms.
**Exit:** the §3.3 gate holds prospectively, out of sample, in real time.
**Kill-gate:** prospective CLV not significant — **stop.** A backtest that does not
replicate forward is the expected outcome, not an anomaly.

### Phase 3 — Compliance foundation (8–16 weeks, overlaps Phase 2) · *conditional*
Gaming counsel engagement; state allowlist determination; **payment-processor
acceptability test in writing — do this first, it is cheap and dispositive**; terms and
ARL-compliant subscription mechanics; geo/age gating.
**Kill-gate:** any compliance kill criterion in `BUSINESS_PLAN.md` §5.6 trips — **stop.**

### Phase 4 — Product (10–16 weeks; 14–22 if LLM in path) · *conditional on 1–3*
Web delivery, public auditable CLV record, billing, monitoring, drift detection.
**Exit:** a subscriber can sign up, be geo/age-gated, receive picks, and audit the full
record.

**Calendar reality:** a compliant paid launch inside the 2026 season is not achievable.
**2027 is the earliest honest target**, and Phase 2 requires a full season regardless.
Phases 0–1 can and should start immediately — they are the cheap part, and they are
the part that probably ends the project.
