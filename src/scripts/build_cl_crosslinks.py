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

HP2CL = r"""
PREFIX HP: <http://purl.obolibrary.org/obo/HP_>
PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
PREFIX RO: <http://purl.obolibrary.org/obo/RO_>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oio: <http://www.geneontology.org/formats/oboInOwl#>
SELECT distinct ?hp (STR(?hpl) as ?hp_label) ?r (STR(?rl) as ?relation_label) ?cl (STR(?clab) as ?cell_label)
WHERE {
  GRAPH <http://reasoner.renci.org/ontology> {
    ?hp rdfs:isDefinedBy obo:hp.owl .
    ?cl rdfs:isDefinedBy obo:cl.owl
  }
  GRAPH <http://reasoner.renci.org/nonredundant> { ?hp ?r ?cl }
  GRAPH <http://reasoner.renci.org/ontology> {
    ?hp rdfs:label ?hpl .
    ?cl rdfs:label ?clab .
    ?r  rdfs:label ?rl
  }
}
"""

GO2CL = r"""
PREFIX GO: <http://purl.obolibrary.org/obo/GO_>
PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
PREFIX RO: <http://purl.obolibrary.org/obo/RO_>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oio: <http://www.geneontology.org/formats/oboInOwl#>
SELECT distinct ?go (STR(?gol) as ?go_label) ?r (STR(?rl) as ?relation_label) ?cl (STR(?clab) as ?cell_label)
WHERE {
  GRAPH <http://reasoner.renci.org/ontology> {
    ?go rdfs:isDefinedBy obo:go.owl .
    ?cl rdfs:isDefinedBy obo:cl.owl
  }
  GRAPH <http://reasoner.renci.org/nonredundant> { ?go ?r ?cl }
  GRAPH <http://reasoner.renci.org/ontology> {
    ?go rdfs:label ?gol .
    ?cl rdfs:label ?clab .
    ?r  rdfs:label ?rl
  }
}
"""

MONDO2CL = r"""
PREFIX MONDO: <http://purl.obolibrary.org/obo/MONDO_>
PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
PREFIX RO: <http://purl.obolibrary.org/obo/RO_>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oio: <http://www.geneontology.org/formats/oboInOwl#>
SELECT distinct ?mondo (STR(?mondol) as ?mondo_label) ?r (STR(?rl) as ?relation_label) ?cl (STR(?clab) as ?cell_label)
WHERE {
  GRAPH <http://reasoner.renci.org/ontology> {
    ?mondo rdfs:isDefinedBy obo:mondo.owl .
    ?cl rdfs:isDefinedBy obo:cl.owl
  }
  GRAPH <http://reasoner.renci.org/nonredundant> { ?mondo ?r ?cl }
  GRAPH <http://reasoner.renci.org/ontology> {
    ?mondo rdfs:label ?mondol .
    ?cl rdfs:label ?clab .
    ?r  rdfs:label ?rl
  }
}
"""

UBERON2CL = r"""
PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
PREFIX RO: <http://purl.obolibrary.org/obo/RO_>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oio: <http://www.geneontology.org/formats/oboInOwl#>
SELECT distinct ?uberon (STR(?uberonl) as ?uberon_label) ?r (STR(?rl) as ?relation_label) ?cl (STR(?clab) as ?cell_label)
WHERE {
  GRAPH <http://reasoner.renci.org/ontology> {
    ?uberon rdfs:isDefinedBy obo:uberon.owl .
    ?cl rdfs:isDefinedBy obo:cl.owl
  }
  GRAPH <http://reasoner.renci.org/nonredundant> { ?uberon ?r ?cl }
  GRAPH <http://reasoner.renci.org/ontology> {
    ?uberon rdfs:label ?uberonl .
    ?cl rdfs:label ?clab .
    ?r  rdfs:label ?rl
  }
}
"""

QUERIES = {
    "hp2cl": HP2CL,
    "go2cl": GO2CL,
    "mondo2cl": MONDO2CL,
    "uberon2cl": UBERON2CL,
}


