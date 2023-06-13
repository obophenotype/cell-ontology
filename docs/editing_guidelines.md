# Guidelines for CL editors

## Naming terms

### General rules
1. All labels should be singular nouns.
2. Words should not be capitalized, unless they are proper names or are capitalized as a standard (e.g., “Peyer's” and “B” in “Peyer's patch B cell”).
3. Avoid special characters: use only alphanumeric characters, space, dash (`-`), slash (`/`), and apostrophe (`'`).

### Advice
Bear in mind that users will often encounter terms in isolation. Long, descriptive labels (within reason!) are therefore preferable, especially where there is obvious potential for confusion. For example, _calyx_ (which simply means “cup”) could refer to a structure in the oviduct or in the mushroom body, depending on your field of specialization. It is therefore better to use _mushroom body calyx_ or _oviduct calyx_ rather than simply _calyx_ alone.

Try to maintain consistent patterns of naming where possible. However, it may make sense to override this in order to conform to common usage.


## Defining terms
This section is about the _textual_ definition of terms. Logically consistent classification is important, but an ontology is only useful (and maintainable) if all humans that interact with it (users, curators and editors) can quickly find the terms they need and understand what they refer to. This requires clear, unambiguous, human-readable definitions.

When crafting a definition, editors should aim for a reasonably succinct statement about the class allowing curators and users to easily distinguish it from other, similar classes, and which captures key points of interest about that class. It should capture assertions made in the formal part of the definition (the relationships) as closely as possible without becoming stilted and difficult to read.

The basic structure of a definition should be as follows:

> A `genus` that `diff1` and `diff2`. It also `diff3` and `gloss`...

where `genus` is a general classification and `diff1`, `diff2`, etc. are the _differentia_, which state what differentiates this class from others that share the same general classification. The gloss, when present, gives some key points of interest about the class.

The first sentence of the definition should refer to the definiendum in singular form. The rest of the definition may then invoke the plural form.


### Contents of definitions
It is difficult to specify, _a priori_, which assertions should be included in a textual definition. However there are some general guidelines.

1. DO make sure your definition is consistent with the definition of the superclass(es).
2. DO make sure your definition includes the information that is recorded in all the direct formal relationships to the class.
3. AVOID assertions about structures or cell types that are not part of the cell type being described, except when they pertain to some direct relationships with the cell type being described.
4. AVOID including details that could better be included in the definition of subtypes of the cell type being described.
5. LIMIT information that applies to only some members of the class. This should only be used sparingly; when used, it should be made clear that it does not apply to all members of the class.
6. AVOID using gene expression as the differentium.
7. AVOID extensive repetition of assertions made in superclass definitions, unless these assertions are used to provide direct evidence for class membership.
8. DO NOT add informations about what happens in mutant or pathological states backgrounds or other kinds of non-control conditions.
9. DO NOT include reasons for believing the assertions to be true. These should be recorded in comments.
10. DO NOT raise questions in the definition. The definition should have the sense of being definitive, which is undermined if we show doubt. Any doubt should be recorded in comments instead.


## Comments
Comments should be used for:

1. Providing evidence. In some cases it is useful to know the type of evidence for an assertion. This should not be recorded in the definition, but _can_ be recorded in a comment.
2. Disambiguation. Sometimes a single term is used in the literature with multiple meanings. In such cases, a comment should be added outlining these different uses and how they relate to the definition set in the ontology.
3. Reporting editorial decisions (or decisions in waiting) about the term. This includes providing a reason for obsoleting a term, or letting users and curators know that the term may be merged or split in the future, e.g., when enough evidence for the merge/split will be available.

Try to be consistent in how you phrase the various types of comments. For example:

* when giving a reason for obsoletion, use “Obsoleted as ...”;
* when indicating a potential future merge, use “Possible equivalence with {other term} ...”.


## Synonyms
Extensive addition of synonyms helps “findability” of terms when search. Synonyms can and should be added liberally.

Guidelines on the type of synonyms:

