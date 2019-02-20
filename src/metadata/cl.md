---
layout: ontology_detail
id: cl
title: Cell Ontology
jobs:
  - id: https://travis-ci.org/obophenotype/cell-ontology
    type: travis-ci
build:
  checkout: git clone https://github.com/obophenotype/cell-ontology.git
  system: git
  path: "."
contact:
  email: 
  label: 
  github: 
description: Cell Ontology is an ontology...
domain: stuff
homepage: https://github.com/obophenotype/cell-ontology
products:
  - id: cl.owl
    name: "Cell Ontology main release in OWL format"
  - id: cl.obo
    name: "Cell Ontology additional release in OBO format"
  - id: cl.json
    name: "Cell Ontology additional release in OBOJSon format"
  - id: cl/cl-base.owl
    name: "Cell Ontology main release in OWL format"
  - id: cl/cl-base.obo
    name: "Cell Ontology additional release in OBO format"
  - id: cl/cl-base.json
    name: "Cell Ontology additional release in OBOJSon format"
dependencies:
- id: pr
- id: go
- id: uberon
- id: ro
- id: chebi
- id: clo
- id: pato
- id: ncbitaxon

tracker: https://github.com/obophenotype/cell-ontology/issues
license:
  url: http://creativecommons.org/licenses/by/3.0/
  label: CC-BY
---

Enter a detailed description of your ontology here. You can use arbitrary markdown and HTML.
You can also embed images too.

