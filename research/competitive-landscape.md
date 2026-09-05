# Competitive Landscape & Business Model Memo — NFL/CFB Prediction Subscription
**Analyst role:** Market analyst supporting compliance workstream
**Research date:** 2026-09-05 (2026 NFL/CFB preseason)
**Scope:** U.S. market, NFL and college football only, per brief

> **Framing note, read before anything else:** Section 4 of this memo documents what
> operators *do* — disclaimers, age gates, refund terms, geo-blocking. This is
> **observed industry practice, not a legal safe harbor and not legal advice.** I am
> not a lawyer and draw no legal conclusions. A separate team member owns compliance
> law; treat my observations here as raw input to that analysis, not as authority.

---

## Bottom Line

- **Realistic price band:** $20–$50/month for consumer-facing picks/analytics
  products (Action Network PRO ~$20/mo; Outlier ~$99/mo but discounts to ~$20/mo
  annualized; PFF+ $9.99–$99.99/yr entry tier); $99–$500/month for
  professional-grade odds/EV tooling (Unabated, OddsJam, BetQL). Individual touts
  charge anywhere from $40–$165/month with no real price discipline and enormous
  variance in legitimacy. **A new picks-only entrant should expect a ceiling near
  $30–$50/month for a mass-market consumer product**, with premium/pro tiers only
  viable if bundled with genuine tooling (line shopping, CLV tracking, bet
  tracking), not picks alone.
- **Most serious competitive threat:** The **positive-EV / arbitrage / odds-scanning
  segment** (OddsJam, Unabated, Outlier, BetQL). The manager's hypothesis is
  **correct, with one caveat**: these tools sell a mechanically verifiable
  service — better-than-market odds, live line shopping, CLV tracking against
  the closing line — rather than a forecast that must "come true." That is
  structurally more defensible because you can prove the value proposition
  independent of outcome variance (you can show a user got +3% CLV on a bet
  regardless of whether the bet won). The caveat: this segment competes for
  the *same disposable betting budget and the same customer* as a picks
  subscription, and increasingly bundles picks/model outputs on top of the
  scanning layer (Unabated and OddsJam both now sell "expert" or model picks
  as an add-on), so it is not just an adjacent threat — it is actively moving
  into the picks business from a stronger trust position. **Confidence: High.**
- **Is there a defensible position for a new entrant?** Conditionally yes, but
  narrow. A pure "we're right more often" picks product has no defensible
  position — the entire history of the tout industry is claims nobody can verify,
  and the few players who do report against the closing line (see §3) are
  odds-tooling companies, not touts. The only credible differentiated position is
  **transparent, third-party-auditable CLV reporting bundled with, not
  substituting for, actual line-shopping/EV tooling** — i.e., compete as a
  disciplined analytics/tooling company that also happens to publish picks, not
  as a tout that happens to show a spreadsheet. Whether customers will *pay* for
  the rigor itself, versus just wanting entertainment and hope, is genuinely
  unproven — see §5. **Confidence: Medium** on the opportunity; **Low** on
  willingness-to-pay for rigor specifically.

---

## 1. Landscape Map

### Individual touts / handicappers (personality-driven)

