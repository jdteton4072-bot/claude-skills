# Predictive Edge Memo — NFL / CFB Spreads & Totals

**Author:** Quantitative Research Lead
**Date:** 2026-09-05
**Question owned:** Has any statistical, ML, or LLM/RAG approach ever demonstrated real, sustained closing-line value against NFL or CFB spreads and totals — and if so, from what?

---

## Bottom Line

1. **My single best estimate: a genuine, durable forecasting edge against NFL/CFB *closing* lines is unlikely but not impossible for a solo builder — I put ~20-30% on the true edge being materially positive (≥ +0.25 pts of mean CLV), ~35-45% on it being indistinguishable from zero, and the remainder on a small positive edge that exists but is too small or too capacity-constrained to be a business.** The strongest single piece of evidence is that closing lines dominate every published independent forecasting system that has been tested against them (Fair & Oster 2007 for CFB; Boulier & Stekler 2003 for NFL), and that the recent methodological literature (Winkelmann et al., *JSE* 2024) shows most published "inefficiencies" are consistent with sampling noise.

2. **There is no credible published evidence — none — that an LLM or RAG system produces closing-line value against NFL or CFB point spreads or totals.** The nearest evidence is adjacent and uniformly negative: on KellyBench (arXiv 2604.27865, Apr 2026) every one of 8 frontier models lost money over a full simulated EPL season (mean ROI -89.6% to -7.9%); on a contamination-free 104-match World Cup 2026 benchmark (arXiv 2607.17765) **none of four frontier agents beat the bookmaker's Brier score**; ForecastBench (ICLR 2025) shows LLMs still below superforecasters on general forecasting. Treat "LLM predicts spreads" as an unvalidated hypothesis, not a head start.

3. **The load-bearing arithmetic: to distinguish a true 54% ATS rate from the 52.38% breakeven at p<0.05 one-sided with 80% power requires ~5,870 bets** (~2,570 for a coin-flip 50% chance of detection; ~16,200 if you Bonferroni-correct for 100 tested strategies). That is ~20 NFL seasons betting every spread, ~6.6 CFB seasons betting every spread, or ~2.5 seasons betting all four markets in both sports with zero selectivity. **Win-rate backtesting cannot resolve this question on any business-relevant timescale. CLV can — the same power at ~70 bets.** CLV is not a nice-to-have metric; it is the only feasible one.

4. **The residual inefficiency that plausibly exists is mostly not "better forecasting."** Ranked by plausibility: (a) line shopping / best-number capture — real, mechanical, worth roughly the size of the vig, but capacity-capped by account limiting; (b) CFB low-liquidity and derivative markets (team totals, alternate lines) where the only peer-reviewed post-2020 result showing a >55% strategy lives (Arscott, *JSE* 2023, CFB team totals, ~2 decades); (c) early-week number-taking; (d) injury/weather latency, which is a speed game measured in seconds, not a modeling game. **Every one of these is capacity-constrained by account limiting, which is a first-order business constraint, not a footnote** — Kaunitz et al. (2017) had every bookmaker account limited or closed within months despite a documented +€1,974 real-money profit.

5. **The structural change worth flagging: CFTC-regulated prediction markets (Kalshi, Polymarket) now list NFL and CFB spreads and totals at scale (~$3.5B NFL, ~$3.1B CFB notional through 2026) and do not limit winning accounts.** This materially changes the capacity picture versus a 2019-era analysis — it removes the limiting constraint but replaces it with a tighter, exchange-priced market and explicit fees. Confidence: Medium (industry-reported volumes, not audited).

---

## 0. Sourcing caveat — read this first

**WebFetch was blocked by this session's egress policy for arxiv.org, journals.sagepub.com, link.springer.com, semanticscholar.org, and every other domain I attempted.** I could therefore verify citations only through search-engine result summaries, not primary text. Consequences:

- Author/year/venue/journal metadata is High confidence (multiply corroborated across indexes: RePEc, EconPapers, IDEAS, publisher landing pages).
- **Specific numeric results quoted below are Medium confidence at best** unless flagged otherwise, because I could not read the papers' tables. Any number in this memo that will be used to size a bet must be re-verified against the PDF before it drives a decision.
- I have flagged each finding's confidence explicitly. Where I could not confirm whether a result was measured against the opening or the closing line, **I say so, and that omission is itself a finding** — a large fraction of this literature does not distinguish, which is why the literature systematically overstates exploitable edge.

---

## 1. The arithmetic that governs everything

### 1.1 Sample size to detect a 54% edge

One-sided test of H₀: p = 0.5238 against H₁: p = 0.54.

n = [ (z_α·√(p₀(1−p₀)) + z_β·√(p₁(1−p₁))) / (p₁ − p₀) ]²

√(0.5238 × 0.4762) = 0.49943  √(0.54 × 0.46) = 0.49840  Δ = 0.0162

| Power | z_β | Numerator | n |
|---|---|---|---|
| 50% (coin-flip chance of detecting a real edge) | 0 | 1.645(0.49943) = 0.82156 | **2,572** |
| 80% | 0.8416 | 0.82156 + 0.41946 = 1.24102 | **5,869** |
| 90% | 1.2816 | 0.82156 + 0.63875 = 1.46031 | **8,125** |
| 80%, Bonferroni for 100 strategies tested (α = 0.0005, z = 3.29) | 0.8416 | 1.6431 + 0.41946 = 2.06256 | **16,210** |

### 1.2 Converting that to seasons

Approximate annual bettable inventory (2026 seasons):

- NFL: 272 regular-season + 13 postseason = **285 games**; spreads + totals = **570 wagers/season**.
- CFB FBS: 138 FBS teams × 12 games ÷ 2 ≈ 830 regular-season games involving an FBS team, + ~10 conference championships + ~43 bowls + ~11 CFP ≈ **~890 games**; spreads + totals ≈ **1,780 wagers/season**. (My arithmetic; team count from the 2026 FBS season listings. Medium confidence on the exact total; the order of magnitude is right.)

| Betting universe | Wagers/season | Seasons to n=5,869 (80% power) |
|---|---|---|
| NFL spreads only, every game | 285 | **20.6** |
| NFL spreads + totals, every game | 570 | **10.3** |
| CFB spreads only, every game | ~890 | **6.6** |
| CFB spreads + totals, every game | ~1,780 | **3.3** |
| Both sports, both markets, every game | ~2,350 | **2.5** |
| Both sports, both markets, selective (bet 20% of board) | ~470 | **12.5** |

**Implication.** A model that is selective — which every real model is — cannot be validated on win rate within a decade. Any vendor or backtest claiming to have "proven" a 54-56% edge on a few hundred or few thousand bets has proven nothing at conventional significance. This single fact invalidates the great majority of the industry's edge claims and a meaningful fraction of the academic ones.

### 1.3 Why CLV is the gold standard — and the arithmetic that makes it so

Two arguments, one theoretical and one statistical. **The statistical one is the strong one and I want to foreground it, because the theoretical one is over-cited and under-evidenced.**

**Theoretical.** The closing line is the market's consensus forecast after the maximum amount of information and capital has been applied to it. The empirical support: closing lines are near-unbiased and dominate independent forecasting systems. Fair & Oster (*Journal of Sports Economics*, 2007) found that **no college football ranking system — nor the optimal weighted combination of all of them — contained information not already in the final Las Vegas point spread**, which they characterise as a strong test of CFB market efficiency. Boulier & Stekler (*International Journal of Forecasting*, 2003, NFL 1994-2000) ranked forecasters and concluded **the betting market was the best predictor**, ahead of probit models on published power scores, ahead of expert judgment, ahead of naive models. Štrumbelj (*IJF*, 2014) showed odds-implied probabilities (with Shin de-vigging) are accurate probability forecasts. Confidence: **High** on the direction; Medium on the specific magnitudes since I could not read the tables.

**Statistical — this is the load-bearing part.** Win/loss is a Bernoulli observation with variance ≈ 0.25 against a signal of ~0.016. CLV is a near-continuous observation. Suppose your bets beat the close by a mean of +0.30 points with a cross-bet SD of 1.0 point (a realistic dispersion for a systematic bettor taking numbers 1-4 days early). One-sided test of mean CLV > 0:

