# Project Objective

**User:** Priya Desai, Regional Program Manager, Licensing & Monitoring, Alberta Children's Services.
**Decision:** *"Which licensed child care centres should inspectors follow up on first?"*
**Purpose:** this workspace turns the raw Alberta child care inspection extract into a centre-level view that lets Priya prioritize inspector follow-up using only the compliance history the data actually records.

---

# What Good Looks Like

- Priya can get a current, ranked list of centres by repeated non-compliance and enforcement actions without manually reading raw inspection rows.
- Every position in the ranking and every explanation given to Priya traces back to specific rows (`Program ID`, `Non Compliance`, `Enforcement Action`, `Inspection Date`) — nothing in the output is unverifiable against the source file.
- The ranking reflects the current extract and can be refreshed as new inspection data is published, rather than going stale as a one-time snapshot.
- Priya can filter to her own region/city and service types and still trust that the underlying ranking logic hasn't changed.
- Follow-up gaps (enforcement with no later inspection row) are surfaced as observed facts, not inferred risk.

---

# Scope

**In scope**
- The 8 capabilities defined in [capability-map.md](capability-map.md): ingest, normalize, aggregate per centre, rank by repeated non-compliance and enforcement actions, filter/segment, detect follow-up gaps, explain why a centre is prioritized, and answer ad hoc questions about centres or the ranking.
- Alberta licensed child care centres represented in the open data extract (`Program ID` as the entity key).
- Analysis strictly at the grain and with the fields confirmed in [dataset-assessment.md](knowledge/dataset-assessment.md).

**Out of scope**
- Any predictive model, risk score, or likelihood estimate — no field in the dataset supports one.
- Inspector assignment, scheduling, or case management — the dataset has no inspector identity or case-status fields.
- Determining whether a violation is legally "resolved" or "closed" — no such field exists; only `Remedy Date` presence/absence can be reported.
- Parent-facing centre lookup, enrollment/utilization analysis, or multi-site/ownership grouping — none of these are supported by fields in the dataset.
- Dashboard/UI design and implementation code — not part of this document.

---

# Data

- **Source:** `data/raw/child-care-open-data-202512.csv` — an Alberta Children's Services child care licensing/inspection open data extract.
- **Update frequency:** the extract already spans roughly 18 months (2024-07-02 to 2025-12-23) and grows by appending new inspection rows and by filling in previously blank fields (e.g., `Remedy Date`) over time. It is not a single-month snapshot; ingestion must support pulling refreshed extracts, not a one-time load.
- **Grain:** one row = one non-compliance citation tied to a specific inspection visit, identified by (`Program ID`, `Inspection Date`, `Inspection Reason`). A visit with no violation produces exactly one row with blank `Non Compliance`/`Enforcement Action`/`Remedy Date`.
- **Important limitations:**
  - No inspector identity or inspecting office/region field.
  - No severity rating — `Enforcement Action` is a fixed, ordered category, not a numeric score.
  - No open/closed case-status field — only whether a `Remedy Date` is present.
  - No enrollment/attendance data — only licensed `Capacity`.
  - No licence start date or unique visit ID; the (`Program ID`, `Inspection Date`, `Inspection Reason`) composite key is not guaranteed unique (135 exact duplicate rows found; 39 rows with a literal `"NULL"` `Inspection Date`).
  - `Remedy Date` and some `Inspection Date` values use the literal string `"NULL"` rather than a true blank.
  - One `Program ID` is recorded under two different `Program Name` values — always resolve identity by `Program ID`.

---

# Capabilities

Defined and rationalized in full in [capability-map.md](capability-map.md). Names and forms below must not be changed without updating the capability map first.

| # | Capability | Form |
|---|---|---|
| 1 | Ingest inspection records | Connector |
| 2 | Normalize records | Fixed pipeline |
| 3 | Aggregate per-centre compliance history | Fixed pipeline |
| 4 | Rank centres by repeated non-compliance and enforcement actions | Fixed pipeline |
| 5 | Filter and segment the centre list | Native action |
| 6 | Detect follow-up gaps after enforcement | Fixed pipeline |
| 7 | Explain why a centre is prioritized | Fixed pipeline (deterministic template) — a Subagent remains a possible future enhancement; see capability-map.md |
| 8 | Answer ad hoc questions about specific centres or the ranking | Subagent (not yet implemented) |

Build order starts at Capability 4 (ranking) — see capability-map.md's "Build First" section for the reasoning.

**Production ranking (Capability 4 — approved):** Candidate B is the approved production ranking, chosen as a human governance decision documented in [eval/final-ranking-recommendation.md](eval/final-ranking-recommendation.md) and [logs/ranking-governance-decision.md](logs/ranking-governance-decision.md). Exact sort order:
1. `total_non_compliance_citations` descending
2. highest recorded `Enforcement Action`, by the existing category order (the *recorded enforcement action order* — this is a governed project sorting rule, not an official severity scale or a field in the source data), descending
3. `most_recent_inspection_date` descending, as the final tiebreaker only

Candidates A and C remain available only as evaluation artifacts (`data/processed/ranking-candidates.json`) and are not used to drive the production list.