| Name | Segment | What they sell | Price | Claimed performance | Verification | Compliance posture | Date verified | URL |
|---|---|---|---|---|---|---|---|---|
| Doc's Sports (est. 1971) | Individual tout / legacy service | Per-game and package picks, phone/email delivery | Package pricing (per-play and monthly bundles; legacy site shows package examples like "$29,150 profit for $100 bettors" over a run of seasons) | Multi-decade "documented" win/profit claims by sport | Self-published on-site record pages; no independent third-party audit found | Standard entertainment disclaimers; age-gating not verifiable from marketing pages | 2026-09-05 | [docsports.com](https://www.docsports.com/current/how-to-use-a-handicapper.html) |
| Gianni "the Greek" Karalis / Vegas-Runner | Individual tout, marketplace-affiliated | Picks/subscriptions via WagerTalk | Package-based (site paywalled, not independently confirmed here) | Decades of Vegas insider positioning; no verified public win/loss ledger found | Sold via WagerTalk marketplace listing; no independent audit located | Not independently assessed | 2026-09-05 | [wagertalk.com profile](https://www.wagertalk.com/profile/gianni-the-greek) |
| "Mazi VS" / Darnell (Mazi) Smith, "Sports Betting King" | Individual tout (personality/social-media) | High-priced picks packages sold via social media to thousands of clients | Reported as "steep prices" (not itemized in reporting) | Claimed outlandish win rates; NYT reporting says losses were "often not disclosed" | **Independently investigated and found non-credible**: NYT profile plus criminal charges (14 felony forgery/identity-fraud counts, Clark County, NV, arrest May 2025; trial scheduled) | N/A — this is the cautionary case, not a functioning compliant business | 2026-09-05 | [Birches Health summary of NYT](https://bircheshealth.com/resources/famous-gambling-tout-mazi-vs); [Gambling911 trial update](https://www.gambling911.com/gambling/mazi-smith-sports-betting-king-trial-072025.html) |
| "Chad Smith" — "Sports Betting Star" | Individual tout | Picks touted at claimed ~95% win rate | Not disclosed publicly at time of exposure | Claimed 95% win rate — implausible for spread betting | **Independently debunked** by Sports Insights investigative writeup | Exposed as a "system scam"; site not confirmed still operating under this framing | 2026-09-05 | [Sports Insights exposé](https://www.sportsinsights.com/sports-betting-articles/sports-betting-star-exposed/) |

*Individual touts are the least verifiable segment by construction: nearly every
sourced piece of journalism found in this research about a *named* high-profile
individual tout describes fraud, forged identity documents, doctored screenshots,
or implausible win-rate claims (see §3), not a functioning, verifiably-compliant
subscription business. This is a real data point about the segment, not a
sourcing failure — the segment self-selects for actors who are hard to verify.*

### Tout marketplaces / aggregators

| Name | Segment | What they sell | Price | Claimed performance | Verification | Compliance posture | Date verified | URL |
|---|---|---|---|---|---|---|---|---|
| Pickswise | Marketplace / media | Free daily picks across NFL/CFB/other sports, "expert" branded | Free (ad/affiliate-supported) | Site claims a vetting process (injuries, trends, line movement) but publishes no aggregate verified win % | Independently tracked, informally, by third-party site NFL Pickwatch, which grades pick accuracy pick-by-pick | Standard "picks are for entertainment" framing typical of the segment | 2026-09-05 | [pickswise.com](https://www.pickswise.com/); [NFL Pickwatch tracking](https://nflpickwatch.com/profile/nfl/pickswise) |
| Covers.com Consensus / Covers Experts | Marketplace / community consensus | Aggregated "public betting consensus" picks, plus paid contest products | Free consensus data; contest products separately monetized | No single win-rate claim — consensus is descriptive (what % of players are on each side), not predictive | Consensus data is inherently "verifiable" in the trivial sense that it's just a vote count, not a forecast record | Standard disclaimers on affiliate/picks pages | 2026-09-05 | [covers.com/picks](https://www.covers.com/picks); [Consensus FAQ](https://contests.covers.com/consensus/faq) |
| CapperTek | Verification/directory marketplace | Directory of handicappers with "documented betting history, win/loss record, profit tracking" | Free directory; monetizes via handicapper listings/referrals | Third-party "verified" badge system for listed handicappers | **This is the closest thing the industry has to third-party verification, but it is verification of self-reported picks submission timing, not of an audited financial outcome or independent line-capture** — treat as directionally useful, not a rigorous audit | Not independently assessed for disclaimer prominence | 2026-09-05 | [cappertek.com verified directory](https://www.cappertek.com/directory.asp?filter=verified) |
| WagerTalk | Marketplace | Roster of named "expert" handicappers sold individually/bundled | Per-handicapper package pricing (not independently itemized here — site access blocked in this research pass) | Handicapper-specific claims, not centrally verified | Not independently assessed | Not independently assessed | 2026-09-05 | wagertalk.com/experts (page identified via search, not directly fetched) |

### Analytics and model subscriptions (data/models, not picks)

| Name | Segment | What they sell | Price | Claimed performance | Verification | Compliance posture | Date verified | URL |
|---|---|---|---|---|---|---|---|---|
| Action Network PRO | Analytics + picks hybrid | Betting system filters, expert picks/projections, sharp-money reports, bet-tracking sync | **$20/month** | Not a single headline win-rate claim; performance surfaced per system/analyst | No independent third-party audit found | Standard site-wide responsible-gambling and entertainment framing (industry standard, not separately verified here) | 2026-09-05 | [actionnetwork.com/pricing](https://www.actionnetwork.com/pricing) |
| Pro Football Focus (PFF+) | Analytics subscription | Grades, premium stats, mock draft simulator, rankings | **$9.99/mo entry; $99.99/yr; PFF Pro tier $199.99/yr** | Not pick-based; grades are PFF's proprietary scoring, not a "win %" claim | N/A — not a picks product, so "verification" framing doesn't apply the same way | Not a gambling-picks product per se, positions as football analytics | 2026-09-05 | [PFF+ pricing](https://www.pff.com/subscribe) |
| FTN Fantasy (absorbed Football Outsiders/DVOA) | Analytics subscription | DVOA-style efficiency metrics, projections, fantasy + betting tools ("GOAT" plan) | Tiered (Pro plan + GOAT plan bundling DFS/betting); exact current price not confirmed from search snippets alone | Not pick-based; DVOA is a descriptive/predictive efficiency metric, not a bet record | N/A | Standard | 2026-09-05 | [ftnfantasy.com/pricing](https://ftnfantasy.com/pricing) |
| Dimers | Analytics/model subscription (Dimers Pro) | Model-driven projections, picks framed as data-driven | **$14.99/week; $29.99/month; $199.99/year** | Markets itself as "data-driven"; explicit entertainment-only disclaimer, does not accept bets | Not independently audited | Explicit, prominent "for entertainment purposes only... does NOT accept bets of any kind" disclaimer | 2026-09-05 | [dimers.com/subscription](https://www.dimers.com/subscription) |
| TeamRankings, Inpredictable, Massey/Sagarin ratings | Free/near-free ratings | Predictive power ratings, no picks framing | Free (Massey, Sagarin) or freemium (TeamRankings) | Descriptive/statistical model output, not a win-rate marketing claim | N/A — these are open methodology sites, arguably more "verifiable" than any tout because methodology is published | Not gambling-marketed | 2026-09-05 | [masseyratings.com](https://masseyratings.com/); [sagarin.com/sports/cfsend.htm](http://sagarin.com/sports/cfsend.htm) |

### Odds tools / positive-EV and arbitrage scanners — **the most serious competitive threat**

| Name | Segment | What they sell | Price | Claimed performance | Verification | Compliance posture | Date verified | URL |
|---|---|---|---|---|---|---|---|---|
| OddsJam | +EV / arbitrage / line-shopping scanner | Arbitrage finder, positive-EV scanner, 160+ book odds screen, **CLV tracker**, bet tracker | Reported range **~$39–$999/mo** depending on tier; Pro commonly cited at **$199.99/mo or $149.99/mo annualized**; Platinum ~$499/mo (~$400/mo annualized); 7-day free trial on some tiers | Sells a mechanical edge (find + capture better prices), not a forecast win rate | Value proposition is self-verifying at the point of use — user can see the odds discrepancy directly; OddsJam's own CLV tracker lets users audit their own results against the close | Standard consumer disclaimers; product is a tool, not a picks/gambling-advice product per se | 2026-09-05 | [OddsJam subscribe](https://oddsjam.com/subscribe); [pricing review](https://getarbitragebets.com/blog/oddsjam-pricing) |
| Unabated | +EV / sharp-line tool | "Unabated Line" (no-vig fair-value line), scanners, **CLV calculator**, ratings | **$99–$199/mo** list; annualized effective price ~**$49/mo (Essentials)** to **~$132/mo (Premium, $1,584/yr)** | Sells methodology (de-vigged fair lines), not a pick-record | Methodology published (de-vig calculation is transparent/replicable), which is a stronger form of "verification" than any picks product in this memo | Standard | 2026-09-05 | [Unabated CLV calculator](https://unabated.com/betting-calculators/closing-line-value-calculator); [pricing review](https://xclsvmedia.com/unabated-review-2026-premium-sharp-bettor-tool-worth-it/) |
| Outlier.bet | Player-prop +EV tool | Prop-betting EV finder across books | **~$99/mo standard; annual tiers $199.99–$359.99/yr; Premium ~$19.99/mo tier also reported** (pricing is inconsistently reported across sources — treat range as approximate) | Mechanical edge-finding, not a forecast | Same self-verifying logic as OddsJam | Standard | 2026-09-05 | [pricing review](https://xclsvmedia.com/oddsjam-vs-avo-vs-outlier-best-ev-betting-software-compared-2026/) |
| BetQL | Odds/sharp-money tool + some picks | Premium stats, sharp-money tracking, "community picks" layer | Weekly/3-month/annual plans; Premium and Sharp tiers; exact current $ not confirmed from search alone | Blends mechanical sharp-money tracking with some pick content — this is the segment's drift toward picks noted in the Bottom Line | Sharp-money tracking is descriptive of market data, not a forecast claim | Standard | 2026-09-05 | [betql.co](https://betql.co/); [pricing page ref](https://support.betql.co/hc/en-us/articles/360047974514-Pricing) |
| Pikkit | Bet-tracking / CLV tool | Automated CLV tracking across 30+ sportsbooks via bet-sync ("BookSync") | Pikkit Pro tier (price not itemized in search results obtained) | Explicitly markets **CLV%, not win/loss**, as the headline metric | Automated sync to sportsbook accounts is a materially stronger verification method than self-reported picks | Standard | 2026-09-05 | [pikkit.com/closing-line-value](https://pikkit.com/closing-line-value) |

**Assessment of the manager's hypothesis:** Correct. The +EV/arb/CLV-tooling segment
is structurally more defensible for three concrete reasons found in this research:
(1) their core claim (odds discrepancy exists, or CLV was captured) is checkable at
the moment of the transaction, independent of game outcome; (2) several publish
methodology (Unabated's no-vig line construction; Pikkit's automated multi-book
sync) rather than asking for trust; (3) none of the fraud/enforcement findings in
§3 implicate this segment — every fraud case found involves a personality-driven
tout. The threat to a new picks entrant is not just "customers might buy this
instead" — it's that this segment is the trust-credible place from which picks
products are now being cross-sold (OddsJam and Unabated both layer picks/model
outputs onto their scanning products), so they compete on both price and integrity
at once.

### Free and open-source alternatives — the real price floor

| Source | What's free | Notes | Date verified | URL |
|---|---|---|---|---|
| Massey Ratings | Full computer ratings, NFL + CFB, methodology described | No paywall found | 2026-09-05 | [masseyratings.com](https://masseyratings.com/) |
| Sagarin Ratings | Full CFB computer ratings | Long-running, no paywall found | 2026-09-05 | [sagarin.com/sports/cfsend.htm](http://sagarin.com/sports/cfsend.htm) |
| r/sportsbook + affiliated Discord | Free community picks, discussion, best-odds sharing | ~185,000-member Discord identified | 2026-09-05 | [discord.com/invite/sportsbook](https://discord.com/invite/sportsbook) |
| PropWave / "Beat The Sportsbook" and similar Discords | Free +EV/prop discussion, daily picks | Free-to-join, ad/referral supported | 2026-09-05 | identified via [thehiveindex.com Discord directory](https://thehiveindex.com/topics/sports-betting/platform/discord/) |
| Covers.com Consensus | Free public betting consensus | No paywall | 2026-09-05 | [covers.com/picks](https://www.covers.com/picks) |

**Price floor finding:** The genuine price floor for "a prediction/analytics
signal" is **$0** — credible, methodologically transparent, free power ratings
(Massey, Sagarin) have existed for decades and are still live, and free
Discord/Reddit communities with six-figure membership provide social,
crowd-sourced picks and +EV discussion at zero cost. Any paid product must beat
"free and transparent" on convenience, timeliness, or trust, not availability.

### Media/affiliate model — free picks monetized by sportsbook referral revenue

- Action Network's business is explicitly described as split between subscription
  ($20/mo PRO tier) and affiliate revenue, with affiliate-driven M&A multiples
  reported as materially richer than pure-subscription comps (a 2023-era deal
  analysis cites a "16x multiple on acquisition relative to other affiliate-based
  transactions" for a comparable deal) — directionally this supports affiliate
  revenue being the larger and more valuable half of the business, though this
  memo could not source current 2026 affiliate-vs-subscription revenue splits.
  **Confidence: Medium** (sourced to a single deal-analysis newsletter, not audited
  financials). [jordanpascasio.substack.com deal analysis](https://jordanpascasio.substack.com/p/deal-analysis-the-action-network)
- Pickswise operates on a fully free, affiliate-monetized model with no visible
  subscription product — consistent with affiliate revenue being sufficient to
  run a large-scale free picks operation. [pickswise.com](https://www.pickswise.com/)
- **How this has shifted:** Sportsbook customer-acquisition spend has been
  reported industry-wide as declining/normalizing since the post-legalization
  land-grab years (2018–2023) as states matured and books cut promotional CAC —
  this memo did not locate a single authoritative, current (2026) citation
  quantifying that shift precisely enough to state a number with confidence, and
  flags this as an **open question** (see below) rather than asserting an
  unsupported figure.
- **Assessment: affiliate model is likely the better business than subscriptions
  for a *content-scale* free-picks operation** (Pickswise-style), but that is a
  different business than what this project is evaluating — the brief is a
  **paid** subscription, and a new entrant without existing scale/SEO/social
  distribution cannot bootstrap affiliate revenue fast enough to substitute for
  subscription revenue in year one. **Confidence: Medium.**

---

## 2. Pricing and Packaging

### Observed price points (all sourced above; consolidated view)

| Tier | Range | Examples |
|---|---|---|
| Free | $0 | Massey/Sagarin ratings, Covers Consensus, Pickswise, Reddit/Discord |
| Entry consumer | $10–$30/mo | PFF+ ($9.99/mo), Action Network PRO ($20/mo), Dimers Pro ($14.99/wk or $29.99/mo) |
| Mid consumer/prosumer | $40–$100/mo | Individual tout packages ($40, $49.99, $75/mo observed via Gumroad-style storefronts — see below), Outlier standard ($99/mo) |
| Professional tooling | $100–$500+/mo | Unabated ($99–$199/mo list), OddsJam (up to $499–$999/mo top tier) |
| Annual/seasonal | $199–$1,584/yr | Dimers Pro annual ($199.99), Unabated Premium annual ($1,584), VSiN Plus (~$240–$348/yr as of 2024 pricing, may have changed) |

Individual-tout package pricing observed via direct storefronts (Gumroad-hosted
picks sellers, illustrative of the unregulated bottom of the market, **not
brand-name businesses this memo can vouch for as legitimate or currently
reputable** — flagged as raw pricing data points only): $40/mo, $49.99/mo,
$75/mo, $99.99/mo, $165/mo, $19.99/mo observed across different named storefronts
in September 2026 search results. [search result set, 2026-09-05](https://ceoishhh.gumroad.com/l/dhiwb)

### Free-tier and trial structure
- OddsJam: free tier with limited data; 7-day free trial on some paid tiers.
  [oddsjam.com/subscribe](https://oddsjam.com/subscribe) (verified 2026-09-05)
- Most picks-only touts observed do not offer a meaningful free tier — they
  offer "free picks" as lead-gen (a subset of picks, or historically cherry-picked
  wins) to drive paid conversion, consistent with long-documented tout-industry
  practice (see §3).
- Paywall typically sits at "today's best bet" / "lock of the day" — free picks
  are volume/lower-confidence, paid picks are framed as higher-confidence.

### Guarantees
- Observed guarantee structures range from genuine-looking to fraud-adjacent:
  - A "profitable season or free extension" model (extend next season free if
    the current one is unprofitable) was found described in aggregate consumer
    guidance, not attributed to one auditable named operator.
  - A bankroll-threshold refund (refund if bankroll falls below X by month-end)
    was similarly found described generically.
  - Consumer-protection reporting (BBB Scam Tracker per secondary source) documents
    cases where "money-back guarantee" picks services **did not honor** the
    guarantee — this is a recurring complaint pattern, not a one-off.
    [hayspost.com scam alert](https://hayspost.com/posts/a98e89a8-d185-403e-a572-3b364268a313);
    [carriagetownenews.com scam alert](https://www.carriagetownenews.com/news/local_news/scam-alert-guaranteed-sports-betting-picks/article_cc447a2a-ba74-11ec-bf0c-2fa30f6b8d43.html)
  - **Assessment:** guarantees in this category should be read skeptically by
    default; the credible-verification bar (see §3) is high and rarely met.

### Churn, retention, LTV — what actually exists publicly
**No credible, publicly available, category-specific churn/retention/LTV data
was found for sports-picks subscriptions in this research pass.** This is a
finding, not a gap in search effort: picks and betting-tools companies are
almost entirely private, don't disclose subscriber metrics, and no analyst
report or investigative piece located here quantifies churn for this category.
What can be stated with confidence, from first-principles structural facts
that are independently sourced:
- The product is **explicitly seasonal** — NFL/CFB run roughly September to
  January — which structurally caps annual engagement to ~4–5 months unless a
  product diversifies across other sports, a pattern visible in the fact that
  essentially every named competitor above (VSiN, Action Network, Unabated,
  OddsJam, PFF, WagerTalk) is multi-sport, not NFL/CFB-only.
- The recurring "guarantee not honored" complaint pattern (above) is itself
  circumstantial evidence of high churn-by-dissatisfaction, but this is an
  inference, not a measured churn rate.
- **Do not substitute generic SaaS churn benchmarks for this category** — I am
  flagging explicitly, per instruction, that no such analogy is offered here
  because it would not be a meaningful comparison (SaaS retention data comes
  from continuously-used software; picks are a discretionary, outcome-linked,
  seasonal purchase with a fundamentally different retention mechanic).

### Distribution channels
- **X/Twitter** — heavily used by individual touts and marketplace personalities
  (Gianni the Greek/Vegas-Runner, WagerTalk roster) for organic reach; no
  paid-ads restriction data found specific to this vertical on X, but paid
  ad policy risk is well known to be higher for gambling-adjacent content
  generally across platforms (Meta and Google both maintain restrictive
  gambling-ad certification regimes) — this is background industry knowledge,
  not independently sourced in this pass, and should be verified by whoever
  owns paid-media planning.
- **Discord** — large free communities (185K+ member "sportsbook" server) are a
  proven, zero-CAC distribution and retention channel for the free tier of this
  market. [discord.com/invite/sportsbook](https://discord.com/invite/sportsbook)
- **YouTube/podcasts** — VSiN and WagerTalk both run podcast/video content as
  top-of-funnel for paid picks; this is qualitative observation from their
  public presence, not independently quantified here.
- **Affiliate networks** — the dominant channel for the free-picks/media model
  (Pickswise, Covers) — see §1 affiliate section.

---

## 3. Claims and Verification Norms

### How performance is stated
Across every operator surveyed, the dominant public-facing metric is **win/loss
record or win percentage** — a marketing-friendly but analytically weak metric
because it ignores odds/vig and says nothing about value captured relative to
market price. Examples: Doc's Sports profit-per-$100 claims; Chad Smith's ~95%
win-rate claim (debunked, see below); individual Gumroad-style sellers'
undifferentiated "picks" framing. **Units won** and **ROI** framing appear less
often in the tout segment and more often in the tooling segment.

### Who reports against the closing line — the serious/marketing dividing line
This is the sharpest finding in this research and matches the manager's framing
exactly:
- **Operators that explicitly build products around Closing Line Value (CLV)**:
  Unabated (CLV calculator, [unabated.com](https://unabated.com/betting-calculators/closing-line-value-calculator)),
  OddsJam (CLV tracker bundled into paid tiers, [oddsjam.com/subscribe](https://oddsjam.com/subscribe)),
  and Pikkit (CLV% as the headline metric, automatically synced from sportsbook
  accounts across 30+ books, [pikkit.com/closing-line-value](https://pikkit.com/closing-line-value)).
  These are **all in the odds-tooling segment, none in the picks/tout segment.**
- **No individual tout or tout marketplace in this research reports CLV.** Every
  tout-segment performance claim found is raw win/loss or a dollar-profit claim
  at assumed flat-bet unit sizing — never against the closing number.
- This is exactly the distinction the manager asked about, and it is real: **the
  presence of CLV reporting is close to a perfect proxy for "which segment of
  this market is analytically serious."** A new entrant that reported CLV
  transparently would be doing something the picks/tout segment structurally
  does not do — see §5 for whether that is monetizable.

### Third-party verification services — credibility assessment
- **CapperTek**: bills itself as a directory of "verified" handicappers with
  documented win/loss and profit tracking. Assessment: this verifies that a
  pick was *logged before the game* (timestamp integrity), which rules out the
  most basic form of after-the-fact fraud (claiming picks post-hoc). It does
  **not** verify bet sizing, actual money risked, CLV, or auditor independence
  from the handicapper's own reporting. **Assessment: meaningful for the
  narrow claim it makes (timestamped pick submission), theatrical if presented
  as "verified profitability" — treat as a weak but non-zero signal.**
  [cappertek.com](https://www.cappertek.com/directory.asp?filter=verified)
  (Confidence: Medium on the mechanism, Low on how much it should move a buyer's
  trust.)
- **NFL Pickwatch**: independently grades named pundits'/sites' picks
  pick-by-pick against actual outcomes (e.g., tracks Pickswise's accuracy).
  This is closer to genuine independent verification because Pickwatch has no
  commercial relationship with the graded party visible in this research.
  [nflpickwatch.com](https://nflpickwatch.com/profile/nfl/pickswise) **Assessment:
  the most credible third-party verification mechanism found in this entire
  research pass, precisely because it is win/loss-only and simple — but it still
  does not report against the closing line, so even the best verification found
  is not "serious analytics" by the CLV standard.**

### Track record of the paid-picks industry — documented and unflattering, as expected
- **"Mazi VS" (Darnell/Mazi Smith), "Sports Betting King"**: New York Times
  investigative profile; subsequently arrested in Clark County, NV (May 2025) on
  14 felony counts of forgery and identity fraud (including possession of 14
  fraudulent IDs); trial scheduled per later reporting. Sold high-priced picks
  to thousands of clients while allegedly not disclosing losses.
  [Birches Health summary](https://bircheshealth.com/resources/famous-gambling-tout-mazi-vs);
  [Gambling911 trial coverage](https://www.gambling911.com/gambling/mazi-smith-sports-betting-king-trial-072025.html)
  (Confidence: High that the arrest/charges occurred as reported by multiple
  outlets; the NYT original piece itself was accessed only via secondary
  summary in this research pass.)
- **"Chad Smith" / "Sports Betting Star"**: publicly claimed ~95% win rate;
  independently characterized as a "system scam" by an industry publication.
  [Sports Insights](https://www.sportsinsights.com/sports-betting-articles/sports-betting-star-exposed/)
  (Confidence: Medium — single source, industry publication rather than
  neutral press, but consistent with the pattern documented elsewhere.)
- **General fraud tactics documented across secondary sources**: "double-siding"
  (selling opposite picks to different client segments so someone always wins
  and can be shown as a testimonial), doctored win-screenshot editing, touts
  with prior unrelated fraud convictions (one cited case: a handicapper
  claiming 71.5% win rate had a prior telemarketing-fraud conviction involving
  ~$234,000 taken from elderly victims), and referral arrangements in which
  touts are paid based on the *losses* of the customers they refer to
  sportsbooks (a direct conflict of interest between tout and customer).
  [Birches Health overview](https://bircheshealth.com/resources/sports-betting-touts)
  (Confidence: Medium — these are aggregated claims from a single secondary
  source; the underlying cases are not independently re-verified here, but the
  pattern is consistent with the two named cases above that do have independent
  corroboration.)
- **FTC/state AG enforcement specific to sports-picks touts**: **this research
  did not locate a specific, current, named FTC or state Attorney General
  enforcement action against a sports-picks/handicapping subscription
  business.** Enforcement and class-action activity found in this space is
  concentrated instead on **sportsbooks themselves** (DraftKings and FanDuel
  face proposed class actions over promotional/advertising practices; Kalshi
  and Polymarket face state-regulator and class-action activity over prediction
  markets) — **not on the picks/tout segment specifically.** This is a genuine
  finding, not a search failure: it suggests picks/tout fraud is being
  addressed (where addressed at all) through criminal fraud/identity-theft
  charges against individuals (as with Mazi Smith) and BBB/consumer-complaint
  channels, rather than through FTC rulemaking or coordinated state AG action
  against the picks-subscription business model as such. **Confidence: Medium**
  that this absence is real rather than a research gap — it is consistent
  across every enforcement-focused search run in this project.
  [amNewYork on Polymarket suit](https://www.amny.com/law/polymarket-gets-hit-with-class-action-lawsuit-over-sports-betting/);
  [King Law on gambling-addiction suits](https://www.robertkinglawfirm.com/mass-torts/sports-gambling-addiction-lawsuit/)

**Net assessment for §3, as the manager expected:** the paid-picks industry's
documented track record is unflattering — criminal fraud, identity theft,
implausible win-rate claims later debunked, a documented "double-siding"
technique, and a structural conflict of interest (loss-based referral pay) all
appear in the record for named, real operators. Formal regulatory enforcement
specifically targeting picks-touts (as opposed to sportsbooks) appears thin or
absent in what is publicly discoverable — that itself may be worth flagging to
the compliance lead as a fact about the *current* enforcement environment, not
a conclusion about legality or risk going forward.

---

## 4. Observed Compliance Patterns — Practice, Not Law

**This entire section documents what operators do. It is evidence of industry
norms, not a determination of what is legally required or sufficient. I draw no
legal conclusions. This is input for the compliance team member, not authority.**

| Practice | What was observed | Example | Date verified |
|---|---|---|---|
| "Entertainment purposes only" disclaimer | Common and often prominent on data/model-forward sites; less consistently prominent on tout storefronts observed via search snippets | Dimers: explicit statement that content is "for entertainment purposes only" and the site "does NOT accept bets of any kind" | 2026-09-05, [dimers.com](https://www.dimers.com/subscription) |
| Age gating | Legal minimum age for sports betting itself varies 18 vs 21 by state (18 in KY, NH, MT, RI, DC, WY per secondary compilation); picks/content sites' own age-gating enforcement mechanism (checkbox vs. verified ID) was not independently observed to be more than self-attestation on any site checked in this pass | General compilation, not a single operator's implementation | 2026-09-05, [athlonsports.com age requirements](https://athlonsports.com/betting/sports-betting-age-requirements-state-by-state) |
| Responsible-gambling messaging / helpline | 1-800-GAMBLER (National Council on Problem Gambling) referenced across multiple adjacent sites (sportsbook-affiliate sites, PropJuice, FanDuel's own research/help content) | PropJuice responsible-gambling page; FanDuel "TheDuel" responsible gambling content | 2026-09-05, [propjuice.ai/legal/responsible-gambling](https://propjuice.ai/legal/responsible-gambling); [fanduel.com research](https://www.fanduel.com/research/theduel/responsible-gambling-and-problem-gambling-assistance-01e763c8gk1t/) |
| Geographic restriction / geo-blocking | Not independently observed/tested in this pass for any named picks or analytics product (this would require live geo-testing, out of scope for a desk research pass) | — | — |
| Refund / auto-renewal / cancellation terms | Mixed and inconsistent; consumer-complaint sources describe cases where advertised money-back guarantees were **not honored**; more structured/legitimate-seeming variants (bankroll-threshold refund, free-season-extension-if-unprofitable) were found described generically, not attributed with confidence to a single named, currently-operating business | Underdog Sports (DFS-adjacent, not strictly a picks tout) publishes a formal money-back-guarantee policy, illustrating that clear published terms exist at least in the adjacent DFS category | 2026-09-05, [Underdog money-back guarantee](https://help.underdogsports.com/en/articles/10861465-money-back-guarantee) |
| Payment processors used | Sports-picks and betting-advice subscriptions are widely described (by high-risk-payment-processing vendors themselves) as chargeback-prone and consequently routed to specialist high-risk merchant-account providers rather than mainstream processors (Stripe/PayPal/Square are described as prone to declining or terminating such merchants due to pooled-account chargeback exposure) | Specialist providers named in vendor marketing: PayKings, Durango Merchant Services, Easy Pay Direct | 2026-09-05, [PayKings sports-betting merchant solutions](https://paykings.com/high-risk-processing-industries/sports-betting-merchant-account-solutions/); [general high-risk processor guide](https://www.seamlesschex.com/deep-dives/what-makes-a-business-high-risk-to-payment-processors) |

---

## 5. Positioning Gap Analysis

**Is there a defensible position?** Conditionally, narrowly, and unproven on
willingness-to-pay:

- **What is saturated / not defensible:** raw win-rate/pick-selling. The segment
  is crowded (dozens of named individual touts and marketplaces), has a
  documented fraud history (§3), has a free substitute of comparable or better
  analytical rigor (Massey/Sagarin, free Discords), and is actively being
  encroached upon by better-capitalized, better-trusted odds-tooling companies
  layering picks on top of their existing CLV-literate products.
- **Is transparent, publicly-verifiable CLV reporting a real differentiator,
  or a niche the market won't pay for?** Genuinely uncertain, and I want to be
  honest about that rather than force a confident answer:
  - **Case that it is real:** it is the one thing that structurally separates
    "serious" from "marketing" in this whole market (§3), the tooling segment
    that already does it commands materially higher price points ($99–$500/mo
    vs. $20–$75/mo for picks-only), and it directly answers the credibility
    problem documented throughout §3 (fraud, double-siding, undisclosed losses)
    by making manipulation much harder — you cannot fake CLV against an
    independently-recorded closing line as easily as you can fake a "record."
  - **Case that it is a niche the market won't pay for:** every operator that
    reports CLV in this research sells it as part of a *betting tool*
    (find/place better bets), not as *proof behind a picks product*. No
    evidence was found of a picks-selling business succeeding by leading with
    CLV transparency as the marketing hook — the customers who care enough
    about CLV to demand it are largely the same sophisticated, price-insensitive
    segment already being served by Unabated/OddsJam/Pikkit directly, and may
    not need or want a "picks" wrapper around it at all. The mass-market
    picks customer (the one paying $40–$75/mo to a tout) shows little evidence
    of caring about CLV — the fraud pattern documented in §3 persists precisely
    because that customer segment does not demand or verify it.
  - **My honest assessment: real but narrow.** CLV-transparency is a
    credible differentiator *for a specific, smaller, more sophisticated
    customer segment* that overlaps heavily with people the odds-tooling
    companies already serve — it is not proven to move the mass-market
    picks buyer, who is this category's larger revenue pool historically.
    **Confidence: Low-Medium**, explicitly because no source in this research
    demonstrates a picks business monetizing CLV transparency as its
    primary hook — this is inference from adjacent evidence, not a direct
    finding.

### Recommendation
- **Positioning:** Do not position as a picks/tout brand. Position as an
  analytics/tooling brand that happens to publish model outputs, with CLV
  reporting as a structural, non-marketing feature (i.e., report CLV on every
  published pick, win or lose, by default) — explicitly designed to be legible
  to the sophisticated segment that already trusts Unabated/OddsJam-style
  products, while accepting that this narrows, not expands, the addressable
  market versus a mass-market tout play. **Confidence: Medium.**
- **Target customer:** the "sophisticated recreational" bettor already paying
  for line-shopping/EV tools or adjacent analytics (PFF+, Dimers, Action
  Network PRO) who wants a credible second opinion, not the mass-market
  "give me a lock" customer the tout segment currently serves and periodically
  defrauds. **Confidence: Medium.**
- **Pricing model:** $20–$40/month consumer tier (matching the credible,
  non-fraud comps: Action Network PRO $20/mo, Dimers Pro $29.99/mo), with an
  annual discount, and explicitly **no lifetime/high-ticket packages** — those
  are a marker of the least credible part of this market (Gumroad-style
  $100–$165/mo storefronts) and would undercut the trust-based positioning.
  **Confidence: Medium.**
- **Launch channel:** owned content (podcast/newsletter/X) plus a free
  Discord community modeled on the proven free-community pattern (185K-member
  "sportsbook" Discord, PropWave), using free CLV-transparent picks as top of
  funnel, converting to paid for deeper tooling/analysis rather than "more
  picks." Avoid reliance on paid social ads given known platform restrictions
  on gambling-adjacent advertising (background knowledge, not independently
  re-verified in this pass — confirm current platform ad policy before
  committing budget). **Confidence: Medium on channel choice, Low on paid-ad
  feasibility until platform policies are independently checked by whoever
  owns media buying.**

---

## Open Questions

1. Current (2026), quantified sportsbook customer-acquisition-spend trend data —
   this memo found only a directional, dated (2023-era) claim about
   affiliate-deal multiples and could not source a current, authoritative
   figure on how CAC has shifted; needed to properly assess the affiliate-model
   opportunity.
2. Whether any FTC or state AG action against a picks/tout business specifically
   (as opposed to a sportsbook) exists but was not surfaced by this search
   methodology — worth a dedicated legal-database search (PACER, state AG press
   archives) by the compliance lead rather than relying on open web search.
3. Actual, current WagerTalk and individual-handicapper package pricing —
   wagertalk.com was blocked from direct fetch in this research pass; pricing
   cited is from secondary search snippets only and should be re-verified
   directly.
4. Any audited (not self-reported) churn/LTV figures from a picks or
   betting-tools company — none were found; if any team member has access to
   private company data rooms or trade-press subscriber disclosures, that would
   materially improve this section.
5. Live geo-blocking behavior of named competitors — not tested in this desk
   research pass.

---

## Source Table

| Source | Used for | Date verified |
|---|---|---|
| [docsports.com](https://www.docsports.com/current/how-to-use-a-handicapper.html) | Individual tout, legacy pricing/claims | 2026-09-05 |
| [wagertalk.com/profile/gianni-the-greek](https://www.wagertalk.com/profile/gianni-the-greek) | Individual tout profile | 2026-09-05 |
| [Birches Health: Mazi VS](https://bircheshealth.com/resources/famous-gambling-tout-mazi-vs) | Tout fraud case | 2026-09-05 |
| [Gambling911: Mazi Smith trial](https://www.gambling911.com/gambling/mazi-smith-sports-betting-king-trial-072025.html) | Tout fraud case, criminal charges | 2026-09-05 |
| [Sports Insights: Sports Betting Star exposé](https://www.sportsinsights.com/sports-betting-articles/sports-betting-star-exposed/) | Tout fraud case | 2026-09-05 |
| [Birches Health: sports betting touts overview](https://bircheshealth.com/resources/sports-betting-touts) | Industry fraud tactics | 2026-09-05 |
| [pickswise.com](https://www.pickswise.com/) | Marketplace/media, free model | 2026-09-05 |
| [NFL Pickwatch: Pickswise tracking](https://nflpickwatch.com/profile/nfl/pickswise) | Independent verification example | 2026-09-05 |
| [Covers.com Consensus FAQ](https://contests.covers.com/consensus/faq) | Marketplace consensus model | 2026-09-05 |
| [CapperTek verified directory](https://www.cappertek.com/directory.asp?filter=verified) | Third-party verification credibility | 2026-09-05 |
| [Action Network pricing](https://www.actionnetwork.com/pricing) | Pricing, affiliate+subscription model | 2026-09-05 |
| [Deal analysis: The Action Network (Substack)](https://jordanpascasio.substack.com/p/deal-analysis-the-action-network) | Affiliate revenue economics | 2026-09-05 |
| [PFF+ subscribe/pricing](https://www.pff.com/subscribe) | Analytics subscription pricing | 2026-09-05 |
| [FTN Fantasy pricing](https://ftnfantasy.com/pricing) | Analytics subscription pricing | 2026-09-05 |
| [Dimers Pro subscription](https://www.dimers.com/subscription) | Analytics/model pricing, disclaimer language | 2026-09-05 |
| [Massey Ratings](https://masseyratings.com/) | Free alternative | 2026-09-05 |
| [Sagarin Ratings](http://sagarin.com/sports/cfsend.htm) | Free alternative | 2026-09-05 |
| [OddsJam subscribe](https://oddsjam.com/subscribe) | +EV/arb tool pricing, CLV tracker | 2026-09-05 |
| [OddsJam pricing analysis (ArbBets)](https://getarbitragebets.com/blog/oddsjam-pricing) | +EV/arb tool pricing | 2026-09-05 |
| [Unabated CLV calculator](https://unabated.com/betting-calculators/closing-line-value-calculator) | CLV methodology | 2026-09-05 |
| [Unabated pricing review (XCLSV)](https://xclsvmedia.com/unabated-review-2026-premium-sharp-bettor-tool-worth-it/) | Pricing | 2026-09-05 |
| [Outlier/OddsJam/AVO comparison (XCLSV)](https://xclsvmedia.com/oddsjam-vs-avo-vs-outlier-best-ev-betting-software-compared-2026/) | Pricing comparison | 2026-09-05 |
| [Pikkit closing line value](https://pikkit.com/closing-line-value) | CLV-first tool | 2026-09-05 |
| [BetQL](https://betql.co/); [BetQL pricing support article](https://support.betql.co/hc/en-us/articles/360047974514-Pricing) | Odds/sharp-money tool | 2026-09-05 |
| [discord.com/invite/sportsbook](https://discord.com/invite/sportsbook) | Free community distribution | 2026-09-05 |
| [thehiveindex.com Discord directory](https://thehiveindex.com/topics/sports-betting/platform/discord/) | Free community distribution | 2026-09-05 |
| [athlonsports.com sports betting age requirements](https://athlonsports.com/betting/sports-betting-age-requirements-state-by-state) | Age-gating context | 2026-09-05 |
| [PropJuice responsible gambling](https://propjuice.ai/legal/responsible-gambling) | RG messaging example | 2026-09-05 |
| [FanDuel responsible gambling research page](https://www.fanduel.com/research/theduel/responsible-gambling-and-problem-gambling-assistance-01e763c8gk1t/) | RG messaging example | 2026-09-05 |
| [Underdog Sports money-back guarantee](https://help.underdogsports.com/en/articles/10861465-money-back-guarantee) | Refund terms example (adjacent category) | 2026-09-05 |
| [Hayspost scam alert](https://hayspost.com/posts/a98e89a8-d185-403e-a572-3b364268a313) | Guarantee-not-honored complaint pattern | 2026-09-05 |
| [Carriage Town News scam alert](https://www.carriagetownenews.com/news/local_news/scam-alert-guaranteed-sports-betting-picks/article_cc447a2a-ba74-11ec-bf0c-2fa30f6b8d43.html) | Guarantee-not-honored complaint pattern | 2026-09-05 |
| [PayKings sports betting merchant solutions](https://paykings.com/high-risk-processing-industries/sports-betting-merchant-account-solutions/) | Payment processor difficulty | 2026-09-05 |
| [Seamless Chex: what makes a business high-risk](https://www.seamlesschex.com/deep-dives/what-makes-a-business-high-risk-to-payment-processors) | Payment processor difficulty | 2026-09-05 |
| [VSiN subscriptions info](https://vsin.com/news/what-you-should-know-about-vsin-subscriptions/) | Marketplace/media pricing (2024-era, may be stale) | 2026-09-05 |
| [amNewYork: Polymarket class action](https://www.amny.com/law/polymarket-gets-hit-with-class-action-lawsuit-over-sports-betting/) | Enforcement/litigation landscape (adjacent, not touts) | 2026-09-05 |
| [King Law: sports gambling addiction lawsuits](https://www.robertkinglawfirm.com/mass-torts/sports-gambling-addiction-lawsuit/) | Enforcement/litigation landscape (adjacent, not touts) | 2026-09-05 |
