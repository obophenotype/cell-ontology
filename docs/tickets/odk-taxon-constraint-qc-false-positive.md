# Taxon-constraint QC check reports false violations on every failing build

**Target repository:** [INCATools/ontology-development-kit](https://github.com/INCATools/ontology-development-kit)

**Reported from:** `obophenotype/cell-ontology`

**Environment:** `obolibrary/odkfull:v1.6`; `ODK_VERSION_MAKEFILE = v1.6.1`; ROBOT 1.9.10

## Summary

The taxon-constraint QC check decides whether an ontology violates taxon
constraints by testing whether a report file is **non-empty**, but that report
file captures ROBOT's *stdout* rather than a list of violations. ROBOT routinely
writes non-fatal parser logging to stdout, so the file is non-empty even when
reasoning succeeds and no constraint is violated.

The net effect is that **any** failing QC build is reported to the contributor as
a taxon-constraint violation, regardless of what actually failed. The misleading
comment is posted to the pull request, so contributors act on it.

## Where the code lives

Two pieces cooperate. In Cell Ontology:

- The Make target is repo-local, in `src/ontology/cl.Makefile`:

  ```make
  $(REPORTDIR)/taxon-constraint-check.txt: $(EDIT_PREPROCESSED) $(TMPDIR)/taxslim-disjoint-over-in-taxon.owl
  	$(ROBOT) merge $(foreach src,$^,-i $(src)) \
  		 expand -o $(TMPDIR)/cl-plus-taxon-disjoints.ofn \
  		 reason -r WHELK > $@

  test: $(REPORTDIR)/taxon-constraint-check.txt
  ```

- The reporting step is in the ODK-generated `.github/workflows/qc.yml`:

  ```yaml
  - name: Reason over taxon constraints
    id: explaintc
    continue-on-error: true
    if: steps.check.outcome == 'failure'
    run: |
      if [ -s src/ontology/reports/taxon-constraint-check.txt ]; then
        robot explain -i src/ontology/tmp/cl-plus-taxon-disjoints.ofn -M unsatisfiability -u all -r ELK -e taxon-unsats.md
        echo "<details>\n<summary>This PR violates some taxon constraints. Here is what the reasoner has to say:</summary>\n" > comments.md
        cat taxon-unsats.md >> comment.md
        echo "</details>" >> comment.md
        exit 1
      fi
  ```

**Provenance is unclear and maintainers should confirm it.** CL's `cl-odk.yaml`
sets only `workflows: [docs]`, yet `qc.yml` carries the ODK template header and
contains these taxon-constraint steps. We could not determine from the repository
alone whether the `qc.yml` step ships in the ODK template or was hand-added to
CL. Whichever side owns it, the defect is generic and worth fixing once upstream.

## Bug 1 — the report captures stdout, not violations

`reason -r WHELK > $@` redirects ROBOT's stdout into the report. ROBOT/OWLAPI log
non-fatal messages there. Running the target against current CL:

```
$ robot merge -i cl-edit.owl -i taxslim-disjoint-over-in-taxon.owl \
      expand -o cl-plus-taxon-disjoints.ofn reason -r WHELK > taxon-constraint-check.txt
$ echo $?
0
$ cat taxon-constraint-check.txt
2026-09-15 18:40:55,050 ERROR org.semanticweb.owlapi.rdf.rdfxml.parser.OWLRDFConsumer - Entity not properly recognized, missing triples in input? http://org.semanticweb.owlapi/error#Error1 for type Class
... (5 such lines)
```

Reasoning **succeeded**, there are no unsatisfiable classes, and yet the report is
non-empty. The messages come from parsing `taxslim.owl` /
`taxslim-disjoint-over-in-taxon.owl`, which CI downloads fresh on every run, so
this reproduces on every build rather than intermittently.

## Bug 2 — non-empty is used as the violation predicate

`if [ -s ... ]` treats "file has content" as "constraints are violated". Combined
with Bug 1 this is always true. Because the step is gated on
`steps.check.outcome == 'failure'`, every red build — whatever the cause — posts
"This PR violates some taxon constraints" to the pull request and exits 1.

## Bug 3 — the posted comment is assembled incorrectly

Three smaller defects in the same block:

1. The `<details>`/`<summary>` opener is written to `comments.md` (plural) while
   the body and closing `</details>` are appended to `comment.md` (singular). The
   step then posts `../../comment.md`, so the opener is missing and the posted
   HTML is unbalanced.
2. `echo "<details>\n<summary>...</summary>\n"` relies on `\n` being interpreted;
   with the default shell `echo` it is emitted literally. `printf` or `echo -e`
   is needed.
3. `robot explain` runs with `-r ELK`, while the check that produced the report
   ran with `-r WHELK`. Since the disjointness axioms use `ObjectComplementOf`,
   which is outside OWL EL, the explanation step may not reproduce what the check
   found. The two should use the same reasoner.

## Impact

A CL contributor debugging a red build was told the PR violated taxon
constraints. It did not: reasoning with WHELK over the ontology plus the fresh
disjointness axioms passed cleanly, and all 13 SPARQL validation checks passed.
The actual failure was the unrelated `test_obsolete` target, tripped by an object
property that had been obsoleted upstream in RO. The false attribution sent the
investigation toward reasoner differences (ELK vs WHELK) and cost substantial
time, because taxon-constraint violations are exactly the class of problem that
*would* plausibly behave differently between reasoners.

## Proposed fix

1. **Key the check off ROBOT's exit status, not the report's file size.** `robot
   reason` already exits non-zero when it finds unsatisfiable classes. For
   example:

   ```make
   $(REPORTDIR)/taxon-constraint-check.txt: $(EDIT_PREPROCESSED) $(TMPDIR)/taxslim-disjoint-over-in-taxon.owl
   	$(ROBOT) merge $(foreach src,$^,-i $(src)) \
   		 expand -o $(TMPDIR)/cl-plus-taxon-disjoints.ofn \
   		 reason -r WHELK -o /dev/null > $@ 2>&1 || touch $(TMPDIR)/tc-violations
   ```

   and have the workflow test for the marker file rather than for report content.

2. **Or** generate the report from `robot explain -M unsatisfiability` only, so
   that its contents are violations by construction and `-s` becomes a correct
   predicate.

3. Fix the `comments.md`/`comment.md` filename mismatch, use `printf` for the
   multi-line HTML, and align the `explain` reasoner with the `reason` reasoner.

4. Consider shipping this as a supported ODK option (e.g. a
   `taxon_constraint_check` flag in `*-odk.yaml`) that generates both the Make
   target and the workflow step correctly, so downstream ontologies do not
   hand-roll the pattern. CL, Uberon and others all need it.

## How to reproduce

From a clean CL checkout, introduce a failure in any QC check unrelated to taxon
constraints — for example add a term with no definition so `robot report` fails —
then run the workflow. The build comments that the PR violates taxon constraints
even though `reason -r WHELK` over `cl-plus-taxon-disjoints.ofn` exits 0.
