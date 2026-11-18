#!/usr/bin/env python3
"""Template-level validation for the CAP seeAlso links ROBOT template.

Runs before ROBOT compiles ``src/templates/cap_links.tsv`` into
``components/cap_links.owl``. ROBOT silently mints a class for an unknown
ID, so we have to catch mistakes before the build.

Checks performed (fail fast; prints every failure then exits non-zero):

* Every row's ID resolves to a class declared in ``cl-edit.owl``.
* The referenced class is not marked obsolete (``owl:deprecated true``).
* No duplicate (ID, URL) pair appears twice in the template.
* Every URL matches the CAP production label pattern.
* Every row has a non-empty link label.

Usage::

    python3 validate_cap_links.py src/templates/cap_links.tsv src/ontology/cl-edit.owl
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

CAP_URL_PATTERN = re.compile(
    r"^https://celltype\.info/project/\d+/dataset/\d+/label/\d+$"
)

# Match a single-line Functional-Syntax declaration like
# ``Declaration(Class(obo:CL_0000000))`` or using a full IRI.
_DECL_RE = re.compile(
    r"Declaration\(Class\((?:obo:(CL_\d+)|<http://purl\.obolibrary\.org/obo/(CL_\d+)>)\)\)"
)
_OBSOLETE_RE = re.compile(
    r"AnnotationAssertion\(\s*owl:deprecated\s+(?:obo:(CL_\d+)|<http://purl\.obolibrary\.org/obo/(CL_\d+)>)\s+\"true\""
)


def load_cl_state(edit_owl: Path) -> tuple[set[str], set[str]]:
    """Return (declared_ids, obsolete_ids) parsed line-by-line from cl-edit.owl."""
    declared: set[str] = set()
    obsolete: set[str] = set()
    with edit_owl.open("r", encoding="utf-8") as fh:
        for line in fh:
            m = _DECL_RE.search(line)
            if m:
                declared.add(m.group(1) or m.group(2))
            m = _OBSOLETE_RE.search(line)
            if m:
                obsolete.add(m.group(1) or m.group(2))
    return declared, obsolete


def _normalise_id(raw: str) -> str | None:
    """Accept ``CL:NNNNNNN``, ``CL_NNNNNNN`` or the full obo IRI."""
    raw = raw.strip()
    if not raw:
        return None
    if raw.startswith("http://purl.obolibrary.org/obo/"):
        raw = raw[len("http://purl.obolibrary.org/obo/"):]
    raw = raw.replace("CL:", "CL_")
    if re.fullmatch(r"CL_\d+", raw):
        return raw
    return None


def validate(template: Path, edit_owl: Path) -> list[str]:
    declared, obsolete = load_cl_state(edit_owl)
    errors: list[str] = []

    with template.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh, delimiter="\t")
        rows = list(reader)

    if len(rows) < 2:
        return ["cap_links.tsv must have both a header row and a ROBOT directive row"]

    header = rows[0]
    robot_header = rows[1]
    data_rows = rows[2:]

    try:
        id_col = robot_header.index("ID")
        url_col = robot_header.index("A rdfs:seeAlso")
        label_col = robot_header.index(">A rdfs:label")
    except ValueError as exc:
        return [f"required ROBOT header column missing: {exc}"]

    seen_pairs: set[tuple[str, str]] = set()

    for i, row in enumerate(data_rows, start=3):  # line numbers are 1-based, +2 for headers
        # Allow a short row (ROBOT would too) by padding empty cells.
        padded = row + [""] * (max(id_col, url_col, label_col) + 1 - len(row))

        raw_id = padded[id_col]
        url = padded[url_col].strip()
        label = padded[label_col].strip()

        cl_id = _normalise_id(raw_id)
        if cl_id is None:
            errors.append(f"line {i}: ID '{raw_id}' is not a well-formed CL identifier")
            continue
        if cl_id not in declared:
            errors.append(f"line {i}: {cl_id} is not declared in cl-edit.owl")
        if cl_id in obsolete:
            errors.append(f"line {i}: {cl_id} is marked obsolete in cl-edit.owl")

        if not url:
            errors.append(f"line {i}: missing CAP URL")
        elif not CAP_URL_PATTERN.match(url):
            errors.append(
                f"line {i}: URL '{url}' does not match the CAP label pattern "
                f"({CAP_URL_PATTERN.pattern})"
            )

        if not label:
            errors.append(f"line {i}: missing rdfs:label on the link")

        pair = (cl_id or raw_id, url)
        if pair in seen_pairs:
            errors.append(f"line {i}: duplicate (ID, URL) pair {pair}")
        seen_pairs.add(pair)

    # Silence unused-variable linters without weakening the error output.
    del header
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: validate_cap_links.py <cap_links.tsv> <cl-edit.owl>",
            file=sys.stderr,
        )
        return 2
    template = Path(argv[1])
    edit_owl = Path(argv[2])

    errors = validate(template, edit_owl)
    if errors:
        print("cap_links.tsv validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"cap_links.tsv OK ({template}): all rows valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