n = [(1.645 + 0.8416) × 1.0 / 0.30]² = (2.4866/0.30)² ≈ **69 bets** for 80% power.

**~70 bets versus ~5,870 bets for the same statistical conclusion.** That ratio — roughly 85× — is why every serious operator, and every sportsbook's risk desk, evaluates on CLV. It is also why sportsbooks limit on CLV rather than on P&L: they reach a confident verdict about you far faster than your own P&L does. Confidence: **High** (this is my own arithmetic; the inputs are assumptions, the conclusion is robust to them across any plausible range).

**Where the CLV-predicts-profit literature is weak, and I want to be honest about it.** The claim "CLV predicts long-run profitability" is asserted constantly by industry sources (Pinnacle, Unabated, VSiN, Buchdahl's work) and I could find **no peer-reviewed study that establishes it with a large sample of individual bettors' records.** Joseph Buchdahl's analyses are the most rigorous public work and are widely cited — including his claim that beating the close by 10% yields ~10% return over turnover — but they are a practitioner's blog-and-book corpus, not independently replicated, and the specific numeric claims returned by search (e.g., "closing lines explain ~86% of outcome variability", "50 bets suffices at a 5% edge") appeared only in secondary vendor write-ups that I could not trace to a primary methodology. **Treat "CLV predicts profit" as: near-certain on theory and arithmetic, thinly evidenced on direct empirics.** Confidence: **Medium-High** for the proposition, **Low** for any specific published coefficient.

### 1.4 The exchange rate: points of CLV ↔ ATS percentage points

NFL closing-spread error has a standard deviation of ~13.2 points (industry analysis across 7,276 games with a closing line, reporting mean error +0.09 points — essentially unbiased; nfelo). This matches Stern's classic estimate of ~13.86 from 1981/83/84 seasons. Marginal win probability per point of line near a fair number:

φ(0)/σ = 0.3989 / 13.2 = **3.02 percentage points of win probability per point of spread (NFL)**

CFB is more dispersed; published σ estimates I found range from ~14 to ~21 depending on era and sample (Sides & Harvill, arXiv 2212.08116, 2022, use season-specific σ; one 2021-season fit used 21). Taking σ ≈ 16: **~2.5 pp per point (CFB)**. Confidence: **Medium** — the CFB σ is genuinely unsettled across sources and needs original estimation.

Therefore:

| Target | NFL CLV required | CFB CLV required |
|---|---|---|
| Break even at −110 (52.38%) | **+0.79 points** | **+0.95 points** |
| 54% ATS | **+1.32 points** | **+1.60 points** |
| Break even at −105 (51.22%) | +0.40 points | +0.49 points |

**This is the most sobering number in the memo.** Betting *at* the closing number wins ~50% and loses the vig. To merely break even you must beat the close by roughly **three-quarters of a point on average, on every bet**. Getting +3.5 instead of +3 once is not enough; you must average that. Note the exception: these are non-key-number conversions. Crossing NFL 3 is worth far more (~9-10 pp) and crossing 7 ~5-6 pp because of push mass, which is precisely why key-number capture is where the mechanical edge concentrates.

---

## 2. Baseline: how efficient are these markets?

### 2.1 NFL

**The closing line is a well-calibrated, near-unbiased forecast.** Mean error ≈ +0.09 points over 7,276 games with σ ≈ 13.2 (industry, Medium confidence). Levitt (*Economic Journal*, 2004, "Why are gambling markets organised so differently from financial markets?", 20,000+ bets from a 2002-season NFL handicapping contest) established the structural reason: bookmakers do not balance books; they take positions, are **better forecasters than their bettors**, and set prices deliberately away from market-clearing to exploit bettor bias. Confidence: **High** on the paper's existence and thesis; the specific contest sample I could not re-verify from the PDF.

Levitt's finding has an underappreciated consequence for this project: **the book's number is not a naive prior you are improving on. It is a skilled forecast produced by a party with more information than you, deliberately shaded.**

Closing lines are also measurably better than openers: one thesis-level analysis reports closing spreads picked the correct winner 65.9% of the time vs. 63.5% for openers (Greer 2021, cited via secondary source — **Low confidence**, unverified thesis). Spinosa (2014, CMC thesis, NFL 1992-2012, 21 seasons) concluded the closing line is efficient in aggregate. Confidence: **Medium** (thesis-grade, not peer-reviewed).

**Dissent exists and should not be dismissed.** Shank (*Journal of Economics and Finance*, 2018, "Is the NFL betting market still inefficient?", 2009-2017) reports home underdogs — particularly large ones and those on losing ATS streaks — are undervalued, and that **both the spread and totals markets are statistically inefficient**. Ramesh, Mostofa, Bornstein & Dobelman (arXiv 1910.08858, 2019) claim above-market returns for NFL, NBA, NCAAF, NCAAB and WNBA using a non-parametric win-probability model. **Neither states clearly, in what I could verify, whether the results were measured against opening or closing lines, or whether vig was deducted in the reported figures — that omission is the finding.** Confidence in these as *exploitable* edges: **Low**.

### 2.2 Is college football measurably less efficient?

**This is the most decision-relevant question in the memo for the business case, and the honest answer is: the academic evidence is mixed and does not cleanly support "CFB is softer", but the market-microstructure evidence does.**

**Evidence that CFB is efficient:**
- Fair & Oster (*JSE*, 2007): no ranking system, alone or optimally combined, adds information beyond the final Vegas spread. This is a strong efficiency result and it is *about CFB specifically*. Confidence: **High**.

**Evidence that CFB is inefficient:**
- **Arscott, "Market Efficiency and Censoring Bias in College Football Gambling," *Journal of Sports Economics* 24(5): 664-689, 2023.** Team totals and spreads jointly imply team scores; scores are censored at zero, which biases the market's implied predictions. A naive strategy using **only information contained in the two posted lines themselves** wins **>55% over the past two decades**. This is the single most credible post-2020 published CFB edge claim I found: peer-reviewed, recent, mechanism-based (not data-mined), and it lives in a **derivative market (team totals)**. Confidence: **Medium-High** for the claim as published; **Medium** for its persistence and executability today (the paper's sample ends before the market-wide sharpening of the post-2018 legalisation era, and team-total limits are small). **I could not verify whether the lines used were closing or opening.**
- Sinkey & Logan (*Eastern Economic Journal*, 2013), "Does the Hot Hand Drive the Market?", >11,000 CFB games 1985-2003: market is inefficient after stripping common behavioural strategies. Confidence: **Medium**; sample is old.
- Bennett (*Atlantic Economic Journal* 47:103-110, 2019), "Holdover Bias": prior-season AP top-10 teams are significantly overvalued in their **first game of the following season**; betting against them beats 52.4% significantly, **especially against non-Power-5 opponents**. Teams ranked 11-25 show no such effect. Sample: 2008-2016 seasons. Confidence: **Medium-High** as published — but note the mechanical capacity limit: this is roughly **10 bets per season**. At 10 bets/year it would take centuries to validate independently (§1.1). This is a real, well-motivated bias with essentially zero business capacity.
- "College football and the Vegas line: Deconstruction and arbitrage" (*Journal of Prediction Markets*), 4,590 games 2005-2011: betting the top 35% most-mispriced games yielded **55% correct picks and 2.7% APY**. Note that 2.7% annual return is *below* what the authors' own selection implies is needed to be a business, and 55% on a ~1,600-bet subsample is at the edge of significance. Confidence: **Medium** on the paper, **Low** on exploitability.
- Berkowitz, Depken & Gandar (via *Journal of Economics and Business* / secondary): favorite-longshot bias documented in college football and college basketball **money-line** markets, persisting through their sample — in contrast to MLB/NHL where the reverse bias appears. Confidence: **Medium**. Note this is money-line, not spread, and is not directly monetisable at scale.

**Structural argument (not from the academic literature):** CFB has ~890 games versus the NFL's 285, spread across a far wider talent and information gradient, with sportsbook limits on Group-of-Five, FCS and "added" games materially below FBS-marquee limits, and with sharp capital concentrated on the highest-limit games. Sportsbooks historically excluded pure FCS matchups from the main rotation and treat FBS-vs-FCS as low-limit added games. **The inefficiency is real but it is inversely proportional to the limits.** This is the core tension of the CFB thesis: the soft games are soft *because* nobody can bet enough into them to make them hard.

