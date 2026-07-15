# Final Ranking Recommendation

Governance review, not an implementation change. Extends [eval/ranking-candidate-comparison.md](ranking-candidate-comparison.md) with a full top-20 comparison across five fields, per governance request. Grounded in [CLAUDE.md](../CLAUDE.md), [capability-map.md](../capability-map.md), [knowledge/business-discovery.md](../knowledge/business-discovery.md), and computed directly from [data/processed/centre-summary.json](../data/processed/centre-summary.json) using the same logic as [scripts/build_centre_summary.py](../scripts/build_centre_summary.py) (unchanged by this document).

**This document does not modify the dashboard, the ranking selector, or the pipeline.** It recommends one candidate for review before anything is locked in.

---

## 1. Top 20 under each candidate

Columns: total inspection visits, non-compliance citations, visits with a citation, highest recorded Enforcement Action, most recent inspection, most recent non-compliance citation.

### Candidate A — highest recorded Enforcement Action first, then citations, then recency

| # | Centre | City | Visits | Citations | Visits w/ Citation | Highest Enforcement Action | Last Inspection | Last Citation |
|---|---|---|---|---|---|---|---|---|
| 1 | LITTLE SCHOLARS DAYCARE ECS LTD. | Calgary | 12 | 13 | 4 | LICENCE CANCELLATION | 2025-12-02 | 2024-08-12 |
| 2 | LITTLE SCHOLARS DAYCARE INC. | Calgary | 8 | 10 | 2 | LICENCE CANCELLATION | 2025-12-02 | 2024-08-12 |
| 3 | HINTON CHILDREN'S LEARNING CENTRE | Hinton | 22 | 26 | 9 | LICENCE SUSPENSION | 2025-12-09 | 2025-10-29 |
| 4 | HAPPY HOUSE DAYCARE (SOUTH) | Cold Lake | 22 | 19 | 7 | LICENCE SUSPENSION | 2025-12-10 | 2025-12-10 |
| 5 | ZEBRA CROSSING ACADEMY | Calgary | 23 | 14 | 6 | LICENCE SUSPENSION | 2025-12-15 | 2025-10-23 |
| 6 | ST. ALBERT DAY CARE CENTRE | St. Albert | 17 | 11 | 8 | LICENCE SUSPENSION | 2025-11-26 | 2025-11-26 |
| 7 | PACESETTERS EARLY LEARNING AND CHILDCARE CENTRE | Fort McMurray | 13 | 3 | 1 | LICENCE SUSPENSION | 2025-09-19 | 2025-07-07 |
| 8 | LITTLE STARS MONTESSORI EARLY LEARNING CENTER | Spruce Grove | 22 | 44 | 11 | PROBATIONARY LICENCE | 2025-11-03 | 2025-07-28 |
| 9 | PLAY 'N' FUN DAY CARE LTD. | Edmonton | 34 | 35 | 14 | PROBATIONARY LICENCE | 2025-09-17 | 2025-06-06 |
| 10 | ALOTTA FUN CHILDCARE OSC | Edmonton | 16 | 18 | 5 | PROBATIONARY LICENCE | 2025-10-09 | 2024-09-19 |
| 11 | CLEARWATER DAYCARE AND OUT OF SCHOOL CARE | Edmonton | 17 | 12 | 5 | PROBATIONARY LICENCE | 2025-12-03 | 2025-12-03 |
| 12 | KLORIOUS KIDS DAYCARE | Fort McMurray | 8 | 6 | 2 | PROBATIONARY LICENCE | 2025-11-06 | 2024-11-20 |
| 13 | LAMONT DAYCARE | Lamont | 11 | 5 | 3 | PROBATIONARY LICENCE | 2025-10-15 | 2025-05-01 |
| 14 | MILESTONES DAYCARE AND EARLY LEARNING | Calgary | 25 | 22 | 6 | CONDITIONS ON LICENCE | 2025-11-17 | 2025-10-20 |
| 15 | SUMMIT KIDS - NELLIE | Calgary | 10 | 8 | 2 | CONDITIONS ON LICENCE | 2025-09-26 | 2025-06-17 |
| 16 | WING KEI MONTESSORI SCHOOL | Calgary | 10 | 7 | 1 | CONDITIONS ON LICENCE | 2025-10-03 | 2025-06-12 |
| 17 | KIDS R FUN DAYCARE | Calgary | 12 | 6 | 3 | CONDITIONS ON LICENCE | 2025-10-21 | 2025-10-08 |
| 18 | WHIMSY CHILDCARE | Cold Lake | 10 | 5 | 2 | CONDITIONS ON LICENCE | 2025-11-25 | 2025-09-09 |
| 19 | LITTLE M-DESTINY PRESCHOOL & DAYCARE LTD | Olds | 4 | 1 | 1 | CONDITIONS ON LICENCE | 2025-10-06 | 2025-01-09 |
| 20 | LEARN, LOVE 'N' LAUGH CHILD CARE CENTRE | Devon | 5 | 1 | 1 | CONDITIONS ON LICENCE | 2025-09-19 | 2025-04-22 |

