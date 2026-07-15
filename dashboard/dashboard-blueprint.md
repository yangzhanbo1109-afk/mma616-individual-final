# Dashboard Blueprint

Information architecture only — no visual styling, no implementation. Grounded in [CLAUDE.md](../CLAUDE.md), [capability-map.md](../capability-map.md), and [knowledge/dataset-assessment.md](../knowledge/dataset-assessment.md).

**User:** Priya Desai, Regional Program Manager, Licensing & Monitoring
**Decision this dashboard answers:** *"Which licensed child care centres should inspectors follow up on first?"*

**Design philosophy:** decision-first, one screen, morning-coffee test (Priya must be able to open this, know who to follow up on, and know why, before she finishes her coffee), every panel earns its place — nothing appears unless it maps to a capability from the capability map.

**Layout order (top to bottom, one screen):** Panel A is the answer to the decision and sits first. Panel B is a control that scopes A and C, not independent content. Panel C is the second most time-sensitive signal. Panels D and E are on-demand, entered only from A or C — they do not occupy primary screen space until invoked.

---

## Panel A — Priority Follow-Up List

1. **Title:** Priority Follow-Up List
2. **Business question:** Which centres show repeated non-compliance and the strongest enforcement actions on record, right now?
3. **Capability supported:** Capability 4 — Rank centres by repeated non-compliance and enforcement actions
4. **Fields used:** `Program ID` (key), `Program Name`, `Program City`, `Non Compliance` (count of citations per centre), `Enforcement Action` (highest category recorded for that centre), `Inspection Date` (most recent)
5. **Why this panel exists:** this is the decision itself. Everything else on the dashboard either scopes this list (Panel B), adds a second, time-sensitive signal to it (Panel C), or explains an entry in it (Panels D/E). If Priya sees nothing else, this panel alone answers "who first."

---

## Panel B — Scope Filter

1. **Title:** Scope Filter
2. **Business question:** Which part of my own coverage area am I looking at right now?
3. **Capability supported:** Capability 5 — Filter and segment the centre list
4. **Fields used:** `Program City`, `Type of Program`, `Day Care Y/N`, `Out of School Care Y/N`, `Preschool Y/N`
5. **Why this panel exists:** Priya is responsible for a defined region and set of program types, not the entire province. Without this control, Panel A would show centres outside her scope of responsibility, breaking the morning-coffee test — she'd have to mentally filter the list herself every time.

---

## Panel C — Follow-Up Gaps After Enforcement

1. **Title:** Follow-Up Gaps After Enforcement
2. **Business question:** Which centres had an enforcement action with a remedy date on record, but no later inspection shows up to confirm what happened next?
3. **Capability supported:** Capability 6 — Detect follow-up gaps after enforcement
4. **Fields used:** `Program ID`, `Program Name`, `Enforcement Action`, `Remedy Date`, `Inspection Date` (latest on record for that centre)
5. **Why this panel exists:** a centre can have a real, time-sensitive gap in its record (enforcement acted on, but nothing recorded since) without necessarily being at the top of Panel A's ranking. This is a directly observable fact in the data, not a duplicate of Panel A, so it earns a separate, second-priority place on the same screen.

---

## Panel D — Why This Centre Is Prioritized

1. **Title:** Why This Centre Is Prioritized
2. **Business question:** For a specific centre I've selected from Panel A or C, what actually happened that put it there?
3. **Capability supported:** Capability 7 — Explain why a centre is prioritized
4. **Fields used:** `Non Compliance`, `Enforcement Action`, `Inspection Date`, `Inspection Reason` — the full row history for the one selected `Program ID`
5. **Why this panel exists:** Panel A's count and category tell Priya *that* a centre ranks high; this panel exists so she isn't left reading raw inspection rows herself to find out *why*. It only appears once a centre is selected — it is not standing content on the main screen.

---

## Panel E — Ask About a Centre or the Ranking

1. **Title:** Ask About a Centre or the Ranking
2. **Business question:** Any specific follow-up question Priya has in the moment that isn't already answered by a fixed panel (e.g., "has anything changed for this centre since last time," "why is this centre above that one").
3. **Capability supported:** Capability 8 — Answer ad hoc questions about specific centres or the ranking
4. **Fields used:** the same aggregated fields already surfaced in Panels A–D (`Program ID`, `Non Compliance`, `Enforcement Action`, `Inspection Date`, `Inspection Reason`, `Program City`) — no new or external data
5. **Why this panel exists:** not every question Priya has can be anticipated as a fixed report. This panel exists as the release valve for those questions, strictly grounded in data already shown elsewhere on the dashboard — it does not introduce any new capability or field.

---

## Panels considered but excluded

- **Inspection-reason mix per city/centre (Story #3 — complaint/incident-driven vs. routine inspections):** a real, supported view, but it answers a *leading-indicator* question, not "who first" — it doesn't map to the primary decision this dashboard is scoped to, so it was left out of the one-screen build rather than competing for space with Panels A–C.
- **Capacity or program-type breakdown as a standalone chart:** these fields are used only as filter criteria (Panel B); a separate chart of capacity distribution doesn't answer the follow-up decision and was excluded.
- **A single combined "risk score" panel:** rejected — no field in the dataset supports a score, and merging Panel A and Panel C into one number would hide the fact that they represent two different, independently verifiable observations (repeated citations/enforcement vs. an observed follow-up gap).