**Verdict on CFB:** Medium confidence that residual per-game inefficiency in low-tier CFB exceeds NFL by a meaningful margin. **High confidence that the dollar capacity of that inefficiency is far smaller than its percentage size suggests.** These are different findings and the business case depends on the second one.

### 2.3 Documented biases — and whether each survived publication

| Bias | Original finding | Survived publication? | Confidence |
|---|---|---|---|
| **Home-underdog bias (NFL)** | Home dogs 58.1% ATS 1973-79; Gray & Gray (*Journal of Finance* 52:1725-1737, 1997) probit on 1976-1994 found home dogs undervalued and in-sample profits significant | **Largely decayed.** Reported win rate falls 58.1% (1973-79) → 52.5% (1981-96) → 53.5% (2002-11). Gray & Gray themselves found out-of-sample results inconsistent. Shank (2018) revives it for 2009-2017 for *large* home dogs specifically; other post-2010 replications contradict. | **High** that it decayed; **Low** that any residual is exploitable |
| **Favorite-longshot bias (CFB/CBB money lines)** | Berkowitz/Depken/Gandar, college football + basketball money lines | **Persists in sample** per authors; note it is a *pricing* regularity in long odds, hard to monetise net of vig, and does not transfer to spreads | Medium |
| **Overs overbet / bettor preference for scoring** | Paul & Weinbach (*JSE* 3:256-263, 2002), NFL totals 1979-2000: contrarian "under" on totals 5-7+ points above the mean violates a fair bet; extended to CFB and arena football | **Partially survived as a *preference* finding, not as a *profit* finding.** Later work (Paul & Weinbach 2011) found a profitable contrarian rule on *spreads* at >70% public-on-favorite but **explicitly did not find one in the over/under market.** | Medium |
| **Prior-season top-10 holdover (CFB)** | Bennett (2019), 2008-2016 | Not yet retested post-publication; ~10 bets/season capacity | Medium-High on the finding, Low on capacity |
| **Score censoring at zero (CFB team totals)** | Arscott (*JSE*, 2023), ~20 years | Published 2023 — **too recent to know.** This is the one to test first. | Medium-High |
| **Weather under-adjustment on totals** | Borghesi, "Weather biases in the NFL totals market", *Applied Financial Economics* 18(12), 2008 (5,008 games, 1984-2004): bettors underestimate heat, wind and rain; out-of-sample strategy beat 52.38% significantly | **Unclear/likely decayed.** Sample ends 2004 — before commodity weather APIs, before books priced weather algorithmically. I found no post-2015 peer-reviewed replication. | Medium on the original; **Low** on current exploitability |
| **Reverse line movement (CFB totals)** | Francisco & Moore, *Journal of Economics and Finance* 43:813-827, 2019, all CFB totals Sept 2005-Jan 2016 | **Refuted.** Following RLM is **not** profitable on CFB totals; the authors find a weak signal in betting *against* RLM in a 16-20% under subset. | Medium-High |
| **"Fade the public"** | Paul & Weinbach (2007, 2011) spreads at extreme public percentages | Survives weakly and conditionally in the academic literature; **the widely-circulated 63%+ figures are vendor claims and should be rejected outright** (see §2.4) | Medium (academic), Low (vendor) |

**The meta-finding, and it is the most important one in this section:** Winkelmann, Ötting, Deutscher & Makarewicz, "Are Betting Markets Inefficient? Evidence From Simulations and Real Data," *Journal of Sports Economics* 25(1): 54-97, 2024 — simulate efficient markets and show that **inefficient-looking periods appear routinely inside genuinely efficient markets at realistic sample sizes**, then analyse 14 seasons of real football markets and find inefficiencies occur in singular seasons but are **not persistent or systematic**. This is exactly §1.1 restated by professionals, and it is the correct prior for reading every entry in the table above. Confidence: **High**.

---

## 3. What has actually worked — evidence review

### 3.1 The one well-documented real-money case, and what it actually teaches

**Kaunitz, Zhong & Kreiner, "Beating the bookies with their own numbers — and how the online sports betting market is rigged," arXiv:1710.02824 (Oct/Nov 2017).** Soccer, not football, but it is the most methodologically honest real-money study in the literature and its lessons are sport-agnostic.

- **Mechanism: not superior forecasting.** They built no competing model. They took the *consensus* of the odds market and bet where an individual bookmaker's price was an outlier against consensus. This is **odds-arbitrage against the market's own information**, i.e., a line-shopping/mispricing strategy.
- Validated three ways: 10-year historical simulation on closing odds; 6-month minute-to-minute simulation; and **5 months of real money staked with real bookmakers**, returning approximately **+€1,974 profit on 265 real bets**.
- **And then every account was limited or closed.** The paper's subtitle — "how the online sports betting market is rigged" — is precisely about this. The strategy worked; the business did not.

**This is the single most transferable result in the memo.** It says: (i) the demonstrable public edge came from *market microstructure*, not from forecasting; (ii) real-money validation is achievable at a few hundred bets *if you measure the right thing*; (iii) **account limiting, not model quality, was the binding constraint.** Confidence: **High** (open data, open code, widely cited, and I corroborated the design and the limiting outcome across multiple indexes; the exact profit/bet figures are **Medium** since I could not read the PDF).

### 3.2 Syndicates — sharply distinguishing the mechanisms

The mechanisms below have wildly different transferability to a solo builder. Note that essentially all of this is **journalism, memoir, and secondary reporting, not independently verified** — Billy Walters' own book is a self-reported source with obvious incentives. Confidence: **Low-Medium** throughout on specifics, **High** on the qualitative taxonomy.

| Mechanism | Example | Transferable to a solo builder? |
|---|---|---|
| **Distribution / beard networks** — getting size down at many books and shops before lines move | Computer Group; Walters | **No.** Requires headcount, capital, and relationships. This was arguably Walters' *actual* edge, more than the model. |
| **Line origination / market-making** — being the price-setter and earning the spread | Modern market-making books and their partner quant shops | **No.** Requires being a book. |
| **Speed / latency on news** | Modern injury-news bots | **Marginal.** The window on major NFL injury news is reported at 30-60 seconds before lines are pulled (industry sources, Medium confidence). This is an infrastructure race against funded competitors, not a research problem. |
| **Genuine superior forecasting in an under-modelled niche** | Voulgaris on NBA coach substitution patterns and 1H/Q4 totals | **Yes in principle** — and note it was a *derivative market* (halves/quarters), not the full-game side. That pattern recurs. |
| **Correlated / structural pricing errors** | Arscott's CFB team-total censoring; the CFB same-game-parlay correlation result (JPM, 2005-2015: favorites covering correlate with the over; books historically refused these parlays and thereby *forwent* profit) | **Yes** — this is the most solo-accessible category, and it is where I would look first. |
| **Stale-line / cross-book arbitrage** | Kaunitz et al. | **Yes, mechanically** — but see limiting. |

**Note what is absent from this table: nobody's documented, verified edge came from "we had a better regression on team quality."**

### 3.3 Modeling approaches with claimed edge

