# Ranking Governance Decision

**Date:** 2026-07-14
**Decision owner:** Program governance (on behalf of Priya Desai, Regional Program Manager, Licensing & Monitoring), based on the analysis in the linked evaluation documents.
**Status:** Approved for production use in `dashboard/index.html` and `scripts/build_centre_summary.py`.

---

## Decision made

**Candidate B is adopted as the production ranking for Capability 4** (Rank centres by repeated non-compliance and enforcement actions):

1. `total_non_compliance_citations` descending
2. highest recorded `Enforcement Action`, by the existing recorded enforcement action order, descending
3. `most_recent_inspection_date` descending — final tiebreaker only

This is a plain, three-key deterministic sort over fields already present in `data/processed/centre-summary.json`. It is not a combined score, not normalized into a probability, and not a prediction. The recorded enforcement action order is a governed project sorting rule for this ranking only — it is not an official severity scale and not a field in the source dataset.

## Candidates considered

- **Candidate A** — highest recorded Enforcement Action first, then citations, then recency.
- **Candidate B** — repeated non-compliance count first, then highest recorded Enforcement Action, then recency. **(Adopted.)**
- **Candidate C** — visits with non-compliance first, then highest recorded Enforcement Action, then recency.

All three remain computed and available as evaluation artifacts in `data/processed/ranking-candidates.json`, each labeled with its `role` (`production` for B, `evaluation_only` for A and C). Their comparison outputs were not deleted.

## Why Candidate B was chosen

- It directly operationalizes "repeated non-compliance," the criterion named first in Story #1's own language (see `knowledge/business-discovery.md`), as the primary sort key, with the recorded enforcement action order as a real secondary factor — a strong enforcement history still matters, it just cannot alone override a low, non-repeating citation count.
- A top-20, staleness-focused review (see `eval/final-ranking-recommendation.md`) found that only **1 of Candidate B's top 20 centres** had gone 10+ months without a new citation, versus **5 of 20 for Candidate A**.
- Candidate B's exposure to inspection-volume bias is no worse than Candidate C's (correlation with total inspection visits: B ≈0.73 vs. C ≈0.79; top-20 median visit count: B 16.5 vs. C 20.0) — so choosing C over B for volume-bias reasons would not actually have helped.

## Why A and C were rejected as the production ranking

- **Candidate A** lets a single old, severe enforcement action dominate the ranking regardless of how long ago it happened, with no ongoing pattern required. Its top 2 centres (both "LITTLE SCHOLARS" entities) had no new citation in roughly 16 months and rank #1/#2 solely because a `LICENCE CANCELLATION` outranks every other category — and the dataset has no licence-status field, so it cannot even be confirmed whether that centre is still operating. This is a structural risk of using enforcement tier as the *primary* key rather than citation repetition.
- **Candidate C** does not reduce inspection-volume bias relative to B (see correlation figures above) and, by weighting breadth of bad visits over raw citation count, it discounts centres with a serious, recent, but visit-concentrated problem (e.g., a centre with 23 citations from only 2 visits drops from B's rank 6 to C's rank 458) — a real risk of under-prioritizing an acute, recent case.

## Actionable-centre rule (retained, governance rule)

`total_non_compliance_citations > 0 OR highest_enforcement_action != NONE` — a centre must satisfy at least one to appear in the default Priority Follow-Up List.

Verified directly against `data/processed/centre-summary.json`: zero centres currently satisfy one condition without the other (the two are always equivalent today, mirroring the row-level `Non Compliance`/`Enforcement Action` pairing already documented in `knowledge/dataset-assessment.md`). The rule is retained in its `OR` form rather than simplified to a single condition, specifically so it stays correct if a future data extract ever breaks that pairing. **This is an explicit governance rule — do not narrow it to a single condition without revisiting this decision.**

## Known limitations (carried forward, not resolved by this decision)

- **Inspection-volume bias** — the production ranking still correlates with how often a centre has been inspected (≈0.73 with `total_inspection_visits`), not independently with how serious its situation is. A centre visited only once or twice cannot rank highly regardless of severity.
- **Same-visit citation inflation** — a single visit that produces many citations at once counts the same as many separate bad visits (e.g., one centre's 23 citations came from only 2 visits). Candidate B is exposed to this, though less broadly than the dataset as a whole (about 14% of actionable centres show a citations-per-bad-visit ratio of 3 or higher).
- **Recency as tiebreaker only** — none of the three candidates, including the adopted one, treat "how long ago" as a primary ranking factor; it only breaks ties between otherwise-equal centres.
- **Recorded enforcement action order is a governed sorting rule, not a dataset field or an official severity scale** — it is the fixed category order already established in `CLAUDE.md` / `capability-map.md` (Notice of Non-Compliance → Order to Remedy → Variation of Licence Provisions → Conditions on Licence → Probationary Licence → Licence Suspension → Licence Cancellation), used here for ordering only.

## Human-in-the-loop statement

This ranking produces a triage order, not a directive. Per `CLAUDE.md`'s Human in the Loop section, **Priya (and her program) still make the final follow-up decision** — whether and when to dispatch an inspector, how to weigh a centre's position against context the dataset doesn't capture, and whether any listed centre actually warrants action. The dashboard states this plainly next to the Priority Follow-Up List.

## Links

- [eval/ranking-candidate-comparison.md](../eval/ranking-candidate-comparison.md) — initial top-10 comparison and draft recommendation.
- [eval/final-ranking-recommendation.md](../eval/final-ranking-recommendation.md) — full top-20 governance review that produced this decision.
