# Business Plan — NFL / CFB Spread & Totals Prediction Service

**Prepared:** 2026-09-05
**Status:** Research synthesis for a go/no-go decision. Not an investment document.
**Prepared by:** Manager synthesis over seven independent research artifacts in `research/`.

> **Evidence limitation, stated before anything else.** Every citation underlying this
> plan was obtained by search-index triangulation. The research environment's egress
> proxy returned 403 for effectively every external domain — `arxiv.org`, `ftc.gov`,
> `law.cornell.edu`, `journals.sagepub.com`, and every data-vendor pricing page. **No
> source in this study was read at its origin by any team member.** Claims are
> reported at the confidence their sourcing supports, and the single most important
> affirmative edge citation (Arscott 2023) has been read by nobody. Re-verify before
> committing capital.
>
> **Nothing in the compliance section is legal advice.** It is research to be confirmed
> by a licensed gaming attorney before launch.

---

## 1. Executive Summary

**Recommendation: do not launch the subscription service as specified. Run a bounded,
non-commercial research experiment first, and let it decide.**

The venture's own predictive-edge lead — staffed to find the edge, after a full
literature review — puts the probability of an edge large enough to be a business on
main-market NFL/CFB sides and totals at **5–7%**, with **40–45%** mass on zero or
negative. The median outcome is ~51.5–52.0% true ATS, which is *below* the 52.38%
breakeven imposed by -110 vigorish. Every other workstream in this study is
conditional on that ~1-in-16 proposition, and none of them is priced as though it were.

Three findings independently reached kill-criterion severity:

1. **No published evidence exists that an LLM or RAG system produces closing-line value
   on NFL or CFB spreads or totals.** This was unanimous across the edge, RAG, and
   adversarial members. The nearest adjacent evidence is uniformly negative.
2. **The compliant version of the marketing is unsellable, and the sellable version is
   not compliant.** FTC substantiation requires a reasonable basis *before*
   dissemination; a "54% ATS" claim on a few hundred live bets has a confidence
   interval straddling both breakeven and 59%. Meanwhile zero competitors report
   against the closing line — the honest metric has no demonstrated demand.
3. **The product destroys its own input.** At the subscriber count that makes this a
   business (~1,500), released picks generate roughly 150× the posted limit of the
   most generous U.S. book on the exact markets where the only peer-reviewed edge
   evidence lives.

What survives scrutiny is not a business but a research question, and it is cheap to
answer: **a single-season, self-funded, zero-subscriber prospective CLV experiment on
CFB team totals and alternate lines**, with a kill threshold pre-registered in writing
before the first bet. It has no capacity constraint, no FTC surface, no payment
dependency, and no reputational exposure. It costs low four figures and one season.
Passing it does not license the venture — it licenses the next question, which is the
entirely unmeasured capacity of those markets.

**The honest framing: this is a ~1-in-16 shot at a business, gated behind a metric
whose link to profit is unvalidated in the literature, in a category whose public
record is fraud-dominated. Spend $2–5k and one season finding out, not $50k and a year
building.**

---

## 2. Market & Competitive Landscape

**Price floor is $0.** Massey and Sagarin ratings are free; large free Discord and
Reddit communities distribute picks at no cost. A paid entrant must out-compete free
on trust, using a credential it cannot legally publish until it has been substantiated.

**Observed price bands** (verified 2026-09-05, vendor pages, search-index confirmed):

| Segment | Price | Examples |
|---|---|---|
| Consumer picks/analytics | $20–$50/mo | Action Network PRO ~$20/mo; Dimers Pro ~$29.99/mo |
| Professional odds/EV tooling | $99–$500/mo | Unabated, OddsJam, BetQL, Outlier |
| Individual touts | $40–$165/mo | No price discipline; enormous variance |
| Free tier | $0 | Massey/Sagarin, free Discords, Reddit |

**The most serious competitive threat is the positive-EV / arbitrage scanner category**
(OddsJam, Unabated, Outlier, BetQL). They sell a mechanical, verifiable service rather
than a forecast — a structurally more defensible proposition — and they are moving into
picks from a stronger trust and data-licensing position. The market analyst named them
the top threat and then recommended a position inside their category, which is a
defect this plan does not adopt.

