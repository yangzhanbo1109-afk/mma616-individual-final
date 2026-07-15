"""
Capabilities 2-4 (Normalize, Aggregate, Rank-candidates) for the child care
inspection dataset. Deterministic, rule-based only -- no model, no score,
no invented fields. See CLAUDE.md and capability-map.md for the governing
rules this script must follow.

Ranking governance (see eval/final-ranking-recommendation.md and
logs/ranking-governance-decision.md): Candidate B -- total_non_compliance_citations
descending, then highest recorded Enforcement Action (the recorded enforcement
action order; not an official severity scale) descending, then
most_recent_inspection_date descending as the final tiebreaker -- is the
approved PRODUCTION ranking and drives centre_summary's row order and
production_rank field. Candidates A and C are computed and written only as
evaluation artifacts in ranking-candidates.json; they do not drive production
output. This script does not decide which candidate is production -- that is
recorded governance, not pipeline logic.

Usage:
    python scripts/build_centre_summary.py
"""

import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_CSV = os.path.join(BASE_DIR, "data", "raw", "child-care-open-data-202512.csv")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

# Fixed escalation order already established in CLAUDE.md / capability-map.md.
# This is an ORDERING of an existing categorical field, not an invented score.
ENFORCEMENT_ORDER = [
    "NONE",
    "NOTICE OF NON-COMPLIANCE",
    "ORDER TO REMEDY",
    "VARIATION OF LICENCE PROVISIONS",
    "CONDITIONS ON LICENCE",
    "PROBATIONARY LICENCE",
    "LICENCE SUSPENSION",
    "LICENCE CANCELLATION",
]
ENFORCEMENT_RANK = {name: i for i, name in enumerate(ENFORCEMENT_ORDER)}

REACTIVE_REASONS = [
    "COMPLAINT INVESTIGATION",
    "INCIDENT REPORT",
    "CRITICAL INCIDENT REPORT",
    "FOLLOW UP TO ENFORCEMENT ACTION",
]


def is_missing(value):
    if value is None:
        return True
    v = value.strip()
    return v == "" or v.upper() == "NULL"


def clean(value):
    return None if is_missing(value) else value.strip()


def load_raw_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def remove_exact_duplicates(rows):
    seen = set()
    kept = []
    removed = 0
    for r in rows:
        key = tuple(r.items())
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        kept.append(r)
    return kept, removed


def normalize_row(r):
    return {
        "program_id": clean(r["Program ID"]),
        "program_name": clean(r["Program Name"]),
        "program_city": clean(r["Program City"]),
        "type_of_program": clean(r["Type of Program"]),
        "day_care": clean(r["Day Care Y/N"]) == "Y",
        "out_of_school_care": clean(r["Out of School Care Y/N"]) == "Y",
        "preschool": clean(r["Preschool Y/N"]) == "Y",
        "inspection_date": clean(r["Inspection Date"]),
        "inspection_reason": clean(r["Inspection Reason"]),
        "non_compliance": clean(r["Non Compliance"]),
        "enforcement_action": clean(r["Enforcement Action"]),
        "remedy_date": clean(r["Remedy Date"]),
    }


