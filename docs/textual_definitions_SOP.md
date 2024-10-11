# Guide to writing textual definitions on CL

## Relevant background material

- Chris Mungall's [blog post on ontology term definitions](https://douroucouli.wordpress.com/2019/07/08/ontotip-write-simple-concise-clear-operational-textual-definitions/)
- [OBO foundry reference paper](https://philpapers.org/archive/SEPGFW.pdf)

### **Background**  
It is standard ontology engineering practice to aim for minimal, concise ontology term definitions. However, many cell types can be reliably identified by more than one set of properties: functional, structural, gene expression. This makes it hard to choose which properties to include if we are aiming for a minimal definition. Users of the cell ontology also come from different disciplines/perspectives and have different types of information and levels of detail available when they annotate a term or browse a resource. We need to support users from multiple disciplines with a clear, unambiguous, and human-readable definition that allows them to visualize and identify the cell type being defined. In some cases (e.g., transcriptomically defined types or 't-types'), identification of the cell type requires links to reference data.

Here are a couple of examples of minimal definitions that are correct but not useful to most users:

We could minimally define a corneal endothelial cell as 'Any endothelial cell that is part of the cornea'. This may well be sufficient for an expert in the anatomy and biology of the cornea, but to most biologists, the term ""endothelial cell"" brings to mind the principal cell types of lymphatic or blood vessels. However, ""corneal endothelium"" refers to a monolayer of flat cells on the underside of the cornea.  
Similarly, a perfectly accurate minimal definition of a type II pneumocyte is an epithelial cell that has an 'alveolar lamellar body' (a unique structure only found in these cell types). But this is useless information to a user who knows nothing about this structure (many biologists) or who is annotating data that does not resolve this structure.

A second use of ontologies is to encode knowledge in the form of useful formal links between ontology terms. For example, in CL, we record function and cell components via links to gene ontology terms, location via links to CL, and lineage via links to other CL terms. Not all of this information is particularly useful for recognizing a cell type, but it is of use to our users and so we often record it in CL using formal relationships. This is relevant to ontology definitions because it is good practice for formal and textual definitions to match, and textual definitions are the place we encode supporting references. It’s essential that textual definitions capture the assertions made in the formal relationships as closely as possible without becoming stilted and difficult to read.

We can't, of course, include every known piece of information about a cell in a definition (e.g., all genes expressed). However, extended information is useful to our users—especially where it includes potential marker sets and information relevant to human physiology and disease. To support this, we have an additional extended description field that can contain information about additional marker sets, minor (secondary) functions, and disease. It can also contain information about properties that may not apply to all subclasses—this is especially useful for t-types in the brain where there is typically sparse knowledge of the extent of variation in morphology and function under each t-type. In these cases, information should be included about where these properties do apply.

### **SOP**

#### **Definition**  
Text in the definition field should be no longer than one short paragraph. The text should be referenced following standard academic practice, i.e. use in-line citations, e.g., Avola et al., 2024).  It should follow a classic genus, differentia, and gloss type structure:

