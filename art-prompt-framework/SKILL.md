---
name: art-prompt-framework
description: Turn a high-level task into a well-engineered AI prompt using the ART framework (Act, Request, Terms) by interviewing the user for the missing information. Use this skill whenever the user asks for help writing, building, improving, or structuring a prompt; says "write a prompt for...", "help me prompt...", "use ART", or "make this prompt better"; or describes a task they want an AI to do and needs it turned into an effective, reusable prompt — even if they don't use the word "prompt." Also covers orchestrated prompts, where the AI acts as a manager staffing a team of subagents.
---

# The ART Prompt Framework

ART turns a vague, high-level task into a complete, effective prompt by collecting three kinds of information from the user:

- **A — Act.** The identity the AI should take on — a perspective with *judgment*, not just a job title. "Act as a CFO reviewing this for board presentation, skeptical of unsupported projections" beats "act as a finance expert." The identity earns its place when it changes how the model evaluates things, not just what vocabulary it uses.
- **R — Request.** The specific ask: one strong action verb plus a clear deliverable. **Context lives inside Request** — the situation, audience, and background that make the ask meaningful. A request without context produces generic output.
- **T — Terms.** What the words mean and where the boundaries are. Two halves: *vocabulary* (definitions of key terms the user and the AI might silently define differently) and *conditions* (length, tone, format, exclusions, and what to do when uncertain).

Your job: take the user's high-level task, interview them for what's missing, then write the finished prompt for them.

## Workflow

### Step 1 — Read the task and size the effort

Assess the task's complexity before asking anything. Match the interview depth to the tier — over-interviewing a simple task teaches people to hate prompting.

| Tier | Signals | Interview depth |
|---|---|---|
| **Light** | Quick one-off, low stakes, obvious output ("summarize this email") | 0–2 questions, or none. Draft immediately, note assumptions. |
| **Standard** | Typical daily work: drafting, analysis, comparisons | 3–5 questions in one round |
| **Full** | High stakes, reusable, client-facing, or feeds a workflow | Two rounds: core questions, then follow-ups on gaps |
| **Orchestrated** | The task decomposes into several independent workstreams that could run in parallel, needs different kinds of expertise, or is large enough that one context window would degrade the output | Full-tier interview plus the environment question (Step 2b). Produces a manager prompt, not a worker prompt. |

**Do not reach for Orchestrated by default.** A team of subagents costs more, takes longer, and introduces coordination failure modes. It earns its place only when the work genuinely splits. Test it against three questions — if any answer is no, drop back to Full tier:

1. Can the work be cut into four or more pieces that don't need to talk to each other while running?
2. Would different pieces benefit from genuinely different expertise or different levels of model capability?
3. Is the synthesis step — reviewing and reconciling the pieces — itself substantial work?

Market research, competitive landscapes, multi-jurisdiction reviews, due diligence, and large audits usually pass. Drafting, single-document analysis, and most comparisons do not.

Also mine the conversation first. If the user has already stated the audience, tone, or constraints earlier in the chat, don't ask again — confirm instead ("I'll assume this is for the same ops-director audience as before — correct?").

### Step 2 — Interview, organized by letter

Ask questions grouped under A, R, and T so the user learns the framework while answering. Ask them all in one message (one batch for Standard, up to two batches for Full and Orchestrated). Never ask more than ~6 questions in a batch. Skip any question the task already answers. If an interactive question/option tool is available in your environment, use it; otherwise ask in plain prose.

**A — Act**
1. Who should the AI be for this task? (role or profession)
2. What judgment or attitude should that identity carry? (skeptical, safety-first, budget-conscious, creative, by-the-book...)

**R — Request** (with Context as the sub-question set)
3. What exactly should the AI produce? Push for one verb + one deliverable ("draft a follow-up email," "compare these three bids in a table").
   - **Context sub-questions:**
   - 3a. What's the situation? What led to this task?
   - 3b. Who is the audience for the output, and what do they care about or worry about?
   - 3c. What background does the AI need that it can't guess? (prior decisions, source material, relationships, history)

