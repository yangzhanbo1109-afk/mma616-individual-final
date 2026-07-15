# Dataset Assessment

**File:** `data/raw/child-care-open-data-202512.csv`
**Rows:** 15,772 (+ 1 header row)
**Columns:** 16
**Source (inferred from content):** Alberta Children's Services child care licensing / inspection open data extract.

This is a factual profile of the data as it exists — no business problem or dashboard design is assumed here.

---

## 1. What does one row represent?

One row represents **a single inspection-related event for one licensed child care program, with one row per non-compliance citation (or one row if no citation was issued).**

Evidence:
- Each row carries `Program ID`, `Inspection Date`, and `Inspection Reason` together — this triple identifies a specific inspection *visit*.
- 1,429 of 13,113 distinct (Program ID, Date, Reason) visit-keys have **more than one row** (up to 12 rows for a single visit). In every multi-row case, the rows are identical except for `Non Compliance` (a different violation code/text) and sometimes `Enforcement Action`/`Remedy Date`.
- When an inspection found no violation, `Non Compliance`, `Enforcement Action`, and `Remedy Date` are blank/NULL and there is exactly one row for that visit.

So the grain is **(program, inspection visit, violation-if-any)**, not "one row per centre" and not "one row per inspection visit."

Static attributes of the program (name, address, city, postal code, phone, program type, capacity, service-type flags) are **repeated on every row** — they describe the centre, not the inspection.

---

## 2. How many unique child care centres are there?

**2,913 unique `Program ID` values.**

Two data-quality notes:
- `Program Name` has only 2,880 unique values — slightly fewer than the ID count, meaning some names are reused/shared text-wise across different IDs.
- Conversely, exactly **one `Program ID` maps to two different names** (`T.L.C. PRESCHOOL (THE LEARNING CORNER)` vs `TLC PRESCHOOL`) — the same legal program was recorded under a renamed/reformatted name at some point. Any "count distinct centres" logic should key off `Program ID`, not `Program Name`.
- Address, `Type of Program`, and capacity are **constant per Program ID** in nearly all cases (only 3 of 2,913 programs show a capacity value that changed across rows) — so these fields behave as stable attributes of the centre, confirming Program ID is a reliable entity key.

---

## 3. Are there multiple inspection records for the same centre?

**Yes, overwhelmingly.** Only 197 of 2,913 programs (6.8%) have a single row; the remaining 93% have between 2 and 56 rows.

| Records per program | # of programs |
|---|---|
| 1 | 197 |
| 2–5 | 1,806 |
| 6–10 | 605 |
| 11–20 | 195 |
| 21–56 | 55 |

This confirms the dataset is **longitudinal at the program level** — repeat inspections, follow-ups, complaints, and enforcement actions accumulate over time for the same centre.

Also found: **135 fully identical duplicate rows** (every field, including violation text, repeated verbatim). This is a data-quality issue to be aware of, not something to silently "fix" without understanding — it could be a genuine re-listing in the source system or an extraction artifact.

---

## 4. What are the important fields?

| Field | Role | Notes |
|---|---|---|
| `Program ID` | Entity key | Stable per centre; use this over `Program Name` for identity |
| `Program Name`, `Program Address`, `Program City`, `Postal Code`, `Phone Number` | Centre identity/location | Constant per Program ID |
| `Type of Program` | Category | 4 values: FACILITY-BASED PROGRAM (14,896 rows / 94.5%), FAMILY DAY HOME (790), GROUP FAMILY CHILD CARE PROGRAM (44), INNOVATIVE CHILD CARE PROGRAM (42) |
| `Day Care Y/N`, `Out of School Care Y/N`, `Preschool Y/N` | Service-type flags | Not mutually exclusive — a program can offer more than one service type |
| `Capacity` | Licensed capacity (integer, 6–1,440, mean ≈102) | No missing/non-numeric values |
| `Inspection Date` | Event date | 39 rows (0.2%) have literal `NULL`; valid range 2024-07-02 to 2025-12-23 |
| `Inspection Reason` | Why the inspection happened | 10 categories (see below) |
| `Non Compliance` | Violation cited (code + description) | Blank on ~67% of rows (no violation found); 178 distinct violation texts when present |
| `Enforcement Action` | Regulator's response to a violation | Blank on ~67% of rows; always blank exactly when `Non Compliance` is blank, and always filled exactly when `Non Compliance` is filled (perfectly paired, 0 mismatches) |
| `Remedy Date` | Deadline/date the enforcement action was resolved | Present for 4,876 rows; literal `NULL` string used for missing (not a true blank) |

`Inspection Reason` breakdown (15,772 rows):
- INSPECTION — 8,771
- FOLLOW UP TO ENFORCEMENT ACTION — 2,290
- COMPLAINT INVESTIGATION — 1,540
- INCIDENT REPORT — 999
- CRITICAL INCIDENT REPORT — 503
- VARIANCE REQUEST — 446
- INITIAL LICENCE INSPECTION — 432
- CONSULTATION — 397
- RENEWAL LICENCE INSPECTION — 339
- CONSULTATION REQUESTED BY PROGRAM — 16
- (39 rows NULL)

