# Cell Ontology (CL) relations guide.

## Related documents: 
* [<u>Defining cell types - from free text to formal definitions.</u>](http://fu.bar)

## Intro 
The aim of this document is to provide an accessible guide to how to use relations to record the properties that define cell types including location, lineage, function, morphology and marker genes. The term 'relations' here refers principally to OWL object properties, but also includes annoation properties used as shortcuts for more expressive logical axioms that can be programatically generated from them.

Relations in this guide are grouped by general use case (e.g. recording location) and each is illustrated by an example e.g.-

-   melanocyte subClassOf ‘has part’ some melanosome.

This should be read as ‘**all** melanocytes have some type of melanosome as a part’ as should all axioms of this form. The examples should all be correct, but may not reflect the full complexity of axioms in the ontology. Where no example is currently present in CL, examples are taken from the Drosophila Anatomy Ontology, which follows the same schema.

## Recording location

Location of cell types is recorded by relating a cell type to a term in an anatomical ontology. For the Cell Ontology this means a term from Uberon. 

###  [**'part of'**](http://purl.obolibrary.org/obo/BFO_0000050) 

Use part\_of for cases where the location is a material anatomical structure (rather than a space, such as a sinus) and all of the cell is within the anatomical structure.

‘[epithelial cell'](http://purl.obolibrary.org/obo/CL_0000066)
subClassOf [**'part of'**](http://purl.obolibrary.org/obo/BFO_0000050)
*some* [epithelium](http://purl.obolibrary.org/obo/UBERON_0000483)

‘part of’ is transitive, which means that it applies across chains of relationships. For example,

‘ileal goblet cell’ part\_of some ileum

ilium ‘part of’ some ‘small intestine’

‘small intestine’ ‘part of’ some intestine’

=>

’ileal goblet cell’ ‘part of’ some ‘small intestine’
&
‘ileal goblet cell’ ‘part of’ some intestine

### located\_in

To record the location of a cell in an anatomical space (e.g., a sinus),
[**'located in'**](http://purl.obolibrary.org/obo/RO_0001025) is used.

For example:

‘[lymph node marginal reticular cell](http://purl.obolibrary.org/obo/CL_0009103)’ subClassOf [**'located in'**](http://purl.obolibrary.org/obo/RO_0001025) *some* ['subcapsular sinus of lymph node'](http://purl.obolibrary.org/obo/UBERON_0005463)

### overlaps

[**'part of'**](http://purl.obolibrary.org/obo/BFO_0000050) applies in cases where an entire cell is within an anatomical structure, but some cells have parts in multiple anatomical structures. For example, many neurons span multiple regions of the central nervous system. The general relation for this is [**overlaps**](http://purl.obolibrary.org/obo/RO_0002131) (has some part in).

[**overlaps**](http://purl.obolibrary.org/obo/RO_0002131) is not currently used directly in the cell ontology (time of writing 05/2023), but more specific relationships exist for recording the location of neurons and their parts. These are described in the next section.

### Recording the location of neurons 

### [<u>has soma location</u>](http://purl.obolibrary.org/obo/RO_0002100)

When neurobiologists talk about the location of vertebrate neurons, they are typically referring to soma location. The importance of soma location to identify is underscored by how commonly cell types are named, in part, by soma location. We therefore have a dedicated relation for recording this: [**'has soma location'**](http://purl.obolibrary.org/obo/RO_0002100).

For example, [anterior horn motor neuron](http://purl.obolibrary.org/obo/CL_2000048) has the following subclass axiom:

[**'has soma location'**](http://purl.obolibrary.org/obo/RO_0002100) *some* ['ventral horn of spinal cord'](http://purl.obolibrary.org/obo/UBERON_0002257)

**axiomatization of ‘has soma location’**

-   *subPropertyOf*: overlaps \# if X has\_soma\_location some Y, then X overlaps some Y)

-   *domain*: neuron \# X has\_soma\_location some Y => X is inferred to be a subClassOf neuron

-   *property chain*: has\_soma\_location o part\_of --> has\_soma\_location \# If x has soma location y and y is part\_of z, then x has\_soma\_location\_z

**Example of reasoning with the property chain:**

'cortical interneuron' equivalentTo 'interneuron' that has\_soma\_location some 'cerebral cortex' 'rosehip neuron'

'rosehip neuron' subClassOf interneuron  and has\_soma\_location some 'cortical layer 1' 

'cortical layer 1'  subClassOf part\_of some 'cerebral cortex

=> 'rosehip neuron' subClassOf 'cortical interneuron'

### sends synaptic output to region

A relationship between a neuron and a region, where the neuron has a functionally relevant number of output synapses in that region.

'[<u>adult basket subesophageal neuron</u>](http://purl.obolibrary.org/obo/FBbt_00051856)' SubClassOf [<u>sends synaptic output to region</u>](https://www.ebi.ac.uk/ols4/ontologies/fbbt/properties/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FRO_0013003?lang=en)
*some* [<u>inferior posterior slope</u>](https://www.ebi.ac.uk/ols4/ontologies/fbbt/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FFBbt_00045046?lang=en)

### receives synaptic input in region

A relationship between a neuron and a region, where the neuron has a functionally relevant number of output synapses:

e.g. '[<u>adult basket subesophageal neuron</u>](http://purl.obolibrary.org/obo/FBbt_00051856)' SubClassOf ‘[<u>receives synaptic input in region</u>](https://www.ebi.ac.uk/ols4/ontologies/fbbt/properties/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FRO_0013002?lang=en)*’
some ‘*<u>[superior posterior slope](https://www.ebi.ac.uk/ols4/ontologies/fbbt/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FFBbt_00045040?lang=en)’</u>

### fasciculates\_with

Use this to record the tracts or nerves that a neuron’s projections fasciculate with.

e.g. ‘Betz cell’ subClasssOf ‘fasciculates with’ some ‘corticospinal tract’.

subPropertyOf: overlaps

domain: neuron
range: neuron projection bundle

## Recording synaptic connectivity (neurons)

To record neuron-to-neuron or motor neuron-to-target muscle connectivity, consider the following object properties. These properties should be used when connectivity is key to the definition, for example, in cases where a motor neuron type is defined by the type of muscle fiber on which it synapses.

### [<u>synapsed to</u>](http://purl.obolibrary.org/obo/RO_0002120)

For example, ['alpha motor neuron'](http://purl.obolibrary.org/obo/CL_0008038) SubClassOf [**synapsed to**](http://purl.obolibrary.org/obo/RO_0002120) *some* ['extrafusal muscle fiber'](http://purl.obolibrary.org/obo/CL_0008046)

### [<u>synapsed by</u>](http://purl.obolibrary.org/obo/RO_0002103)

-   This is the the inverse of [**synapsed to**](http://purl.obolibrary.org/obo/RO_0002120)

For example, ['extrafusal muscle fiber'](http://purl.obolibrary.org/obo/CL_0008046) SubClassOf [**synapsed by**](http://purl.obolibrary.org/obo/RO_0002103) *some* ['alpha motor neuron'](http://purl.obolibrary.org/obo/CL_0008038)

## Recording function

Cellular function is recorded by linking GO biological process terms with the object properties [**'capable of'**](http://purl.obolibrary.org/obo/RO_0002215) and ‘capable of part of’

###  [<u>'capable of'</u>](http://purl.obolibrary.org/obo/RO_0002215)

Use this relationships where the cell is capable of carrying out the entirety of the process

For example, ['hilus cell of ovary'](http://purl.obolibrary.org/obo/CL_0002095) has the following subclass:

[**'capable of'**](http://purl.obolibrary.org/obo/RO_0002215) *some* ['androgen secretion'](http://purl.obolibrary.org/obo/GO_0035935)

### ‘capable of part of’

Use this relationship where only part of the process occurs in the cell type.

e.g.  'retinal bipolar neuron' 'capable of part of' some 'visual perception'

## Recording developmental lineage

Developmental lineage is recorded between cell types with the object property [**develops from**](http://purl.obolibrary.org/obo/RO_0002202) (a transitive property), or in the case where there are no intermediates between the cells, [**'directly develops from'**](http://purl.obolibrary.org/obo/RO_0002207) (a non-transitive subproperty of **develops_from**)

For example, ['leukocyte'](http://purl.obolibrary.org/obo/CL_0000738) subClassOf [**develops from**](http://purl.obolibrary.org/obo/RO_0002202) *some* ['hematopoietic stem cell'](http://purl.obolibrary.org/obo/CL_0000037)

## Recording cell markers

Only markers that are necessary to define a cell type should be recorded.

### cell surface (protein) markers

The cell ontology has a set of terms for recording cell surface markers.

The most commonly used relation for recording markers is [**'has plasma
membrane part'**](http://purl.obolibrary.org/obo/RO_0002104). This
object property is used to record cell surface markers, especially in
immune cells. There are also more specific properties, [**'has low
plasma membrane amount'**](http://purl.obolibrary.org/obo/RO_0015016)
and [**'has high plasma membrane
amount'**](http://purl.obolibrary.org/obo/RO_0015015), that can be used
at an editor's discretion. In each case, a term from the [PRotein
Ontology (PRO)](https://github.com/PROconsortium/PRoteinOntology) or a
protein complex term from the [Gene Ontology
(GO)](https://github.com/geneontology/go-ontology) is used as the object
of the relation.

For example, ['alpha-beta T cell'](http://purl.obolibrary.org/obo/CL_0000789) has the following
equivalence axiom:

['T cell'](http://purl.obolibrary.org/obo/CL_0000084) *and* [**'has
plasma membrane part'**](http://purl.obolibrary.org/obo/RO_0002104)
*some* ['alpha-beta T cell receptor complex'](http://purl.obolibrary.org/obo/GO_0042105)

Absence of a marker can be recorded using
[**lacks\_plasma\_membrane\_part**](https://ontobee.org/ontology/CL?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fcl%23lacks_plasma_membrane_part)


 

Warning - this is used in place of the more accurate OWL expression "NOT has_part some X*** in order to keep within the EL profile of OWL. It's use with a general class as a target can potentially lead to reasoning errors.  

### recording gene markers

### ‘expresses’

Use this to link a cell type to a gene or transcript that defines it:

For example:

'lamp5 GABAergic cortical interneuron' EquivalentTo:
interneuron and ('has soma location' some 'cerebral cortex')
and ('capable of' some 'gamma-aminobutyric acid secretion, neurotransmission') 
and (expresses some 'lysosome-associated membrane glycoprotein 5')

### Recording cell parts

To record parts above the granularity of proteins and complexes, use a 'has part' relationship with and object from the Gene Ontology cellular_cmponent branch.

e.g. 'melanocyte' subClassOf 'has part' some 'melanosome'

This GO term can be combined with a PATO quality term (e.g. for shape) where necessary, e.g.

For example:

'mature basophil' subClassOf ('has part' some (nucleus and ('has characteristic' some lobed)))

## Recording general cellular characteristics

The ontology [<u>PATO</u>](https://www.ebi.ac.uk/ols4/ontologies/pato),
has a rich set of terms that can be used to record the general
characteristics of cells, such as their morphology. These are recorded
using [**'has characteristic'**](http://purl.obolibrary.org/obo/RO_0000053).

In choosing PATO terms, avoid those referring to some change in
characteristic (e.g,.’ increased branchiness’). The following list of
examples is not exhaustive:

### Recording Morphology

PATO has a set of general morphology terms which may be applicable to
cells

For example, [erythrocyte](http://purl.obolibrary.org/obo/CL_0000765)
subClassOf [**'has characteristic'**](http://purl.obolibrary.org/obo/RO_0000053)
*some* [biconcave](http://purl.obolibrary.org/obo/PATO_0002039)

PATO also has a set of terms for [<u>specific cell morphologies</u>](https://www.ebi.ac.uk/ols4/ontologies/pato) (mostly
neuronal), e.g.

‘Betz cell’ subClassOf ‘has characteristic’ some ‘standard pyramidal morphology’

### Recording nuclear number 

To record the number of nuclei in a cell, use a PATO subclass
under the term ['nucleate quality'](http://purl.obolibrary.org/obo/PATO_0001404) with the ['has
characteristic'](http://purl.obolibrary.org/obo/RO_0000053) relation.

<img src="media/image1.png" style="width:2.75657in;height:2.39014in" alt="image" />

For example, 

[platelet](http://purl.obolibrary.org/obo/CL_0000233) subClassOf (['has_characteristic'](http://purl.obolibrary.org/obo/RO_0000053) *some* [**anucleate**](http://purl.obolibrary.org/obo/PATO_0001405))

Note - that pato includes bridging axioms that infer part relationships
based on these characteristics.

e.g.

cell and ('has characteristic' some multinucleate) SubClassOf 'has part'
some nucleus
                       
## Taxon constraints

See
<https://oboacademy.github.io/obook/explanation/taxon-constraints-explainer/>.