**T — Terms**
4. Are there any words in this task that need defining? (e.g., what counts as a "qualified lead," what "short" means, what "our standard format" is)
5. Conditions: How long? What tone? What must be included or excluded?
6. What should the AI do when it's unsure — flag it, ask, or make its best guess and label it?
7. Output shape: table, memo, email, bullets, JSON? Any required sections?

For **Full-tier** and **Orchestrated** prompts, also ask: "Do you have an example of what good output looks like?" and fold it in as an example block. Examples beat descriptions.

If the user answers "I don't know" or skips a question, make a sensible default, use it, and **list every assumption** under the delivered prompt so they can correct it.

### Step 2b — The environment question (Orchestrated tier only)

Orchestration is an environment capability, not a prompt trick. A prompt that tells the model to spawn a team only does that where the tooling exists. **Always ask before drafting:**

> "Where will you run this — Claude Code, Cowork, or a plain chat window?"

Then package accordingly:

| Environment | What it supports | How to package the prompt |
|---|---|---|
| **Claude Code** | Subagents defined as markdown files in `.claude/agents/` with frontmatter for `name`, `description`, `tools`, and `model`. Each runs in a fresh, isolated context; the lead receives only the final summary. Per-agent model selection is available. Subagents inherit the lead's model unless the `model` field is set explicitly. | Full orchestration. Instruct the manager to author the agent definition files during the staffing step, then invoke them. Recommend saving the finished prompt as a slash command so the roster is version-controlled and reusable. |
| **Cowork** *(default)* | Agentic execution and strong deliverable packaging — documents, decks, spreadsheets — plus the connectors a consulting engagement usually needs. Per-agent model and effort selection is not confirmed at the same granularity as Claude Code. | Keep the manager framing and the staffing plan, but soften the model-assignment instruction to "assign the strongest available capability where judgment is required and the fastest where retrieval is mechanical." Name the finished artifact and its file type in the Format block — a Word report, a deck, a spreadsheet model — since Cowork can produce it directly rather than returning text to be reformatted. Where the engagement has client-facing output, state the branding and template requirements in Terms. |
| **Plain chat** | No subagent spawning. | Say so plainly. The manager framing still improves structure and forces explicit staffing reasoning, but the team is simulated, not parallelized — the "artifacts" all come from one context. Offer to drop to a Full-tier prompt instead, or to split the work into a numbered sequence of prompts the user runs one at a time. |

**If the user doesn't know, default to Cowork** and say so in the assumptions list. These prompts are built for business and consulting work, where the finished artifact — the report, the deck, the model — is the point, and Cowork produces it directly. Recommend Claude Code only when the user signals that reusability across engagements matters more than packaging: repeated client work, a roster they want version-controlled, or a workflow they intend to turn into a slash command.

### Step 3 — Draft the prompt

Assemble the answers into this structure. Use the labeled format for Standard and Full tiers; collapse to a single tight paragraph for Light. For Orchestrated, use Step 3b instead.

```
ACT: You are [identity] [with this judgment/perspective].

REQUEST: [One strong verb + deliverable].

Context:
- Situation: [what's going on and why]
- Audience: [who reads this and what they care about]
- Background: [facts, source material, prior decisions the AI needs]

TERMS:
- Definitions: [key term] means [definition]. [term] means [definition].
- Conditions: [length, tone, inclusions, exclusions]
- If uncertain: [flag it / ask / label best guess]
- Format: [exact output shape and sections]

[Source material or input pasted here, if any]
```

Writing rules for the draft:
- Positive instructions over negative ones ("write in plain conversational English," not "don't be formal").
- Concrete numbers over adjectives ("under 400 words," not "brief").
- One request per prompt. If the interview surfaced more than one deliverable, split it into as many prompts as the work needs and deliver them as a numbered sequence.
- If the prompt will be reused, add a placeholder in square brackets for the parts that change each run (e.g., `[paste intake notes here]`) and say so.

### Step 3b — Draft the orchestrated prompt

The A of an orchestrated prompt is a **manager**, not a worker. The manager's judgment governs staffing decisions: who gets hired, what each person owns, how much capability each role deserves, and whether the returned work is good enough to use. Write the identity so that it constrains those decisions — a cost-disciplined program manager staffs differently from an academic reviewer.

Everything the user gave you in the interview still applies. It moves into the manager's brief, because the manager writes the workers' instructions.