| Approach | Best evidence | Measured vs. close? | Out-of-sample? | Vig deducted? | Verdict |
|---|---|---|---|---|---|
| **Published power ratings / Elo** | Fair & Oster (2007, CFB): optimal combination of all ranking systems adds **nothing** beyond the final Vegas spread. Boulier & Stekler (2003, NFL 1994-2000): market > power-score probit > expert > naive. Hvattum & Arntzen (2010): Elo performs well for its simplicity but is **outperformed by betting odds**. | Yes (final/closing spread) | Yes | N/A (they lose before vig) | **Negative result. High confidence.** Elo and public power ratings do not beat the close. |
| **Probit/logit on team form** | Gray & Gray (*J. Finance*, 1997), NFL 1976-1994: significant **in-sample** profits; out-of-sample "some inconsistency" | Unclear — likely closing Vegas spread, unverified | Partially | Reported as profitable vs. −110 | **Historical, decayed.** Medium confidence the in-sample result was real; Low that it survives. |
| **Gradient boosting / RF / NN on engineered features** | Galekwa et al., arXiv 2410.21484 (Oct 2024), systematic review of ML in sports betting | Review notes profitability claims across soccer/basketball/tennis/cricket, but flags data quality, real-time decisioning and inherent unpredictability as unresolved | **The review does not establish that any surveyed model was validated against closing lines with vig deducted.** | Mixed/unstated | **Insufficient evidence. Medium confidence in the review's existence, Low in any positive profitability inference from it.** |
| **CNN + decorrelation from bookmaker odds + portfolio sizing** | Hubáček, Šourek & Železný, *International Journal of Forecasting* 35(2):783-796, 2019 (NBA) | Peer-reviewed in a top forecasting journal; the key insight is that **maximising accuracy is the wrong objective — you must maximise *decorrelation* from the bookmaker's forecast.** | Yes, out-of-sample | Yes | **The most important methodological result for this project even though it is the wrong sport.** High confidence in the insight; Medium in the profit magnitude; **not replicated for NFL/CFB.** |
| **Bayesian state-space / hierarchical** | Lopez, Matthews & Baumer, *Annals of Applied Statistics* 12(4):2483-2516, 2018 — Bayesian state-space models **built on betting-market data** across NFL/NHL/NBA/MLB | The models *ingest* market data as the signal rather than competing with it. NFL has among the highest game-to-game randomness of the four leagues. | N/A — not a betting study | N/A | **Supports the baseline, not an edge.** High confidence. The NFL's high per-game variance is a structural reason edges are hard to detect. |
| **Non-parametric win-probability** | Ramesh et al., arXiv 1910.08858 (2019), claims above-market returns for NFL/NCAAF | **Not established as vs. closing line** in what I could verify | Claimed | Unclear | **Low confidence. Treat as unvalidated.** |

**The Hubáček insight deserves its own line because it reframes the whole modelling problem:** your model's value is not its accuracy but its *residual* information after conditioning on the closing line. A model with worse standalone RMSE than the market can still be profitable if its errors are uncorrelated with the market's; a model with better RMSE that is 0.99-correlated with the close is worthless. **Every model this team builds should be evaluated by regressing outcomes on (closing line, model prediction) and testing whether the model coefficient is non-zero — not by its standalone accuracy.**

### 3.4 Totals specifically: more or less efficient than spreads?

**Mixed, leaning "the totals market has a documented behavioural bias but no reliable surviving profit strategy."**

- Kain & Logan, "Are Sports Betting Markets Prediction Markets?", *JSE* 15(1):45-63, 2014, proposed testing spreads and totals jointly on the logic that if both are prediction markets both must be predictive. Their finding (as widely cited): **spreads behave as good predictors of outcomes; the over/under is a comparatively poorer predictor of total points.** Confidence: **Medium** — I could not verify the exact test statistics and this result is frequently paraphrased loosely.
- Paul & Weinbach (*JSE*, 2002; NFL totals 1979-2000) document skewed forecast errors and a contrarian "under" rule on high totals that violates a fair bet. But **their own later work failed to find a profitable contrarian rule in the totals market** where they did find one in spreads (2011).
- Francisco & Moore (*JEF*, 2019, CFB totals 2005-2016): RLM-following on totals is **not** profitable. Clean negative result.
- Arscott (*JSE*, 2023): the >55% strategy is in CFB **team** totals, exploiting censoring — i.e., in a *derivative* of the totals market, not the main total.
- Weather: Borghesi (*Applied Financial Economics*, 2008; 5,008 NFL games 1984-2004) is the canonical under-adjustment finding, with a reported out-of-sample strategy beating 52.38%. **I found no peer-reviewed post-2015 replication.** The commonly cited "20+ mph wind games average 2.7 fewer points" is an industry statistic without a stated sample or significance test — treat as directional colour, not evidence. My prior: books now ingest the same NOAA/ECMWF feeds you would, and the 2004-era edge is mostly gone; the residual, if any, is a **latency** edge on forecast revisions (Tuesday-Thursday), not a **modelling** edge. Confidence: **Medium-Low**, and this is a genuinely testable question — it is on my open-questions list.

**Net:** the main-market total is not obviously softer than the spread. **The derivative totals (team totals, alternates) plausibly are, and that is where the only recent peer-reviewed CFB edge claim sits.**

### 3.5 Explicitly rejected: vendor and tout claims

The following surfaced in search and should be **rejected**, not discounted:
- "Underdogs cover 63.8% when receiving <40% of public bets," "fading the most popular public sides wins 63.3%." No stated sample, period, book, line timestamp, or vig treatment; magnitudes are implausible on their face (a 63% ATS edge would be worth billions and would not survive a week); and they are published by betting-content sites with affiliate incentives. **Survivorship-biased self-report. Zero evidentiary weight.**
- "Professional models achieve 52-55% ATS, 55-60% on moneylines" — plausible-sounding, but circulating without sourcing. Do not anchor on it.
- "Our CFB model is 32-19 on money-line picks since 2024." 51 bets. See §1.1. **This is noise presented as a track record.**
- "LLMs predicting point spreads have claimed accuracy levels of 72-77%." Traced only to a secondary blog; the same blog correctly notes these came from **backtesting, not live prediction** — which, for an LLM, is precisely the contaminated regime (§4.2). **Reject.**

---

## 4. LLM / RAG-specific evidence — the crux

### 4.1 What exists

**There is no credible published evidence that an LLM or RAG system produces closing-line value against NFL or college football point spreads or totals.** I searched arXiv indexes, benchmark literature, and industry write-ups. Nothing. That is the honest answer and I am not going to fill the gap with reasoning.

What *does* exist is adjacent, recent, and consistently negative-to-neutral:

| Source | Date | Sport/domain | Finding | Confidence |
|---|---|---|---|---|
| **KellyBench: A Benchmark for Long-Horizon Sequential Decision Making**, arXiv 2604.27865 | Apr 2026 | 2023/24 EPL season, real market odds, Kelly sizing | **Every one of 8 frontier models lost money on average over 5 seeds.** Mean ROI −89.6% (Kimi K2.5) to **−7.9% (GPT-5.4, best)**. Only 3 of 25 model-seeds finished positive, all negative when averaged across seeds. Best model's seed range −32.9% to +34.1%. Authors identify a "knowledge-action gap." | **High** (widely reported, arXiv + press coverage) |
| **FIFA World Cup 2026 as a Contamination-Free Benchmark for LLM Forecasting Agents**, arXiv 2607.17765 | Jul 2026 | All 104 WC2026 matches; every match after all models' training cutoffs | Claude Opus 4.8, GPT-5.5, Gemini 3.1 Pro, Grok Expert vs. the pre-match betting market. **Agents issued an identical top pick in 92% of matches. None beat the market's Brier score.** Betting ROI ranged −18% to +10%; self-reported error rates on wrong picks 36-86%. | **High** |
| **LLM-SoccerArena**, arXiv 2607.24573 | Jul 2026 | Prospective live soccer forecasting, 7 LLMs, 104 matches | **"Bookmaker probabilities provide a strong external baseline that is often hard to beat."** Web access improves Brier by only **0.023**. Betting markets remain difficult for LLM systems to beat consistently. | **High** |
| **ForecastBench**, Karger et al., ICLR 2025 (arXiv 2409.19839) | 2024-25 | General real-world forecasting, 17 LLMs | LLMs (~0.122 Brier with crowd access) below **superforecasters (0.096)** and roughly at the general public (~0.121). | **High** |
| **Approaching Human-Level Forecasting with LMs**, Halawi et al., NeurIPS 2024 (arXiv 2402.18563) | 2024 | General forecasting, retrieval-augmented | RAG system Brier **0.179 vs. crowd 0.149**; accuracy 71.5% vs. 77.0%. **Beats the crowd only in a *selective* setting** where the system chooses when to forecast. This is the strongest pro-LLM result and it still does not beat the crowd unconditionally. | **High** |
| **Pitfalls in Evaluating Language Model Forecasters**, Paleka, Goel, Geiping & Tramèr, arXiv 2506.00723 | May 2025 | Methodology | Two failure classes: temporal leakage (including **logical leakage** — retrodiction questions whose answers are deducible from the framing) and non-extrapolability from benchmark to real-world performance. Shows a significant share of questions in prior forecasting benchmarks permit deduction of the answer. | **High** |
| **NFL Arena** (Recall, industry blog) | 2025-26 | NFL, Thanksgiving slate, 6 LLMs | LLMs unanimously picked KC, BAL, DET; all three lost. "If they were making pregame bets, they would have lost money." | **Low** — n≈3 games, industry blog, but it is the only NFL-specific LLM datapoint I found, and it is negative |

