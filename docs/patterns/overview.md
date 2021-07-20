# Pattern directory
This is a listing of all the patterns hosted as part of this directory

## Patterns in 
### Cell bearer of quality
*A cell that has a specific quality, such as binucleate.*

| Attribute | Info |
|----------|----------|
| IRI | http://purl.obolibrary.org/obo/cl/cellBearerOfQuality |
| Name | cellBearerOfQuality |
| Classes | CL:0000000, PATO:0000001,  |
| Variables | cell (CL:0000000), quality (PATO:0000001),  |
| Contributors | [0000-0001-5208-3432](https://orcid.org/0000-0001-5208-3432), [0000-0002-6601-2165](https://orcid.org/0000-0002-6601-2165),  |
| Examples | [mondo](https://github.com/monarch-initiative/mondo/blob/master/src/patterns/data/matches/cellBearerOfQuality.tsv) |

#### Data preview: 
| defined:class                             | defined:class:label   | cell                                      | cell:label   | quality                                     | quality:label            |
|:------------------------------------------|:----------------------|:------------------------------------------|:-------------|:--------------------------------------------|:-------------------------|
| CL:0001061 | abnormal cell         | CL:0000000 | cell         | PATO:0000460 | abnormal                 |
| CL:0000225 | anucleate cell        | CL:0000003 | native cell  | PATO:0001405 | anucleate                |
| CL:0000227 | binucleate cell       | CL:0000003 | native cell  | PATO:0001406 | binucleate               |
| CL:0000103 | bipolar neuron        | CL:0000099 | interneuron  | PATO:0070006 | bipolar morphology       |
| CL:4023077 | bitufted neuron       | CL:0000099 | interneuron  | PATO:0070012 | bitufted cell morphology |

See full table [here](https://github.com/monarch-initiative/mondo/blob/master/src/patterns/data/matches/cellBearerOfQuality.tsv)
### Cell capable of biological process
*Any cell that is involved in/capable of a particular biological process, such as acid secretion.*

| Attribute | Info |
|----------|----------|
| IRI | http://purl.obolibrary.org/obo/cl/cellCapableOfBiologicalProcess |
| Name | cellCapableOfBiologicalProcess |
| Classes | CL:0000000, GO:0008150,  |
| Variables | cell (CL:0000000), biological_process (GO:0008150),  |
| Contributors |  |
| Examples | [mondo](https://github.com/monarch-initiative/mondo/blob/master/src/patterns/data/matches/cellCapableOfBiologicalProcess.tsv) |

#### Data preview: 
| defined:class                             | defined:class:label                        | biological:process                        | biological:process:label                             | cell                                      | cell:label                      |
|:------------------------------------------|:-------------------------------------------|:------------------------------------------|:-----------------------------------------------------|:------------------------------------------|:--------------------------------|
| CL:0000236 | B cell                                     | GO:0019724 | B cell mediated immunity                             | CL:0000945 | lymphocyte of B lineage         |
| CL:0000492 | CD4-positive helper T cell                 | GO:0001816 | cytokine production                                  | CL:0000624 | CD4-positive, alpha-beta T cell |
| CL:0000795 | CD8-positive, alpha-beta regulatory T cell | GO:0050777 | negative regulation of immune response               | CL:0000625 | CD8-positive, alpha-beta T cell |
| CL:0011005 | GABAergic interneuron                      | GO:0061534 | gamma-aminobutyric acid secretion, neurotransmission | CL:0000099 | interneuron                     |
| CL:0000617 | GABAergic neuron                           | GO:0061534 | gamma-aminobutyric acid secretion, neurotransmission | CL:0000540 | neuron                          |

See full table [here](https://github.com/monarch-initiative/mondo/blob/master/src/patterns/data/matches/cellCapableOfBiologicalProcess.tsv)
### Cell has plasma membrane part x
*A cell type that is characterized by a plasma membrane part, such as a cilium or receptor. Note - that this is only good for cells defined by a single plasma membrane receptor.*

| Attribute | Info |
|----------|----------|
| IRI | http://purl.obolibrary.org/obo/cl/cellHasPlasmaMembranePartX |
| Name | cellHasPlasmaMembranePartX |
| Classes | CL:0000000, CL:0000003, GO:0005886,  |
| Variables | cell (CL:0000003), plasma_membrane (GO:0005886),  |
| Contributors | [0000-0001-5208-3432](https://orcid.org/0000-0001-5208-3432), [0000-0002-6601-2165](https://orcid.org/0000-0002-6601-2165),  |
| Examples |  |

### Cell part of anatomical entity
*A cell that is part of an anatomical entity.*

| Attribute | Info |
|----------|----------|
| IRI | http://purl.obolibrary.org/obo/cl/cellPartOfAnatomicalEntity |
| Name | cellPartOfAnatomicalEntity |
| Classes | CL:0000000, UBERON:0001062,  |
| Variables | cell (CL:0000000), anatomical_entity (UBERON:0001062),  |
| Contributors | [0000-0001-5208-3432](https://orcid.org/0000-0001-5208-3432), [0000-0002-6601-2165](https://orcid.org/0000-0002-6601-2165),  |
| Examples | [mondo](https://github.com/monarch-initiative/mondo/blob/master/src/patterns/data/matches/cellPartOfAnatomicalEntity.tsv) |

#### Data preview: 
| defined:class                             | defined:class:label                     | anatomical:entity                             | anatomical:entity:label    | cell                                      | cell:label                |
|:------------------------------------------|:----------------------------------------|:----------------------------------------------|:---------------------------|:------------------------------------------|:--------------------------|
| CL:0009032 | B cell of appendix                      | UBERON:0001154 | vermiform appendix         | CL:0000236 | B cell                    |
| CL:0009045 | B cell of medullary sinus of lymph node | UBERON:0009744 | lymph node medullary sinus | CL:0000236 | B cell                    |
| CL:0010007 | His-Purkinje system cell                | UBERON:0004146 | His-Purkinje system        | CL:0000003 | native cell               |
| CL:0002680 | PP cell of intestine                    | UBERON:0000160 | intestine                  | CL:0000696 | PP cell                   |
| CL:0009015 | Peyer's patch follicular dendritic cell | UBERON:0001211 | Peyer's patch              | CL:0000442 | follicular dendritic cell |

See full table [here](https://github.com/monarch-initiative/mondo/blob/master/src/patterns/data/matches/cellPartOfAnatomicalEntity.tsv)
### Taxon specific
*A cell that is restricted to a specific taxon, such as CL:0001200 'lymphocyte of B lineage, CD19-positive' are only in mammals. Note - this is not to be used for any cell that is restricted to a taxon, this is for taxon-specific subclasses of existing cell types. This should hardly ever be used.*

| Attribute | Info |
|----------|----------|
| IRI | http://purl.obolibrary.org/obo/cl/taxonSpecific |
| Name | taxonSpecific |
| Classes | CL:0000000, NCBITaxon:1,  |
| Variables | cell (CL:0000000), taxon (NCBITaxon:1),  |
| Contributors | [0000-0001-5208-3432](https://orcid.org/0000-0001-5208-3432), [0000-0002-6601-2165](https://orcid.org/0000-0002-6601-2165),  |
| Examples |  |