1. Use an _exact_ synonym only when the label and the synonym can be used interchangeably without dispute and refer to the same concept. For example, the terms “leukocyte”, “leucocyte” (spelling variation”) and “white blood cell” (layman’s term) all refer to the exact same concept (a specific cell type) and would be considered exact synonyms. Terms that may refer to other concepts, especially within the biomedical domain, should not be annotated as exact synonyms, including abbreviations. A synonym that is an abbreviation should be annotated as a _related_ synonym and with property type “abbreviation” (technically: the synonym annotation assertion axiom should itself be annotated with a `http://www.geneontology.org/formats/oboInOwl#hasSynonymType` property with value `http://purl.obolibrary.org/obo/cl#abbreviation`). For example, “WBC” can stand for “white blood cell” and refer to “leukocyte”, but within the biomedical domain it can also represent “white blood cell count” or, perhaps less frequently, “whole-body counting”, two distinct concepts with separate OBO ontology terms.
2. Exact synonyms should be unique across the ontology. In other words, if class _A_ has synonym “X”, “X” should not be an exact synonym for any other CL term.
3. Be mindful of the “directionality” of the _narrow_ and _broad_ types of synonyms. They qualify the _synonym_, not the original term. For example, saying that “peripheral blood mononuclear cell” is a narrow synonym of “mononuclear cell” means that “peripheral blood mononuclear cell“ refers to a narrower concept than “mononuclear cell”, not the other way around.
4. The _related_ synonym type should be used for cases where the overlap between the synonym and the term label may be uncler, disputable or not true in all scenarios or contexts, but you want the term to be findable when searching. This includes abbreviations, which should be annotated as _related_ synonyms with synonym type “abbreviation” (see point 1 above).
5. If a synonym includes a mix of abbreviations and words, the _related_ type should still be used unless there is enough context within the synonym itself to make it clear that the synonyms refers only to the concept being annotated. For example, “lung TRM CD8-positive, CD103-positive cell” would be an exact synonym of “lung resident memory CD8-positive, CD103-positive, alpha-beta T cell”, even though “TRM” (in this case) is an abbreviation for “tissue resident T cell”. Note that without this context “TRM” should not be considered an exact synonym for “tissue resident T cell” as “TRM” could also mean “treatment-related mortality”, another OBO ontology concept. Compare the previous example to “IMB cell”, which should be a _related_ synonym of “invaginating midget bipolar cell”.


## Considerations on style
The following considerations apply both to all human-readable fields (names, textual definitions, comments, synonyms).

* **United States (US) English or British English?** Where there are differences in the accepted spelling between British and US English, use the US form. British English variants of the labels may be added as synonyms (e.g., a term labelled “epithelial cell of esophagus” may have “epithelial cell of oesophagus” as an exact synonym).
* **Use of jargon.** The aim of the ontology is to provide useable descriptions and links to the reader. Consequently, try to avoid obscure jargon or pretentious Latin/Greek, especially where widely understood, plain alternatives exist. Where it will aid searching, such terms may be added to synonyms and/or as asides in the “gloss” part of definitions.
* **That or which?** These are so interchangeable that there isn’t really a rule anymore. But as a guideline, use “which” after a comma (e.g., “this study, which cost $10,000, was a success”), and “that” when no comma is used (e.g., “the study that cost $10,000 was a success”).
* **Use of hyphens.** Yes to those that help clarity (e.g., “posterior-most”) and those that are regularly used/accepted in the literature. Generally, no hyphens after prefixes such as “sub”, “mid”, “semi”, “hemi”, etc. (e.g., “hemidesmosome” instead of “hemi-desmosome”), unless it helps with clarity (e.g., “multi-innervated”). No hyphens for composed location adjectives (e.g., “posteroanterior”), unless there are more than two compounds (e.g., “ventro-posterolateral”).
* **Abbreviations.** Avoid abbreviations, contractions, and symbols born out of laziness, such as `&`, `+`, or `vs` for “versus”. Avoid abbreviations unless they are self-explanatory, commonly understood, or they really do help to reduce the amount of typing enough to enhance readability. Use full chemical element names, not symbols (e.g., “hydrogen” instead of “H+”, “copper” instead of “Cu”, etc.). For biomolecules, spell out the term wherever practical (e.g., “fibroblast growth factor” instead of “FGF”). Abbreviations are acceptable in synonyms, in cases where the abbreviation _is_ the synonym.