**The pattern across every prospective, contamination-free evaluation is the same: LLMs cluster on the consensus, do not beat the market's calibration, and lose money when forced to size bets.** Confidence in that pattern: **High**.

### 4.2 Failure modes for an LLM as a point-spread predictor

**(a) Training-cutoff contamination — treat this as a first-order backtest-validity threat, not a caveat.** Any NFL/CFB game before the model's cutoff is in its training data — box scores, recaps, betting previews, and post-game analysis are all heavily represented on the open web. A backtest over 2015-2024 NFL games is not measuring forecasting; it is measuring recall, partially and unevenly. This produces the specific signature Paleka et al. and the contamination literature describe: a *cliff* at the cutoff date. **Practical consequence: any backtest of an LLM component on pre-cutoff games is uninterpretable and should not be run at all, let alone reported.** The only valid LLM evaluation is prospective, on games that kick off after the model version's cutoff, with the model version pinned. This alone reduces the usable evaluation window for a 2026 build to roughly one season per model generation — which, per §1.1, is nowhere near enough for win-rate inference and just barely enough for CLV inference.

**(b) Consensus collapse.** The WC2026 benchmark's 92% identical-top-pick rate is the crux for a product. An LLM's prior is the internet's prior, and the internet's prior is roughly the market's prior. **A model whose output is 0.95-correlated with the closing line has, by Hubáček's argument, no value regardless of its accuracy.** This is the mechanism by which an LLM system can be "right a lot" and worth nothing.

**(c) Miscalibration and arithmetic on margins.** LLMs are trained toward plausible text, not toward proper scoring. Converting "I think Michigan is a bit better than the market thinks" into a defensible number of points, then into a win probability against a 13-16 point σ, then into a Kelly fraction, requires precise arithmetic on small probability differences — the regime where LLMs are least reliable and where a 1.6 pp error is the entire edge.

**(d) Prompt-framing sensitivity and non-determinism.** KellyBench's seed variance for the *best* model was −32.9% to +34.1% — a 67-point ROI spread from seed alone, over a full season. **A system whose season outcome depends this heavily on the seed cannot be backtested to a conclusion**, and it means a "good backtest" is very likely a lucky seed. This is not a tuning problem; it is a fundamental obstacle to statistical validation.

**(e) The knowledge-action gap.** KellyBench's own framing: models often articulate correct reasoning about edge and bankroll and then act inconsistently with it.

### 4.3 What is genuinely unknown

- Whether an LLM used **narrowly** — as a structured-information *extractor* (injury reports, beat-writer reporting, weather narratives, coaching-change context) feeding a conventional statistical model — adds residual signal beyond the closing line. **This has not been tested publicly for NFL/CFB.** It is a materially different and more plausible hypothesis than "LLM predicts the spread," and it is the one worth testing. Note it is also the one where the LLM's contribution is hardest to isolate from the underlying data feed's.
- Whether the *selective* forecasting regime that worked in Halawi et al. (forecast only when confident) transfers to a market with a −110 hurdle. Untested.
- Whether LLM systems can beat the market specifically in **low-liquidity CFB** games, where the market's own information is thinner and an LLM's broad recall of a Sun Belt team's transfer-portal churn might genuinely exceed the local price. **This is the most interesting untested question in the whole memo** and it is also, not coincidentally, the lowest-capacity one.

---

## 5. Where residual inefficiency most plausibly lives — ranked, with capacity

Capacity is an integral part of the edge estimate, not a footnote. An edge you cannot bet is not a business.

**1. Line shopping / best-number capture across books and exchanges.**
- *Mechanism:* Mechanical. Take the best available number and price at bet time. Sharp books average ~2.7% hold on NFL spreads vs. ~5%+ retail (industry, 2007-2022, ~149k games — **Medium confidence, no methodology published**).
- *Size:* Roughly **0.3-0.8 points of CLV** on NFL spreads for a disciplined shopper across 6+ outlets — i.e., **roughly the size of the vig, or ~1-2.5 ATS points.** Larger when it crosses a key number.
- *Evidence:* Kaunitz et al. (2017) is the peer-adjacent proof that this mechanism, alone, generated real-money profit. **High confidence this is real.**
- *Capacity:* **This is where it dies.** Kaunitz's accounts were limited or closed within months. Retail books limit on CLV, not P&L, and reduce max stake quietly (industry reports of £500 → £50). Sharp books (Pinnacle, Circa) and exchanges do not limit but their prices *are* the sharp price, so the shopping edge against them is near zero. **Realistic sustainable capacity for a solo operator across retail books: low four figures per game before limiting, declining over months.** Prediction markets (Kalshi/Polymarket) do not limit and now carry ~$3.5B NFL / ~$3.1B CFB notional (industry-reported, Medium confidence) — this is the meaningful 2026 change, but their prices are sharp and fee-laden.

**2. CFB derivative markets — team totals and alternate lines.**
- *Mechanism:* Structural mispricing from score censoring at zero (Arscott, *JSE* 2023) and from books deriving derivatives mechanically from the main line rather than pricing them independently.
- *Size:* **>55% claimed over ~20 years of CFB.** If real and current, that is +2.6 ATS points over breakeven, or ~1.0-1.3 points of CLV equivalent.
- *Evidence:* One peer-reviewed paper, recent, mechanism-based, not yet independently replicated, sample ends pre-2023. **Medium-High as published; Medium that it survives today.**
- *Capacity:* CFB team totals carry limits typically an order of magnitude below main sides. **Low hundreds to low thousands per market.** Also the most likely market to be pulled or repriced when you hit it repeatedly.
- *This is my #1 recommendation for what to backtest first,* precisely because it has a stated mechanism, a peer-reviewed source, and a falsifiable prediction.

**3. Early-week number-taking (Sunday-night/Monday openers through Wednesday).**
- *Mechanism:* Openers are posted at lower limits and are demonstrably less accurate than closes (65.9% vs 63.5% correct-side, Low confidence source). Taking a number before the market sharpens generates CLV by construction *if* your number is better than the opener.
- *Size:* Plausibly **+0.2 to +0.5 points of CLV** for a model with genuine residual signal; **zero or negative** for a model without it. **This mechanism does not create edge — it amplifies whatever edge you have, in both directions.** A bad model taking early numbers loses faster.
- *Evidence:* Mechanism is well-established; the magnitude for a *specific* model is unknowable ex ante. **Medium.**
- *Capacity:* Low, by design — opener limits are the lowest of the week, and repeatedly hitting openers is the single fastest way to be limited.

**4. Injury-news latency.**
- *Mechanism:* Books pull or move lines within a reported **30-60 seconds** of major NFL injury news; offshore books and deep prop menus are slower, creating stale windows.
- *Size:* Large per-instance (multiple points), tiny in frequency, and requires automated firing.
- *Evidence:* Industry only. **Low-Medium.**
- *Capacity:* Effectively zero for a solo builder without co-located infrastructure and pre-funded accounts. **This is an engineering arms race against funded competitors, not a research edge.** I would not build for it.

**5. Weather-model latency on totals.**
- *Mechanism:* Borghesi's under-adjustment (1984-2004) is likely arbitraged, but forecast *revisions* between Tuesday and Sunday morning may still lead the line.
- *Size:* Unknown today. The 2008 paper's out-of-sample beat of 52.38% is 20+ years stale.
- *Evidence:* **Medium on the historical finding, Low on current exploitability.** No post-2015 replication found.
- *Capacity:* Weather-affected games are few (perhaps 20-40 NFL games/season with meaningful wind), so even a real edge yields ~30 bets/season — unvalidatable per §1.1.

