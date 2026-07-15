# Ranking Candidate Comparison

Computed from the real, normalized dataset by [scripts/build_centre_summary.py](../scripts/build_centre_summary.py), output as [data/processed/ranking-candidates.json](../data/processed/ranking-candidates.json). Grounded in [CLAUDE.md](../CLAUDE.md) and [capability-map.md](../capability-map.md) — Capability 4: *"Rank centres by repeated non-compliance and enforcement actions."*

No candidate below combines its inputs into a single number, normalizes anything into a probability, or claims to be objectively correct. Each is a plain, fully-transparent sort over fields that already exist in the data. **Choosing one as final is a human governance decision, made by Priya/the program, not by this pipeline.**

**Superseded:** the recommendation below (Candidate A) was the initial, top-10-only read of Story #1 and has since been revised. See [eval/final-ranking-recommendation.md](final-ranking-recommendation.md) for the full top-20 governance review and [logs/ranking-governance-decision.md](../logs/ranking-governance-decision.md) for the adopted decision (Candidate B). This document is kept as the historical record of the initial comparison, not the current recommendation.

Data as of: pipeline run against `data/raw/child-care-open-data-202512.csv` (2,913 centres, inspection dates 2024-07-02 to 2025-12-23). See `data/processed/pipeline-audit.json` for the full audit trail.

---

## Candidate A — Recorded enforcement action first

**Exact sort order:** highest recorded `Enforcement Action` category (descending, using the fixed order Notice → Order to Remedy → Variation → Conditions → Probationary → Suspension → Cancellation) → then total non-compliance citations (descending) → then most recent inspection date (descending, as a tiebreaker only).

**Top 10:**

| Rank | Centre | City | Citations | Highest Enforcement Action | Last Inspection |
|---|---|---|---|---|---|
| 1 | LITTLE SCHOLARS DAYCARE ECS LTD. | Calgary | 13 | LICENCE CANCELLATION | 2025-12-02 |
| 2 | LITTLE SCHOLARS DAYCARE INC. | Calgary | 10 | LICENCE CANCELLATION | 2025-12-02 |
| 3 | HINTON CHILDREN'S LEARNING CENTRE | Hinton | 26 | LICENCE SUSPENSION | 2025-12-09 |
| 4 | HAPPY HOUSE DAYCARE (SOUTH) | Cold Lake | 19 | LICENCE SUSPENSION | 2025-12-10 |
| 5 | ZEBRA CROSSING ACADEMY | Calgary | 14 | LICENCE SUSPENSION | 2025-12-15 |
| 6 | ST. ALBERT DAY CARE CENTRE | St. Albert | 11 | LICENCE SUSPENSION | 2025-11-26 |
| 7 | PACESETTERS EARLY LEARNING AND CHILDCARE CENTRE | Fort McMurray | 3 | LICENCE SUSPENSION | 2025-09-19 |
| 8 | LITTLE STARS MONTESSORI EARLY LEARNING CENTER | Spruce Grove | 44 | PROBATIONARY LICENCE | 2025-11-03 |
| 9 | PLAY 'N' FUN DAY CARE LTD. | Edmonton | 35 | PROBATIONARY LICENCE | 2025-09-17 |
| 10 | ALOTTA FUN CHILDCARE OSC | Edmonton | 18 | PROBATIONARY LICENCE | 2025-10-09 |

---

## Candidate B — Repeated non-compliance first

**Exact sort order:** total non-compliance citations (descending) → then highest recorded `Enforcement Action` category (descending) → then most recent inspection date (descending, tiebreaker only).

**Top 10:**

| Rank | Centre | City | Citations | Visits with a citation | Highest Enforcement Action | Last Inspection |
|---|---|---|---|---|---|---|
| 1 | LITTLE STARS MONTESSORI EARLY LEARNING CENTER | Spruce Grove | 44 | 11 | PROBATIONARY LICENCE | 2025-11-03 |
| 2 | PLAY 'N' FUN DAY CARE LTD. | Edmonton | 35 | 14 | PROBATIONARY LICENCE | 2025-09-17 |
| 3 | INNER GARDEN BILINGUAL DAYHOME AGENCY | Calgary | 34 | 10 | ORDER TO REMEDY | 2025-11-17 |
| 4 | CIRCLE SQUARE CHILDCARE | Red Deer | 28 | 6 | ORDER TO REMEDY | 2025-10-17 |
| 5 | HINTON CHILDREN'S LEARNING CENTRE | Hinton | 26 | 9 | LICENCE SUSPENSION | 2025-12-09 |
| 6 | MILESTONES OUT OF SCHOOL CARE | Devon | 23 | 2 | ORDER TO REMEDY | 2025-11-13 |
| 7 | STEPPING STONE ACADEMY DEVELOPMENT CENTER HAMPTON LTD. | Edmonton | 23 | 5 | ORDER TO REMEDY | 2025-07-16 |
| 8 | MILESTONES DAYCARE AND EARLY LEARNING | Calgary | 22 | 6 | CONDITIONS ON LICENCE | 2025-11-17 |
| 9 | CONNECTING DOTS-DAVE BARR | Grande Prairie | 22 | 7 | VARIATION OF LICENCE PROVISIONS | 2025-11-12 |
| 10 | FUN KIDS CLUB CALGARY | Calgary | 20 | 6 | ORDER TO REMEDY | 2025-12-09 |

---

## Candidate C — Breadth of visits with non-compliance first

**Exact sort order:** number of distinct inspection visits that had at least one non-compliance citation (descending) → then highest recorded `Enforcement Action` category (descending) → then most recent inspection date (descending, tiebreaker only).

**Top 10:**