### Candidate B — repeated non-compliance count first, then highest recorded Enforcement Action, then recency

| # | Centre | City | Visits | Citations | Visits w/ Citation | Highest Enforcement Action | Last Inspection | Last Citation |
|---|---|---|---|---|---|---|---|---|
| 1 | LITTLE STARS MONTESSORI EARLY LEARNING CENTER | Spruce Grove | 22 | 44 | 11 | PROBATIONARY LICENCE | 2025-11-03 | 2025-07-28 |
| 2 | PLAY 'N' FUN DAY CARE LTD. | Edmonton | 34 | 35 | 14 | PROBATIONARY LICENCE | 2025-09-17 | 2025-06-06 |
| 3 | INNER GARDEN BILINGUAL DAYHOME AGENCY | Calgary | 17 | 34 | 10 | ORDER TO REMEDY | 2025-11-17 | 2025-11-17 |
| 4 | CIRCLE SQUARE CHILDCARE | Red Deer | 18 | 28 | 6 | ORDER TO REMEDY | 2025-10-17 | 2025-10-02 |
| 5 | HINTON CHILDREN'S LEARNING CENTRE | Hinton | 22 | 26 | 9 | LICENCE SUSPENSION | 2025-12-09 | 2025-10-29 |
| 6 | MILESTONES OUT OF SCHOOL CARE | Devon | 5 | 23 | 2 | ORDER TO REMEDY | 2025-11-13 | 2025-10-28 |
| 7 | STEPPING STONE ACADEMY DEVELOPMENT CENTER HAMPTON LTD. | Edmonton | 10 | 23 | 5 | ORDER TO REMEDY | 2025-07-16 | 2025-02-26 |
| 8 | MILESTONES DAYCARE AND EARLY LEARNING | Calgary | 25 | 22 | 6 | CONDITIONS ON LICENCE | 2025-11-17 | 2025-10-20 |
| 9 | CONNECTING DOTS-DAVE BARR | Grande Prairie | 17 | 22 | 7 | VARIATION OF LICENCE PROVISIONS | 2025-11-12 | 2025-10-20 |
| 10 | FUN KIDS CLUB CALGARY | Calgary | 8 | 20 | 6 | ORDER TO REMEDY | 2025-12-09 | 2025-12-09 |
| 11 | HAPPY HOUSE DAYCARE (SOUTH) | Cold Lake | 22 | 19 | 7 | LICENCE SUSPENSION | 2025-12-10 | 2025-12-10 |
| 12 | RISING PILLARS CHILDCARE | Calgary | 19 | 19 | 7 | ORDER TO REMEDY | 2025-12-04 | 2025-12-04 |
| 13 | THE CHILD CLUB DAYCARE | Stony Plain | 11 | 19 | 6 | ORDER TO REMEDY | 2025-11-28 | 2025-11-28 |
| 14 | ALOTTA FUN CHILDCARE OSC | Edmonton | 16 | 18 | 5 | PROBATIONARY LICENCE | 2025-10-09 | 2024-09-19 |
| 15 | BRIGHT STARS DAYCARE AND OSC | Edmonton | 15 | 18 | 7 | ORDER TO REMEDY | 2025-11-26 | 2025-11-13 |
| 16 | FUELING BRAINS ACADEMY WEST 85TH | Calgary | 15 | 18 | 7 | ORDER TO REMEDY | 2025-11-19 | 2025-11-05 |
| 17 | A2Z KIDZ ED. | Calgary | 13 | 18 | 5 | ORDER TO REMEDY | 2025-09-23 | 2025-08-29 |
| 18 | CREATIVE CHILDREN'S DAY CARE (2003) LTD. | Spruce Grove | 12 | 18 | 6 | ORDER TO REMEDY | 2025-08-13 | 2025-07-11 |
| 19 | ALBERTA CHILDREN PLACE DAYCARE | Cochrane | 12 | 18 | 7 | ORDER TO REMEDY | 2025-07-14 | 2025-07-08 |
| 20 | TLC DAYCARE | St. Paul | 22 | 17 | 9 | VARIATION OF LICENCE PROVISIONS | 2025-12-16 | 2025-12-04 |

