## Guide to writing textual definitions on CL

Background links to add: obook; Chris Mungall blog on definitions (ttps://douroucouli.wordpress.com/2019/07/08/ontotip-write-simple-concise-clear-operational-textual-definitions/); OBO foundry reference paper; DOS slides on the problem of defining cell types

### Background

Cell types can be uniquely/reliably identified by more than one set of properties: functional, structural, gene expression. This makes it hard to choose which properties to include if we are aiming for a minimal definition.  Users of the cell ontology come from different disciplines/perspectives and have different types of information and levels of detail available when they come to annotate a term or browse a resource.  We need to be able to support users from multiple disciplines with a definition that allows them to visualise and identify the cell type being defined. For example we could minimally define a corneal endothelial cell as 'any endothelial cell that is part of the cornea, but this does not allow users to visualise or now how to identify instances of this cell type - which are flat cells in a monolayer on the internal surface of the cornea.  Similarly, a prefectly true minimal definition of a type II pneuomocyte is an epithelial cell that has an 'alveolar lamellar body' (a unique structure only found in these cell types). But this is useless information to many users and does not draw a clear picture of the cell type in the minds of most biologists.

### SOP

Text in the definition field should be no longer than one short paragraph and should follow a classic genus, diffentia and gloss type structure:
   - genus: what type of cell is it (e.g. epithlial cell)
   - differentia: a list of properties that can be used to distinguish it from other similar cell types, especially those in the same tissue/organ context.   We should be liberal in listing these in order to support multiple communities who will have different types of data and understanding. Prefer structural and functional properties over molecular markers unless cell types are named for these markers.
   - gloss: Information about developmental origins (if not already in the differentia).  Information about processes the cell is capable of (if not in the core differentia - for example these may be secondary processes like a tendon cell's role stimulating an immune response when damaged.

Extended description text should be referenced following standard academic practice (minirefs in text, e.g. Avola et al, 2004). It can include:
 - Information specific to only some species or subtypes (where the applicability is known this should be made clear).
 - Information about the role of the cell type more broadly in disease and physiology.
 - Species specific markers (?)

Defining t-types:
 - Some cell types are defined with reference to transcriptomic data.  Definitions for these follow a different pattern. { details TBA }





