# Merging Terms in CL 

## How to merge terms
For general instructions on how to merge terms, please see this [How-to Guide](https://oboacademy.github.io/obook/howto/merge-terms/)
In addition to the above, please add the annotation `has_alternative_id` on the winning term with the ID of the losing term.

## Considerations on which should be the winning term
1. Check Usage by GO - This can be done by using [AmiGO 2](http://amigo.geneontology.org/amigo)
1. Check Usage by other ontologies - This can be done by using [Ontobee](http://www.ontobee.org/ontology/CL)
1. Check Usage within CL (you can do this in Protege with the usage tab) - this should be lower priority as you can easily change this while obsoleting the "losing" term