```
ACT: You are [manager identity] running this as the manager of a team
you staff yourself. [The judgment that governs staffing and review —
e.g. skeptical of unsupported claims, cost-disciplined, unwilling to
let confident prose substitute for evidence.]

REQUEST: Staff and run a team to [the work], then compile
[the single consolidated deliverable].

Context:
- Situation: [what's going on and why]
- Audience: [who reads the final report and what they care about]
- Background: [facts, prior decisions, source material]

TERMS:

Definitions
- [Key domain terms, as in a normal ART prompt]
- "Team member" means one subagent with one narrow deliverable.
- "Artifact" means the written deliverable a team member returns:
  findings, sources with dates, confidence labels, open questions.

Staffing and dispatch
- Decide the team yourself. Between four and seven members. For each,
  define: role title, the single question they own, the deliverable,
  the sources to prioritize, and what is explicitly out of scope.
- Cover these areas in this priority order, weighting the team toward
  the top of the list: [the user's ranked priorities].
- Staff one member as an adversarial reviewer whose only job is to
  attack the other members' findings and argue the opposing case.
- For each member, assess task complexity and assign a model and an
  effort level with a one-line rationale. First confirm which models
  this environment exposes, then assign against this rubric:
  judgment-heavy synthesis and adversarial review go to the strongest
  available model at high effort; standard search-and-summarize
  research goes to a mid-tier model at medium effort; mechanical
  retrieval, extraction, and citation checking go to the fastest model
  at low effort. Do not assign the strongest model by default —
  justify every use of it.
- Present the staffing plan and wait for my approval before
  dispatching. [Include or omit per the user's preference.]
- Give each member a complete, self-contained brief. They cannot see
  this conversation and do not share context with each other.
- Members work independently. Surface conflicts between their findings
  rather than resolving them silently.

Review and synthesis
- Review every artifact before using it. State whether you accepted it,
  accepted it with corrections, or sent it back — and why.
- Reject any finding that rests on an uncited claim, and send that
  member back once with a specific correction request.

If uncertain
- [Confidence labeling and source-citation rule]

Format
1. Staffing plan — table: role, question owned, deliverable, model,
   effort level, rationale
2. Roster status — table: member, artifact accepted / corrected /
   rejected, one-line note
3. [The executive deliverable and its required sections]
4. The adversarial reviewer's strongest objection, stated in full and
   unrebutted, followed by the manager's response
5. Unresolved conflicts between team members, if any
```

Additional rules for orchestrated drafts:
- **Four to seven members.** Fewer and the orchestration overhead isn't worth it; more and the synthesis degrades.
- **Every member owns exactly one question.** If a role's brief contains "and," split it or cut it.
- **Always include the adversarial reviewer.** A team of researchers all briefed on the same premise will confirm it. The reviewer is what makes the output trustworthy.
- **Make the model rubric a rule, not a suggestion.** Without "justify every use of the strongest model," the manager assigns it to everyone and the cost advantage disappears.
- **Name the isolation explicitly.** Subagents start with a fresh context and cannot see the parent conversation. If the manager writes thin briefs, the workers produce generic output — this is the single most common orchestration failure.

### Step 4 — Deliver with the diagnostic key

Present the finished prompt, then add two short things:

1. **Assumptions made** (if any) — one line each, inviting correction. For Orchestrated prompts, include the environment assumption.
2. **The diagnostic key** — teach the user how to debug the prompt themselves:

| If the output is... | Fix this letter |
|---|---|
| Right facts, wrong instincts — too generic, wrong priorities, wrong skepticism | **A** — sharpen the identity's judgment |
| Wandering, doing too many things, or the wrong thing | **R** — tighten the verb and deliverable |
| Right substance, wrong for the audience | **R** (Context) — add situation/audience detail |
| Confidently wrong on specifics, or wrong shape/length/tone | **T** — define the term or add the condition |
| *(Orchestrated)* Team members return shallow or overlapping work | **A** — the manager's staffing judgment is too loose, or the briefs are too thin |
| *(Orchestrated)* Every member got assigned the top model | **T** — the model rubric needs "justify every use" as a hard condition |
| *(Orchestrated)* The report reads as consensus with no tension | **T** — the adversarial reviewer's role is missing or under-specified |

