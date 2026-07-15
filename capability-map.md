# Capability Map

Grounded in [knowledge/dataset-assessment.md](knowledge/dataset-assessment.md) and [knowledge/business-discovery.md](knowledge/business-discovery.md). This maps only the capabilities required to support one decision — nothing is added because the data happens to allow it.

**Primary user:** Priya Desai, Regional Program Manager, Licensing & Monitoring
**Primary decision:** *"Which licensed child care centres should inspectors follow up on first?"*

Implementation form options: **Native action** (direct, on-demand operation triggered per request) · **Fixed pipeline** (deterministic, repeatable, rule-based transformation) · **Connector** (integration that pulls/refreshes data from an external source) · **Subagent** (LLM-based reasoning over language/judgment that can't be reduced to a fixed rule).

---

## Capabilities

### 1. Ingest inspection records
**Why it matters:** Priya's decision depends on the full inspection history, not a one-time snapshot — the dataset assessment (Q9) found the extract already spans 18 months and updates by adding new inspection rows over time, so the tool needs a repeatable way to bring in the current extract.
**Form:** Connector
**Why this form:** The source is a periodically-published open data extract, not a static file that only ever gets read once. A connector supports pulling refreshed extracts as they're published, which a one-off manual load cannot.

### 2. Normalize records
**Why it matters:** The assessment found concrete data-quality issues that would distort any rollup if left as-is: 135 exact duplicate rows, a literal `"NULL"` string used instead of a true blank in `Remedy Date` and some `Inspection Date` values, and one `Program ID` recorded under two different `Program Name` values.
**Form:** Fixed pipeline
**Why this form:** These are deterministic, rule-based corrections (drop exact duplicates, treat `"NULL"` as missing, key on `Program ID` rather than `Program Name`) that must be applied identically every time — no judgment or interpretation is involved.

### 3. Aggregate per-centre compliance history
**Why it matters:** The raw grain is one row per violation-or-clean-visit; Priya's decision is at the centre level. Rows must be rolled up per `Program ID` into a per-centre history before any prioritization is possible.
**Form:** Fixed pipeline
**Why this form:** Grouping rows by `Program ID` and summarizing `Non Compliance` occurrences, `Enforcement Action` values, and `Inspection Date` recency is a deterministic aggregation — the same input always produces the same rollup.

### 4. Rank centres by repeated non-compliance and enforcement actions
**Why it matters:** This is the direct operationalization of the primary decision and of Story #1 — surfacing which centres show repeated `Non Compliance` citations and the strongest `Enforcement Action` already recorded against them, so follow-up effort goes there first.
**Form:** Fixed pipeline
**Why this form:** The `Enforcement Action` field already contains a fixed vocabulary (Notice of Non-Compliance → Order to Remedy → Variation of Licence Provisions → Conditions on Licence → Probationary Licence → Licence Suspension → Licence Cancellation) in which later actions represent a stronger regulatory response than earlier ones. Centres whose recorded history includes one of these higher actions are given greater priority than centres with only lower ones, and "repeated" is just a count of rows per `Program ID`. Ordering by an existing categorical field and a count is deterministic — no severity score or model needs to be invented.

**Approved production ordering (Candidate B):** following the governance review in [eval/final-ranking-recommendation.md](eval/final-ranking-recommendation.md) (see also [logs/ranking-governance-decision.md](logs/ranking-governance-decision.md)), the deterministic sort actually used is:
1. `total_non_compliance_citations` descending
2. highest recorded `Enforcement Action`, by the recorded enforcement action order above (not an official severity scale), descending
3. `most_recent_inspection_date` descending — final tiebreaker only

Candidates A and C from the same review remain available only as evaluation artifacts (`data/processed/ranking-candidates.json`); they do not drive the production list.

### 5. Filter and segment the centre list
**Why it matters:** Priya's region covers specific cities/communities (per her persona), and the dataset carries `Program City`, `Type of Program`, and the service-type flags (`Day Care Y/N`, `Out of School Care Y/N`, `Preschool Y/N`) — she needs to narrow the ranked list to her own scope of responsibility.
**Form:** Native action
**Why this form:** Filtering a list by a field value is a simple, on-demand query with no multi-step transformation or judgment — it doesn't need a pipeline or a subagent, just a direct action against already-aggregated data.

### 6. Detect follow-up gaps after enforcement
**Why it matters:** This is Story #2 — flagging centres where an `Order to Remedy` (or stronger action) has a `Remedy Date` on record but no later `Inspection Date` row appears for that `Program ID`, which is a directly observable gap in the record, not an inferred risk.
**Form:** Fixed pipeline
**Why this form:** Comparing a `Remedy Date` against the set of subsequent `Inspection Date` values for the same `Program ID` is a deterministic date comparison — it either finds a later row or it doesn't.

### 7. Explain why a centre is prioritized
**Why it matters:** `Non Compliance` is free text with 178 distinct values recorded across the dataset. A ranked list or count tells Priya *that* a centre ranks high, but she also needs to understand *why* it landed near the top of the list — which citations and enforcement actions drove its position — without reading every row herself.
**Form (as implemented):** Fixed pipeline — a deterministic template.
**Why this form:** The shipped implementation (`dashboard/index.html`, `buildCentreExplanation()`) generates its opening sentence, supporting facts, and closing limitation entirely from the pre-approved aggregated fields (citation count, visits with a citation, highest recorded Enforcement Action, inspection/citation dates, reactive-visit counts) — it never reads or concatenates the free-text `Non Compliance` field, so the phrasing-variance problem a naive template would hit (see "Forms considered but rejected" below) doesn't arise. The same input always produces the same explanation, with no LLM call.
**Possible future enhancement:** a Subagent remains a reasonable next step if Priya later wants the explanation to draw on the free-text `Non Compliance` detail itself (e.g., summarizing *what* was cited, not just *how many times*) rather than only the structured counts and categories used today. That would require revisiting this capability's form, not changing today's deterministic template silently.

### 8. Answer ad hoc questions about specific centres or the ranking
**Why it matters:** Priya will not only want the standing ranked list — she will ask follow-up questions in the moment (e.g., "why does this centre rank where it does," "what changed for this centre since last cycle") that can't all be anticipated as fixed reports.
**Form:** Subagent
**Why this form:** These are open-ended, natural-language questions grounded in the same aggregated data (Capabilities 3–4) rather than fixed report shapes — a subagent can interpret the question and answer from the existing rollup, whereas a fixed pipeline would need one hardcoded report per possible question.

---

## Build First

**Capability 4 — Rank centres by repeated non-compliance and enforcement actions.**

This is the capability that *is* the primary decision: everything else either feeds it (ingest, normalize, aggregate) or is built on top of it (filtering, gap detection, narrative summary, ad hoc Q&A). Capabilities 1–3 are necessary plumbing, but they produce no value on their own — Priya cannot act on raw or merely aggregated rows. The ranking is the first point where the tool produces something she can actually use to decide who gets followed up on first, so it is the capability to prove out before investing in the supporting narrative and Q&A layers.

---

## Forms considered but rejected

- **Subagent for ranking (Capability 4):** considered, because an LLM could plausibly read through a centre's rows and judge its priority. Rejected — ranking depends only on an existing ordered category (`Enforcement Action`) and a row count (`Non Compliance` occurrences), both of which are fully deterministic. Using a subagent here would make the ranking non-reproducible and harder to audit for no added benefit.
- **Fixed pipeline concatenating raw citation text (Capability 7):** considered, e.g., a template that concatenates each citation's free-text `Non Compliance` description. Rejected — the 178 distinct texts vary too much in phrasing and detail to read well when simply concatenated. This is a different, narrower design than the template actually implemented: the shipped Capability 7 template never touches `Non Compliance` free text at all, generating its explanation only from structured aggregate fields (counts, categories, dates), which sidesteps the concatenation problem entirely. A Subagent remains the fallback if a future version needs to synthesize the free-text detail itself.
- **Native action for ingestion (Capability 1):** considered, i.e., a single manual file load done once. Rejected — the dataset assessment found the extract already reflects ~18 months of accumulating history and is likely to be republished over time, so a repeatable connector is needed rather than a one-time load.
- **Connector to an inspector scheduling or case-management system:** considered, since Priya's real-world workflow presumably involves assigning inspectors to visits. Rejected as out of scope — the dataset has no inspector identity, scheduling, or case-status fields at all, so building a connector to a system that isn't represented in the data would be inventing a capability the data can't support.
- **Predictive risk-scoring capability:** considered, since "which centres to prioritize" sounds like a natural fit for a risk model. Rejected — there is no severity rating, no labeled outcome, and no enrollment/incident-rate field to train or validate a model against; anything presented as a predicted risk score would be fabricated rather than derived from the data. Ranking (Capability 4) uses only the categorical/count facts that already exist.
