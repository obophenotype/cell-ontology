#!/usr/bin/env python3
"""Regenerate the generated rows in ``src/templates/cap_links.tsv``.

Reads a curated config of CAP datasets at ``src/metadata/cap_datasets.yaml``
(project ID, dataset ID, display title plus optional species/tissue), calls
the CAP public API for each dataset to pull its labels that carry a CL
term, and writes generated rows back into the template.

Manual rows (``manual_or_generated = manual``) are preserved verbatim.

This is **not** run as part of the normal ontology build — it is driven
through an explicit ``make update-cap-links`` target so the resulting
template diff can be reviewed in a PR.

Mapping precision follows issue #3875: broader mappings are allowed, the
closest CL term wins, and if several CAP labels within one dataset map
equally well to the same CL term the script emits a warning (rows are
still written).

Dataset labels are expected to expose their CL mapping as either
``cl_term`` (``CL:NNNNNNN`` or ``CL_NNNNNNN`` or an obo IRI) or an
equivalent field — the exact field name is configured per dataset in the
YAML under ``cl_field`` so that the script does not have to hard-code
the CAP schema.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    print(
        "PyYAML is required: pip install pyyaml (or run inside the ODK image)",
        file=sys.stderr,
    )
    raise

CAP_URL_TEMPLATE = (
    "https://celltype.info/project/{project}/dataset/{dataset}/label/{label}"
)
LABEL_PREFIX = "Reference data on Cell Annotation Platform: "

CL_ID_RE = re.compile(r"CL[:_](\d{7})")


def _normalise_cl(raw: str | None) -> str | None:
    if not raw:
        return None
    m = CL_ID_RE.search(raw)
    return f"CL:{m.group(1)}" if m else None


def _fetch_dataset(project_id: int, dataset_id: int, api_base: str) -> list[dict[str, Any]]:
    """Return the labels payload for one CAP dataset.

    The exact API endpoint is parametrised through ``api_base`` so this
    script can be redirected at a staging instance or a cached JSON file
    when developing offline.
    """
    url = f"{api_base}/project/{project_id}/dataset/{dataset_id}/labels"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
        payload = json.load(resp)
    if isinstance(payload, dict) and "labels" in payload:
        payload = payload["labels"]
    if not isinstance(payload, list):
        raise RuntimeError(
            f"unexpected CAP response for project {project_id} dataset {dataset_id}"
        )
    return payload


def _read_existing(template: Path) -> tuple[list[str], list[str], list[list[str]]]:
    with template.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    if len(rows) < 2:
        raise RuntimeError(f"{template} is missing header or ROBOT directive row")
    return rows[0], rows[1], rows[2:]


def _partition_manual(data_rows: list[list[str]], flag_col: int) -> tuple[list[list[str]], list[list[str]]]:
    manual: list[list[str]] = []
    generated: list[list[str]] = []
    for row in data_rows:
        flag = row[flag_col].strip().lower() if flag_col < len(row) else ""
        if flag == "manual":
            manual.append(row)
        else:
            generated.append(row)
    return manual, generated


def _row_for(label: dict[str, Any], dataset_cfg: dict[str, Any]) -> list[str] | None:
    cl_field = dataset_cfg.get("cl_field", "cl_term")
    cl_id = _normalise_cl(label.get(cl_field))
    if not cl_id:
        return None
    label_id = label.get("label_id") or label.get("id")
    if label_id is None:
        return None
    url = CAP_URL_TEMPLATE.format(
        project=dataset_cfg["project_id"],
        dataset=dataset_cfg["dataset_id"],
        label=label_id,
    )
    link_label = f"{LABEL_PREFIX}{dataset_cfg['title']}"
    return [
        label.get("cl_label", ""),
        str(dataset_cfg["project_id"]),
        str(dataset_cfg["dataset_id"]),
        str(label_id),
        label.get("name", ""),
        dataset_cfg.get("species", ""),
        dataset_cfg.get("tissue", ""),
        "generated",
        dataset_cfg.get("source_issue", ""),
        cl_id,
        url,
        link_label,
        "",
    ]


def _warn_ties(rows: list[list[str]]) -> None:
    """Flag CAP labels in the same dataset that map to the same CL term."""
    by_dataset: dict[tuple[str, str], dict[str, list[str]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in rows:
        _, project, dataset, label_id, *_rest, cl_id, _url, _lbl, _cmt = row + [""] * (13 - len(row))
        by_dataset[(project, dataset)][cl_id].append(label_id)
    for (project, dataset), mapping in by_dataset.items():
        for cl_id, label_ids in mapping.items():
            if len(label_ids) > 1:
                print(
                    f"warning: project {project} dataset {dataset}: "
                    f"{cl_id} has multiple CAP labels mapped ({', '.join(label_ids)}). "
                    "Review and pick the closest match manually.",
                    file=sys.stderr,
                )


def regenerate(template: Path, config: Path, api_base: str, dry_run: bool) -> int:
    header, robot_header, data_rows = _read_existing(template)
    flag_col = header.index("manual_or_generated")

    manual, _old_generated = _partition_manual(data_rows, flag_col)

    with config.open("r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}
    datasets = cfg.get("datasets", [])

    new_generated: list[list[str]] = []
    for dataset_cfg in datasets:
        print(
            f"fetching CAP project {dataset_cfg['project_id']} "
            f"dataset {dataset_cfg['dataset_id']} ({dataset_cfg['title']})",
            file=sys.stderr,
        )
        try:
            labels = _fetch_dataset(
                dataset_cfg["project_id"], dataset_cfg["dataset_id"], api_base
            )
        except urllib.error.URLError as exc:
            print(f"  skipped: {exc}", file=sys.stderr)
            continue
        for label in labels:
            row = _row_for(label, dataset_cfg)
            if row is not None:
                new_generated.append(row)

    _warn_ties(new_generated)

    combined = manual + new_generated
    combined.sort(key=lambda r: (r[header.index("ID")], r[header.index("CAP URL")]))

    out_rows: list[list[str]] = [header, robot_header, *combined]

    if dry_run:
        print(
            f"dry-run: would write {len(new_generated)} generated rows "
            f"({len(manual)} manual preserved)",
            file=sys.stderr,
        )
        return 0

    with template.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerows(out_rows)
    print(
        f"wrote {template}: {len(new_generated)} generated rows "
        f"({len(manual)} manual preserved)",
        file=sys.stderr,
    )
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        default="src/templates/cap_links.tsv",
        help="path to the CAP links TSV (default: src/templates/cap_links.tsv)",
    )
    parser.add_argument(
        "--config",
        default="src/metadata/cap_datasets.yaml",
        help="path to the curated CAP datasets config",
    )
    parser.add_argument(
        "--api-base",
        default="https://celltype.info/api",
        help="CAP API base URL (override for staging or a local JSON cache)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="fetch and report but do not write the template",
    )
    args = parser.parse_args(argv[1:])
    return regenerate(
        Path(args.template), Path(args.config), args.api_base, args.dry_run
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