**Actionable-centre rule (governance rule):** a centre appears in the default Priority Follow-Up List only if `total_non_compliance_citations > 0` OR `highest_enforcement_action != NONE`. The two conditions are currently always equivalent in the data, but the `OR` form is kept deliberately rather than simplified, in case a future extract breaks that pairing.

**Known limitations of the production ranking (documented, not corrected):**
- Inspection-volume bias — the ranking correlates with how often a centre has been inspected, not independently with how serious its situation is.
- Same-visit citation inflation — one visit that produces many citations at once counts the same as many separate bad visits.
- Recency is used only as a final tiebreaker, never as a primary ranking factor.
- Priya still makes the final follow-up decision — the ranking is a triage order, not a directive (see Human in the Loop below).

---

# Human in the Loop

The following remain Priya's (or her team's) decisions, never the workspace's:
- Whether and when to actually dispatch an inspector to a flagged centre.
- How to weigh a centre's ranking against context the dataset doesn't capture (e.g., local operational knowledge).
- Whether a follow-up gap (Capability 6) warrants action or has a legitimate explanation not visible in the data.
- Final judgment on any explanation the workspace provides (Capability 7/8) — the workspace explains what the data shows; it does not decide what Priya should do about it.

The workspace's role is limited to surfacing, ranking, and explaining what is already recorded — it does not make the follow-up decision itself.

---

# Must Never Produce

- Invented risk scores, probabilities, or likelihood language not derived from an existing field.
- A severity rating beyond the existing `Enforcement Action` category order — no numeric or invented severity scale.
- Claims that a violation is "resolved," "closed," or "compliant now" — no such status field exists; only `Remedy Date` presence can be stated.
- Fabricated inspector names, identities, or scheduling information.
- Explanations (Capability 7/8) that reference rows, dates, or violations not actually present in the source data for that centre.
- Enrollment, attendance, or capacity-utilization claims — only licensed `Capacity` exists, not actual attendance.
- Ownership/chain groupings across centres — no such field exists.
- Predictions about future inspections, violations, or enforcement outcomes.

---

# Knowledge

This workspace's reasoning is grounded in three documents, in this order of authority:
1. [knowledge/dataset-assessment.md](knowledge/dataset-assessment.md) — what the data actually contains and its limitations.
2. [knowledge/business-discovery.md](knowledge/business-discovery.md) — the user, the decision, the pain point, and the persona.
3. [capability-map.md](capability-map.md) — the capabilities required to support the decision and their implementation form.

Any new capability, field, or business rule must first be justified against these documents before being added here.

---

# Skills

Only the skills needed to support the 8 capabilities above — none are implemented here:
- **Extract refresh:** pulling/reloading the published open data extract (supports Capability 1).
- **Record normalization:** deduplication and null-marker handling per the rules in Data limitations above (supports Capability 2).
- **Per-centre rollup:** grouping rows by `Program ID` into a compliance history (supports Capability 3).
- **Ranking:** ordering centres by repeated `Non Compliance` count and highest `Enforcement Action` category (supports Capability 4).
- **Filtering/query:** narrowing the ranked list by `Program City`, `Type of Program`, or service-type flags (supports Capability 5).
- **Gap detection:** comparing `Remedy Date` against subsequent `Inspection Date` values per `Program ID` (supports Capability 6).
- **Grounded explanation:** producing a plain-language explanation of a centre's ranking from its own rows only (supports Capability 7).
- **Grounded Q&A:** answering centre/ranking questions from the aggregated data only, with no external or invented information (supports Capability 8).

---

# Governance

Deterministic fixed pipelines (Capabilities 1–4, 6) are the system of record: they produce the ingestion, normalization, aggregation, ranking, and gap-detection outputs, and the same input always produces the same output. These are the only components allowed to compute the ranking or determine what counts as a follow-up gap.

Capabilities 7 and 8 sit strictly on top of those outputs — they may read and explain what the fixed pipelines have already computed, in natural language, but they do not recompute the ranking, alter the enforcement-action ordering, or introduce information not present in the underlying rows. Capability 7 is currently implemented as a deterministic template (a Fixed pipeline in form, not a Subagent) generating its explanation only from the aggregated facts already produced by Capabilities 3–4; a Subagent remains a possible future enhancement if a richer, free-text-aware explanation is wanted later (see capability-map.md). Capability 8 is designed as a Subagent and is not yet implemented. Native action (Capability 5) operates directly on the aggregated output for simple filtering and does not sit in the deterministic computation path.

This separation keeps the ranking itself fully auditable back to source rows at all times, while confining language-based interpretation to explanation and question-answering — never to computation.

**Ranking governance:** Capability 4's production ranking (Candidate B, see above) was selected through an explicit governance review, not decided by the pipeline itself — see [eval/ranking-candidate-comparison.md](eval/ranking-candidate-comparison.md), [eval/final-ranking-recommendation.md](eval/final-ranking-recommendation.md), and [logs/ranking-governance-decision.md](logs/ranking-governance-decision.md) for the full trail. Candidates A and C are retained as evaluation artifacts so the decision remains auditable, but only Candidate B drives what Priya sees by default. No candidate combines its inputs into a single score, probability, or prediction, and none is described as an official severity scale.
