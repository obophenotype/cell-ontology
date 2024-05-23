## Guide to writing textual definitions on CL

### Relevant background material

- Chris Mungall's [blog post on ontology term definitions](https://douroucouli.wordpress.com/2019/07/08/ontotip-write-simple-concise-clear-operational-textual-definitions/)
- [OBO foundry reference paper](https://philpapers.org/archive/SEPGFW.pdf)

### Background

It is standard ontology engineering practise to aim for minimal, concise ontology term definitions.  However many cell types can be reliably identified by more than one set of properties: functional, structural, gene expression. This makes it hard to choose which properties to include if we are aiming for a minimal definition.  Users of the cell ontology also come from different disciplines/perspectives and have different types of information and levels of detail available when they annotate a term or browse a resource.  We need to be able to support users from multiple disciplines with a definition that allows them to visualise and identify the cell type being defined. In some cases (e.g. transcriptomically defined types or 't-types') identification of the cell type requires links to reference data.

Here are a couple of examples of minimal definitions that are correct but not useful to most users:

1. We could minimally define a corneal endothelial cell as 'Any endothelial cell that is part of the cornea'.  This may well be sufficient for an expert in the anatomy and biology of the cornea, but to most biologists, the term "endothelial cell" brings to mind the principal cell types of lymphatic or blood vessels.  However, "corneal endothelium" refers to a monolayer of flat cells on the underside of the cornea.    
2. Similarly, a perfectly accurate minimal definition of a type II pneuomocyte is an epithelial cell that has an 'alveolar lamellar body' (a unique structure only found in these cell types). But this is useless information to a user who knows nothing about this structure (many biologists) or who is annotating data that does not resolve this structure.

A second use of ontologies is to encode knowledge in the form of useful formal links between ontology terms.  For example, in CL we record function and cell components via links to gene ontology terms, location via links to CL and lineage via links to other CL terms. Not all of this information is particularly useful for recognising a cell type, but it is of use to our users and so we often record it in CL using formal relationships. This is relevant to ontology definitions because it is good practise for formal and textual definitions to match, and textual definitions are the place we encode supporting references.

We can't of course, include every known piece of information about a cell in a definition (e.g. all genes expressed). However extended information is useful to our users - especially where it includes potential marker sets and information relevant to human physiology and disease. To support this, we have an additioal extended description field which can contain information about additional marker sets, minor (secondary) functions and disease.  It can also contain information about properties that may not apply to all subclasses - this is especially useful for t-types in the brain where there is typically sparse knowledge of the extent of variation in morphology and function under each t-type.  In these cases, information should be included about where these proporites do apply.

### SOP

#### Definition

Text in the definition field should be no longer than one short paragraph and should follow a classic genus, differentia and gloss type structure:
   - _genus_: what type of cell is it (e.g. epithelial cell)
   - _differentia_: a list of properties that can be used to distinguish it from other similar cell types, especially those in the same tissue/organ context and those of the same genus. _This SHOULD include location_ unless the term is so abstract that this is not possible. We should be liberal in listing properties here in order to support multiple communities who will have different types of data and understanding. Structural and functional properties are preferred over molecular markers unless cell types are named for these markers or they are generally accepted as definitional by the community. Care should be taken not to attach species-specific markers to species-general cell types. Please note that while CL supports recording multiple marker sets for cell types, ideally with provenance, evidence and confidence, this is supported is outside of the core definition text.
   - _gloss_: Additional information not required for identification, including but not limited to, all assertions recorded in formal local assertions not covered in the differentia. This can include information about developmental origins, processes the cell is capable of (for example these may be secondary processes like a tendon cell's role stimulating an immune response when damaged) or roles that the cell may have.

### Extended description text.

This is optional descriptive information in the rdfs:comment value (although we may switch to a dedicated annotation property in future).  The text should be referenced following standard academic practice (minirefs in text, e.g. Avola _et al_., 2024). It can include:
 - Descriptions of marker genes and marker gene sets.  These MUST include species and provenance, and ideally evidence (e.g. identified by use of the NS-Forest algorithm on dataset x; identified by in-situ hybridization) and confidence.
 - Information specific to only some species or subtypes (where the applicability is known this should be made clear).
 - Information about the role of the cell type more broadly in disease and physiology.

The comment section may also be used to record evidence and and name/synonym disambiguation.

### Defining transcriptomic types (t-types):

Some cell types are defined with reference to transcriptomic data.  This is especially common in brain datasets.  In these cases, naming is often based on semi-automated transfer of names that are based on some specific set of properties.  We do not always know how widely those properties apply so need to be careful in choosing them for differentia.  Extended multi-modal descriptions may be available, for example based on patch-seq data, but this is typically derived from very sparse data, so such information belongs in the extended definition, along with details of the brain regions where these properties have been assayed.

Definitions for these follow a different pattern:
 - First sentence: "A transcriptomically distinct { genus } with { description of primary differentia here }.  Second sentence may include more differentia.  
 - Gloss: see above
 - Last sentence:  The standard transcriptomic reference data for this cell type can be found on the { site } under { human readable details of how to access dataset }, { human readable details of annotation key/value pair that marks the reference cell set.

_Example_:

label: 
A transcriptomically distinct intratelencephalic-projecting glutamatergic neuron with a soma found between cortical layer 2-4. The standard transcriptomic reference data for this cell type can be found on the CellxGene census under the collection: "Transcriptomic cytoarchitecture reveals principles of human neocortex organization", dataset: "Supercluster: IT-projecting excitatory neurons", Author Categories: "CrossArea_subclass", value: L2/3 IT.

Comment: In the barrel cortex (of rodents), these neurons have thin-tufted apical dendrites, extend their axonal projections into L5 in the neocortex and have a hyperpolarised resting membrane potential (Harris & Shepherd 2016). Historically, these neurons were identified in cortical layer 2/3. MERFISH data shows that this intratelencephalic-projecting glutametergic neuron can have its soma in layer 2/3, 4B, 4C (Jorstad et al., 2023). The position of the soma in layer 4b and 4C is less frequent for this neuronal type in comparison to cortical layer 2/3.

Note: the reference dataset should MUST also be referenced directly via an xref.

_Axiomatisation of t-types:

Axiomatisation of t-types is tricky for a number of reasons:
1. Transcriptomic hierarchy does not necessarily follow property based hierarchy, for example we might define SST cortical interneurons as any cortical interneuron expressing SST.  However, in transcriptomic hierarchies, one SST expressing type (SST CHODL) is only distantly related to the other SST cells and so is treated as a disjoint type (e.g. see Jorstad et al., 2023).
2. We have limited knowledge about how widely particular properties of t-types apply.

In the former case, it is sufficient to express the property with a subClassOf axiom (avoiding use of equivalent class axioms). In the latter, mention of the property should be confined to the extended description, or in some cases we may use annotation properties. For example, in linking a single transcriptomic cell type to multiple brain regions or layers, an annotation property must be used. 

Given the limited knowledge we have about how  and whether they are unique to a particular cell type, care needs to be taken in adding formal axioms recording them.  Where there is a possibility that it is important to limit clauses in EquivalentClass expressions.

We have a standard pattern that can be used to convert transcriptomic heirarchies into SubClassOf hierarchies - using equivalence axioms with a 'has_examplar' clause with value cell set (see Tan et al., 2023 for details).  However care should be taken in using this given the potential for inheritance of properties that don't apply to all subclusters in a transcriptomic hierarchy.  A formal link to a defining cell set can be represented using subClassOf in order to avoid this.