**6. Low-liquidity CFB games (G5, FCS, added games).**
- *Mechanism:* Less sharp capital, thinner information, wider posted numbers.
- *Size:* Plausibly the largest *percentage* edge available anywhere in this scope.
- *Evidence:* Structural/microstructural, not peer-reviewed. Sinkey & Logan and Bennett are consistent with it. **Medium.**
- *Capacity:* **The lowest of any item on this list, and it is low precisely because the edge is high.** Books cap these games specifically because they know they cannot price them. Expect three-figure limits and fast limiting.

**7. Stale correlated markets / same-game correlation.**
- *Mechanism:* The JPM CFB study (2005-2015) documents that favorites covering correlates with the over; books historically refused these parlays, and the paper argues they *forwent* profit by doing so.
- *Evidence:* **Medium on the correlation, and note the paper's own conclusion cuts against the bettor** — books were over-conservative, meaning the parlays they *do* offer are the ones they've priced.
- *Capacity:* Where SGPs are offered they carry heavy correlation-adjusted pricing. **Assume this is closed.**

**8. Superior full-game forecasting of NFL sides via better statistical modelling.**
- *Ranked last deliberately.* Fair & Oster and Boulier & Stekler both find the closing line dominates the best available independent systems, and the NFL is the single most heavily modelled market in sports. **Low confidence any residual exists at solo scale.**

---

## 6. Flagged finding: the evidence points away from main-market sides and totals

Per the manager's standing permission, surfacing rather than suppressing:

**The consistent pattern in the strongest evidence is that documented edges live in *derivatives*, not in main-market NFL/CFB sides and totals.** Arscott's >55% CFB result is in **team totals**. Voulgaris' documented NBA edge was in **halves and quarters**, not full games. The CFB parlay paper is about **correlated derivatives**. Industry consensus (unverified, but internally consistent and mechanistically plausible) is that **player props are the least efficient football market** because sharp capital concentrates where limits are highest — sides and totals — leaving props under-modelled and under-attacked.

**Implication for the product:** a service built exclusively on NFL/CFB main-market spread and total picks is targeting the two most efficient markets in American sports. If the goal is to find edge rather than to sell picks, the evidence says point the research at CFB team totals, alternate lines, and player props. **I flag that this conflicts with the stated scope and defer the product decision — but the manager asked to be told if the evidence redirects the product, and it does.** Confidence: **Medium-High** on the direction, **Low** on any specific prop-market edge magnitude, because I found no peer-reviewed quantification of prop-market inefficiency at all.

---

## 7. Honest expected-value statement

For a competent solo quant — walk-forward discipline, good data, no distribution network, no latency infrastructure — attacking NFL/CFB spreads and totals, after vig, measured against the closing line at a sharp book:

| Outcome | Probability | ATS% (true) | Mean CLV |
|---|---|---|---|
| **Genuinely negative or zero edge** (model adds nothing beyond the close; all apparent edge is noise, overfit, or line-shopping mistaken for forecasting) | **40%** | ≤ 50.0% | ≤ 0 pts |
| **Marginal positive, sub-breakeven** — real residual signal but below the vig hurdle. Profitable only at reduced juice or on an exchange. | **30%** | 50.5-52.4% | +0.1 to +0.75 pts |
| **Small real edge, above breakeven, capacity-limited** — 52.5-54%. Real, but yields low-four-figure to low-five-figure annual profit before limiting, and is unvalidatable within 3 seasons on win rate. | **22%** | 52.5-54.0% | +0.8 to +1.3 pts |
| **Genuine edge, 54-56%** — requires finding a live structural mispricing (Arscott-type) in a derivative market. | **7%** | 54-56% | +1.3 to +2.0 pts |
| **>56% sustained** | **<1%** | >56% | >2.0 pts |

**Point summary: median outcome is ~51.5-52.0% true ATS — i.e., a small real signal that does not clear the vig on main markets.** Probability the true edge is zero-or-negative: **40%**. Probability of an edge large enough to be a *business* on main-market NFL/CFB sides and totals (>54%, sustainable, with capacity): **~5-7%**.

**Justification, not optimism.** The 40% zero-edge mass comes from: Fair & Oster's and Boulier & Stekler's direct negative results against the close; Winkelmann et al.'s demonstration that most published anomalies are sampling artefacts; the decay of the home-underdog bias post-publication; and the total absence of any verified solo-scale success in the literature. The ~29% mass above breakeven comes from: Arscott (2023) surviving peer review with a mechanism-based >55% CFB result; Shank (2018) rejecting NFL efficiency on 2009-2017 data; and the persistent microstructural gap between retail and sharp pricing.

**Two adjustments that matter more than the model:**
- **Line shopping and reduced juice are worth more than most models will ever be.** Moving the hurdle from 52.38% (−110) to 51.22% (−105) cuts the required CLV nearly in half (0.79 → 0.40 points). A mediocre model at a good price beats a good model at a bad price.
- **Exchange access changes the capacity distribution, not the edge distribution.** It removes limiting risk; it does not make you a better forecaster, and exchange prices are sharp.

---

## 8. What the evaluation framework must look like

Pitched at practitioner level. The builder's walk-forward HMM experience transfers directly; the sports-specific traps do not.

### 8.1 Primary metric: CLV, not win rate

Per §1.3, win rate is statistically useless on business timescales and CLV is ~85× more efficient. **Design the entire evaluation around CLV and treat P&L as a secondary sanity check.**

- **Metric:** signed CLV in points (spreads/totals) = (line you took) − (closing line), signed so positive = better than close. Also record CLV in cents on the price where the number is identical.
- **Reference close:** use a single, pre-registered market-making book — **Pinnacle** (or Circa where available) — captured at the **last odds tick before the official scheduled kickoff**, not at kickoff-plus-anything. Never use a retail book's close as the reference; retail closes are shaded and will flatter you. Record the timestamp of the observed close, the book, and the price alongside the number.
- **Pre-register this choice before running anything.** Changing the reference book after seeing results is the most common silent form of p-hacking in this domain.
- **Report the full CLV distribution**, not the mean: mean, SD, % of bets with positive CLV, and the mean conditional on positive/negative. A high mean driven by a few key-number crossings is a different (and less reliable) thing than a broadly positive distribution.
- **Handle pushes and key numbers explicitly.** Report CLV both raw (in points) and converted to win-probability using an empirical NFL/CFB margin distribution — **not** a normal approximation — because the mass at 3, 7, 10, 14 dominates the conversion and a Gaussian will systematically misprice your edge.

### 8.2 Walk-forward design for football seasons

- **Never use random k-fold.** Games within a season share team-strength state; random folds leak future information into the past. This is the single most common error in the ML-sports literature.
- **Temporal split unit: the week, not the game.** Train on all data through week *w*, predict week *w+1*, roll forward. Refit at weekly cadence, matching how you would actually operate.
- **Season boundaries are regime breaks.** Roster turnover, coaching changes, and (in CFB) the transfer portal mean cross-season parameter carryover must be an explicit, tested modelling decision, not an accident of the data pipeline. Test both a hard reset and a shrunk carryover.
- **Embargo the first N weeks of each season** from evaluation (N ≈ 3-4). Early-season is where team-strength priors dominate and where both your model and the market are least informed; including it inflates apparent edge in a way that does not persist. If you want to *trade* early season, evaluate it as a separate strategy with its own sample.
- **Feature construction must be point-in-time.** Every feature must be computable from information available at the timestamp of the simulated bet. Specifically: injury designations as known at that hour (not the final game-status), weather forecast as issued (not observed weather — this is a classic and fatal leak in totals models), and betting lines as of that timestamp. **Store the as-of timestamp with every feature value.**
- **Simulate the line you could actually have taken**, including the price, at the specific timestamp — not the day's opener or a daily average.

### 8.3 Detecting overfitting and correcting for multiple comparisons