### Candidate C — visits with non-compliance first, then highest recorded Enforcement Action, then recency

| # | Centre | City | Visits | Citations | Visits w/ Citation | Highest Enforcement Action | Last Inspection | Last Citation |
|---|---|---|---|---|---|---|---|---|
| 1 | PLAY 'N' FUN DAY CARE LTD. | Edmonton | 34 | 35 | 14 | PROBATIONARY LICENCE | 2025-09-17 | 2025-06-06 |
| 2 | BRIGHTPATH WINDERMERE | Edmonton | 32 | 16 | 12 | ORDER TO REMEDY | 2025-12-11 | 2025-08-08 |
| 3 | LITTLE STARS MONTESSORI EARLY LEARNING CENTER | Spruce Grove | 22 | 44 | 11 | PROBATIONARY LICENCE | 2025-11-03 | 2025-07-28 |
| 4 | INNER GARDEN BILINGUAL DAYHOME AGENCY | Calgary | 17 | 34 | 10 | ORDER TO REMEDY | 2025-11-17 | 2025-11-17 |
| 5 | HINTON CHILDREN'S LEARNING CENTRE | Hinton | 22 | 26 | 9 | LICENCE SUSPENSION | 2025-12-09 | 2025-10-29 |
| 6 | TLC DAYCARE | St. Paul | 22 | 17 | 9 | VARIATION OF LICENCE PROVISIONS | 2025-12-16 | 2025-12-04 |
| 7 | GROWING MIRACLES CHILDCARE AND EARLY LEARNING LTD | Airdrie | 23 | 14 | 9 | ORDER TO REMEDY | 2025-11-25 | 2025-07-18 |
| 8 | ASPEN LAKES DISCOVERY CENTER LTD. | Blackfalds | 11 | 13 | 9 | ORDER TO REMEDY | 2025-10-21 | 2025-10-21 |
| 9 | ST. ALBERT DAY CARE CENTRE | St. Albert | 17 | 11 | 8 | LICENCE SUSPENSION | 2025-11-26 | 2025-11-26 |
| 10 | EVANSPARK ELCC ACADEMY | Calgary | 24 | 15 | 8 | VARIATION OF LICENCE PROVISIONS | 2025-12-11 | 2025-11-26 |
| 11 | CHILD DEVELOPMENT DAYHOMES OF ALBERTA | Calgary | 23 | 13 | 8 | ORDER TO REMEDY | 2025-12-17 | 2025-07-25 |
| 12 | HAPPY HOUSE DAYCARE (SOUTH) | Cold Lake | 22 | 19 | 7 | LICENCE SUSPENSION | 2025-12-10 | 2025-12-10 |
| 13 | CONNECTING DOTS-DAVE BARR | Grande Prairie | 17 | 22 | 7 | VARIATION OF LICENCE PROVISIONS | 2025-11-12 | 2025-10-20 |
| 14 | BRIGHTPATH WEST HENDAY | Edmonton | 21 | 11 | 7 | ORDER TO REMEDY | 2025-12-15 | 2025-11-05 |
| 15 | RISING PILLARS CHILDCARE | Calgary | 19 | 19 | 7 | ORDER TO REMEDY | 2025-12-04 | 2025-12-04 |
| 16 | EDSON EARLY LEARNING & CHILD CARE | Edson | 18 | 11 | 7 | ORDER TO REMEDY | 2025-12-01 | 2025-10-28 |
| 17 | BRIGHT STARS DAYCARE AND OSC | Edmonton | 15 | 18 | 7 | ORDER TO REMEDY | 2025-11-26 | 2025-11-13 |
| 18 | TODDLE INN DAY CARE SOCIETY | Strathmore | 11 | 13 | 7 | ORDER TO REMEDY | 2025-11-25 | 2025-11-25 |
| 19 | FUELING BRAINS ACADEMY WEST 85TH | Calgary | 15 | 18 | 7 | ORDER TO REMEDY | 2025-11-19 | 2025-11-05 |
| 20 | ACTIVE START CHILD CARE SETON | Calgary | 16 | 13 | 7 | ORDER TO REMEDY | 2025-11-14 | 2025-10-22 |