| Rank | Centre | City | Visits with a citation | Citations | Highest Enforcement Action | Last Inspection |
|---|---|---|---|---|---|---|
| 1 | PLAY 'N' FUN DAY CARE LTD. | Edmonton | 14 | 35 | PROBATIONARY LICENCE | 2025-09-17 |
| 2 | BRIGHTPATH WINDERMERE | Edmonton | 12 | 16 | ORDER TO REMEDY | 2025-12-11 |
| 3 | LITTLE STARS MONTESSORI EARLY LEARNING CENTER | Spruce Grove | 11 | 44 | PROBATIONARY LICENCE | 2025-11-03 |
| 4 | INNER GARDEN BILINGUAL DAYHOME AGENCY | Calgary | 10 | 34 | ORDER TO REMEDY | 2025-11-17 |
| 5 | HINTON CHILDREN'S LEARNING CENTRE | Hinton | 9 | 26 | LICENCE SUSPENSION | 2025-12-09 |
| 6 | TLC DAYCARE | St. Paul | 9 | 17 | VARIATION OF LICENCE PROVISIONS | 2025-12-16 |
| 7 | GROWING MIRACLES CHILDCARE AND EARLY LEARNING LTD | Airdrie | 9 | 14 | ORDER TO REMEDY | 2025-11-25 |
| 8 | ASPEN LAKES DISCOVERY CENTER LTD. | Blackfalds | 9 | 13 | ORDER TO REMEDY | 2025-10-21 |
| 9 | ST. ALBERT DAY CARE CENTRE | St. Albert | 8 | 11 | LICENCE SUSPENSION | 2025-11-26 |
| 10 | EVANSPARK ELCC ACADEMY | Calgary | 8 | 15 | VARIATION OF LICENCE PROVISIONS | 2025-12-11 |

---

## Major differences between candidates

- **Candidates B and C largely agree** (7 of the top 10 centres overlap), because both are driven primarily by how much non-compliance a centre has accumulated, differing only in whether repeated citations *within the same visit* count extra (B) or only the *number of distinct bad visits* counts (C). PLAY 'N' FUN DAY CARE LTD. and LITTLE STARS MONTESSORI top both.
- **Candidate A diverges sharply from B/C.** Its #1 and #2 (LITTLE SCHOLARS DAYCARE ECS LTD. / INC., both Calgary) have only 13 and 10 citations respectively — far below LITTLE STARS MONTESSORI's 44 or PLAY 'N' FUN's 35 — but rank above them because a `LICENCE CANCELLATION` outranks a `PROBATIONARY LICENCE` regardless of citation volume. Under A, a centre with very few citations but one severe enforcement action jumps ahead of centres with much larger, ongoing citation counts.
- **PACESETTERS EARLY LEARNING AND CHILDCARE CENTRE (Candidate A, rank 7)** is the clearest illustration: only 3 citations total, but ranks above every centre in B/C's top 10 because its one enforcement action was a `LICENCE SUSPENSION`. Candidate A treats "one severe action" as more important than "many smaller, ongoing citations" — a real and defensible interpretation of the primary decision, but a different one than B/C.

## Possible bias — especially inspection-volume bias

We checked whether centres simply visited more often look worse under B/C purely because they had more chances to be cited, independent of any real behavior difference:

- Across all 2,913 centres, the correlation between `total_inspection_visits` and `total_non_compliance_citations` is **≈0.73** — a strong positive relationship. Centres with 2 or fewer visits average 0.2 citations; centres with 10+ visits average 8.9 citations.
- In the raw top-10-by-citation-count list, visit counts range from 5 to 34 — e.g., MILESTONES OUT OF SCHOOL CARE has 23 citations from only 5 visits (a high citation-per-visit rate), while PLAY 'N' FUN DAY CARE LTD. has 35 citations from 34 visits (roughly one per visit, on average, spread across a much longer inspection history).
- **This means Candidates B and C are biased toward centres that have simply been inspected more (often because they are the subject of repeat complaints or follow-ups), not necessarily toward centres with the worst citation *rate*.** A centre inspected once with 2 citations and a centre inspected 20 times with 2 citations look identical under B, even though the second centre's rate of new problems per visit is far lower.
- **Candidate A is less exposed to this bias** because it is driven first by the single most severe action on record, which does not mechanically increase with visit count the way a citation count does — though it still uses citation count as its second sort key, so the bias reappears among centres that tie on enforcement action.
- None of the three candidates correct for this — doing so (e.g., a citation-per-visit rate) was not requested and would introduce a derived ratio metric beyond what was asked for here; it is flagged as a limitation, not fixed.

## Recommendation

**Candidate A best matches Story #1** as recorded in [knowledge/business-discovery.md](../knowledge/business-discovery.md) — "repeated non-compliance **and stronger enforcement actions**," in that order of emphasis on stated language, treating the regulator's own escalating response as the primary signal of how seriously a centre's situation has already been judged, with repetition as the tiebreaker rather than the leading factor.

That said, this is a judgment call, not a derived fact:
- Candidate B is a legitimate alternative if the priority is "don't let volume of ongoing problems get buried by a single old severe action."
- Candidate C is close to B but slightly better isolates centres with *persistent* problems across many visits, as opposed to one visit generating many citations at once.

**This document does not select a final ranking.** Per CLAUDE.md's Human in the Loop section, which candidate — or whether to blend criteria differently — is a decision for Priya and her program to make explicitly, not something this pipeline decides on its own. That decision has since been made — see [logs/ranking-governance-decision.md](../logs/ranking-governance-decision.md) for the adopted candidate and [eval/final-ranking-recommendation.md](final-ranking-recommendation.md) for the analysis behind it.