def build_pipeline():
    raw_rows = load_raw_rows(SOURCE_CSV)
    raw_row_count = len(raw_rows)

    deduped_rows, exact_duplicates_removed = remove_exact_duplicates(raw_rows)

    normalized = [normalize_row(r) for r in deduped_rows]

    excluded_missing_date = [r for r in normalized if r["inspection_date"] is None]
    usable = [r for r in normalized if r["inspection_date"] is not None]

    centres = {}
    name_candidates = {}  # program_id -> list of (inspection_date, program_name)

    for r in normalized:
        pid = r["program_id"]
        if pid not in centres:
            centres[pid] = {
                "program_id": pid,
                "program_city": r["program_city"],
                "type_of_program": r["type_of_program"],
                "day_care": r["day_care"],
                "out_of_school_care": r["out_of_school_care"],
                "preschool": r["preschool"],
                "visit_keys": set(),
                "visit_keys_with_non_compliance": set(),
                "total_non_compliance_citations": 0,
                "highest_enforcement_rank": 0,
                "most_recent_inspection_date": None,
                "most_recent_non_compliance_date": None,
                "reactive_visit_keys": {reason: set() for reason in REACTIVE_REASONS},
            }
        name_candidates.setdefault(pid, []).append((r["inspection_date"], r["program_name"]))

    for r in usable:
        c = centres[r["program_id"]]
        visit_key = (r["inspection_date"], r["inspection_reason"])
        c["visit_keys"].add(visit_key)

        if r["non_compliance"] is not None:
            c["total_non_compliance_citations"] += 1
            c["visit_keys_with_non_compliance"].add(visit_key)
            if c["most_recent_non_compliance_date"] is None or r["inspection_date"] > c["most_recent_non_compliance_date"]:
                c["most_recent_non_compliance_date"] = r["inspection_date"]

        if r["enforcement_action"] is not None:
            rank = ENFORCEMENT_RANK.get(r["enforcement_action"])
            if rank is not None and rank > c["highest_enforcement_rank"]:
                c["highest_enforcement_rank"] = rank

        if c["most_recent_inspection_date"] is None or r["inspection_date"] > c["most_recent_inspection_date"]:
            c["most_recent_inspection_date"] = r["inspection_date"]

        if r["inspection_reason"] in REACTIVE_REASONS:
            c["reactive_visit_keys"][r["inspection_reason"]].add(visit_key)

    # Resolve one canonical Program Name per Program ID: name attached to the
    # most recent dated row (deterministic rule, logged in the audit file).
    programs_with_multiple_names = 0
    resolved_names = {}
    for pid, candidates in name_candidates.items():
        dated = [(d, n) for d, n in candidates if d is not None and n is not None]
        undated = [n for d, n in candidates if n is not None]
        distinct_names = {n for _, n in candidates if n is not None}
        if len(distinct_names) > 1:
            programs_with_multiple_names += 1
        if dated:
            resolved_names[pid] = max(dated, key=lambda x: x[0])[1]
        elif undated:
            resolved_names[pid] = undated[0]
        else:
            resolved_names[pid] = None

    centre_summary = []
    for pid, c in centres.items():
        complaint = len(c["reactive_visit_keys"]["COMPLAINT INVESTIGATION"])
        incident = len(c["reactive_visit_keys"]["INCIDENT REPORT"])
        critical_incident = len(c["reactive_visit_keys"]["CRITICAL INCIDENT REPORT"])
        follow_up = len(c["reactive_visit_keys"]["FOLLOW UP TO ENFORCEMENT ACTION"])

        centre_summary.append({
            "program_id": pid,
            "program_name": resolved_names.get(pid),
            "program_city": c["program_city"],
            "type_of_program": c["type_of_program"],
            "day_care": c["day_care"],
            "out_of_school_care": c["out_of_school_care"],
            "preschool": c["preschool"],
            "total_inspection_visits": len(c["visit_keys"]),
            "total_non_compliance_citations": c["total_non_compliance_citations"],
            "visits_with_non_compliance": len(c["visit_keys_with_non_compliance"]),
            "highest_enforcement_action": ENFORCEMENT_ORDER[c["highest_enforcement_rank"]],
            "highest_enforcement_rank": c["highest_enforcement_rank"],
            "most_recent_inspection_date": c["most_recent_inspection_date"],
            "most_recent_non_compliance_date": c["most_recent_non_compliance_date"],
            "complaint_investigation_visits": complaint,
            "incident_report_visits": incident,
            "critical_incident_report_visits": critical_incident,
            "follow_up_to_enforcement_visits": follow_up,
        })

    # --- Follow-up gaps: observed record gaps only, per CLAUDE.md Capability 6 ---
    rows_by_program = {}
    for r in usable:
        rows_by_program.setdefault(r["program_id"], []).append(r)

    follow_up_gaps = []
    for pid, rows in rows_by_program.items():
        remedy_rows = [r for r in rows if r["enforcement_action"] is not None and r["remedy_date"] is not None]
        if not remedy_rows:
            continue
        latest_remedy_row = max(remedy_rows, key=lambda r: r["remedy_date"])
        remedy_date = latest_remedy_row["remedy_date"]
        inspection_dates = [r["inspection_date"] for r in rows]
        later_dates = [d for d in inspection_dates if d > remedy_date]
        if later_dates:
            continue  # a later inspection row exists -- not a gap
        follow_up_gaps.append({
            "program_id": pid,
            "program_name": resolved_names.get(pid),
            "program_city": latest_remedy_row["program_city"],
            "enforcement_action": latest_remedy_row["enforcement_action"],
            "remedy_date": remedy_date,
            "most_recent_inspection_date_overall": max(inspection_dates) if inspection_dates else None,
            "label": "Observed record gap: no inspection row found after this remedy date.",
        })

    # --- Ranking candidates: three deterministic orderings, no combined score ---
    def recency_key(row):
        # Descending recency; missing date sorts last.
        return row["most_recent_inspection_date"] or ""

    candidate_a = sorted(
        centre_summary,
        key=lambda c: (c["highest_enforcement_rank"], c["total_non_compliance_citations"], recency_key(c)),
        reverse=True,
    )
    candidate_b = sorted(
        centre_summary,
        key=lambda c: (c["total_non_compliance_citations"], c["highest_enforcement_rank"], recency_key(c)),
        reverse=True,
    )
    candidate_c = sorted(
        centre_summary,
        key=lambda c: (c["visits_with_non_compliance"], c["highest_enforcement_rank"], recency_key(c)),
        reverse=True,
    )

    def slim(c, rank):
        return {
            "rank": rank,
            "program_id": c["program_id"],
            "program_name": c["program_name"],
            "program_city": c["program_city"],
            "total_non_compliance_citations": c["total_non_compliance_citations"],
            "visits_with_non_compliance": c["visits_with_non_compliance"],
            "highest_enforcement_action": c["highest_enforcement_action"],
            "most_recent_inspection_date": c["most_recent_inspection_date"],
        }

    ranking_candidates = {
        "production_candidate": "b",
        "candidate_a": {
            "label": "Highest recorded Enforcement Action first, then repeated non-compliance count, then recency",
            "role": "evaluation_only",
            "top_20": [slim(c, i + 1) for i, c in enumerate(candidate_a[:20])],
        },
        "candidate_b": {
            "label": "Repeated non-compliance count first, then highest recorded Enforcement Action, then recency",
            "role": "production",
            "top_20": [slim(c, i + 1) for i, c in enumerate(candidate_b[:20])],
        },
        "candidate_c": {
            "label": "Visits with non-compliance first, then highest recorded Enforcement Action, then recency",
            "role": "evaluation_only",
            "top_20": [slim(c, i + 1) for i, c in enumerate(candidate_c[:20])],
        },
    }

    # centre_summary is ordered by the approved production ranking (Candidate
    # B) and each row carries its production_rank. Candidates A and C above
    # are evaluation artifacts only and do not affect this order.
    production_rank_by_id = {c["program_id"]: i + 1 for i, c in enumerate(candidate_b)}
    for c in centre_summary:
        c["production_rank"] = production_rank_by_id[c["program_id"]]
    centre_summary.sort(key=lambda c: c["production_rank"])

    valid_dates = [r["inspection_date"] for r in usable]

    audit = {
        "source_file": "data/raw/child-care-open-data-202512.csv",
        "raw_row_count": raw_row_count,
        "exact_duplicate_rows_removed": exact_duplicates_removed,
        "rows_after_deduplication": len(deduped_rows),
        "rows_excluded_missing_inspection_date": len(excluded_missing_date),
        "rows_used_in_aggregation": len(usable),
        "unique_program_ids": len(centres),
        "program_ids_with_multiple_program_names_resolved": programs_with_multiple_names,
        "inspection_date_range": {
            "min": min(valid_dates) if valid_dates else None,
            "max": max(valid_dates) if valid_dates else None,
        },
        "follow_up_gap_count": len(follow_up_gaps),
        "production_ranking": {
            "candidate": "b",
            "sort_order": [
                "total_non_compliance_citations descending",
                "highest_enforcement_action by the recorded enforcement action order, descending",
                "most_recent_inspection_date descending (final tiebreaker only)",
            ],
            "approved_via": [
                "eval/final-ranking-recommendation.md",
                "logs/ranking-governance-decision.md",
            ],
        },
        "notes": [
            "Literal 'NULL' strings and blank strings are both treated as missing values.",
            "Program identity is keyed on Program ID; Program Name is resolved to the "
            "name recorded on the most recent dated row when a Program ID has more than one name.",
            "Rows with a missing Inspection Date cannot be assigned to a visit and are "
            "excluded from all visit-based counts, recency, and ranking calculations.",
            "highest_enforcement_rank is a position in the existing Enforcement Action "
            "category order (the recorded enforcement action order, see ENFORCEMENT_ORDER) "
            "-- it is not an official severity scale or a computed score.",
            "centre_summary.json is ordered by the approved PRODUCTION ranking, Candidate B, "
            "and each row carries its production_rank. Candidates A and C are retained in "
            "ranking-candidates.json as evaluation-only artifacts; they do not drive this order.",
        ],
    }

    return centre_summary, follow_up_gaps, ranking_candidates, audit


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    centre_summary, follow_up_gaps, ranking_candidates, audit = build_pipeline()

    with open(os.path.join(OUT_DIR, "centre-summary.json"), "w", encoding="utf-8") as f:
        json.dump(centre_summary, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT_DIR, "follow-up-gaps.json"), "w", encoding="utf-8") as f:
        json.dump(follow_up_gaps, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT_DIR, "ranking-candidates.json"), "w", encoding="utf-8") as f:
        json.dump(ranking_candidates, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT_DIR, "pipeline-audit.json"), "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    # Browsers block fetch()/XHR of local JSON files opened via file://, so the
    # same centre_summary/follow_up_gaps/audit content is also emitted as a
    # plain <script>-loadable JS file for dashboard/index.html to include
    # directly. This is a loading-mechanism detail only -- the data is
    # identical to the JSON files above.
    dashboard_payload = {
        "audit": audit,
        "centres": centre_summary,
        "gaps": follow_up_gaps,
    }
    with open(os.path.join(OUT_DIR, "dashboard-data.js"), "w", encoding="utf-8") as f:
        f.write("window.DASHBOARD_DATA = ")
        json.dump(dashboard_payload, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print("Pipeline complete.")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