Offer one round of revision: "Run it and tell me what's off — name the symptom and we'll fix the letter."

## Worked example — Standard tier

**User's high-level task:** "I need a prompt to review vendor proposals."

**Interview (one batch):** Who should the AI act as, and how skeptical? What's the deliverable — a summary, a score, a list of questions? Who reads the review? What counts as a "red flag" for you? Length and format?

**Answers:** Shop foreman perspective, very skeptical of software vendors. Deliverable: the top questions to ask before signing. Audience: the owner. Red flag = anything promised without a named feature in the document. Keep it to one page, practical concerns only.

**Delivered prompt:**

```
ACT: You are an experienced shop foreman who has seen software purchases
fail. You are skeptical of vendor promises and care only about whether
this will work on the floor.

REQUEST: Review the vendor proposal below and list the three most
important questions to ask the vendor before signing.

Context:
- Situation: A 40-person machining shop evaluating its first AI tool
  purchase; a previous software purchase went unused.
- Audience: The owner — practical, time-poor, burned before.
- Background: Only the attached proposal is in scope.

TERMS:
- Definitions: A "red flag" is any promised outcome not tied to a named
  feature in the document.
- Conditions: Practical concerns only — not pricing. Each question under
  two sentences, with one line on why it matters.
- If uncertain: If the proposal is ambiguous on a point, turn the
  ambiguity itself into one of the questions.
- Format: Numbered list of exactly three questions, each followed by a
  one-line "why this matters."

[paste vendor proposal here]
```

## Worked example — Orchestrated tier

**User's high-level task:** "Research whether a tutoring marketplace with AI test prep is a real opportunity."

**Sizing:** Passes all three orchestration tests — the work splits cleanly into competitive landscape, efficacy research, regulatory review, and unit economics; those need different expertise; and reconciling them is real work. Orchestrated tier.

**Interview:** Full-tier A/R/T questions, plus: which risk areas matter most, in order? And the environment question — Claude Code, Cowork, or chat?

**Answers:** Skeptical operator-investor. Ranked: AI defensibility, then efficacy, then regulatory, then liquidity. No stated preference on environment, so it defaults to Cowork.

**Delivered prompt:** The Step 3b structure, with the manager identity carrying the investor's skepticism, the four ranked areas becoming the staffing priority order, an adversarial reviewer briefed to argue no-go, and the capability-assignment rubric in its Cowork phrasing. The Format block names the deliverable as a formatted report with the unit economics as a linked spreadsheet. Assumptions list flags the Cowork default and notes that Claude Code is the better call if this research pattern will be rerun across multiple client engagements.

## Edge cases

- **User pastes an existing prompt and asks to improve it:** Map its pieces onto A, R, and T; report which letters are strong, thin, or missing; interview only for the gaps; return the rebuilt prompt with a one-line before/after note per letter.
- **The task is really more than one task:** Say so plainly, then break the request into as many prompts as it takes to satisfy it properly — two, three, or more. Do not force multiple deliverables into one prompt to keep the count down, and do not ask the user to pick just one. Build the full set, numbered in run order, and for each one state what it produces and what it needs from the prompt before it. Where a later prompt consumes an earlier prompt's output, put a bracketed placeholder at the handoff point (e.g. `[paste the output of Prompt 1 here]`) and say so in the delivery. If the chain runs past four prompts, flag it — that usually means the request should be scoped down rather than split further. This is common at Orchestrated tier, where research, design, and build are separate engagements rather than one.
- **User asks for an orchestrated prompt for work that doesn't need it:** Say so once, explain the coordination cost, and offer the Full-tier version. If they still want the team, build it — but keep the roster at four.
- **User wants orchestration in a plain chat window:** Deliver the manager prompt with a plain note that the team will be simulated rather than parallelized, and offer the sequenced-prompts alternative.
- **User wants a prompt for a non-Claude model:** The ART structure transfers as-is. Adjust packaging only: Markdown headers for OpenAI models (and skip "think step by step" scaffolding for reasoning models — state the problem cleanly); more literal instructions and more examples for local/open-source models, which need spelled out what frontier models infer. Orchestration instructions do not transfer — check what that platform's agent tooling actually supports before promising a team.
