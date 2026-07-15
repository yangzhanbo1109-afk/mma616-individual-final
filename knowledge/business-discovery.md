# Business Discovery

Grounded entirely in [dataset-assessment.md](dataset-assessment.md). No fields, workflows, or capabilities are assumed beyond what that assessment established.

---

## 1. Strongest primary business user

**A regional/program-level inspection supervisor at Alberta Children's Services** (the licensing regulator itself) — not a parent, not a centre operator.

Why this beats the alternatives from the assessment's Q7 list:
- **Parents/guardians**: a plausible secondary user, but the dataset has no severity rating and no "is this resolved" flag — a parent-facing tool would be showing raw, unweighted violation text with real risk of misinterpretation, and the underlying decision ("enroll here or not") is one-shot and low-frequency, not a recurring operational decision.
- **Multi-site operators**: the dataset has no ownership/chain field linking Program IDs to a common operator, and a single centre's own director already receives their own inspection results directly from the regulator — the dataset adds little they don't already have.
- **Municipal planners / journalists**: interested in aggregate trends, not a recurring decision with a clear action attached.
- **Regulator's own inspection supervisor**: this is the one user whose recurring, resource-constrained decision is *fully* answerable from fields that actually exist in the file — `Non Compliance`, `Enforcement Action`, `Remedy Date`, `Inspection Reason`, and the per-`Program ID` history — with no invented fields required.

## 2. The real decision this user makes

**Given limited inspector time, which licensed child care centres should inspectors follow up on first?**

This is a recurring triage/allocation decision, made repeatedly as new inspection rows accumulate — not a one-time lookup.

## 3. The biggest pain point they have today

The dataset assessment shows the raw data is a flat, per-violation event log: 15,772 rows, one per citation-or-clean-visit, with no rollup, no severity tier, and no "open vs resolved" status field. To know *which* of 2,913 centres deserve attention right now, someone would have to manually trace each centre's own row history — checking whether violations recur, whether enforcement has escalated (Notice → Order to Remedy → Probationary → Suspension), and whether a `Remedy Date` was ever logged after an enforcement action — one centre at a time. At this volume (up to 56 rows for a single centre), that is not something that can be done reliably by eyeballing case files; there is no systematic, rolled-up view of centre-level risk.

## 4. How our decision-support tool changes their workflow

**Before:** supervisor reviews individual centre files/case history reactively (e.g., after a new complaint comes in) with no standing view of which centres are already trending toward repeat non-compliance.

**After:** supervisor opens a rolled-up view, built only from fields the data actually has — count of non-compliance citations per centre, the highest recorded `Enforcement Action` on record, how recently that happened, and whether the `Inspection Reason` mix for a centre is dominated by reactive reasons (COMPLAINT INVESTIGATION / INCIDENT REPORT / CRITICAL INCIDENT REPORT / FOLLOW UP TO ENFORCEMENT ACTION) rather than routine ones (INSPECTION / RENEWAL LICENCE INSPECTION) — and uses that to decide where to send inspector time next. It changes the workflow from *per-centre lookup after something happens* to *portfolio-level triage before the next cycle*.

This is explicitly a **triage aid**, not a case-management system — it cannot tell the supervisor whether a violation is legally "closed" (no such field exists), only what the recorded history shows.

## 5. Persona

**Priya Desai** — Regional Program Manager, Licensing & Monitoring, Alberta Children's Services (Central Region, covering Calgary-area and surrounding communities).

Responsibilities:
- Oversees a team of field inspectors covering several hundred licensed programs in her region.
- Allocates inspector time weekly between routine renewal inspections, complaint response, and follow-ups on open enforcement actions.
- Accountable for making sure `ORDER TO REMEDY` and more serious actions get timely follow-up.
- Reports regional compliance trends upward to the Ministry.

This maps directly to Q8 of the dataset assessment: the fields that exist (compliance events + dates + program identity) support exactly this kind of resource-prioritization role, more directly than they support the other candidate users.

## 6. Three possible user stories

1. **Decision:** Priya Desai, Regional Program Manager, Licensing & Monitoring, needs to answer: *"Which child care centres should inspectors follow up on first?"*
   **Current pain:** Today, answering that means manually reviewing thousands of individual inspection records — up to 56 per centre across 2,913 centres — to piece together which ones show a pattern of repeated non-compliance and stronger enforcement actions over time. There is no existing way to see that pattern without reading each centre's row history one at a time.
   **What changes:** Using only the recorded inspection history already in the data (`Non Compliance`, `Enforcement Action`, `Inspection Date`, `Program ID`/`Program City`), Priya can identify which centres show repeated non-compliance and stronger enforcement actions without manually reading every inspection record for every centre.
   **Business outcome:** Priya can direct her team's limited inspection time to the centres showing repeated non-compliance and stronger enforcement actions first, instead of discovering those patterns only after another complaint or incident.
   *(Uses: `Non Compliance`, `Enforcement Action`, `Inspection Date`, `Program ID`, `Program City` — no other fields or calculations assumed.)*

2. **As Priya, I want to see centres that received an `ORDER TO REMEDY` (or more serious action) with a `Remedy Date`, so I can check whether a subsequent inspection row exists after that date and flag centres where no follow-up appears in the record.**
   *(Uses: `Enforcement Action`, `Remedy Date`, per-`Program ID` inspection-date sequence.)*

3. **As Priya, I want to see the mix of `Inspection Reason` values per centre or city over time, so I can identify centres or areas generating disproportionately complaint-/incident-driven inspections rather than routine ones, which may signal risk building before enforcement even occurs.**
   *(Uses: `Inspection Reason`, `Program City`, `Inspection Date`.)*

## 7. Recommended Story #1

**Story 1 — identify centres with repeated non-compliance and stronger enforcement actions, so Priya knows which centres inspectors should follow up on first — is the strongest starting point.**

Reasons:
- It is anchored to the one decision Priya actually owns every cycle — *which centres get follow-up first* — not a general analytics question.
- It is fully supported by fields confirmed present and clean in the assessment (`Non Compliance`, `Enforcement Action`, `Inspection Date`, `Program ID`/`Program City`), with no dependency on a field the dataset lacks. No severity score is invented — the existing `Enforcement Action` categories already represent an escalating regulatory response (Notice of Non-Compliance → Order to Remedy → Variation of Licence Provisions → Conditions on Licence → Probationary Licence → Licence Suspension → Licence Cancellation), and "repeated" is directly observable as multiple `Non Compliance` rows against the same `Program ID` over time.
- It matches the highest-value, most recurring form of the decision (ongoing triage), rather than a narrower one-time check (Story 2) or a softer leading-indicator signal (Story 3).
- Story 2 is worth pursuing next, but is weaker as a *first* story because "no follow-up row appears after the remedy date" is an absence-based inference, not a directly recorded status — it's a reasonable second layer once Story 1 is in place, not the strongest entry point.
- Story 3 is a good complementary/early-warning view but doesn't by itself answer "who do I follow up on first" — it surfaces pattern, not priority.
