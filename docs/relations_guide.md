# A guide to what relations to use where in the Cell Ontology

## Recording location

We record anatomical location by linking to terms from Uberon.

For most purposes we record the anatomical location of cells using **'part of'**. 

e.g. epithelial cell SubClassOf **'part of'** *some* epithelium 

means that

 1. All epithelial cells are part of an epithelium.  We wouldn't say 'epithelial cell' part_of some 'kidney tubule epithelium', because not all of them are.
 1. All parts of an epithelial cell are part of an epithelium.
 1. Epithelial cells are part_of some epithelium at all times.  This last stricture can be hard to apply in the context of development.  Some judgment may be required, e.g. -   (TBA)

Related Equivalence patterns: [cellPartOfAnatomicalEntity](https://github.com/obophenotype/cell-ontology/blob/master/src/patterns/dosdp-patterns/cellPartOfAnatomicalEntity.yaml).  Use this as a guide for creating simple grouping classes for cells of type X in structures of type Y.

Some cells, most obviously neurons, only have some parts in the anatomical structure we want to relate them to. For example, anteriior horn motor neurons have a soma in the anterior (ventral) horn of the spine, but also project out of the spine to innervate muscles.  We have a general relation for this, **'overlap'** (has some part in), but often we want to say something more specific.  For example, neuron types are often referred to in part by the location of their soma. We have a dedicated relation for this: **'has soma location'**, allowing us to record:

'anterior horn motor neuron' SubClassOf **'has soma location'** *some* 'ventral horn of spinal cord'

We also have a dedicated set of relations for recording the location of synaptic terminals and projections of neurons.  See [Relations for neurons](#Relations_for_neurons) for details.

To record the location of a cell in an anatomical space (e.g. a sinus), use **'located in'**, for an example of this, see 'Kupffer cell'.

## Taxon constraints

Please see https://ontology-development-kit.readthedocs.io/en/latest/TaxonRestriction.html


## Recording function

We record cellular function by linking to GO biological process terms using the relation (objectProperty) **'capable of'** 

e.g. 'hilus cell of ovary' **'capable of'** *some* 'androgen secretion'

## Recording developmental lineage

We record developmental lineage relationships between cell types using **develops from**, or where we are sure there are not intermediates between the related cells, by using **'develops directly from'**

For example:

'leukocyte' **develops from** *some* 'hematopoietic stem cell'

## Relations for neurons

### Synaptic connectivity

To record neuron to neuron or motor neuron -> target cell connectivity use.  Use these relations sparingly where connectivity is key to definition, e.g. motor neuron types defined by the type of muscle cell they synapse to.

**synapsed to** - preferred direction to record, as it fits with 

**synapsed_by** - Useful in cases where all X synapsed by some Y but there reverse is not true

To record connection between a neuron and a region it innervates we have a number of relations, all sub properties of overlaps

![image](https://user-images.githubusercontent.com/112839/94337631-e0a83300-ffe3-11ea-8f13-ac8a484a5fb3.png)

Historically we have used **has(pre/post)synaptic terminal in** to record this. However, these relations are defined as being true when a single synapse is present in a region.  As these relations are also used with data, this turns out to be too sensitive to biological and experimental noise.  We therefore now prefer the more specific relations for defining classes - defined in terms of functionally significant synaptic inputs/output in a region.


## Recording cell markers

Only markers that are necessary to define a cell type should be recorded.

NOTE: The details of how and when we record cell markers are are in flux.  If in doubt, ask an editor.

The most commonly used relation for recording markers is **'has plasma membrane part'**.  This is used for recording cell surface markers, especially in immune cells.  We also have subproperties **has low plasma membrane amount** and **has low plasma membrane amount'**, used to the same end.  In each case, a term from the protein ontology or a protein complex term from GO is used as the object of the relation:

e.g.  alpha-beta T cell EquiavlentTo 'T cell' *and* **'has plasma membrane part'** *some* 'alpha-beta T cell receptor complex' 

Absence of a marker can be recorded using **lacks_plasma_membrane_part**.

## Recording qualities of cells:

Use **has characteristic**
 
### Recording cell shape or other morphological qualities

e.g. erythrocyte subClassOf **has characteristic** *some* biconcave

### Recording cellular qualities (eg. ploidy, nuclear number)

#### nuclear number

Use subproperty of PATO: nuclate auality 

![image](https://user-images.githubusercontent.com/112839/147105229-685b5cdf-8b09-4a36-b826-41ad405886b6.png)

e.g. 

'enucleate erythrocyte' EquivalentTo erythrocyte *and* **'has characteristic'** *some* anucleate

Note that 'anucleate cell' and 'multinucleate cell' are disjoint.








