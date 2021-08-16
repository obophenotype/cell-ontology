# Importing a new UBERON term to CL

Often an UBERON term that is not yet imported by CL will be necessary (e.g. for a nice logic definition). 

For updating the imports, the step-by-step is:

- Make sure you are working on a new branch, in the context of the ticket you are working on 

- Add the UBERON term to the end of the list in `cell-ontology/src/ontology/imports/uberon_terms.txt`

- Run `./run.sh make imports/uberon_import.owl`

An  script will wherever necessary. Note that this step might use some memory (at least 2 GB of RAM), so make sure you have some free space before starting it. 