---

## 2. Findings

### Inspection-volume bias

Across all 2,913 centres: `total_inspection_visits` correlates with `total_non_compliance_citations` at **≈0.73**, and with `visits_with_non_compliance` at **≈0.79**. The dataset-wide median `total_inspection_visits` is **4**, but the median within each candidate's top 20 is **12.5 (A), 16.5 (B), 20.0 (C)**.

**Contrary to the intuitive assumption in the earlier draft comparison, Candidate C is not less volume-biased than B — it is slightly more.** Ranking by "visits with a citation" still rewards centres that simply had more total visits to accumulate those citations from; a centre only inspected 4 times (the dataset median) essentially cannot compete on this metric no matter how serious its situation, regardless of which of B or C is used.

### Same-visit citation inflation

`total_non_compliance_citations` counts every citation line, so one visit that produces many citations at once inflates the count the same as many separate bad visits. **MILESTONES OUT OF SCHOOL CARE** is the clearest case: 23 citations from only 2 visits with a citation (a ratio of 11.5 citations per bad visit, versus a dataset median of 1.5 and only 203 of 1,431 actionable centres — 14% — at or above a ratio of 3). It ranks #6 under Candidate B but falls to #458 under Candidate C, which is exactly the distortion Candidate C's second sort key (`visits_with_non_compliance`) is designed to reduce.

### Centres that move substantially between candidates

The most dramatic movements are the same centres driving the "old enforcement" question below: **LITTLE SCHOLARS DAYCARE ECS LTD.** (A=1, B=42, C=82) and **INC.** (A=2, B=73, C=327), **KLORIOUS KIDS DAYCARE** (A=12, B=214, C=328), **LITTLE M-DESTINY** (A=19, B=978, C=690), and **LEARN, LOVE 'N' LAUGH** (A=20, B=979, C=692) — all ranked in Candidate A's top 20 almost entirely on one severe or moderate enforcement action, but far outside the top 100 under B or C because their actual citation volume is low. In the other direction, **INNER GARDEN BILINGUAL DAYHOME AGENCY** (A=30, B=3, C=4), **CIRCLE SQUARE CHILDCARE** (A=31, B=4, C=38), and **MILESTONES OUT OF SCHOOL CARE** (A=32, B=6, C=458) show heavy, recent citation activity but rank only mid-table under A because their single worst enforcement action (`ORDER TO REMEDY`) is not as severe as another centre's one-time suspension or cancellation.

### Old historical enforcement vs. recent repeated non-compliance

This is checked directly: of each candidate's top 20, how many have their **most recent non-compliance citation** more than ~10 months before the dataset's latest inspection date (2025-12-23, cutoff 2025-02-23)?

| Candidate | Stale centres in top 20 | Which ones |
|---|---|---|
| A | **5 / 20** | LITTLE SCHOLARS DAYCARE ECS LTD. (2024-08-12), LITTLE SCHOLARS DAYCARE INC. (2024-08-12), ALOTTA FUN CHILDCARE OSC (2024-09-19), KLORIOUS KIDS DAYCARE (2024-11-20), LITTLE M-DESTINY (2025-01-09) |
| B | 1 / 20 | ALOTTA FUN CHILDCARE OSC (2024-09-19) |
| C | 0 / 20 | — |

