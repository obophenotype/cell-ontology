# A guide to selecting **object properties** in the Cell Ontology (CL)


### Recording anatomical location (general cell types)

To record anatomical locations for cell types, axioms are written using object properties to relate CL terms to Uberon terms.

The most commonly used object property to record anatomical location is [**'part of'**](http://purl.obolibrary.org/obo/BFO_0000050). 

For example, ['epithelial cell'](http://purl.obolibrary.org/obo/CL_0000066) has the following subclass:

[**'part of'**](http://purl.obolibrary.org/obo/BFO_0000050) *some* [epithelium](http://purl.obolibrary.org/obo/UBERON_0000483) 

In Manchester OWL syntax, this is represented as:

SubClassOf(obo:CL_0000066 ObjectSomeValuesFrom(obo:BFO_0000050 obo:UBERON_0000483))


This statement connotes the following:

 1. All epithelial cells are part of an epithelium.
 1. All parts of an epithelial cell are part of an epithelium.
 1. Epithelial cells are part of some epithelium at all times. This can be hard to apply in the context of development and may require additional consideration from an editor.

 In contrast, asserting that an ['epithelial cell'](http://purl.obolibrary.org/obo/CL_0000066) is ['part of'](http://purl.obolibrary.org/obo/BFO_0000050) *some* ['kidney epithelium'](http://purl.obolibrary.org/obo/UBERON_0004819) is not correct because there are epithelial cells that exist that are not located in kidney epithelium.


### Recording anatomical location (neurons)

Due to the morphology of some neurons (i.e., neurons with neurites that extend across various anatomical structures), these cell types require additional consideration to record location. For example, an [anterior horn motor neuron](http://purl.obolibrary.org/obo/CL_2000048) has a soma located in the [anterior (ventral) horn of the spinal cord](http://purl.obolibrary.org/obo/UBERON_0002257), but also projects an axon out of the spine to innervate muscles. There is a general relation for this, [**overlaps**](http://purl.obolibrary.org/obo/RO_0002131) (has some part in), but a more specific relation exists for neurons. Since neuron types are often referred to in part by soma location, there is a dedicated relation for this: [**'has soma location'**](http://purl.obolibrary.org/obo/RO_0002100).


For example, [anterior horn motor neuron](http://purl.obolibrary.org/obo/CL_2000048) has the following subclass:

[**'has soma location'**](http://purl.obolibrary.org/obo/RO_0002100) *some* ['ventral horn of spinal cord'](http://purl.obolibrary.org/obo/UBERON_0002257)

In Manchester OWL syntax, this is represented as:

SubClassOf(obo:CL_2000048 ObjectSomeValuesFrom(obo:RO_0002100 obo:UBERON_0002257))

There is also a dedicated set of relations for recording the location of synaptic terminals and projections of neurons.  See Recording synaptic connectivity below.

### Recording anatomical location (cells in immaterial spaces)

To record the location of a cell in an anatomical space (e.g., a sinus), [**'located in'**](http://purl.obolibrary.org/obo/RO_0001025) is used. For example, [lymph node marginal reticular cell](http://purl.obolibrary.org/obo/CL_0009103) has the following subclass:


[**'located in'**](http://purl.obolibrary.org/obo/RO_0001025) *some* ['subcapsular sinus of lymph node'](http://purl.obolibrary.org/obo/UBERON_0005463)


### Recording function

Cellular function is recorded by linking GO biological process terms with the object property [**'capable of'**](http://purl.obolibrary.org/obo/RO_0002215). 

For example, ['hilus cell of ovary'](http://purl.obolibrary.org/obo/CL_0002095) has the following subclass:

[**'capable of'**](http://purl.obolibrary.org/obo/RO_0002215) *some* ['androgen secretion'](http://purl.obolibrary.org/obo/GO_0035935)


### Recording developmental lineage

Developmental lineage is recorded between cell types with the object property [**develops from**](http://purl.obolibrary.org/obo/RO_0002202), or in the case where there are no intermediates between the cells, [**'directly develops from'**](http://purl.obolibrary.org/obo/RO_0002207).

For example, ['leukocyte'](http://purl.obolibrary.org/obo/CL_0000738) has the following subclass:

[**develops from**](http://purl.obolibrary.org/obo/RO_0002202) *some* ['hematopoietic stem cell'](http://purl.obolibrary.org/obo/CL_0000037)


### Recording cell markers

Only markers that are necessary to define a cell type should be recorded.

The most commonly used relation for recording markers is [**'has plasma membrane part'**](http://purl.obolibrary.org/obo/RO_0002104). This object property is used to record cell surface markers, especially in immune cells.  There are also more specific properties, [**'has low plasma membrane amount'**](http://purl.obolibrary.org/obo/RO_0015016) and [**'has high plasma membrane amount'**](http://purl.obolibrary.org/obo/RO_0015015), that can be used at an editor's discretion. In each case, a term from the [PRotein Ontology (PRO)](https://github.com/PROconsortium/PRoteinOntology) or a protein complex term from the [Gene Ontology (GO)](https://github.com/geneontology/go-ontology) is used as the object of the relation.

For example, ['alpha-beta T cell'](http://purl.obolibrary.org/obo/CL_0000789) has the following equivalence axiom:

['T cell'](http://purl.obolibrary.org/obo/CL_0000084) *and* [**'has plasma membrane part'**](http://purl.obolibrary.org/obo/RO_0002104) *some* ['alpha-beta T cell receptor complex'](http://purl.obolibrary.org/obo/GO_0042105) 

Absence of a marker can be recorded using [**lacks_plasma_membrane_part**](https://ontobee.org/ontology/CL?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fcl%23lacks_plasma_membrane_part).

 
### Recording general cellular qualities (e.g., morphology)

To record qualities of cells when a more specific object property does not exist, [**'has characteristic'**](http://purl.obolibrary.org/obo/RO_0000053) may be used.

For example, [erythrocyte](http://purl.obolibrary.org/obo/CL_0000765) has the following subclass to describe the morphology of this cell type:

[**'has characteristic'**](http://purl.obolibrary.org/obo/RO_0000053) *some* [biconcave](http://purl.obolibrary.org/obo/PATO_0002039)


### Recording nuclear number

To record the number of nuclei in a cell, one may use a subclass from the PATO term ['nucleate quality'](http://purl.obolibrary.org/obo/PATO_0001404) with the ['has characteristic'](http://purl.obolibrary.org/obo/RO_0000053) relation.

![image](https://user-images.githubusercontent.com/112839/147105229-685b5cdf-8b09-4a36-b826-41ad405886b6.png)

For example, [platelet](http://purl.obolibrary.org/obo/CL_0000233) has the following equivalence axiom:

['myeloid cell'](http://purl.obolibrary.org/obo/CL_0000763) *and* (['has characteristic'](http://purl.obolibrary.org/obo/RO_0000053) *some* [**anucleate**](http://purl.obolibrary.org/obo/PATO_0001405)) *and* (['has characteristic'](http://purl.obolibrary.org/obo/RO_0000053) *some* [discoid](http://purl.obolibrary.org/obo/PATO_0001874)) *and* (['capable of'](http://purl.obolibrary.org/obo/RO_0002215) *some* ['blood coagulation'](http://purl.obolibrary.org/obo/GO_0007596)) *and* (['capable of'](http://purl.obolibrary.org/obo/RO_0002215) *some* ['blood circulation'](http://purl.obolibrary.org/obo/GO_0008015))


### Recording synaptic connectivity (neurons)

To record neuron-to-neuron or motor neuron-to-target cell connectivity, consider the following object properties. These properties should be used when connectivity is key to the definition, for example, in cases where a motor neuron type is defined by the type of muscle cell on which it synapses.

[**synapsed to**](http://purl.obolibrary.org/obo/RO_0002120)

For example,
['alpha motor neuron'](http://purl.obolibrary.org/obo/CL_0008038) SubClassOf [**synapsed to**](http://purl.obolibrary.org/obo/RO_0002120) *some* ['extrafusal muscle fiber'](http://purl.obolibrary.org/obo/CL_0008046)

[**synapsed by**](http://purl.obolibrary.org/obo/RO_0002103), which is the inverse of [**synapsed to**](http://purl.obolibrary.org/obo/RO_0002120)

For example,
['extrafusal muscle fiber'](http://purl.obolibrary.org/obo/CL_0008046) SubClassOf [**synapsed by**](http://purl.obolibrary.org/obo/RO_0002103) *some* ['alpha motor neuron'](http://purl.obolibrary.org/obo/CL_0008038)


Of note, historically ['has presynaptic terminal in'](http://purl.obolibrary.org/obo/RO_0002113) and ['has postsynaptic terminal in'](http://purl.obolibrary.org/obo/RO_0002110) have been used to record synaptic connectivity. However, these relations are defined as being true when a single synapse is present in a region. In some use cases, these relations may be too sensitive to biological and/or experimental noise. 'synapsed to / by' are now preferred as the more specific relations to record functionally significant synaptic inputs and outputs.


### Taxon constraints

See https://oboacademy.github.io/obook/explanation/taxon-constraints-explainer/.