**Two findings that constrain every financial model:**

- **No public churn or LTV data exists for this category.** Any spreadsheet containing
  LTV, payback period, or a CAC ceiling is therefore fiction. Generic SaaS benchmarks
  were considered and deleted as unverifiable analogies.
- **Zero touts or tout marketplaces report performance against the closing line.**
  This is simultaneously the clearest evidence that the category is marketing rather
  than analytics, *and* the clearest evidence that there is no demonstrated demand for
  the one metric this venture would compete on.

**Category reputation.** The only on-point U.S. prosecution of a sports tout located —
*United States v. Adam Meyer* / Real Money Sports (E.D. Wis., indicted 2015, 8-year
sentence 2017) — was built on inflated win-percentage representations and prosecuted as
wire fraud, not as a gambling offense. An honest operator inherits this prior.

Countervailing and credited: **no FTC or state-AG enforcement action specifically
against a picks/tout business could be located** by either the compliance researcher or
the market analyst working independently. Enforcement attention has been on sportsbooks
and prediction markets instead.

---

## 3. Product & Value Proposition

**What it would be:** a subscription publishing model-generated positions on NFL and
college football point spreads and totals, benchmarked against live sportsbook lines,
with a transparent, timestamped, publicly-auditable closing-line-value record.

**The intended differentiator — publishing CLV on every pick — is real but
unmonetizable on current evidence.** It is a genuine gap (nobody does it) supported by
no demand signal (nobody pays for it), and the market analyst graded willingness-to-pay
for rigor at Low confidence. A gap plus no demand is an untested hypothesis presented
where a finding belongs.

**It also does not escape the FTC.** A published mean CLV is an objective, quantitative
performance claim about the product. Calling it "structural" or "non-marketing" does
not change its legal category — arguably it is a *cleaner* claim than a win rate, but
it is the same kind of claim and needs the same substantiation.

**Honest positioning, if the research experiment ever passes:** an analytics/tooling
product that publishes its own audited record, sold to the small segment that already
understands CLV — priced at the professional tier ($99+/mo), not the consumer tier,
because the consumer tier cannot absorb high-risk payment processing (below) and the
CLV-literate buyer is not a $20/mo buyer.

---

## 4. The Edge Case

### 4.1 The strongest evidence FOR

- **Arscott, "Market Efficiency and Censoring Bias in College Football Gambling,"**
  *Journal of Sports Economics* 24(5):664–689 (2023) — peer-reviewed, mechanism-based,
  reported to find >55% from posted lines alone over roughly two decades in CFB team
  totals. Computable from two posted numbers: no corpus, no index, no LLM, no
  retrieval. **Caveat that must travel with this citation: nobody on this team has read
  the paper. Its sample size, period, and whether the >55% was measured against closing
  or opening lines are all unverified.** By the project's own standard — CLV, not raw
  win rate — a result whose reference line is unknown is non-probative until read.
- **CFB is plausibly less efficient than the NFL**, particularly in low-liquidity
  games, derivatives, and team totals.
- **CLV is measurable fast.** ~70–150 bets versus ~5,868 for a win-rate read — roughly
  85× cheaper as a test. (The 70 figure assumes mean CLV +0.30pt and cross-bet SD
  1.0pt; at SD 2.0 it becomes 275. Plan against 150–300, not 70.)
- **Prediction markets (Kalshi, Polymarket) now list NFL and CFB spreads and totals and
  do not limit winners**, which removes the constraint that ended the cleanest
  documented real-money case (Kaunitz et al. 2017, arXiv:1710.02824 — strategy
  validated, accounts limited or closed within months).
- **The builder is genuinely equipped** for the falsification test: walk-forward
  validation and leakage discipline are already in hand.

### 4.2 The strongest evidence AGAINST