## Cross-references to the literature
Assertions in textual definitions, evidence provided in comments, and synonyms should be as much as possible backed up by citing the appropriate literature.

Citations are made by cross-references, that is by adding `http://www.geneontology.org/formats/oboInOwl#hasDbXref` annotations to the definition, comment, and synonym annotations. Add one such annotation per reference, using the CURIE syntax with well-known prefixes:

* `PMID:1234567` for a PubMed identifier;
* `doi:xx.yyyy/...` for a DOI;
* `ISBN:...` for a ISBN.

If the main source for an assertion is a term in another ontology, the short identifier for that term may be used as a cross-reference. For example, `WBbt:0006799` to cross-reference a term in the _C. elegans_ Gross Anatomy Ontology.

ORCID identifiers may also be used when the only available source for an assertion is an individual researcher. This should be done sparingly.


## Formal definitions
The formal definition of a class is made up of all the logical axioms about the class (as opposed to the annotation assertion axioms). This includes classification assertions, relationship assertions, equivalence assertions, and disjointness assertions.

> Note: In OWL formalism, both classification and relationship assertions are represented using `SubClassOf` axioms. However, in this document, we make a strict distinction between a _classification_ (where a class is a subclass of a _named class_), and a _relationship_ (where a class is a subclass of an _anonymous class expression_).
>
> For example, in the formal definition of CL:0000392 (“crystal cell”):
>
> ```
> Class: 'crystal cell'
>   SubClassOf: 'hemocyte'
>   SubClassOf: 'develops from' some 'procrystal cell'
> ```
>
> The first `SubClassOf` axiom denotes an actual classification, whereas the second denotes a relationship.


### Asserting classification
In order to keep the ontology maintainable, asserted classifications should be limited where possible. Ideally, all terms would have only a single asserted parent (also known as “superclass”). Given the presence of suitable logically defined classes (see below) and sufficient relationships for the term you are making, additional classification can be inferred automatically by reasoning.

However, as we are limited in what types of classification we are able to infer, you may need to assert multiple parents. Two asserted classifications are plainly acceptable. If you must assert three or ore classifications, then you should make a note with a suggestion for which of the asserted classifications are good candidates for formalisation and inferred classification.


### Logically defined classes
Logically defined classes are terms that have formal definitions that specify complete necessary and sufficient conditions for membership of the class. They can be used by a reasoner to auto-classify the ontology by searching for terms that fulfill these conditions.

> Logically defined classes are variously referred to as “cross-products” (XPs), “genus and differentia definitions”, “equivalent classes”, or “intersections”. In OWL formalism, they are represented using `EquivalentClasses` axioms.

Generally, logical definitions follow the structure: “Any `X` that `REL` some `Y` [and `REL` some `Z`...]”, where `X` is the genus and each following clause (“that `REL` some `Y`”) is a differentium.

> Strictly speaking, logical definitions can be arbitrarily complex. It is recommended, however, to stick as much as possible to “simple” logical definitions following the structure above. More complex definitions are harder to understand, and may involve OWL constructs that are legal but not fully supported by the available reasoners.

Good candidates for logically defined classes include classes whose only differentium is:

* what the cell is part of;
* what it innervates (or, if more precisely known, what its axon(s) or dendrite(s) innervate);
* its function.

Care must be taken not to use logically defined classes too liberally. You should be satisfied that all automatic classifications that result would make sense (or at least be justifiable) to a biologist and would cover most cases of usages with as few edge cases as possible.

If you are unsure whether a characteristic of a cell should be expressed as a relationship or as a differentium in a logically defined class: use a relationship.

The textual definition of a logically defined class should be a plain English equivalent of the logical definition. However, in some cases it can be useful to add more details in the “gloss” part when relevant.


### Asserting relationships

Please refer to the [relations guide](relations_guide.md) for detailled guidelines about which relations to use for most cases.
