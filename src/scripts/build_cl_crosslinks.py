#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Dict, List
import urllib.parse
import urllib.request

import pandas as pd

DEFAULT_ENDPOINT = "https://ubergraph.apps.renci.org/sparql"

# --------------------------
# Generic SPARQL query
# --------------------------
GENERIC_QUERY = r"""
PREFIX RO: <http://purl.obolibrary.org/obo/RO_>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oio: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?term (STR(?term_label) AS ?term_label_str) ?r (STR(?rl) AS ?relation_label) ?cl (STR(?clab) AS ?cell_label)
WHERE {{
  GRAPH <http://reasoner.renci.org/ontology> {{
    ?term rdfs:isDefinedBy obo:{obo_file} .
    ?cl   rdfs:isDefinedBy obo:cl.owl .
  }}
  GRAPH <http://reasoner.renci.org/nonredundant> {{
    ?term ?r ?cl .
  }}
  GRAPH <http://reasoner.renci.org/ontology> {{
    ?term rdfs:label ?term_label .
    ?cl   rdfs:label ?clab .
    ?r    rdfs:label ?rl .
  }}
}}

"""

# Which ontologies to build. Add more by appending to this list.
CONFIG = [
    {
        "key": "uberon2cl",
        "obo_file": "uberon.owl",
        "title": "UBERON → CL",
        "short": "UBERON",
    },
    {"key": "go2cl", "obo_file": "go.owl", "title": "GO → CL", "short": "GO"},
    {"key": "hp2cl", "obo_file": "hp.owl", "title": "HPO → CL", "short": "HPO"},
    {
        "key": "mondo2cl",
        "obo_file": "mondo.owl",
        "title": "MONDO → CL",
        "short": "MONDO",
    },
]


def _req(query_endpoint: str, query: str) -> Dict:
    data = urllib.parse.urlencode({"query": query}).encode("utf-8")
    req = urllib.request.Request(query_endpoint, data=data, method="POST")
    req.add_header("Accept", "application/sparql-results+json")
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _iri_to_curie(iri: str) -> str:
    # Turn OBO PURL into CURIE when possible
    if iri.startswith("http://purl.obolibrary.org/obo/"):
        frag = iri.rsplit("/", 1)[-1]
        return frag.replace("_", ":")
    return iri


def _results_to_df(bindings: List[Dict]) -> pd.DataFrame:
    # Single generic parser for ?term / ?term_label / ?r / ?cl
    rows = []
    for b in bindings:
        term = b["term"]["value"]
        rel = b["r"]["value"]
        cl = b["cl"]["value"]
        rows.append(
            {
                "subject_id": _iri_to_curie(term),
                "subject_label": b["term_label_str"]["value"],
                "relation_iri": rel,
                "relation_label": b["relation_label"]["value"],
                "cl_id": _iri_to_curie(cl),
                "cl_label": b["cell_label"]["value"],
            }
        )
    df = pd.DataFrame(rows).drop_duplicates()
    return df.sort_values(["subject_id", "relation_label", "cl_id"]).reset_index(
        drop=True
    )


def inspect_ontology(endpoint: str, obo_file: str) -> pd.DataFrame:
    """Run the generic query for a given ontology and return results as a DataFrame.

    Args:
      endpoint: SPARQL endpoint URL.
      obo_file: OBO filename for the source ontology (e.g., "go.owl").

    Returns:
      A DataFrame with columns:
      subject_id, subject_label, relation_iri, relation_label, cl_id, cl_label.
    """
    q = GENERIC_QUERY.format(obo_file=obo_file)
    res = _req(endpoint, q)
    bindings = res.get("results", {}).get("bindings", [])
    return _results_to_df(bindings)


def write_markdown(dfs: Dict[str, pd.DataFrame], md_path: str) -> None:
    """Write a Markdown summary with per-ontology collapsible sections.

    Args:
      dfs: Mapping from CONFIG keys to DataFrames produced by inspect_ontology.
      md_path: Output path for the Markdown file.
    """
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("## CL cross-ontology links\n\n")
        for item in CONFIG:
            key, title, short = item["key"], item["title"], item["short"]
            df = dfs[key]
            cols = [
                "subject_id",
                "subject_label",
                "relation_label",
                "cl_id",
                "cl_label",
            ]
            table = df[cols].rename(
                columns={
                    "subject_id": f"{short} ID",
                    "subject_label": f"{short} label",
                    "relation_label": "relation",
                    "cl_id": "CL ID",
                    "cl_label": "CL label",
                }
            )
            f.write(f"<details>\n<summary>{title} (count: {len(df)})</summary>\n\n")
            f.write(table.to_markdown(index=False))
            f.write("\n\n</details>\n\n")


def main() -> None:
    """CLI entry point for building cross-ontology tables and optional Markdown.

    Parses arguments, queries configured ontologies, writes CSV outputs, and
    optionally writes a Markdown summary file.
    """
    ap = argparse.ArgumentParser(
        description="Build CL cross-ontology link tables (HP/GO/MONDO/UBERON → CL)."
    )
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="SPARQL endpoint URL")
    ap.add_argument("--outdir", default="reports", help="Output directory for CSV/MD")
    ap.add_argument(
        "--markdown",
        action="store_true",
        help="Also write a Markdown summary for release notes",
    )
    ap.add_argument(
        "--markdown-file",
        default="cl_crosslinks.md",
        help="Markdown filename (inside outdir)",
    )
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    dfs: Dict[str, pd.DataFrame] = {}
    for item in CONFIG:
        key, obo_file = item["key"], item["obo_file"]
        print(f"Running {key} ({obo_file})…")
        df = inspect_ontology(args.endpoint, obo_file)
        dfs[key] = df
        out_csv = os.path.join(args.outdir, f"{key}.csv")
        df.to_csv(out_csv, index=False)
        print(f"Wrote {out_csv} ({len(df)} rows)")

    if args.markdown:
        md_path = os.path.join(args.outdir, args.markdown_file)
        write_markdown(dfs, md_path)
        print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