- **Direct negative results against the close.** Fair & Oster (*JSE*, 2007) found no
  college football ranking system — nor the optimal weighted combination of all of
  them — contained information beyond the final Las Vegas spread. Boulier & Stekler
  (*IJF*, 2003, NFL 1994–2000) ranked the betting market above probit models, expert
  judgment, and naive baselines. Levitt (*Economic Journal*, 2004) established books
  are better forecasters than their bettors.
- **Most published "inefficiencies" are sampling artifacts** (Winkelmann et al., *JSE*
  2024), and documented biases such as the home-underdog effect decayed after
  publication.
- **No evidence for the LLM/RAG premise.** Unanimous across three members. Adjacent
  evidence is negative: on ForecastBench (arXiv:2409.19839, ICLR 2025) the best LLM
  tested scored **0.111** Brier against **0.093** for superforecasters and **0.107**
  for an ordinary public crowd — the best model underperformed *both*. (These figures
  are the ones this synthesis adopts; see §8, Unresolved Conflicts.)
- **The sample-size wall.** Distinguishing a true 54% strategy from 52.38% breakeven at
  α=0.05, 80% power requires **5,868 bets** — 12.4 seasons betting selectively across
  both sports and both markets, or **34.1 seasons** after Bonferroni correction for 100
  tested variants. Win rate never becomes evidence within a founder's working life.
- **The selection problem, which nobody had quantified.** A strategy with *zero* true
  edge, backtested 100 ways over 200 bets, is essentially certain to produce a
  57%-ATS "winner" and will produce about **nine or ten** of them. This is the entire
  history of the paid-picks industry expressed as a binomial.
