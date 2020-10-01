# A guide to what relations to use where in the Cell Ontology

## Recording location

We record anatomical location by linking to terms from Uberon.

For most purposes we record the anatomical location of cells using **'part of'**. 

e.g. eipthelial cell SubClassOf **'part of'** *some* eipthelium 

means that

 1. All epithelial cells are part of an epithelium.  We wouldn't say 'epithelial cell' part_of some 'kidney tubule epithelium', because not all of them are.
 1. All parts of an epithelial cell are part of an epithelium.
 1. Epithelial cells are part_of some epithelium at all times.  This last stricture can be hard to apply in the context of development.  Some judgment may be required, e.g. -   (TBA)

Some cells, most obviously neurons, only have some parts in the anatomical structure we want to relate them to. For example, anteriior horn motor neurons have a soma in the anterior (ventral) horn of the spine, but also project out of the spine to innervate muscles.  We have a general relation for this, **'overlap'** (has some part in), but often we want to say something more specific.  For example, neuon types are often referred to in part by the location of their soma. We have a dedicated relation for this: **'has soma location'**, allowing us to record:

'anterior horn motor neuron' SubClassOf **'has soma location'** *some* 'ventral horn of spinal cord'

We also have a dedicated set of relations for recording the location of synaptic terminals and projections of neurons.  See [Relations for neurons](#Relations_for_neurons) for details.

### Taxon constraints

We can record taxon specificity of terms using

**'in taxon'** *some* <NCBI_taxon term>

For example, the term 'alpha motor neuron' refers to a type of motor neuron that innervates skeletal muscle in vertebrates, so we can record

'alpha motor neuron' subClassOf **'in taxon'** *some* 'Vertebrata <Metazoa>'

Other relation are available for recording taxon constraints (details TBA)
Further reading: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3098089/


### Recording function

We record cellular function by linking to GO biological process terms using the relation (objectProperty) **'capable of'** 

e.g. 'hilus cell of ovary' **'capable of'** *some* 'androgen secretion'

### Recording developmental lineage

We record developmental lineage relationships between cell types using **develops from**, or where we are sure there are not intermediates between the related cells, by using **'develops directly from'**

For example:

'leukocyte' **develops from** *some* 'hematopoietuc stem cell'

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
 
### Recording cell shape or other morphological qualities

e.g. erythrocyte bearer_of some biconcave

### Recording cellular qualities (eg. ploidy, nuclear number)

e.g. 'enucleate erythrocyte' EquivalentTo erythrocyte and ('bearer of' some anucleate)