**Yes — Candidate A over-prioritizes old historical enforcement over recent repeated non-compliance, concretely and measurably.** Its top 2 centres (both LITTLE SCHOLARS entities) have had no new citation recorded in about 16 months, yet outrank every centre in the dataset purely because a `LICENCE CANCELLATION` outranks everything else in the fixed category order. The dataset has no licence-status field (per CLAUDE.md's data limitations), so it cannot even be confirmed whether a cancelled-licence centre is still operating — ranking it #1 for "who should inspectors follow up on first" is questionable regardless. Recency is used in all three candidates only as a last-resort tiebreaker, never as a factor that can demote an old enforcement action — this weakness is structural to Candidate A specifically, because its primary sort key (enforcement tier) can be satisfied by a single old event with no ongoing pattern.

---

## 3. Actionable-centre rule review

**Rule:** `total_non_compliance_citations > 0 OR highest_enforcement_action != NONE`.

**Finding:** checked directly against `data/processed/centre-summary.json` — there are **zero** centres where one condition is true and the other false. Every centre with `total_non_compliance_citations > 0` also has a non-`NONE` enforcement action, and vice versa. This is the same row-level pairing already documented in [knowledge/dataset-assessment.md](../knowledge/dataset-assessment.md) (`Non Compliance` and `Enforcement Action` are always both present or both absent on a row) holding at the centre level too. Under this rule, **1,431 of 2,913 centres (49%)** are actionable and appear in the default Priority List; **1,482 (51%)** are excluded.

**Is it appropriate for Story #1?** Yes. Story #1 is specifically about centres showing "repeated non-compliance and stronger enforcement actions" — excluding centres with neither is a direct restatement of that decision's own scope, not an added assumption or derived signal.

**Disposition: retain the rule as written, unchanged.** The `OR` is logically redundant against the current extract (confirmed above), but it should not be simplified to a single condition — it correctly expresses "either signal qualifies," and would only stop being redundant if a future data extract ever recorded an enforcement action without an accompanying citation (or vice versa), which the current pairing invariant does not guarantee will always hold. This is recorded here as an explicit governance rule: **do not narrow the actionable definition to only one of the two conditions**, and revisit this note if a future extract breaks the pairing.

---

## 4. Final recommendation

**Recommended candidate: B — repeated non-compliance count first, then highest recorded Enforcement Action, then recency.**

This revises the draft recommendation in [eval/ranking-candidate-comparison.md](ranking-candidate-comparison.md), which favored Candidate A based on a top-10, language-emphasis reading of Story #1. The deeper top-20 and staleness review above found concrete, quantified evidence that Candidate A's design lets a single old enforcement event dominate the list regardless of how long ago it happened (5 of its top 20 are stale by 10+ months; its top 2 entries have had no new citation in about 16 months and may not even reflect an operating centre). Candidate B does not have this problem to nearly the same degree (1 of 20 stale) while still using the recorded `Enforcement Action` category as its second sort key, so a strong enforcement history still matters — it just cannot alone override a low, non-repeating citation count.

**Why B over C specifically:** Candidate C does not solve inspection-volume bias any better than B (0.79 vs. 0.73 correlation with total visits; higher top-20 median visit count) and, by discounting `MILESTONES OUT OF SCHOOL CARE`-type cases (many citations concentrated in very few visits) down to rank 458, C risks under-prioritizing a centre with a serious, recent, concentrated problem. B's exposure to that specific same-visit-inflation pattern is real but narrower (14% of actionable centres have a citations-per-bad-visit ratio of 3 or higher) than A's exposure to stale-history domination or C's exposure to volume bias.

**How this stays deterministic, score-free, and grounded:** Candidate B is a plain, three-key sort — `total_non_compliance_citations` (descending), then `highest_enforcement_action` by its existing fixed category order (descending), then `most_recent_inspection_date` (descending, tiebreaker only) — over fields already present in `centre-summary.json`. No field is invented, no weights are combined into a single number, and nothing is normalized into a probability.

**Limitations, stated plainly:**
- B still correlates with how often a centre has been inspected (≈0.73), so a centre visited only once or twice cannot rank highly under B no matter how serious that one visit was — this is a real, unresolved limitation, not something this recommendation corrects for.
- B is still exposed to same-visit citation inflation (e.g., `MILESTONES OUT OF SCHOOL CARE`, ratio 11.5), just less broadly than the dataset as a whole.
- B is not immune to staleness either (`ALOTTA FUN CHILDCARE OSC`'s last citation is 2024-09-19), just far less exposed than A.
- Recency is only a final tiebreaker in all three candidates, including B — none of them treat "how long ago" as a primary ranking factor. If that turns out to matter more than this analysis assumes, that would require a new, separately governed candidate, not a silent change to B.

**This is a recommendation, not a decision.** Per CLAUDE.md's Human in the Loop section, selecting a final ranking candidate — and whether to act on any centre's position in it — remains Priya's (and her program's) governance decision. The ranking candidate selector in `dashboard/index.html` is left in place and unchanged so that comparison remains possible until that decision is made.
