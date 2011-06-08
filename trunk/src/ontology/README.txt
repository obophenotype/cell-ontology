cl ontology repository
======================

ontology/
  cl           Core public ontology release
                * pre-reasoned
                * subsets of external ontologies MIREOTed in

  cl-basic     Simple basic version of the ontology
                * pre-reasoned
                * NO external ontology terms and all inter-ontology links REMOVED

               Note that cl-basic.obo corresponds exactly with
               cell.obo in obo sourceforge CVS.

  cl-edit      Editors version of the ontology
               Currently this corresponds to the primary cell.edit.obo in obo sourceforge CVS
                * NOT pre-reasoned
                * subsets of external ontologies MIREOTed in

Note that .obo and .owl files are provided for each alternate
version. These should be semantically equivalent, and use the new
obo2owl translation

URLs
====

The following URLs should be used for the two release versions:

http://purl.obolibrary.org/obo/cl.owl
http://purl.obolibrary.org/obo/cl.obo
http://purl.obolibrary.org/obo/cl-basic.owl
http://purl.obolibrary.org/obo/cl-basic.obo
