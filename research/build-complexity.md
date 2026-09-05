# Build Complexity Assessment: NFL/CFB Spread & Totals Prediction Service

**Role:** Implementation & Build Complexity Engineer
**Date:** 2026-09-05 (corrected 2026-09-05, post-citation-audit)

---

## Bottom Line

- **Effort to a defensible backtest verdict (edge exists / does not exist):** 5–9 weeks
  solo-developer effort (Medium confidence), assuming 25–30 hrs/week and that historical
  data access (odds, stats, PBP) is already solved by the data-sourcing owner. This is
  the number that matters most — everything else is contingent on this verdict.
- **Effort to a shippable paid product (statistical/ML variant, post-edge-confirmation):**
  additional 10–16 weeks (Medium confidence).
- **Effort to a shippable paid product (LLM-in-the-loop variant):** additional 14–22
  weeks — larger because of contamination-control engineering, prompt/output
  evaluation harnesses, and inference cost/latency management that the statistical
  variant doesn't need.
- **Single highest technical risk:** data leakage / lookahead bias producing a fake
  backtest. In point-in-time sports data (injury reports amended after the fact, lines
  moving on information not available at bet-time, roster/coaching data retroactively
  corrected), leakage is the default failure mode, not an edge case — and it is
  invisible unless the storage layer is bitemporal from day one. A leaking backtest
  will show a plausible-looking edge (e.g., 53–55% ATS) that evaporates the moment
  real money and real timing constraints are applied. This is why the backtest/CLV
  harness is scoped as Phase 0, before any model exists.

**Assumptions used throughout:** solo builder, 25–30 hrs/week (part-time-plus, consistent
with someone who has shipped RAG + custom PyTorch builds + a trading model alongside other
work), Claude Code used as an implementation accelerant (not a source of domain knowledge),
and data vendor access/pricing already resolved by another workstream (explicitly out of
scope here — flagged as a hard external dependency).

---

## 1. Work Breakdown (solo-developer-weeks, 25–30 hrs/week)

Effort is split where the two architecture variants diverge. Where not split, effort is
the same for both.

| Component | Low | Expected | High | Complexity | Variant delta | Confidence |
|---|---|---|---|---|---|---|
| Data ingestion — box scores / team & player stats (nflverse, CFBD-style APIs) | 1.0 | 1.5 | 2.5 | Medium | none | Medium |
| Data ingestion — play-by-play (NFL + CFB) | 1.5 | 2.5 | 4.0 | High | none | Medium |
| Data ingestion — injuries (official reports + beat-reporter scrape/API) | 1.5 | 2.5 | 4.0 | High | none | Low — injury data is notoriously messy and inconsistently timestamped |
| Data ingestion — weather (stadium, historical + forecast) | 0.5 | 1.0 | 1.5 | Low | none | High |
| Data ingestion — betting lines (open/close, multi-book, line movement) | 1.5 | 2.5 | 4.0 | High | none | Medium — vendor API stability is a real risk, see register |
| **Point-in-time / bitemporal storage layer** | 3.0 | 5.0 | 8.0 | **Very High** | none | Medium |
| Feature engineering pipeline (rolling stats, EPA/success-rate derivatives, matchup features, market-derived features) | 2.0 | 3.5 | 5.5 | Medium-High | slightly higher for (b) if features must be serialized to text for LLM context | Medium |
| Retrieval layer / index | (a) 1.0 / (b) 2.5 | (a) 1.5 / (b) 3.5 | (a) 2.5 / (b) 5.0 | (a) Low-Medium / (b) High | **diverges** — in (a) retrieval is a feature-feed lookup (structured k-NN or similar-game similarity join, low novelty for this builder given RAG experience); in (b) retrieval must feed a context window reliably, requires citation/traceability so the LLM's claims can be audited against ground truth | Medium |
| Model training & tuning | (a) 2.5 / (b) 1.5 | (a) 4.0 / (b) 2.5 | (a) 6.0 / (b) 4.0 | (a) High / (b) Medium | **diverges** — (a) needs real model selection/tuning work (gradient boosting, calibration, possibly the HMM-style regime framing the builder already knows); (b) shifts much of this effort into prompt/output-schema engineering instead, so raw "training" time drops but total system time does not | Medium |
| **Backtesting & walk-forward harness w/ CLV measurement** | 2.0 | 3.0 | 4.5 | **Very High** | (b) adds ~1 week for contamination controls (holding out any game the LLM could plausibly "recall") | High — this is the one place estimate confidence is high because the builder has already built one of these for the HMM trading system |
| Live inference & scheduling (weekly/nightly jobs, line-freeze cutoffs) | 1.0 | 1.5 | 2.5 | Medium | (b) adds latency/cost-control logic | Medium |
| Monitoring, alerting, drift detection (feature drift, CLV drift, data-source outage detection) | 1.5 | 2.0 | 3.0 | Medium | (b) adds LLM output-quality monitoring (hallucinated stats, schema violations) | Medium |
| User-facing delivery | 1.0 | 1.5 | 2.5 | Low-Medium | none | High |
| Billing/subscription integration (Stripe or similar) | 0.5 | 1.0 | 1.5 | Low | none | High |
| Compliance surface (geo-gating, age-gating, disclaimer plumbing, performance-claim record-keeping) | 1.0 | 1.5 | 2.5 | Medium | none | Medium |
| **Total, variant (a) statistical/ML core** | **20.0** | **31.0** | **48.0** | | | |
| **Total, variant (b) LLM-in-the-loop** | **21.5** | **33.0** | **50.5** | | | |