- **The backtest-overfitting literature is directly on point** (Bailey, Borwein, López
  de Prado & Zhu, *Notices of the AMS* 61(5), 2014; "The Probability of Backtest
  Overfitting"; "The Deflated Sharpe Ratio," SSRN 2460551). Sports betting is *worse*
  than the equity setting these study: a Bernoulli draw with variance ≈0.25 against a
  signal of 0.016.
- **The primary metric is itself unvalidated.** No peer-reviewed study establishes that
  CLV predicts long-run profitability with a large sample of individual bettors'
  records. The project's only feasible success metric rests on sportsbook marketing
  blogs and one practitioner's self-published corpus.
- **After the citation audit, the project has no sourced quantitative estimate of a
  positive edge from any mechanism.** The edge lead's one confidently-asserted
  edge — line shopping at "0.3–0.8 points of CLV" — was his own unsourced estimate and
  was deleted when no published quantification could be found.
- **No differential advantage.** Of the mechanisms by which documented winners actually
  won — distribution networks, line origination, latency infrastructure, structural
  derivative mispricing — the builder has access only to the last. Production ML
  capability is a commodity here and is the attribute least correlated with winning.

### 4.3 Verdict

**The edge case does not clear.** The affirmative evidence reduces to one unread paper
about a market with no measured capacity, in a strategy profile (mechanical, computable
from posted lines, published in a mainstream journal in 2023) that is the archetype of
a finding that gets patched on publication. The negative evidence is broad, replicated,
and comes from the venture's own researchers.

---

## 5. Regulatory & Compliance Requirements

**Every item below requires review by a licensed gaming attorney before launch. This is
research, not legal advice. Several of the most important findings are *negative*
findings produced in an environment where the primary statutory sources were blocked
and could not be read.**

### 5.1 The binding constraint is distribution and payments, not gaming licensure

Google Ads, Meta, and PayPal each have written policies that expressly capture
"tips/picks" services; Stripe's restricted-business list expressly names "sports
forecasting or odds making." This is a **platform-contract risk that can zero the
business overnight with no due process** — it cannot be lawyered around.
`[REQUIRES REVIEW BY LICENSED GAMING ATTORNEY]`

If an acquirer reclassifies the business under MCC 7995: processing costs commonly
2–5× standard-risk, lower chargeback thresholds, and rolling reserves frequently in
double-digit percentages. **A $20–40/mo product with a five-month revenue window
cannot absorb that**, which is why the pricing recommendation above moves to the
professional tier.

### 5.2 Claims substantiation is the highest-probability enforcement trigger

FTC law requires a **reasonable basis in hand before dissemination** (1984 Advertising
Substantiation Policy Statement; *Pfizer*, 81 F.T.C. 23 (1972)). Where an ad conveys a
specific level of support, the advertiser must possess at least that level. The only
on-point tout prosecution located was built on inflated win-percentage claims.
`[REQUIRES REVIEW BY LICENSED GAMING ATTORNEY]`

**"For entertainment purposes only" is largely folk wisdom.** No authority was located
holding that such a disclaimer converts a deceptive performance claim into a lawful
one. `[REQUIRES REVIEW BY LICENSED GAMING ATTORNEY]`

### 5.3 State layer

**No U.S. state with an express licensing or registration regime for consumer-facing
sports-pick sellers was located.** Note that the brief's own premise was wrong and the
compliance researcher corrected it: Nevada Gaming Commission **Regulation 5A is
"Operation of Interactive Gaming,"** not an information-service regime, and Nevada's
information-service license (NRS 463.01642 / 463.160) reaches those who sell
information *to a licensed sports pool* — B2B, not consumer-facing.
**This is a negative finding from a blocked-source environment and is the single most
important item for counsel to verify**, because the downside under NRS is criminal.
`[REQUIRES REVIEW BY LICENSED GAMING ATTORNEY]`

**Two state criminal statutes do reach transmission of gambling information** and are
not cured by never accepting a wager: Oklahoma 21 O.S. § 987 (felony) and Illinois 720
ILCS 5/28-1(a)(9). Both have narrow broadcaster/news carve-outs a paid subscription
likely does not fit. No enforcement action against a picks subscription was located
under either. `[REQUIRES REVIEW BY LICENSED GAMING ATTORNEY]`

### 5.4 Other binding items

- **Auto-renewal**: California ARL and the FTC negative-option regime — subscription
  mechanics must be built to the statute, not to a template.
- **Age gating** (21+ attestation) and responsible-gambling messaging.
- **Geo-gating must be enforced at signup *and at content delivery***, not merely
  stated in terms. This is in direct tension with the free-Discord/podcast funnel
  (see §8).
- **Immutable, timestamped pick log** — an engineering dependency, not a launch-day
  checklist item. It must exist *before* the first marketing claim.

### 5.5 Compliance cost and calendar

| Posture | Year-1 cost | Calendar before first paid subscriber |
|---|---|---|
| Subscription-only, state allowlist | **$15,000–$50,000** | **8–16 weeks** |
| Broad U.S. + sportsbook affiliate revenue | **$40,000–$120,000** | **4–8 months** |

Cost figures are Low-Medium confidence planning numbers, not quotes. The load-bearing
line is gaming counsel's initial opinion at **$8,000–$25,000** — and the adversarial
reviewer's objection that a genuine fifty-state survey is not an $8,000 engagement is
accepted.

**A compliant paid launch inside the 2026 season is not achievable. 2027 is the
earliest honest target.** This was unanimous across the team.

### 5.6 Kill criteria (compliance)

Any one of these, confirmed, is a stop: payments unavailable from both Stripe and a
mainstream alternative; counsel confirms a dissemination-of-gambling-information
statute plausibly reaches the service in more than a handful of states; counsel finds
an express tout-licensing requirement in a target state; **the performance record
cannot be substantiated to the FTC standard**; both Meta and Google Ads deny
authorization with no viable organic channel; founder unwilling to fund counsel at the
$8–25k level.

---

## 6. Data & Technology Costs

**The decisive finding, and it sits in the artifact least likely to be read closely:**

> The free path breaks *exactly* at timestamped historical odds with opening/movement/
> closing granularity per book. Free archives give single opening/closing values with no
> intraday timestamps and inconsistent book attribution — **the resulting backtest
> cannot compute true CLV.**

CLV is the project's only feasible success metric. The cheap stack cannot measure it.

| Tier | Annual cost | What it buys |
|---|---|---|
| Research / validation (free stack) | **$0–$300** | nflfastR/nflverse, CollegeFootballData, NOAA, Kaggle/SBR odds archives. **Cannot compute CLV.** |
| MVP production (lean, RSS news) | **~$1,600–$1,900** | The Odds API Business ($1,188/yr), Open-Meteo ($348/yr), CFBD/nflverse |
| **Realistic for true CLV backtesting** | **$6,000–$18,000** | Adds a quote-gated provider (OddsJam / OpticOdds / SportsGameOdds). **Vendor quote required; third-party estimate only.** |

**Licensing is a business-model risk, not a formality.** Sportradar's terms prohibit use
"in a betting, gaming, gambling, or wagering capacity" without written approval;
OpticOdds bars use "for any revenue-generating endeavor or commercial enterprise"
without an upgraded agreement; CFBD reportedly prohibits redistribution. **The product
is a derived work of odds data, and the provider the MVP depends on — The Odds API — is
the one whose commercial-use and derived-works terms nobody has read.**
`[REQUIRES REVIEW BY LICENSED ATTORNEY]`

**Compute** is not a constraint. The builder's existing GPU covers training; LLM
inference at the recommended architecture (offline feature extraction only) is modest.

**Missing line item:** no artifact costed the immutable pick-log and grading
infrastructure that compliance calls the highest-ROI compliance investment.

---

## 7. Pricing & Go-to-Market

**Conditional on the research experiment passing — which on current evidence it
probably will not.**

- **Price at the professional tier ($99+/mo), not the consumer tier.** The $20–40/mo
  band matches the picks comps, but it cannot absorb high-risk processing at 2–5× on a
  five-month revenue window, and the CLV-literate buyer is not a $20/mo buyer.
- **Cap subscribers deliberately.** This is not a growth business; it is a
  capacity-constrained one. Beyond roughly 100–200 subscribers on CFB derivatives, the
  released pick moves the number and the product destroys its own input. Model the cap
  explicitly before writing any revenue projection.
- **Channel is the unresolved problem.** Paid social and search are policy-restricted;
  the organic alternative (podcast, X, free Discord) **cannot be geo-gated at content
  delivery by construction** — which is what makes it cheap, and what puts it in direct
  conflict with the compliance requirement. Resolve with counsel before building a
  funnel around it.
- **Do not take sportsbook affiliate revenue.** It is the fact pattern most likely to
  drag an information seller across the Wire Act's "engaged in the business" line, and
  it adds a multi-state licensing layer (~$200–500/state across 15+ states) that
  roughly triples year-1 compliance cost.
- **No financial projection is offered here.** With no category churn or LTV data in
  existence, an LTV/CAC model would be fabrication.

---

## 8. Key Risks

| Risk | Severity | Note |
|---|---|---|
| **No edge exists** | Existential | 40–45% probability by the project's own researcher |
| **Edge exists but is unsellable** | Existential | Compliant marketing needs a sample that never arrives |
| **Self-defeat** | Existential | Business-scale subscribers ≫ market capacity by 1–2 orders of magnitude |
| **First backtest is contaminated** | Near-certain | Six independent leak vectors, each failing toward a *better* result |
| **Overfitting via variant selection** | Near-certain | ~9–10 false 57% "winners" per 100 zero-edge variants at n=200 |
| **Payment processor refuses or reclassifies** | High | Test first — cheap, fast, dispositive |
| **Data license prohibits the product** | High | The MVP's key vendor terms are unread |
| **Timestamped odds history unaffordable** | High | Quote-gated; 2–3× the stated budget |
| **CLV→profit link unvalidated** | High | The success metric itself lacks literature support |
| **Category reputational prior** | Medium | Fraud-dominated public record |
| **Seasonality** | Medium | ~5-month revenue window against annual fixed costs |
| **Solo-founder concentration** | Medium | Standard |

---

## 9. Decision

**Do not build the subscription service now.** Run the bounded experiment in
`BRD.md` Phase 0–1, which is designed to falsify the edge hypothesis as cheaply as
possible and to stop the project if it fails. Revisit this plan only if Phase 1 clears
its pre-registered gate.
