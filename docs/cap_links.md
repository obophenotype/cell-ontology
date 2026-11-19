# CAP reference-data `rdfs:seeAlso` links

CL terms carry `rdfs:seeAlso` links back to the matching cell type on the
[Cell Annotation Platform (CAP)](https://celltype.info). These links let
tooling and portals jump from a CL class to the transcriptomic reference
data for the same cell type.

This page covers how the links are modelled, how they are managed, and
the rules that keep them consistent. It mirrors the pattern already in
place for the Allen Brain Cell (ABC) Atlas links in `wmbo-cl-comp.owl`
and `bgo-cl-comp.owl`.

## Where to edit

**CAP links are managed only through
[`src/templates/cap_links.tsv`](https://github.com/obophenotype/cell-ontology/blob/master/src/templates/cap_links.tsv).**
Do not add `rdfs:seeAlso` links to `celltype.info` URLs directly in
`cl-edit.owl`. A release-level SPARQL check will flag any CAP links that
sit outside the component.

The template compiles into `src/ontology/components/cap_links.owl`,
which is imported by `cl-edit.owl` and therefore reaches `cl.obo`,
`cl-base.owl`, OLS and every other CL consumer by the same route as the
ABC links.

## Axiom shape

Each row produces one axiom-annotated `rdfs:seeAlso`:

```
AnnotationAssertion(
  Annotation(rdfs:label "“<CAP label name>” in <dataset title>")
  rdfs:seeAlso obo:CL_XXXXXXX
  "https://celltype.info/project/P/dataset/D/label/L"
)
```

For example, a link to CAP label `214551` in the retinal atlas:

```
AnnotationAssertion(
  Annotation(rdfs:label "“retinal bipolar neuron” in Single cell atlas of the human retina - Bipolar cell subclass - scRNA-seq")
  rdfs:seeAlso obo:CL_0000748
  "https://celltype.info/project/544/dataset/1157/label/214551"
)
```

- The URL is a plain string literal, matching the ABC links.
- The axiom annotation label is `“<CAP label name>” in <dataset title>`
  — the CAP label's own display name wrapped in Unicode curly double
  quotes (`U+201C` and `U+201D`), then a literal ` in `, then the
  dataset title. Quoting the CAP label name surfaces the label verbatim
  so tools and humans can recognise CAP links without a shared fixed
  prefix, and makes multiple CAP links on one CL term distinguishable
  at a glance.
- **Use curly quotes (`“ ”`), not straight ASCII `"`.** The TSV is
  parsed as CSV by both ROBOT and the validator, and a straight `"` at
  the start of a field is treated as a CSV quote delimiter and silently
  stripped. Curly quotes pass through unchanged.
- h5ad download links are **not** modelled on CL terms. CAP exposes
  h5ad download through its own client; adding it here would duplicate
  that.

## URL rules

CAP URLs must be label URLs on the production host:

```
^https://celltype\.info/project/\d+/dataset/\d+/label/\d+$
```

Labelset URLs (`/labelset/`) and the `rc1.celltype.info` staging host
are both rejected.

## Which datasets count as "reference"

Reference datasets are the official **Human Cell Atlas (HCA)** datasets
hosted on CAP. When no HCA dataset exists for a region or tissue, open a
tracker issue to discuss before adding a non-HCA source.

## Mapping precision

Broader mappings are allowed. Pick the **closest** CL term for each CAP
label.

If more than one CAP label in the same dataset maps equally well to the
same CL term, pick the single best match and note the alternatives in
the tracker issue so the decision can be revisited.

## Template format

`src/templates/cap_links.tsv` is tab-separated because dataset titles
contain commas. It uses the usual two-row ROBOT header: the first row
is the human-readable column names, the second is the ROBOT directive
row. Bookkeeping columns (for the editor's own notes) carry an empty
ROBOT directive so ROBOT ignores them.

Columns:

| Column                | ROBOT directive   | Purpose                                                        |
|-----------------------|-------------------|----------------------------------------------------------------|
| `cl_label`            | *(empty)*         | CL label, for readability                                      |
| `cap_project_id`      | *(empty)*         | CAP project ID                                                 |
| `cap_dataset_id`      | *(empty)*         | CAP dataset ID                                                 |
| `cap_label_id`        | *(empty)*         | CAP label ID                                                   |
| `cap_label_name`      | *(empty)*         | CAP label display name                                         |
| `species`             | *(empty)*         | NCBI taxon or species name                                     |
| `tissue`              | *(empty)*         | UBERON term or tissue name                                     |
| `source_issue`        | *(empty)*         | Tracker issue that justified the row                           |
| `ID`                  | `ID`              | CL term ID (e.g. `CL:0000540`)                                 |
| `CAP URL`             | `A rdfs:seeAlso`  | CAP label URL                                                  |
| `Link label`          | `>A rdfs:label`   | Axiom annotation label on the link                             |
| `Link comment`        | `>A rdfs:comment` | Optional axiom annotation comment                              |

Each row maps to a single CAP label. Do **not** use `SPLIT` because the
axiom annotation would then apply to every value.

## Workflow

CAP links are curated by hand in `src/templates/cap_links.tsv`.

1. Append one row per CAP label. Fill in the bookkeeping columns
   (`cl_label`, `cap_project_id`, `cap_dataset_id`, `cap_label_id`,
   `cap_label_name`, `species`, `tissue`, `source_issue`) as well as
   the ROBOT directive columns (`ID`, `CAP URL`, `Link label`, optional
   `Link comment`).
2. Validate locally:
   ```
   python3 src/scripts/validate_cap_links.py \
     src/templates/cap_links.tsv src/ontology/cl-edit.owl
   ```
3. Build the component:
   ```
   cd src/ontology && make components/cap_links.owl
   ```
4. Commit the TSV; the component is regenerated on every build.

## Checks

### Template-level, before ROBOT compiles

`src/scripts/validate_cap_links.py` runs as part of
`components/cap_links.owl`'s Make rule. It verifies that:

- every `ID` exists in `cl-edit.owl` and is not obsolete;
- no duplicate (ID, URL) pair appears twice;
- every URL matches the production CAP label pattern above;
- every row has a link label matching `“<cap label name>” in <dataset title>`
  (curly quotes `U+201C` / `U+201D`, not straight `"`).

A failure here aborts the build. This is critical: without the check,
ROBOT would silently mint a stub class for an unknown ID.

### Release-level SPARQL check

`src/sparql/cap-link-violation.sparql` is wired into
`cl-odk.yaml :: custom_sparql_checks` as `cap-link` and runs on every
release. It flags:

- CAP links on obsolete classes;
- CAP URLs that fail the production label pattern (including labelset
  URLs and `rc1` staging URLs);
- CAP links without an `rdfs:label` axiom annotation;
- CAP links whose `rdfs:label` does not match
  `“<cap label name>” in <dataset title>` (curly quotes `U+201C` /
  `U+201D`).

The query can also be run on demand:

```
cd src/ontology && robot query \
  --input cl-edit.owl \
  --query ../sparql/cap-link-violation.sparql \
  cap-link-violations.tsv
```

### Optional link-health

A periodic external link-checker that follows each CAP URL would catch
retired CAP IDs. That is out of scope for this repository's CI; run it
as a separate cron or routine when ready.

## Related

- `src/ontology/components/wmbo-cl-comp.owl` — ABC atlas links for the
  whole mouse brain ontology.
- `src/ontology/components/bgo-cl-comp.owl` — ABC atlas links for the
  basal ganglia ontology.
