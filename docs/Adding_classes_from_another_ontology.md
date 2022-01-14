# How to add (import) classes to the Cell Ontology (CL) from another ontology

## 1. Follow steps 1 - 5 under the heading [Protege-based declaration.](https://obophenotype.github.io/cell-ontology/odk-workflows/UpdateImports/#protege-based-declaration)

_NB: Even though the instructions state that this workflow is to be avoided, the other solutions in the current documentation are out of date._


## 2. Refresh the imports

To refresh the imports, open Docker so it is running in the background. Then open Terminal, navigate to src/ontology directory in the cell-ontology repository and run:

`sh run.sh make imports/merged_import.owl`

Running the above command requires > 8GB RAM and sufficient computational power. If the refresh fails to complete due to hardware limitations, create a new issue in GitHub detailing which class(es) need to be imported and another editor can add it on your behalf.

Once the imports are refreshed, return to Protégé, add the logical axioms that include the newly imported class(es) and create a pull request per standard procedure. 

_Note that the import refresh process seems to be quite laborious/computationally expensive as-is, and a centralised database approach may be an improved longterm solution._