- **Genus**: What type of cell is it (e.g., epithelial cell)?
- **Differentia**: A list of properties that can be used to distinguish it from other similar cell types, especially those in the same tissue/organ context and those of the same genus. This SHOULD include location unless the term is so abstract that this is not possible. We should be liberal in listing properties here in order to support multiple communities who will have different types of data and understanding. Structural and functional properties are preferred over molecular markers unless cell types are named for these markers or they are generally accepted as definitional by the community. Care should be taken not to attach species-specific markers to species-general cell types. Please note that while CL supports recording multiple marker sets for cell types, ideally with provenance, evidence, and confidence, this is supported outside of the core definition text.
- **Gloss**: Additional information not required for identification, covering all assertions recorded in formal logical assertions not covered in the differentia. This can include information about developmental origins, processes the cell is capable of (for example, these may be secondary processes like a tendon cell's role in stimulating an immune response when damaged), or roles that the cell has.

**Guidelines on Content Inclusion**:
-**Do not include the name of the cell type being defined at the start of the definition.**  Instead, the genus cell type should be named here.
- **Ensure consistency with the definition of superclass(es)**: Make sure your definition is consistent with the definition of the superclass(es).
- **Include information from formal relationships**: Ensure that your definition includes the information recorded in all the direct formal relationships to the class. This helps maintain alignment between the textual and formal definitions.
- **Avoid unrelated assertions**: Avoid assertions about structures or cell types that are not part of the cell type being described, except when they pertain to some direct relationships with the cell type being described.
- **Limit information specific to subtypes**: Avoid including details that could better be included in the definition of subtypes of the cell type being described.
- **Gene expression**: Avoid using gene expression as the *differentium* unless the cell type is named for these markers or they are generally accepted as definitional by the community.
- **Limit repetition**: Avoid extensive repetition of assertions made in superclass definitions, unless these assertions are used to provide direct evidence for class membership.
- **Non-control conditions**: Do not add information about what happens in mutant or pathological states, backgrounds, or other kinds of non-control conditions.
- **Do not raise questions in definitions**: The definition should have the sense of being definitive. Any doubt should be recorded in comments instead.

#### **Extended Description Text**  

Extended descriptions provide a broader context for cell types that can include information that doesn’t apply to all subtypes or species. They may duplicate information in the definition. This information is recorded in a dcterms:description field and must be referenced.

Sources:
We have an increasing number of standardised extended descriptions from CellGuide, in the form of curated chatGPT output from a standard prompt, with citations.  These are directly loaded into CL following review using a semi-automated pipeline.
A local pipeline using Perplexity generates these extended descriptions for new cell types along with references. These need to be checked for accuracy against references.
Text can be extended with additional information on species specific marker sets - this must be referenced.


#### **Comment text**

The comment section should be used to record name/synonym disambiguation - i.e. text that documents and clarifies conflicting or confusing terminology related to the name and/or synonyms.  It may also include evidence for assertions made in the definition and any doubts/controversy about the definition or relationship to other cell types (e.g. where there is a suspicion that the term refers to the same cell type as another term, but there is not yet sufficient evidence/agreement to merge.

### **Defining Transcriptomic Types (t-types)**:  
Some cell types are defined with reference to transcriptomic data. This is especially common in brain datasets. In these cases, naming is often based on semi-automated transfer of names that are based on some specific set of properties. We do not always know how widely those properties apply, so we need to be careful in choosing them for differentia. Extended multi-modal descriptions may be available, for example, based on patch-seq data, but this is typically derived from very sparse data, so such information belongs in the extended definition, along with details of the brain regions where these properties have been assayed.

Definitions for these follow a different pattern:

- **First sentence**: A transcriptomically distinct {genus} with {description of primary differentia here}.
- **Second sentence**: May include more differentia.
- **Gloss**: See above.
- **Last sentence**: The standard transcriptomic reference data for this cell type can be found on the {site} under {human-readable details of how to access dataset}, {human-readable details of annotation key/value pair that marks the reference cell set}.

**Example**:  
Label: A transcriptomically distinct intratelencephalic-projecting glutamatergic neuron with a soma found between cortical layer 2-4. The standard transcriptomic reference data for this cell type can be found on the CellxGene census under the collection: ""Transcriptomic cytoarchitecture reveals principles of human neocortex organization"", dataset: ""Supercluster: IT-projecting excitatory neurons"", Author Categories: ""CrossArea_subclass"", value: L2/3 IT.

**Comment**: In the barrel cortex (of rodents), these neurons have thin-tufted apical dendrites, extend their axonal projections into L5 in the neocortex, and have a hyperpolarized resting membrane potential (Harris & Shepherd, 2016). Historically, these neurons were identified in cortical layer 2/3. MERFISH data shows that this intratelencephalic-projecting glutamatergic neuron can have its soma in layer 2/3, 4B, 4C (Jorstad et al., 2023). The position of the soma in layer 4B and 4C is less frequent for this neuronal type in comparison to cortical layer 2/3.

**Note**: The reference dataset must also be referenced directly via an xref.

**Axiomatisation of t-types**:

Axiomatisation of t-types is tricky for several reasons:

- Transcriptomic hierarchy does not necessarily follow property-based hierarchy. For example, we might define SST cortical interneurons as any cortical interneuron expressing SST. However, in transcriptomic hierarchies, one SST-expressing type (SST CHODL) is only distantly related to the other SST cells and so is treated as a disjoint type (e.g., see Jorstad et al., 2023).
- We have limited knowledge about how widely particular properties of t-types apply.
                                                                                                                                                                                                                                                                                                                                                     In the former case, it is sufficient to express the property with a subClassOf axiom (avoiding use of equivalent class axioms). In the latter, mention of the property should be confined to the extended description, or in some cases we may use annotation properties. For example, in linking a single transcriptomic cell type to multiple brain regions or layers, an annotation property must be used.

Given the limited knowledge we have about how and whether they are unique to a particular cell type, care needs to be taken in adding formal axioms recording them. Where there is a possibility that it is important to limit clauses in EquivalentClass expressions.

We have a standard pattern that can be used to convert transcriptomic heirarchies into SubClassOf hierarchies - using equivalence axioms with a 'has_examplar' clause with value cell set (see Tan et al., 2023 for details). However care should be taken in using this given the potential for inheritance of properties that don't apply to all subclusters in a transcriptomic hierarchy. A formal link to a defining cell set can be represented using subClassOf in order to avoid this.

## References

- Harris, Kenneth D., and Gordon M. G. Shepherd. 2015. “The Neocortical Circuit: Themes and Variations.” Nature Neuroscience 18 (2): 170–81. https://doi.org/10.1038/nn.3917.
- Jorstad, Nikolas L., Jennie Close, Nelson Johansen, Anna Marie Yanny, Eliza R. Barkan, Kyle J. Travaglini, Darren Bertagnolli, et al. 2023. “Transcriptomic Cytoarchitecture Reveals Principles of Human Neocortex Organization.” Science 382 (6667): eadf6812. https://doi.org/10.1126/science.adf6812.
- Tan, Shawn Zheng Kai, Huseyin Kir, Brian D. Aevermann, Tom Gillespie, Nomi Harris, Michael J. Hawrylycz, Nikolas L. Jorstad, et al. 2023. “Brain Data Standards - A Method for Building Data-Driven Cell-Type Ontologies.” Scientific Data 10 (1): 50. https://doi.org/10.1038/s41597-022-01886-2.