`Enforcement Action` breakdown (non-blank rows only, n=5,281):
- ORDER TO REMEDY — 4,684
- NOTICE OF NON-COMPLIANCE — 409
- VARIATION OF LICENCE PROVISIONS — 49
- PROBATIONARY LICENCE — 36
- CONDITIONS ON LICENCE — 32
- LICENCE SUSPENSION — 22
- LICENCE CANCELLATION — 10

---

## 5. Which fields could support real operational decisions?

- **`Non Compliance` + `Enforcement Action` + `Remedy Date`** — the core signal for compliance risk: what was violated, how the regulator responded, and whether/when it was remedied. This is the richest decision-relevant content in the file.
- **`Inspection Reason`** — distinguishes routine oversight (INSPECTION, RENEWAL) from reactive/risk-driven events (COMPLAINT INVESTIGATION, INCIDENT/CRITICAL INCIDENT REPORT, FOLLOW UP TO ENFORCEMENT ACTION). The mix of reasons for a given centre indicates whether its inspection history is routine or complaint-driven.
- **`Program ID` (repeat-visit history)** — enables tracking a centre's trajectory over time: recurring violations, repeat enforcement, time between an `ORDER TO REMEDY` and its `Remedy Date` or the next `FOLLOW UP TO ENFORCEMENT ACTION`.
- **`Capacity`, `Type of Program`, service-type flags** — enable segmentation (e.g., do larger facility-based programs get cited more/less often than small family day homes?).
- **`Program City` / `Postal Code`** — enables geographic rollups (region-level compliance rates, inspector workload by area).

These fields could plausibly support decisions by a regulator (where to focus inspection resources), an operator (self-monitoring compliance status across multiple sites), or a parent (screening a specific centre's history) — see Q7/Q8.

---

## 6. What important information is missing?

- **No inspector identity or inspecting office/region** — can't analyze by inspector or regulatory office, only by city/postal code.
- **No severity/risk rating on violations** — `Non Compliance` gives a code and description but no standardized severity tier, so all violations look equally weighted unless the code prefix is manually parsed.
- **No outcome/closure status field** — whether a violation is currently "open" vs "resolved" must be inferred from presence/absence of a `Remedy Date`, and `Remedy Date` uses the literal string `"NULL"` rather than a true blank for ~69% of rows, which will break naive date-parsing if not handled explicitly.
- **No enrollment or actual attendance data** — only licensed `Capacity`, not how many children are actually enrolled/attending, so "utilization" cannot be computed.
- **No cost, fee, or subsidy information.**
- **No licence start date / years-in-operation** — can't tell how long a program has been operating, only its inspection history within the extract window.
- **No unique identifier for a "visit" itself** — must be reconstructed as (Program ID + Inspection Date + Inspection Reason), and this composite key is not guaranteed unique (see the 135 exact duplicate rows, and 39 rows with a NULL date).
- **No indication of appeals or reversals** — if a program contests a violation or enforcement action, that outcome isn't captured.

---

## 7. What kinds of business users could realistically use this dataset?

- **Provincial regulator / Children's Services program staff** — resource planning (where to send inspectors), identifying repeat offenders, monitoring enforcement follow-through.
- **Child care operators running multiple centres** — tracking compliance status and inspection history across their own portfolio of locations.
- **Parents/guardians choosing a child care provider** — looking up a specific centre's inspection and violation history before enrolling.
- **Municipal or regional planners** — understanding the supply, capacity, and program-type mix of licensed child care by city.
- **Journalists / advocacy or research organizations** — trend analysis on enforcement actions, violation types, or geographic disparities.

---

## 8. Which user would make the strongest MMA 616 project?

Not decided here — this document is data understanding only, per the assignment instructions. Note only that the dataset's structure (longitudinal per-centre compliance events, paired violation/enforcement fields, no severity rating, no true "open case" flag) will make some of the above users far more supportable than others with this data *as it exists*. That trade-off should be weighed explicitly once a business problem is chosen, not assumed now.

---

## 9. Would one month of data be enough, or should we download multiple months?

**This file is already NOT a single month** — despite the filename (`...202512`, suggesting a December 2025 snapshot/extract date), the `Inspection Date` values span **2024-07-02 through 2025-12-23**, i.e. roughly 18 months of inspection history, with inspection counts fairly stable month-to-month (625–1,089 rows/month). So "202512" appears to be the date the extract was pulled, not the period it covers.

Given that:
- The file as provided is a rolling multi-month history, not a single-month cut, so the "one month vs. multiple months" question is really about **whether to pull additional/future extracts over time**, not about this file alone.
- Because the grain is (program, visit, violation) and most compliance-relevant analysis (repeat violations, time-to-remedy, enforcement trends) is inherently longitudinal, a single-month snapshot — if one were used instead — would be insufficient: 93% of programs need multiple visits to show any pattern at all, and violation/enforcement counts by month show real variation (e.g., 625 rows in 2024-12 vs 1,089 in 2025-10), so one month could not be assumed representative.
- Downloading successive future extracts (e.g., monthly) would let new inspections be appended and would let "currently open" enforcement actions be tracked as they get remedy dates filled in later — something impossible from a single static pull.

**Conclusion:** the current 18-month extract is a reasonable analytical base as-is; if the project needs freshness or wants to observe how open enforcement actions get resolved over time, additional periodic pulls (not just one additional month) would be needed, since this data updates by adding new inspection rows and by populating previously-blank fields for existing rows.
