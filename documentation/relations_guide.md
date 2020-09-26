## A guide to what relations to use where in the Cell Ontology

The cell ontology is not a database for recording all properties of cell types.  We can't record all genes expressed in a cell type, or all synaptic connectoins. Some judgement is therefore necessary when adding relationship in the cell ontology - are they necessary to define a cell type?

Relations have their own heirarchy, with more general relations at the top and more specific ones underneath.  If you use a specific relation, then the 

### Recording location

We record anatomical location by linking to terms from Uberon.

For most purposes we record the anatomical location of cells using **'part of'**. 

e.g. eipthelial cell 'part of' some eipthelium 

means that
(a) All epithelial cells are part of an epithelium.  We wouldn't say 'epithelial cell' part_of some 'kidney tubule epithelium', because not all of them are.
(b) All parts of an epithelial cell are part of an epithelium.
(c) Epithelial cells are part_of some epithelium at all times.  This last stricture can be hard to apply in the context of development.  Some judgment may be required, e.g. -   (TBA)

Some cells, most obviously neurons, often do not have all parts in an anatomical structure we want to relate them to. We have a general relation for this: **'overlap'**, but often we want to say something more specific.  For example, neuon types are often referred to in part by the location of their soma, for example anterior horn cells have a soma in the anterior (ventral) horn of the spine.  We have a dedicated relation for this: 'has soma location'.

We also have a dedicated set of relations for recording the location of synaptic terminals and projections of neurons.  See [Relations for neurons](#Relations_for_neurons) for details.

### Taxon constraints

in_taxon some <NCBI_taxon term>
only_in_taxon some <NCBI_taxon term>

e.g. 
TBA

The following should be recorded using an annotation_property axiom:

never_in_taxon 

e.g. 

TBA

Further reading: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3098089/

Inference of taxon constraints from other ontologies:

Relationships to taxon constrained terms from other ontologies can result in inferred taxon constraints.

Examples: 
 - Inference of Taxon constraints from taxon constrainted makers: 
 - Inference of Taxon constraints from taxon constrainted anatomy: 

### Recording function

We record cellular function by linking to GO biological process terms using the relation (objectProperty) **'capable of'** 

e.g. 'capable of' some 'androgen secretion'

### Recording developmental lineage

We record developmental lineage relationships between cell types using **develops from**, or where we are sure there are not intermediates between the related cells, by using **'develops directly from'**

### Relations for neurons

#### Synaptic connectivity

To record neuron to neuron or motor neuron -> target cell connectivity use.  Use these relations sparingly where connectivity is key to definition, e.g. motor neuron types defined by the type of muscle cell they synapse to.

**synapsed to** - preferred direction to record, as it fits with 

**synapsed_by** - Useful in cases where all X synapsed by some Y but there reverse is not true

To record connection between a neuron and a region it innervates we have a number of relations, all sub properties of overlaps

![image](https://user-images.githubusercontent.com/112839/94337631-e0a83300-ffe3-11ea-8f13-ac8a484a5fb3.png)

Historically we have used *has synaptic terminal in*


### Recording cell markers

has part
  . has plasma membrane part
  
expresses
  . has plasma membrane part
 
 Absence of a marker 
 lacks_plasma_membrane_part
 
#### A note on cell markers and taxon constraints

If you choose a cell specific marker 

#### A note on when to record cell markers
 
# Recording cell shape or other morphological qualities

e.g. erythrocyte bearer_of some biconcave

# Recording cellular qualities (eg. ploidy, nuclear number)

e.g. 'enucleate erythrocyte' EquivalentTo erythrocyte and ('bearer of' some anucleate)



