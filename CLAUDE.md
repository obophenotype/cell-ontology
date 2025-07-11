# CL Ontology Project Guide

This includes instructions for editing the cl ontology. 

## Project Layout
- Main development file is `src/ontology/cl-edit.owl` (functional syntax, one line per axiom)
- ODK and ontology documentation can be found in `/docs/`

## Querying ontology

- Use grep/rg to find terms. Exploit the fact that typically it is one axiom per line
    - `grep -i neuron src/ontology/cl-edit.owl` - all axioms that mention neuron
    - `grep 'AnnotationAssertion(rdfs:label.*neuron' src/ontology/cl-edit.owl` - all label axioms that mention neuron
- All mentions of an ID
    - `obo-grep.pl -r 'CL_0004177' src/ontology/cl-edit.owl`
- Only search over `src/ontology/cl-edit.owl`
- DO NOT bother doing your own greps over the file, or looking for other files, unless otherwise asked, you will just waste time.
- ONLY use the methods above for searching the ontology

## Before making edits
- Read the request carefully and make a plan, especially if there is nuance
- If related issues are mentioned read them: `gh issue view GITHUB-ISSUE-NUMBER`
- if a PMID is mentioned in the issue, ALWAYS try and read it
- ALWAYS check proposed parent terms for consistency
- For terms that are compositional, check `src/patterns/dosdp-patterns/*.yaml`

## Editors guide
- design patterns are in docs/patterns
- a guide to what relations to use for recording locations, properties etc can be found in docs/relations_guide.md


## OBO Guidelines
- Term ID format: CL_NNNNNNN (7-digit number)
- Handling New Term Requests (NTRs):
  - New terms start  CL_777xxxx
  - Do `grep CL_777 src/ontology/cl-edit.owl` to check for clashes
- Each term requires: id, name, definition with references
- Never guess CL IDs, or ontology term IDs, use search tools above to determine actual term
- Never guess PMIDs for references, do a web search if needed
- Use standard relationship types: is_a, part_of, has_part, etc.
- Follow existing term patterns for consistency

## Publications
- Run the command `aurelian fulltext <PMID:nnn>` to fetch full text for a publication. A doi or URL can also be used
- You should cite publications appropriately, e.g. `def: "...." [PMID:nnnn, doi:mmmm]

## GitHub Contribution Process
- most requests from users should follow one of two patterns:
    - you are not confident how to proceed, in which case end with asking a clarifying question (via `gh`)
    - you are confident how to proceed, you make changes, commit on a branch, and open a PR for the user to review
- Check existing terms before adding new ones
- For new terms: provide name, definition, place in hierarchy, and references
- Include PMIDs for all assertions
- Follow naming conventions from parent terms
- always commit in a branch, e.g. issue-NNN
- if there is an existing PR which you started then checkout that branch and continue, rather than starting a new PR (unless you explicitly want to abandon the original PR, e.g. it was on completely the wrong tracks)
- always make clear detailed commit messages, saying what you did and why
- always sign your commits `@dragon-ai-agent`
- create PRs using `gh pr create ...`
- File PRs with clear descriptions, and sign your PR

## Handling GitHub issues and requests
- Use `gh` to read and write issues/PRs
- Sign all commits and PRs as `@dragon-ai-agent`

## TROUBLESHOOTING

- if your obo file has syntax errors, you can use `robot convert -vvv` to see full trace
- use `robot reason` to validate

## Obsoleting terms

obsolete terms should have no logical axioms (e.g. SubClassOf, EquivalentClasses) on them. Obsolete terms may be replaced by a single
term (so-called obsoletion with exact replacement), or by zero to many `consider` tags.


Synonyms and xrefs can be migrated judiciously,

We never do complete merges now, so there should be no `alt_ids` or
disappearing stanzas. If a user asks for a merge, they usually mean
obsoletion with direct replacement, as here:

Example:

```
# Class: obo:CL_4072102 (Purkinje layer interneuron)
AnnotationAssertion(Annotation(oboInOwl:hasDbXref "PMID:35803588") obo:IAO_0000115 obo:CL_4072102 "A type of GABAergic interneuron residing in the Purkinje cell layer of the cerebellar cortex.")
AnnotationAssertion(terms:date obo:CL_4072102 "2025-04-29T13:06:36Z"^^xsd:dateTime)
AnnotationAssertion(Annotation(oboInOwl:hasDbXref "PMID:35803588") Annotation(oboInOwl:hasSynonymType obo:OMO_0003000) oboInOwl:hasRelatedSynonym obo:CL_4072102 "PLI")
AnnotationAssertion(rdfs:label obo:CL_4072102 "Purkinje layer interneuron")
EquivalentClasses(obo:CL_4072102 ObjectIntersectionOf(obo:CL_0000099 ObjectSomeValuesFrom(obo:RO_0002100 obo:UBERON_0002979)))
SubClassOf(obo:CL_4072102 ObjectSomeValuesFrom(obo:RO_0002215 obo:GO_0061534))
```

No relationship should point to an obsolete term - when you obsolete a term, you may need to also rewire
terms to "skip" the obsoleted term.

## Other metadata

- Link back to the issue you are dealing with using the `term_tracker_item`
- All terms should have definitions, with at least one definition xref, ideally a PMID
- You can sign terms as `created_by: dragon-ai-agent`

## Relationships

All terms should have at least one "is_a" (SubClassOf to a named class) -- (this can be implicit by a logical definition, see below).
Many terms in this ontology have part_of relationships to UBERON.

## Logical definitions

These should follow genus-differentia form, and the text definition should mirror the logical definition. Example:

```
# Class: obo:CL_4072102 (Purkinje layer interneuron)
AnnotationAssertion(Annotation(oboInOwl:hasDbXref "PMID:35803588") obo:IAO_0000115 obo:CL_4072102 "A type of GABAergic interneuron residing in the Purkinje cell layer of the cerebellar cortex.")
AnnotationAssertion(terms:date obo:CL_4072102 "2025-04-29T13:06:36Z"^^xsd:dateTime)
AnnotationAssertion(Annotation(oboInOwl:hasDbXref "PMID:35803588") Annotation(oboInOwl:hasSynonymType obo:OMO_0003000) oboInOwl:hasRelatedSynonym obo:CL_4072102 "PLI")
AnnotationAssertion(rdfs:label obo:CL_4072102 "Purkinje layer interneuron")
EquivalentClasses(obo:CL_4072102 ObjectIntersectionOf(obo:CL_0000099 ObjectSomeValuesFrom(obo:RO_0002100 obo:UBERON_0002979)))
SubClassOf(obo:CL_4072102 ObjectSomeValuesFrom(obo:RO_0002215 obo:GO_0061534))
```

The reasoner can find the most specific `is_a`, so it's OK to leave this off.