- **Pre-register the strategy set.** Write down every strategy variant you intend to test *before* testing. Then correct.
- **Correction:** Bonferroni is defensible and conservative; per §1.1, testing 100 strategies raises the n for 80% power on a 54% edge from 5,869 to **16,210 bets**. Prefer **Benjamini-Hochberg FDR** if the strategy set is large and correlated. Better still, use **White's Reality Check / Hansen's SPA test**, which are designed exactly for this (data-snooping over a universe of trading rules) and account for correlation across strategies — this should be familiar territory from the HMM work.
- **Deflated Sharpe / PBO.** Compute the Probability of Backtest Overfitting (Bailey & López de Prado's combinatorially-symmetric cross-validation) over the strategy set. If PBO > 0.5, the selected strategy's out-of-sample performance is expected to be below median. This is the right tool for "I tried a lot of things and picked the best one."
- **The decorrelation test is mandatory.** Per Hubáček et al. (*IJF* 2019): regress realised margin on (closing line, model prediction). If the model coefficient is not significantly non-zero, **the model has no information beyond the market and nothing else matters.** Run this before running any P&L simulation. It is cheap, it is the single most informative diagnostic available, and it will kill most candidate models in one line of code.
- **LLM-component-specific:** any LLM component must be evaluated **only on games after the pinned model version's training cutoff**. No pre-cutoff backtesting, at all. Pin the model version, temperature, and prompt as versioned artefacts; run ≥5 seeds per configuration and report the seed dispersion (KellyBench's −32.9% to +34.1% for the best model is the cautionary number). If seed dispersion swamps the effect, you have no result.

### 8.4 Minimum samples before drawing conclusions

| Conclusion | Minimum n | Basis |
|---|---|---|
| "This model has positive CLV" | **~70-150 bets** | §1.3, assuming mean +0.3 pts / SD 1.0 pt; scale as (SD/mean)² |
| "This model has ≥54% true ATS" | **~5,870 bets** (80% power) | §1.1 |
| "This model has ≥54% ATS, after testing 100 variants" | **~16,210 bets** | §1.1 |
| "This LLM configuration is better than that one" | Prospective only, ≥5 seeds each, and expect to need a full season | KellyBench seed variance |

**Decision rule I would adopt:** *no capital is deployed on a strategy until it has demonstrated statistically significant positive CLV on ≥150 prospectively-timestamped paper bets against a pre-registered Pinnacle close, and has passed the decorrelation test.* Win-rate P&L is monitored but is never the go/no-go criterion, because it cannot be within the life of the project.

### 8.5 Live-tracking infrastructure requirements

- Log, at bet time: UTC timestamp, book, market, side, number, price, stake, model prediction, model version, feature vector snapshot.
- Log, at close: reference-book number and price with its timestamp.
- Compute CLV nightly. Plot cumulative CLV with a confidence band. **The CLV curve, not the bankroll curve, is the dashboard.**
- Track account health as a first-class metric: max accepted stake per book over time. **A falling limit curve is the leading indicator that your edge is real and that your capacity is dying** — the two facts arrive together.

---

## 9. Open questions only original backtesting can resolve

1. **Does Arscott's CFB team-total censoring edge still exist in 2023-2026 data?** It is the highest-value single test in this memo: peer-reviewed, mechanism-based, falsifiable, and cheap to test with historical team-total lines. If it survives at >54% out-of-sample against closing team totals, the project has a thesis. If it does not, that is strong evidence the post-legalisation market has closed the published gaps.
2. **What is the current standard deviation of CFB closing-spread error, by conference tier?** Published estimates range 14-21 and the answer determines every points-to-probability conversion. Also: does σ differ materially between P4 and G5/FCS games? If yes, that quantifies the "low-tier CFB is softer" thesis directly.
3. **Does an ensemble EPA/DVOA-style model carry non-zero coefficient in the decorrelation regression against the NFL and CFB closing line, out-of-sample, 2015-2025?** This is the go/no-go on conventional modelling and can be answered in weeks.
4. **Is there residual weather signal on totals after 2015?** Specifically: does the *revision* in forecast wind between Wednesday and Sunday predict the residual of (total points − closing total)? Borghesi's finding is 20+ years stale and this is the direct modern test.
5. **How much CLV does line shopping alone generate on NFL/CFB in 2026, and how fast does it decay as accounts are limited?** This is measurable with a small real-money pilot and it directly sizes the only edge I am confident exists.
6. **Do prediction-market (Kalshi/Polymarket) closes differ systematically from sharp sportsbook closes on CFB spreads and totals?** If exchange prices lag sharp-book prices on low-liquidity CFB, that is an unlimited-capacity, no-limiting-risk edge — and it would be the single best finding available to this project.
7. **Does an LLM used purely as a point-in-time information extractor add residual signal beyond a conventional model plus the closing line?** Prospective evaluation only, post-cutoff games only. This is the only LLM question worth spending on.

---

## 10. Source table