def _req(endpoint: str, query: str) -> Dict:
    data = urllib.parse.urlencode({"query": query}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=data, method="POST")
    req.add_header("Accept", "application/sparql-results+json")
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _iri_to_curie(iri: str) -> str:
    if iri.startswith("http://purl.obolibrary.org/obo/"):
        frag = iri.rsplit("/", 1)[-1]
        return frag.replace("_", ":")
    return iri


def _results_to_df(bindings: List[Dict], mapping: str) -> pd.DataFrame:
    # Normalize columns based on which mapping it is
    if mapping == "hp2cl":
        sid, slabel = "hp", "hp_label"
    elif mapping == "go2cl":
        sid, slabel = "go", "go_label"
    elif mapping == "mondo2cl":
        sid, slabel = "mondo", "mondo_label"
    elif mapping == "uberon2cl":
        sid, slabel = "uberon", "uberon_label"
    else:
        raise ValueError(mapping)

    rows = []
    for b in bindings:
        subj = b[sid]["value"]
        rel = b["r"]["value"]
        cl = b["cl"]["value"]
        rows.append(
            {
                "subject_id": _iri_to_curie(subj),
                "subject_label": b[slabel]["value"],
                "relation_iri": rel,
                "relation_label": b["relation_label"]["value"],
                "cl_id": _iri_to_curie(cl),
                "cl_label": b["cell_label"]["value"],
            }
        )
    df = pd.DataFrame(rows).drop_duplicates()
    # Stable sort for deterministic files
    return df.sort_values(["subject_id", "relation_label", "cl_id"]).reset_index(
        drop=True
    )


def run_one(endpoint: str, key: str, query: str) -> pd.DataFrame:
    res = _req(endpoint, query)
    bindings = res.get("results", {}).get("bindings", [])
    return _results_to_df(bindings, key)


def write_markdown(
    dfs: Dict[str, pd.DataFrame], md_path: str, max_rows_per_section: int = 50
) -> None:
    # Compact, release-notes-friendly MD file with collapsible sections
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("## CL cross-ontology links\n\n")
        order = [
            ("uberon2cl", "UBERON → CL"),
            ("go2cl", "GO → CL"),
            ("hp2cl", "HP → CL"),
            ("mondo2cl", "MONDO → CL"),
        ]
        for key, title in order:
            df = dfs[key]
            # Preview head to keep release notes tidy; actual CSVs contain all rows.
            if max_rows_per_section is None:
                preview = df[["subject_id", "subject_label", "relation_label", "cl_id", "cl_label"]]
            else:
                preview = df.head(max_rows_per_section)[
                    ["subject_id", "subject_label", "relation_label", "cl_id", "cl_label"]
                ]
            preview.rename(
                columns={
                    "subject_id": title.split(" ")[0] + " ID",
                    "subject_label": title.split(" ")[0] + " label",
                    "relation_label": "relation",
                    "cl_id": "CL ID",
                    "cl_label": "CL label",
                }
            )
            f.write(f"<details>\n<summary>{title} (count: {len(df)})</summary>\n\n")
            f.write(preview.to_markdown(index=False))
            f.write("\n\n</details>\n\n")


def main():
    ap = argparse.ArgumentParser(
        description="Build CL cross-ontology link tables (HP/GO/MONDO/UBERON → CL)."
    )
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="SPARQL endpoint URL")
    ap.add_argument(
        "--outdir", default="reports", help="Output directory for CSV/MD"
    )
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
    ap.add_argument(
        "--rows",
        type=int,
        default=None,
        help="Rows per section in Markdown preview (default: all rows)",
    )
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    dfs = {}
    for key, query in QUERIES.items():
        print(f"Running {key}…", file=sys.stderr)
        df = run_one(args.endpoint, key, query)
        dfs[key] = df
        out_csv = os.path.join(args.outdir, f"{key}.csv")
        df.to_csv(out_csv, index=False)
        print(f"Wrote {out_csv} ({len(df)} rows)", file=sys.stderr)

    if args.markdown:
        md_path = os.path.join(args.outdir, args.markdown_file)
        write_markdown(dfs, str(md_path), args.rows)
        print(f"Wrote {md_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