Notes on the table:

- **Point-in-time/bitemporal storage is flagged Very High and is the most
  underestimated component in projects like this.** Concretely: sports data is
  revised constantly after the fact — injury designations change hour-to-hour,
  officially "final" box scores get stat corrections days later, depth charts and
  weather forecasts are retroactively different from what was knowable at kickoff,
  and closing lines are only known *after* the window they're meant to evaluate.
  A model that queries "what did we know as of T-1hr before kickoff" needs every
  ingested table to carry both a `valid_time` (when the fact was true in the world)
  and a `recorded_time`/`ingested_at` (when the pipeline learned it), and every
  feature-generation and backtest query must filter strictly on `recorded_time <=
  as_of`. Retrofitting this after building a naive "latest snapshot" schema is
  typically as expensive as building it correctly the first time, which is why it is
  scoped as its own Very High line rather than folded into "ingestion." The builder's
  trading-model experience with walk-forward validation is a real asset here — the
  *concept* is familiar — but the sports-specific gotcha (facts revised after the
  fact, not just new facts arriving) is the new part.
- **Should the backtest/CLV harness be built before any model?** Yes, unambiguously.
  The harness — point-in-time feature reconstruction, walk-forward split logic, and
  CLV computation against closing lines — is what makes a "53% ATS" claim falsifiable
  at all. Building a model first and bolting on evaluation later all but guarantees
  the naive-snapshot leakage failure mode described above, because early feature
  code will implicitly use "current" data. A trivial baseline (e.g., "always take
  the favorite," "regress to market close," home-field-only) run through the harness
  first also gives a floor CLV number for comparison and shakes out harness bugs
  before any model complexity is added. This ordering is reflected in Phase 0/1 below.
- Retrieval and model-training lines are where the two variants genuinely diverge in
  kind, not just magnitude: in (a) retrieval is infrastructure in service of a
  numeric model; in (b) retrieval *is* the model's working memory, so its failure
  modes (stale index, wrong-game contamination, missing citations) become
  prediction-quality bugs, not just latency bugs.

---

## 2. Technical Risk Register

| Risk | Likelihood | Impact | Early warning sign | Mitigation |
|---|---|---|---|---|
| Data leakage / lookahead bias producing a fake backtest | High | Critical | Backtest CLV or ATS% looks "too good" (e.g., >56–58% consistently) with no clear causal story | Bitemporal storage from Phase 0; strict `as_of` filtering enforced at the query layer (not just convention); a leakage unit-test suite that asserts no feature depends on data recorded after the bet-freeze timestamp |
| LLM training-data contamination (variant b only) | High if using a general-purpose LLM on historical games | Critical | Backtest performance on older/well-known games (e.g., 2023 playoff games) is implausibly strong vs. performance on very recent/obscure games | Restrict backtest evaluation to games occurring after the LLM's training cutoff where possible; for pre-cutoff games, use a "blind" prompt format that withholds identifying info (dates, team names replaced with tokens) and test whether performance degrades — degradation confirms memorization rather than reasoning; prefer variant (a) for anything claiming historical backtest validity |
| Overfitting across many strategy/feature variants (multiple-comparisons problem) | High | High | Best-of-N backtested variants shows a big gap between in-sample and out-of-sample/holdout performance | Pre-register the feature set and model class before looking at holdout results (the builder's trading-model discipline transfers directly here); apply a multiple-testing correction (e.g., deflated Sharpe-style adjustment) when reporting the "best" variant's edge; hold out at least one full season never touched during development |
| Odds-data gaps and vendor API instability | Medium-High | Medium-High | Missing closing-line rows, timestamp gaps, or schema changes from the odds vendor | Multi-vendor redundancy or at minimum a monitoring job that alerts on missing expected rows per game-week; treat odds vendor as a hard external dependency (owned by the data-sourcing team member) |
| Insufficient sample size within 1–2 seasons | High | High | Confidence intervals on CLV remain wide enough to include 0 after a full season | See computation below — plan explicitly for a multi-season validation horizon, not a single-season verdict |
| Sportsbook account limiting if builder bets own model | Medium-High (near-certain if consistently profitable) | Medium (business-model risk, not technical, but affects whether "surfacing picks" can include the builder's own track record) | Reduced max bet sizes, delayed bet acceptance, outright account closure | Track CLV (which is book-agnostic and survives limiting) rather than realized bankroll growth as the primary success metric — this is already the plan and is the right call |
| LLM inference cost overrun at scale (variant b) | Medium | Medium-High | Per-prediction cost climbing due to larger context windows (more retrieved documents) or retry loops on malformed output | Cap context size, use structured-output/JSON mode to reduce retries, use a cheaper model tier for high-volume routine predictions and reserve larger models for edge cases; budget and alert on $/week spend |
| Key-person / solo-founder concentration risk | High (structural, not a bug) | High | N/A — always present | Document pipeline thoroughly (Claude Code + this memo's phase plan double as documentation); avoid single-region hosting/single-vendor dependencies where cheap to avoid; not fully mitigable for a solo project — flag as a standing business risk, not something engineering alone fixes |

**Sample-size computation (as requested):**

- **Breakeven win rate at standard -110 odds: 52.38%.** This figure is a direct
  arithmetic consequence of the standard American-odds-to-implied-probability
  conversion, not an empirical or attributed claim, and is shown here in full so it
  does not rest on an unstated external authority: for negative American odds of
  magnitude *M* (e.g., -110, so *M* = 110), the break-even (implied) probability is
  *M* / (*M* + 100). For *M* = 110: 110 / 210 = 0.52380..., i.e., 52.38%. The "vig"
  is the amount by which the two-sided implied probability (52.38% + 52.38% =
  104.76%) exceeds 100% (a 4.76-point overround), which is how a sportsbook prices
  in its commission on a two-way market. **Sourcing status:** in this correction
  round, an attempt was made to locate and retrieve an independent, dated,
  third-party authoritative source for this figure (sportsbook-education sites,
  betting-math calculator sites, and a general reference encyclopedia entry on
  moneyline odds were identified via search). Every one of these could not be
  retrieved in this session — page fetches to bettingpros.com, procomputergambler.com,
  boydsbets.com, sportsbettingoddscalculator.com, pikkit.com, topendsports.com, and
  en.wikipedia.org all failed due to this session's network egress restrictions, so
  none is cited here as a verified source (citing a URL that could not actually be
  retrieved would violate this audit's sourcing standard). **Confidence: High** on
  the arithmetic itself (it follows directly from the definition of American odds
  and can be checked independently by anyone with a calculator); **Low** on
  independent third-party corroboration, since no external dated source was
  successfully retrieved and verified this session. If a specific attributable
  source is required for the final deliverable, that retrieval should be attempted
  again from a network context that is not subject to this environment's egress
  restrictions.
- NFL 2026 regular season: reported at 272 games (32 teams x 17 games each, 18
  weeks), kicking off 2026-09-09, consistent across several independent items
  surfaced via search (an NFL.com media schedule-release PDF, NFL.com's own
  by-team schedule listing, and CBS Sports' schedule coverage). **Sourcing status:**
  none of these pages could be independently fetched and verified in this session —
  the NFL.com PDF, NFL.com by-team page, CBS Sports article, and topendsports.com
  recap all failed to resolve under this session's network egress restrictions.
  The figure is therefore retained (multiple independent outlets converge on the
  same numbers in search-result summaries) but its confidence is downgraded from
  the original draft: **Confidence: Low-Medium** (previously stated as Medium/High
  on the assumption the primary-source PDF had been verified; it had not been
  independently confirmed by direct retrieval, only by search-snippet agreement).
- CFB FBS 2025 season: approximately 134–136 FBS teams playing roughly 12–13 games
  each, yielding on the order of ~800–870 FBS regular-season games league-wide per
  year (before bowls). This was flagged in the original memo as "a derived
  estimate, not a cited count," and that status is unchanged: the Wikipedia page
  used to source the team count could not be retrieved and verified in this
  session either. **Confidence: Low** (unsourced, derived approximation only —
  treat as a planning-order-of-magnitude number, not a defensible fact for any
  external-facing claim).
- Combining NFL + FBS gives on the order of 1,050–1,150 total graded games/season
  across both leagues — but the number that matters for statistical power is *bets
  placed against a specific, stable strategy*, which is smaller than total games
  because most strategies won't bet every game (a selective model targeting, say,
  30–50% of games at a perceived edge yields only 300–600 graded bets/season).
- At a plausible true edge of 2–3 percentage points over the 52.38% breakeven
  threshold (i.e., ~54–55% true ATS win rate), the binomial standard error on a
  400-bet sample is roughly 2.5 percentage points — meaning a single season's worth
  of selective bets is **not** sufficient to distinguish a real 2–3pt edge from
  variance at conventional confidence levels. Two to three full seasons (800–1,500+
  graded bets) is closer to the minimum needed for a statistically credible verdict,
  which directly shapes the timeline in Section 3. This conclusion is not sensitive
  to whether the 52.38% constant is externally corroborated beyond its own
  arithmetic (see above) — it would hold under any -110-equivalent vig structure in
  this range.

---

## 3. Timeline

**Seasonal constraint, stated explicitly:** NFL and FBS CFB seasons run roughly
early September through mid-January. Per search-surfaced (not independently
fetched/verified this session — see Section 2 sourcing note) reporting, the 2026
NFL regular season is expected to run 2026-09-09 to roughly early-to-mid January
2027; CFB runs slightly earlier, late August, through the January bowl
season/CFP. Outside that window there is no live betting market to validate
against — historical backtesting can continue year-round, but **live, real-time
CLV validation is only possible roughly September–January.**

**What 2026-09-05 implies:** the 2026 season has already begun or is about to
(NFL kickoff reported as 2026-09-09). That means:
- There is **not enough runway left before kickoff to build and validate a model
  in time for meaningful live validation in the 2026 season's early weeks** — Phase 0
  (historical backtest) alone is estimated at 5–9 weeks.
- The realistic plan is to use **September 2026–January 2027 for passive/paper-trade
  live validation** of a model whose historical backtest was completed in parallel
  (i.e., start Phase 0 now, and by the time a defensible historical verdict exists —
  roughly October/November 2026 — begin shadow-tracking live CLV against the
  remainder of the 2026 season without accepting subscriber money yet).
- The **next full season available for a complete, ungated live-validation cycle from
  Week 1 is the 2027 season** (NFL kickoff expected ~September 2027, per the same
  seasonal pattern, not independently re-verified this session). This is the
  realistic target for "shippable, revenue-taking product with a season's worth of
  forward live evidence," not late 2026.

| Milestone | Calendar timeframe (from 2026-09-05, at 25–30 hrs/wk) | Notes |
|---|---|---|
| Phase 0 complete (harness + baseline, kill-gate check #1) | ~3–4 weeks → late Sept/early Oct 2026 | Can run entirely on historical data; not blocked by live season |
| Phase 1 complete (statistical model backtest verdict) | ~5–9 weeks total → mid-Oct to early Nov 2026 | This is the primary "defensible backtest verdict" milestone |
| Shadow/paper live-validation window | Nov 2026 – Jan 2027 (remainder of 2026 season) | Live CLV tracked, no money changes hands; partial-season data only, so treat as directional, not conclusive |
| Off-season (Feb–Aug 2027) | Model refinement, product build-out, compliance plumbing, billing integration | No live games to validate against — this dead period should be used for the "product" phases (3–5), not left idle |
| Full-season live validation from Week 1 | September 2027 – January 2028 | First season where live validation starts at kickoff with a finished pipeline; earliest point at which "a season of live evidence" claim is honest |
| Earliest responsible paid-subscriber launch with real track record to show | Early-to-mid 2027 season (soft launch, in-season) at the earliest for a truncated season's live data, or September 2027 for a full clean season | Depends on how much prior-season shadow data the builder is willing to lean on for the "have we shown edge" gate |

---

## 4. Phased Claude Code Build Plan

Each phase is written so a later Claude Code session can execute it as a standalone
unit of work with concrete file/module boundaries and testable acceptance criteria.

### Phase 0 — Backtest & CLV Harness (build before any model exists)

**Goal:** Prove the harness itself is trustworthy using only a trivial baseline, before
any real modeling effort is invested.

**Modules:**
- `storage/bitemporal.py` — schema + accessor layer enforcing `valid_time` and
  `recorded_time` on every table; a single `as_of(query, timestamp)` function that all
  downstream code must use to read data.
- `backtest/walkforward.py` — season-by-season (or rolling-window) train/holdout
  splitter; no shuffling, no cross-season leakage.
- `backtest/clv.py` — computes CLV per graded bet: `(implied_prob(closing_line) -
  implied_prob(bet_line))`, aggregated with confidence intervals.
- `backtest/baselines.py` — implements at least 3 trivial baselines: always-favorite,
  always-home, regress-to-market-close (i.e., bet whichever side the market eventually
  moved toward).

**Deliverables:** a runnable backtest CLI/script that takes historical odds + results
and outputs baseline CLV with confidence intervals, plus a unit-test suite asserting
zero leakage (e.g., a test that corrupts a feature with future data and confirms the
harness rejects/flags it).

**Exit criteria:** all three baselines run end-to-end on at least one full historical
season for each of NFL and CFB; leakage unit tests pass; CLV confidence intervals are
computed and reported (not just point estimates).

**Kill-gate:** if the bitemporal storage design cannot be made to work cleanly against
the actual data vendor's update semantics (e.g., vendor provides no reliable
"as-of" or revision timestamps at all) within the allotted 3–4 weeks, stop and escalate
to the data-sourcing owner — building a model on ungoverned data is not worth doing.
This is a data-availability kill-gate, not a "we didn't try hard enough" gate.

### Phase 1 — Falsify or Confirm the Edge Hypothesis (cheapest possible path)

**Goal:** Determine, as cheaply as possible, whether *any* simple statistical signal
survives point-in-time-correct backtesting with a CLV edge over the 52.38% break-even
threshold (see Section 2 derivation).

**Modules:**
- `features/simple.py` — a small, deliberately limited feature set (recent-form
  rolling stats, market-implied features, home/away, rest days) — resist the urge to
  build the full feature pipeline here.
- `models/baseline_ml.py` — one well-understood model class (e.g., regularized
  logistic regression or gradient-boosted trees), no ensembling, no hyperparameter
  search beyond basic regularization tuning.
- `eval/report.py` — runs the Phase 0 harness against this model, outputs CLV,
  ATS%, and confidence intervals split by season and by league (NFL vs CFB reported
  separately, since they may behave differently).

**Deliverables:** a single report showing walk-forward CLV for the simple model vs.
Phase 0 baselines, across at least 2 full historical seasons per league.

**Exit criteria:** report is generated, statistically reviewed (confidence intervals
computed, multiple-comparisons correction applied if more than one feature set/model
was tried), and a written verdict exists: "edge present," "no edge," or "inconclusive,
needs more data/seasons."

**Kill-gate (the one that matters most):** if the simple model's CLV confidence
interval, after correction for the number of variants tried, does not exclude 0 (i.e.,
cannot statistically distinguish itself from breakeven) across at least 2 seasons of
walk-forward testing, **stop the project** rather than proceeding to feature
engineering, retrieval, or product work. This is the fail-fast gate the manager
requires: it should trigger before Phases 2–5 (feature expansion, model tuning,
delivery, billing) consume any further effort. Note per Section 2's sample-size
math: an "inconclusive" result after only 1 season should route back to "collect
another season of shadow data," not to "add complexity to the model" — adding
model complexity in response to noise is exactly the multiple-comparisons trap.

### Phase 2 — Feature & Model Expansion (only if Phase 1 passes)

**Goal:** Expand the feature set and model sophistication only against a harness
already proven trustworthy, testing whether a real, larger edge exists.

**Modules:** `features/full.py` (injuries, weather, PBP-derived advanced metrics),
`retrieval/index.py` (variant-dependent — see Section 1), `models/tuned.py`.

**Deliverables:** updated walk-forward report showing whether expanded features move
CLV meaningfully vs. the Phase 1 simple model.

**Exit criteria:** documented, statistically-corrected improvement (or documented lack
thereof) over Phase 1's model.

**Kill-gate:** if expanded features/retrieval produce no improvement over the simple
model's CLV (within the same statistical rigor as Phase 1), stop adding complexity —
ship the simpler model or stop, do not keep layering features hoping for a different
result.

### Phase 3 — Live Shadow Validation

**Goal:** Validate the Phase 2 model against real, live closing lines in real time,
with no money exchanged, during the remainder of an in-progress season.

**Modules:** `inference/scheduler.py` (weekly job pulling in-season data respecting
the bitemporal cutoff), `monitoring/drift.py` (feature and CLV drift alarms).

**Deliverables:** live weekly predictions logged and graded against actual closing
lines and outcomes.

**Exit criteria:** at least 4–6 weeks of live shadow data collected with CLV tracked.

**Kill-gate:** if live shadow CLV diverges sharply and persistently (beyond
what's explainable by sample noise) from the historical backtest's CLV, treat this as
evidence of an undetected leakage bug in the backtest and return to Phase 0/1 rather
than proceeding to product build-out.

### Phase 4 — Delivery, Billing, Compliance

**Goal:** Build the minimum viable paid product only after Phases 0–3 have produced a
positive verdict.

**Modules:** `delivery/` (recommend Discord bot or simple static/email digest as the
cheapest-to-ship channel — a full web app is not the cheapest path and should be
deferred), `billing/stripe_integration.py`, `compliance/geo_gate.py`,
`compliance/disclaimers.py`, `compliance/record_keeping.py` (append-only log of every
pick made and its outcome, timestamped before the game, to substantiate any
performance claims later).

**Deliverables:** working subscription flow gated by geography/age, disclaimer
surfaced pre-signup, and a tamper-evident record of all historical picks made
(not retroactively edited).

**Exit criteria:** a paying test subscriber can sign up, receive picks, and the
record-keeping log is independently verifiable (e.g., hash-chained or append-only
storage) against picks actually delivered.

**Kill-gate:** none technical here — this phase only starts if Phases 0–3 passed; if
compliance plumbing (record-keeping in particular) can't be made tamper-evident
cheaply, that's a signal to delay launch, not a kill-gate on the whole project.

### Phase 5 — Monitoring & Ongoing Drift Detection

**Goal:** Keep the live system honest across future seasons.

**Modules:** `monitoring/dashboard.py`, alerting on CLV drift, data-source outages,
and (variant b only) LLM output-schema violations or cost spikes.

**Deliverables:** an always-on dashboard and alert channel.

**Exit criteria:** at least one full season running with alerting live and no missed
outages going undetected for more than one game-week.

---

## 5. Recommended Tech Stack

| Layer | Recommendation | Justification |
|---|---|---|
| Language | Python | Already the builder's primary language across RAG, PyTorch, and the HMM trading system — no new tooling cost |
| Storage (bitemporal core) | PostgreSQL (with explicit `valid_time`/`recorded_time` columns and a disciplined query layer, not a bespoke bitemporal DB engine) | Boring and debuggable; a bespoke temporal database (e.g., Datomic-style) adds novelty risk with no clear payoff at this scale; Postgres window functions are sufficient for as-of queries |
| Orchestration | Simple cron/systemd-timer or a lightweight scheduler (e.g., APScheduler) rather than a full workflow engine (Airflow/Dagster) at this scale | Weekly/nightly jobs on a modest number of data sources do not justify the operational overhead of a distributed orchestrator; revisit only if data-source count or job DAG complexity grows substantially |
| Feature store | Flat versioned Parquet/Postgres tables keyed by `(entity_id, as_of)` rather than a dedicated feature-store product (Feast, Tecton) | A dedicated feature store solves multi-team/real-time-serving problems this solo project doesn't have yet; the bitemporal Postgres layer already gives point-in-time correctness, which is the actual requirement |
| Experiment tracking | MLflow (self-hosted, local) or plain structured logging to Postgres/CSV+git | The builder needs to compare walk-forward runs across seasons/leagues/model variants — MLflow is boring, free, and sufficient; do not reach for a hosted SaaS experiment tracker at this scale |
| Model libraries | scikit-learn / LightGBM or XGBoost for variant (a); the existing PyTorch environment is available if a neural approach is later justified but is not the default starting point | Gradient-boosted trees are the standard, well-understood baseline for tabular sports-prediction problems and are far cheaper to iterate on than deep learning; the builder's from-source PyTorch/Blackwell GPU build is an asset if/when a neural model is justified, but using it by default here would be over-engineering relative to the problem's actual shape |
| Retrieval / index (variant a) | A structured similarity/k-NN lookup over historical games (e.g., pgvector on top of the same Postgres instance, or a simple in-memory index) rather than a dedicated vector DB | Keeps infra minimal; the builder's RAG experience transfers directly to standing this up quickly, but the retrieval need here is modest (structured feature similarity, not unstructured document search) |
| Retrieval / index (variant b) | pgvector or a lightweight dedicated vector store (e.g., Chroma) feeding an LLM context window, with mandatory source-citation in every retrieved chunk | The builder's production RAG experience is a direct, real advantage for this variant specifically — this is the one place existing expertise maps almost one-to-one onto the new problem |
| LLM (variant b only) | Claude Sonnet (mid-tier) for routine weekly predictions, reserving a larger/more capable tier only for cases needing deeper reasoning, using Anthropic's Batch API where predictions can be generated non-interactively | Sonnet-tier pricing balances capability and cost for a recurring weekly workload; batch discounts materially reduce spend for non-real-time inference [Anthropic Claude Platform pricing docs, accessed 2026-09-05](https://platform.claude.com/docs/en/about-claude/pricing) |
| Serving | A simple internal script/API (FastAPI) run on a schedule, not a persistent low-latency service | Predictions are generated on a weekly cadence tied to the betting calendar, not real-time-per-request — no need for always-on low-latency serving infrastructure |
| Deployment target | A single small VPS or a personal workstation/homelab (the builder already has a capable local GPU) for research and batch inference; a cheap managed host (e.g., Fly.io/Render) only for the user-facing delivery bot/app | Avoid cloud GPU spend for a workload that is not latency-sensitive and runs a handful of times per week; the existing local Blackwell GPU is a genuine cost advantage for variant (a) model training and is underused if the project instead pays for cloud training compute |
| Delivery channel | Discord bot first, web app deferred | Cheapest and fastest to ship a gated, paid channel; Stripe + Discord role-gating is a well-trodden, low-build-cost pattern compared to a full web app with auth |

---

## 6. Compute and Inference Cost Estimate

All figures are **estimates**, labeled by scale and variant, and should be revisited
once actual data-vendor costs (out of scope here) and real usage patterns are known.

**Research/backtest scale (Phases 0–2, one builder, historical data only):**
- Compute: near-zero incremental cost — CPU-bound feature engineering and
  gradient-boosted tree training on historical seasons run comfortably on commodity
  hardware; the existing local GPU covers any experimental neural-model work at no
  marginal cloud cost. Estimate: **$0–50/month** (electricity/incidental cloud
  storage only).
- Storage: historical NFL+CFB stats, PBP, injuries, weather, and odds for several
  seasons is on the order of low tens of GB — trivial on local disk or a small
  managed Postgres instance. Estimate: **$0–20/month**.
- LLM API (variant b, research scale, backtesting only): assume ~1,000–2,000 games/
  season evaluated with a moderate-context prompt (retrieved stats + injury/weather
  context, ~3,000–6,000 input tokens, ~500–1,000 output tokens per prediction) across
  2–3 seasons for walk-forward testing = roughly 5,000–10,000 total predictions.
  At Claude Sonnet-tier pricing of **$2 input / $10 output per million tokens** for
  Claude Sonnet 5 [Claude Platform pricing docs, accessed 2026-09-05](https://platform.claude.com/docs/en/about-claude/pricing),
  and applying the documented 50% Batch API discount for non-interactive backtest runs
  [same source], this works out to roughly **$50–150 total** for a full multi-season
  backtest run — cheap enough that LLM cost is not a meaningful constraint at research
  scale.

**Production scale (paid product, weekly in-season cadence, variant a):**
- Compute: weekly retraining/inference on a modest VPS or the builder's own hardware.
  Estimate: **$20–100/month** (a small always-on VPS for the delivery bot/scheduler,
  plus incidental storage growth).
- No meaningful LLM inference cost in variant (a) since retrieval feeds a numeric
  model rather than an LLM call per prediction.

**Production scale (paid product, weekly cadence, variant b):**
- LLM API: assume ~15–20 NFL games + ~60–70 FBS games per week during the ~18-week
  season = roughly 1,300–1,600 predictions/season, each with a moderate-context
  prompt (as above). At non-batch (real-time-in-week) Sonnet-tier pricing of $2/$10
  per million input/output tokens, a single prediction (~5,000 in / ~800 out tokens)
  costs roughly $0.02; across the full season this is on the order of **$25–40/season
  in raw LLM spend at Sonnet-tier pricing** — genuinely low unless the prompt design
  balloons context size (e.g., pulling in full play-by-play text rather than
  structured summaries), which is the realistic cost-overrun risk flagged in the
  register. Budget **$50–200/month** in-season to leave headroom for retries,
  larger-context experiments, and occasional escalation to a higher-tier model for
  harder cases.
- Hosting/delivery: same **$20–100/month** as variant (a).

**Overall monthly estimate range:** research phase **$0–70/month**; in-season
production **$50–300/month** for either variant, with variant (b)'s LLM line being
the more volatile of the two and the one most sensitive to prompt-design discipline.

---

## Open Questions

1. What does the data-sourcing team member's plan actually provide re: whether odds
   vendors expose true point-in-time/revision timestamps? This materially affects
   whether the Phase 0 kill-gate triggers.
2. Which architecture variant (a or b) does the retrieval-placement decision-owner
   land on? This memo estimates both, but resourcing should follow one path once
   decided rather than building both in parallel.
3. Is any in-season 2026 data usable for a partial-season shadow-validation dry run,
   or should the team wait for a clean full-season (2027) start given the compressed
   timeline noted in Section 3?
4. Does the compliance/record-keeping requirement (Section 1, Section 4 Phase 4) need
   to satisfy any specific external substantiation standard, or is "tamper-evident
   internal log" sufficient for now? (Explicitly out of scope for this memo per the
   brief, but it gates Phase 4 exit criteria.)
5. Should the 272-game 2026 NFL schedule figure and the 52.38% breakeven figure be
   re-verified by direct primary-source retrieval from a network context without this
   session's egress restrictions before either is used in any external-facing
   document? Both are currently carried at reduced confidence pending that retrieval
   (see Section 2 and Correction Log).

---

## Source Table

| Claim | Source | Published/Updated | Still likely to hold? |
|---|---|---|---|
| Breakeven win rate at standard -110 vig is 52.38% | Self-contained mathematical derivation from the definition of American/moneyline odds (110/(110+100) = 0.5238), shown in full in Section 2; no third-party dated source was successfully retrieved this session (attempted: bettingpros.com, procomputergambler.com, boydsbets.com, sportsbettingoddscalculator.com, pikkit.com, topendsports.com, en.wikipedia.org — all blocked by this session's network egress controls) | N/A — derived, not externally dated | Yes, structurally true as long as -110 juice is the reference line; the arithmetic does not depend on any external authority |
| 2026 NFL season: reportedly 272 regular-season games, 17 games/team, 18 weeks, season runs approx. 2026-09-09 to early/mid-January 2027 | Surfaced via search (NFL.com media schedule-release PDF, NFL.com by-team schedule page, CBS Sports schedule coverage); none independently fetched/verified this session — all blocked by network egress controls | Reported 2026-05-14 (per search snippet, not independently confirmed) | Likely, given convergence across independent outlets in search results, but carries reduced confidence pending direct-source verification |
| 2025 FBS season: ~134–136 teams, derived estimate of ~800–870 FBS regular-season games/year | Wikipedia page on the 2025 FBS season — URL failed to resolve/could not be independently verified this session | Unknown — could not confirm | Low confidence; treat as an unsourced, order-of-magnitude planning estimate only |
| Claude Sonnet 5 pricing: $2 input / $10 output per million tokens (standard pricing as of Sept 2026) | [Claude Platform Docs — Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Accessed 2026-09-05 | Yes for pricing as of this date; API pricing changes over time and should be re-checked before any cost-sensitive commitment |
| Claude API model tier overview (Haiku 4.5, Sonnet 4.6, Opus 4.6/4.7/4.8 pricing tiers) and Batch API 50% discount | BenchLM.ai — Claude API Pricing (September 2026), third-party aggregator; could not be re-fetched/re-verified in this correction round (also blocked by network egress) | 2026-09 (per title, unverified this session) | Unverified this session; flagged in the original memo as needing cross-check against Anthropic's own docs, and that caveat stands — do not treat as an independently confirmed source |

---

## Correction Log

This section records the citation-audit correction round completed 2026-09-05.

1. **52.38% breakeven win rate (Section 2, load-bearing throughout Section 2 and
   the Phase 1 kill-gate).** Audit finding: load-bearing claim with no cited,
   dated source. **Route taken: (b) weakened, combined with an explicit inline
   derivation, plus honest disclosure of a failed sourcing attempt (partial route
   c).** The claim was not deleted, because it is not fundamentally an empirical
   claim requiring third-party testimony — it is arithmetic that follows directly
   from the definition of American moneyline odds. The memo now shows that
   derivation in full inline (Section 2) so the number is self-justifying rather
   than resting on an unnamed authority. Separately, a genuine attempt was made to
   locate and retrieve an independent, dated, third-party source (sportsbook
   education sites, betting-math calculator sites, and a general encyclopedia
   entry were identified via search); every retrieval attempt failed due to this
   session's network egress restrictions, and per the audit's standard, a URL that
   cannot actually be retrieved is not cited. This failure is now disclosed
   explicitly in Section 2 and in the Source Table, and the confidence label was
   split: High for the arithmetic itself, Low for independent third-party
   corroboration (none obtained this session).
2. **NFL 2026 schedule figures (272 games, 17/team, 2026-09-09 kickoff).** Audit
   finding: the cited media.nfl.com PDF URL failed to resolve. **Route taken: (b)
   weakened.** The underlying figures were retained because multiple independent
   outlets converge on the same numbers in search-result summaries, but the
   confidence label was downgraded from the original Medium/High (which had
   implicitly assumed the primary source had been verified) to Low-Medium, and the
   Source Table and Section 2/3 text now state plainly that no direct retrieval
   succeeded this session.
3. **CFB FBS 2025 team-count figure (~134–136 teams).** Audit finding: the cited
   Wikipedia URL failed to resolve. **Route taken: (b) weakened further /
   reinforced existing caveat.** This was already flagged in the original memo as
   a derived, uncited estimate; that status is preserved and made more explicit,
   with confidence downgraded to Low and an explicit statement that the source
   could not be verified this session.
4. **BenchLM.ai Claude API pricing aggregator citation.** Audit finding: this URL
   is blocked and was already flagged in the memo as needing cross-check; no
   correction to the underlying claim was demanded. **Route taken: (b) note added.**
   The Source Table now states explicitly that this source could not be
   re-fetched/re-verified in this correction round, reinforcing (not replacing)
   the original caveat that it should not be treated as independently confirmed.
5. No citations were found where a retrieved source contradicted or failed to
   support its associated claim (the audit's "citations whose source does not
   support the claim" category returned no actionable items for this memo).

**What was not changed:** all work-breakdown estimates, the risk register content
and structure, the phased build plan (goals, deliverables, exit criteria, and
kill-gates), the tech stack recommendations, and the compute/cost estimates are
unchanged from the original memo — none of those rested on the flagged citations.