| Citation | Year | Sport | Sample | vs. open/close | Vig? | What it supports | Confidence | URL |
|---|---|---|---|---|---|---|---|---|
| Levitt, "Why are gambling markets organised so differently from financial markets?", *Economic Journal* 114(495):223-246 | 2004 | NFL | ~20,000 bets, 2002 handicapping contest | Posted line (bookmaker price) | N/A | Books are better forecasters than bettors; prices deliberately non-clearing | High (paper), Medium (numbers) | https://academic.oup.com/ej/article-abstract/114/495/223/5086012 |
| Gray & Gray, "Testing Market Efficiency: Evidence From The NFL Sports Betting Market", *Journal of Finance* 52:1725-1737 | 1997 | NFL | 1976-1994 | Unstated in what I could verify | Claimed vs. −110 | Probit strategies profitable in-sample; inconsistent out-of-sample; home dogs undervalued | Medium | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1997.tb01129.x |
| Boulier & Stekler, "Predicting the outcomes of National Football League games", *IJF* 19(2):257-270 | 2003 | NFL | 1994-2000 | Betting market forecast | N/A | **Betting market is the best predictor**, ahead of power-score probit and experts | High | https://www.sciencedirect.com/science/article/abs/pii/S0169207001001443 |
| Fair & Oster, "College Football Rankings and Market Efficiency", *JSE* 8(1) | 2007 | CFB | Multi-season | **Final Vegas spread** | N/A | **No ranking system adds info beyond the closing spread** — strong CFB efficiency result | High | https://journals.sagepub.com/doi/abs/10.1177/1527002505276724 |
| Štrumbelj, "On determining probability forecasts from betting odds", *IJF* 30:934-943 | 2014 | Multi | Multi-sport | Odds-implied | De-vigged via Shin | Odds-implied probabilities are accurate forecasts; Shin > basic normalisation | High | https://www.sciencedirect.com/science/article/abs/pii/S0169207014000533 |
| Kain & Logan, "Are Sports Betting Markets Prediction Markets?", *JSE* 15(1):45-63 | 2014 | NFL/CFB | Multi-season | Unstated | N/A | Spreads predictive of outcomes; totals comparatively weaker predictors | Medium | https://journals.sagepub.com/doi/abs/10.1177/1527002512437744 |
| Paul & Weinbach, "Market Efficiency and a Profitable Betting Rule: Evidence From Totals on Professional Football", *JSE* 3:256-263 | 2002 | NFL totals | 1979-2000 | Unstated | Claimed vs. fair-bet | Skewed totals forecast errors; contrarian under on high totals violates fair bet | Medium | https://journals.sagepub.com/doi/10.1177/1527002502003003003 |
| Borghesi, "Weather biases in the NFL totals market", *Applied Financial Economics* 18(12) | 2008 | NFL totals | 5,008 games, 1984-2004 | Unstated | Beat 52.38% out-of-sample (claimed) | Market under-adjusts for heat/wind/rain | Medium (original); Low (today) | https://www.tandfonline.com/doi/full/10.1080/09603100701335432 |
| Sinkey & Logan, "Does the Hot Hand Drive the Market?", *Eastern Economic Journal* 40 | 2013 | CFB | >11,000 games, 1985-2003 | Unstated | Unstated | CFB market inefficient after stripping behavioural strategies | Medium | https://link.springer.com/article/10.1057/eej.2013.33 |
| Kaunitz, Zhong & Kreiner, "Beating the bookies with their own numbers", arXiv:1710.02824 | 2017 | Soccer | 10-yr sim (closing odds); 6-mo tick sim; **265 real bets over 5 months, ~+€1,974** | **Closing odds** in the historical sim | Yes | Odds-outlier-vs-consensus strategy profits with real money; **all accounts limited/closed** | High (design/outcome), Medium (figures) | https://arxiv.org/abs/1710.02824 |
| Shank, "Is the NFL betting market still inefficient?", *J. Economics & Finance* | 2018 | NFL | 2009-2017 | Unstated | Claimed economically significant | Large home dogs and post-non-cover dogs undervalued; spreads AND totals inefficient | Medium | https://link.springer.com/article/10.1007/s12197-018-9431-4 |
| Lopez, Matthews & Baumer, "How often does the best team win?", *Annals of Applied Statistics* 12(4):2483-2516 | 2018 | NFL+3 | ~decade per league | Uses market data as input | N/A | NFL has high game-to-game randomness; market data is the modelling substrate | High | https://projecteuclid.org/euclid.aoas/1542078053 |
| Hubáček, Šourek & Železný, "Exploiting sports-betting market using machine learning", *IJF* 35(2):783-796 | 2019 | NBA | Multi-season | Vs. published odds | Yes | **Decorrelation from bookmaker odds, not accuracy, drives profit** | High (insight), Medium (magnitude) | https://www.sciencedirect.com/science/article/abs/pii/S016920701930007X |
| Bennett, "Holdover Bias in the College Football Betting Market", *Atlantic Economic Journal* 47:103-110 | 2019 | CFB | 2008-2016, first game of season for prior AP top-25 | Unstated | Beats 52.4% significantly (claimed) | Prior-season top-10 overvalued, esp. vs. non-P5; top 11-25 efficient | Medium-High (finding), Low (capacity: ~10 bets/yr) | https://link.springer.com/article/10.1007/s11293-019-09611-y |
| Francisco & Moore, "Betting with house money: RLM strategies in CFB totals", *J. Economics & Finance* 43:813-827 | 2019 | CFB totals | Sept 2005-Jan 2016, all games with a total | Line movement open→close | Yes | **RLM-following is NOT profitable** on CFB totals | Medium-High | https://link.springer.com/article/10.1007/s12197-019-09479-3 |
| Ramesh, Mostofa, Bornstein & Dobelman, "Beating the House", arXiv:1910.08858 | 2019 | NFL/NBA/NCAAF/NCAAB/WNBA | Unstated | **Not established** | Unclear | Claims above-market returns | Low | https://arxiv.org/abs/1910.08858 |
| Sides & Harvill, "Converting College Football Point Spread Differentials to Probabilities", arXiv:2212.08116 | 2022 | CFB | Season-specific | Spread-implied | N/A | CFB margin σ estimates (14-21 range across sources) | Medium | https://arxiv.org/abs/2212.08116 |
| **Arscott, "Market Efficiency and Censoring Bias in College Football Gambling", *JSE* 24(5):664-689** | **2023** | **CFB team totals** | **~2 decades** | **Unstated — needs verification** | **Exceeds transaction costs (stated)** | **Naive strategy on posted lines alone wins >55%; market semi-strong inefficient** | **Medium-High** | https://journals.sagepub.com/doi/10.1177/15270025221148991 |
| Winkelmann, Ötting, Deutscher & Makarewicz, "Are Betting Markets Inefficient? Evidence From Simulations and Real Data", *JSE* 25(1):54-97 | 2024 | Soccer + simulation | 14 seasons | N/A | N/A | **Apparent inefficiencies arise routinely inside efficient markets; no persistent systematic inefficiency** | High | https://journals.sagepub.com/doi/10.1177/15270025231204997 |
| Galekwa et al., "A Systematic Review of Machine Learning in Sports Betting", arXiv:2410.21484 | 2024 | Multi | Review | **Mostly unstated across surveyed works** | Mixed | ML techniques surveyed; **does not establish closing-line-validated profitability** | Medium (review), Low (profitability inference) | https://arxiv.org/abs/2410.21484 |
| Halawi et al., "Approaching Human-Level Forecasting with Language Models", NeurIPS 2024, arXiv:2402.18563 | 2024 | General | Real-world binary questions | N/A | N/A | RAG LLM Brier 0.179 vs crowd 0.149; beats crowd only in selective regime | High | https://arxiv.org/pdf/2402.18563 |
| Karger et al., "ForecastBench", ICLR 2025, arXiv:2409.19839 | 2024/25 | General | Contamination-free by construction | N/A | N/A | LLMs (~0.122) below superforecasters (0.096) | High | https://arxiv.org/abs/2409.19839 |
| Paleka, Goel, Geiping & Tramèr, "Pitfalls in Evaluating Language Model Forecasters", arXiv:2506.00723 | May 2025 | Methodology | N/A | N/A | N/A | **Temporal and logical leakage invalidate retrodictive LLM backtests** | High | https://arxiv.org/abs/2506.00723 |
| **KellyBench, arXiv:2604.27865** | **Apr 2026** | **EPL 2023/24** | **Full season, 8 models × 5 seeds** | **Real market odds** | **Yes (real odds)** | **Every model lost money; best (GPT-5.4) −7.9% mean ROI; seed range −32.9% to +34.1%** | **High** | https://arxiv.org/abs/2604.27865 |
| **FIFA World Cup 2026 contamination-free LLM benchmark, arXiv:2607.17765** | **Jul 2026** | **Soccer, 104 matches** | **All post-cutoff** | **Pre-match market odds** | **Yes** | **No agent beat the market's Brier; 92% identical top picks; ROI −18% to +10%** | **High** | https://arxiv.org/abs/2607.17765 |
| LLM-SoccerArena, arXiv:2607.24573 | Jul 2026 | Soccer, 104 matches, 7 LLMs | Prospective | Bookmaker baseline | N/A | Bookmaker baseline "hard to beat"; web access worth only 0.023 Brier | High | https://arxiv.org/abs/2607.24573 |
| "College football and the Vegas line: Deconstruction and arbitrage", *Journal of Prediction Markets* | — | CFB | 4,590 games, 2005-2011 | "Vegas line", unspecified | Claimed 2.7% APY | Top-35% mispriced games → 55% correct | Medium (paper), Low (exploitability) | https://www.ubplj.org/index.php/jpm/article/view/1183 |
| "Correlated Parlay Betting: Betting Market Profitability Scenarios in College Football", *Journal of Prediction Markets* | — | CFB | 2005-2015 | Posted lines | Discussed | Favorite-covers correlates with over; books over-conservative in refusing SGPs | Medium | https://www.ubplj.org/index.php/jpm/article/view/1562 |
| nfelo, "Margin Probabilities from NFL Spreads" (industry) | — | NFL | 7,276 games with a closing line | **Closing line** | N/A | Mean spread error +0.09 pts, σ ≈ 13.2 | Medium (industry, no peer review) | https://www.nfeloapp.com/analysis/margin-probabilities-from-nfl-spreads/ |
| Recall, "NFL Arena: Can LLMs predict football outcomes?" (industry blog) | 2025/26 | NFL | ~3 Thanksgiving games, 6 LLMs | Live, prospective | N/A | Only NFL-specific LLM datapoint found; all models wrong, would have lost money | Low (n≈3) | https://blog.recall.network/nfl-arena-can-llms-predict-football-outcomes |
| Industry reporting on account limiting (SBC Americas, BettingUSA, etc.) | 2025-26 | All | Anecdotal/journalistic | N/A | N/A | Books limit on CLV not P&L; graduated stake reduction; NY/WY/MA legislative attention | Medium | https://sbcamericas.com/2025/10/01/new-york-bill-limiting-sportsbooks/ |
| Industry reporting on prediction-market volumes (FOX Sports, XCLSV, etc.) | 2026 | NFL/CFB | ~$3.5B NFL, ~$3.1B CFB notional | N/A | Fees, not vig | Exchanges list NFL/CFB spreads & totals and **do not limit winners** | Medium (unaudited) | https://www.foxsports.com/stories/betting/polymarket-vs-kalshi |

**Rejected as unsourced/survivorship-biased (zero evidentiary weight):** "underdogs cover 63.8% at <40% public bets"; "fading the public wins 63.3%"; "professional models achieve 52-55% ATS"; "LLM point-spread accuracy 72-77%"; any vendor model track record under ~2,500 bets. See §3.5.
