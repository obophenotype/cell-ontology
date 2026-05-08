#!/usr/bin/env python3

"""Select ticket-relevant CLARA validation targets from stage-1 output.

Phase 2 is still a routing preview. This script reads `changes.json` from
`clara_workflow.stage1.extract` and emits a normalized `routing.json` payload
that identifies which downstream CLARA checks should run for the current PR.

Current routing policy mirrors the ticket scope:

- New terms (NTRs): route added definitions/comments plus added structural
  axioms as one NTR validation bundle.
- Existing terms: route added structural axioms (`subclass`, `relationship`,
  `equivalent_class`) as direct atomic checks.
- Any term: route added synonym axioms only when the synonym axiom itself has
  attached refs.

Intentionally not routed yet:

- Existing-term text definition revisions
- Reviewable removals
- Synonyms without refs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEXTUAL_KINDS = frozenset({"text_def", "comment"})
STRUCTURAL_KINDS = frozenset({"subclass", "relationship", "equivalent_class"})
SYNONYM_KINDS = frozenset(
    {"synonym_exact", "synonym_broad", "synonym_narrow", "synonym_related"}
)


def _stable_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def _is_searchable_ref(value: str) -> bool:
    upper = value.upper()
    return upper.startswith("PMID:") or upper.startswith("DOI:")


def _refs_for_changes(changes: list[dict]) -> list[str]:
    refs: list[str] = []
    for change in changes:
        refs.extend(ref for ref in change.get("refs", []) if _is_searchable_ref(ref))
    return _stable_unique(refs)


def _change_target(
    *,
    route: str,
    validation_mode: str,
    ordinal: int,
    change: dict,
    term_id: str,
    term_label: str,
    term_is_new: bool,
    term_level_candidate_refs: list[str],
) -> dict:
    return {
        "target_id": f"{route}:{term_id}:{ordinal}",
        "route": route,
        "validation_mode": validation_mode,
        "term_id": term_id,
        "term_label": term_label,
        "term_is_new": term_is_new,
        "change": change,
        "candidate_refs": _refs_for_changes([change]),
        "term_level_candidate_refs": term_level_candidate_refs,
    }


def select_targets(payload: dict) -> dict:
    targets: list[dict] = []
    ignored: list[dict] = []
    route_counts = {"ntr": 0, "relationship": 0, "synonym": 0}
    ignored_reason_counts: dict[str, int] = {}
    reviewable_terms = 0
    obsoleted_terms_skipped = 0

    for term_id, entry in sorted(payload["by_term"].items()):
        term_label = entry["term_label"]
        term_is_new = bool(entry["is_new_term"])
        term_is_obsoleted = bool(entry["is_obsoleted"])
        term_is_reviewable = bool(entry["is_reviewable"])
        if term_is_reviewable:
            reviewable_terms += 1
        if term_is_obsoleted:
            obsoleted_terms_skipped += 1
            continue

        added_reviewable = [
            change
            for change in entry["changes"]
            if change["side"] == "added" and change["kind"] in (TEXTUAL_KINDS | STRUCTURAL_KINDS | SYNONYM_KINDS)
        ]
        term_level_candidate_refs = _refs_for_changes(
            [change for change in added_reviewable if change["kind"] in TEXTUAL_KINDS]
        )

        if term_is_new:
            ntr_textual = [change for change in added_reviewable if change["kind"] in TEXTUAL_KINDS]
            ntr_structural = [change for change in added_reviewable if change["kind"] in STRUCTURAL_KINDS]
            if ntr_textual or ntr_structural:
                targets.append(
                    {
                        "target_id": f"ntr:{term_id}",
                        "route": "ntr",
                        "validation_mode": "decompose_definition_and_relationships",
                        "term_id": term_id,
                        "term_label": term_label,
                        "term_is_new": True,
                        "textual_changes": ntr_textual,
                        "definition_changes": ntr_textual,
                        "relationship_changes": ntr_structural,
                        "candidate_refs": _refs_for_changes(ntr_textual + ntr_structural),
                        "term_level_candidate_refs": term_level_candidate_refs,
                    }
                )
                route_counts["ntr"] += 1

        structural_ordinal = 0
        synonym_ordinal = 0
        for change in added_reviewable:
            kind = change["kind"]
            if kind in STRUCTURAL_KINDS:
                if term_is_new:
                    continue
                structural_ordinal += 1
                targets.append(
                    _change_target(
                        route="relationship",
                        validation_mode="validate_atomic_relationship",
                        ordinal=structural_ordinal,
                        change=change,
                        term_id=term_id,
                        term_label=term_label,
                        term_is_new=term_is_new,
                        term_level_candidate_refs=term_level_candidate_refs,
                    )
                )
                route_counts["relationship"] += 1
                continue

            if kind in SYNONYM_KINDS:
                if change.get("refs"):
                    synonym_ordinal += 1
                    targets.append(
                        _change_target(
                            route="synonym",
                            validation_mode="validate_synonym_against_attached_refs",
                            ordinal=synonym_ordinal,
                            change=change,
                            term_id=term_id,
                            term_label=term_label,
                            term_is_new=term_is_new,
                            term_level_candidate_refs=term_level_candidate_refs,
                        )
                    )
                    route_counts["synonym"] += 1
                else:
                    ignored.append(
                        {
                            "term_id": term_id,
                            "term_label": term_label,
                            "reason": "synonym_without_refs",
                            "change": change,
                        }
                    )
                continue

            if kind in TEXTUAL_KINDS and not term_is_new:
                ignored.append(
                    {
                        "term_id": term_id,
                        "term_label": term_label,
                        "reason": "existing_term_text_not_yet_routed",
                        "change": change,
                    }
                )

    for item in ignored:
        reason = item["reason"]
        ignored_reason_counts[reason] = ignored_reason_counts.get(reason, 0) + 1

    return {
        "source": {
            "left": payload["left"],
            "right": payload["right"],
        },
        "summary": {
            "terms_touched": len(payload["by_term"]),
            "reviewable_terms": reviewable_terms,
            "obsoleted_terms_skipped": obsoleted_terms_skipped,
            "reviewable_changes": len(payload["reviewable"]),
            "decomposable_changes": len(payload["decomposable"]),
            "selected_targets": len(targets),
            "route_counts": route_counts,
            "ignored_changes": len(ignored),
            "ignored_reason_counts": ignored_reason_counts,
        },
        "targets": targets,
        "ignored": ignored,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to stage-1 changes.json")
    parser.add_argument("--output", type=Path, required=True, help="Path to write routing.json")
    args = parser.parse_args(argv)

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    selected = select_targets(payload)
    args.output.write_text(json.dumps(selected, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
