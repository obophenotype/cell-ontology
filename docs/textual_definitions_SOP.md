## Guide to writing textual definitions on CL

Links to relevant background material:

- Chris Mungall's [blog on post ontology definitions](https://douroucouli.wordpress.com/2019/07/08/ontotip-write-simple-concise-clear-operational-textual-definitions/)
- [OBO foundry reference paper](https://philpapers.org/archive/SEPGFW.pdf);
- DOS slides on the problem of defining cell types (TBA)

### Background

It is standard ontology engineering practise to aim for minimal, concise ontology term definitions.  However many cell types can be reliably identified by more than one set of properties: functional, structural, gene expression. This makes it hard to choose which properties to include if we are aiming for a minimal definition.  Users of the cell ontology also come from different disciplines/perspectives and have different types of information and levels of detail available when they annotate a term or browse a resource.  We need to be able to support users from multiple disciplines with a definition that allows them to visualise and identify the cell type being defined. In some cases (e.g. transcriptomically defined types or 't-types') identification of the cell type  require links to reference data.

Here are a couple of examples of minimal definitions that are correct but not useful to most users:

1. We could minimally define a corneal endothelial cell as 'Any endothelial cell that is part of the cornea'.  This may well be sufficient for an expert in the anatomy and biology of the cornea, but to most biologists, the term "endothelial cell" brings to mind a the principle cell types of lymphatic or blood vessels.  However, the corneal endothelium is a monolayer of flat cell on the underside of the cornea.    
2. Similarly, a perfectly accurate minimal definition of a type II pneuomocyte is an epithelial cell that has an 'alveolar lamellar body' (a unique structure only found in these cell types). But this is useless information to a user who knows nothing about this structure (many biologists) or who is annotating data that does not resolve this structure.

A second use of ontologies is to encode knowledge in the form of useful formal links between ontology terms.  For example, in CL we record function and cell components via links to gene ontology terms, location via links to CL and lineage via links to other CL terms. Not all of this information is particularly useful for recognising a cell type, but it is of use to our users and so we often record it in CL using formal relationships. This is relevant to ontology definitions because it is good practise for formal and textual definitions to match, and textual definitions are the place we encode supporting references.

We can't of course, include every known piece of information about a cell in a definition (e.g. all genes expressed). However extended information is useful to our users - especially where it includes potential marker sets and information relevant to human physiology and disease. To support this, we have an additioal extended description field which can contain information about additional marker sets, minor (secondary) functions and disease.  It can also contain information about properties that may not apply to all subclasses - this is especially useful for t-types in the brain where there is typically sparse knowledge of the extent of variation in morphology and function under each t-type.  In these cases, information should be included about where these proporites do apply.

![image](https://github.com/obophenotype/cell-ontology/assets/112839/eeb45ba5-96c7-4a3e-b68c-62530c043798)

### SOP

#### Defiition

Text in the definition field should be no longer than one short paragraph and should follow a classic genus, diffentia and gloss type structure:
   - _genus_: what type of cell is it (e.g. epithelial cell)
   - _differentia_: a list of properties that can be used to distinguish it from other similar cell types, especially those in the same tissue/organ context and those of the same genus.  _This should include location_ unless the term is so abstract that this is not possible. We should be liberal in listing properties here in order to support multiple communities who will have different types of data and understanding. Structural and functional properties are preferred over molecular markers unless cell types are named for these markers or they are generally accepted as definitional by the community. Care should be taken not to attach species-specific markers to species-general cell types. Please note that while CL supports recording multiple marker sets for cell types, ideally with provenance, evidence and confidence, this is supported is outside of the core definition text.
   - _gloss_: Additional information not required for identification, including but not limited to, all assertions recorded in formal local assertions not covered in the differentia. This can include information about developmental origins,  processes the cell is capable of (for example these may be secondary processes like a tendon cell's role stimulating an immune response when damaged) or roles that the cell may have.

### Extended description text.

This is an additional field in which text should be referenced following standard academic practice (minirefs in text, e.g. Avola et al, 2004). It can include:
 - Descriptions of marker gene sets.  These MUST include provenance, and ideally evidence (e.g. identified in scRNAseq or by in-situ hybridization) and confidence.
 - Information specific to only some species or subtypes (where the applicability is known this should be made clear).
 - Information about the role of the cell type more broadly in disease and physiology.
 - Species specific markers (?)

### Defining t-types:
 - Some cell types are defined with reference to transcriptomic data.  Definitions for these follow a different pattern. { details TBA }






