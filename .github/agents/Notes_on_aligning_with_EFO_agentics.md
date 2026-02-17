CL IMPORT AGENT 

Needs updating to follow CL workflow.  There is some danger containers will not be meaty enough.

REMOVED FROM EFO ONTOLOGIST:

### OWL/XML Formatting

Follow this template for new terms:

```xml
    <!-- http://www.ebi.ac.uk/cl/CL_XXXXXXX -->

    <owl:Class rdf:about="http://www.ebi.ac.uk/cl/CL_XXXXXXX">
        <rdfs:subClassOf rdf:resource="http://www.ebi.ac.uk/cl/PARENT_TERM_IRI"/>
        <obo:IAO_0000115>[Definition text]</obo:IAO_0000115>
        <obo:IAO_0000117>AI agent</obo:IAO_0000117>
        <dc:date rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">[ISO timestamp]</dc:date>
        <oboInOwl:hasExactSynonym>[synonym]</oboInOwl:hasExactSynonym>
        <oboInOwl:hasDbXref>PMID:XXXXXXX</oboInOwl:hasDbXref>
        <rdfs:label xml:lang="en">[term label]</rdfs:label>
    </owl:Class>
```

### Logical Definitions

For terms with genus-differentia patterns:

```xml
    <owl:Class rdf:about="http://www.ebi.ac.uk/cl/CL_XXXXXXX">
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="[PARENT_CLASS_IRI]"/>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="[PROPERTY_IRI]"/>
                        <owl:someValuesFrom rdf:resource="[FILLER_IRI]"/>
                    </owl:Restriction>
                </owl:intersectionOf>
            </owl:Class>
        </owl:equivalentClass>
        <obo:IAO_0000115>[Definition matching logical definition]</obo:IAO_0000115>
        <!-- other annotations -->
        <rdfs:label xml:lang="en">[term label]</rdfs:label>
    </owl:Class>
```

### Common Relationships

#### Measurements
```xml
<!-- is_about relationship -->
<owl:Restriction>
    <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/IAO_0000136"/>
    <owl:someValuesFrom rdf:resource="[IRI_OF_MEASURED_ENTITY]"/>
</owl:Restriction>
```

#### Diseases
```xml
<!-- has_disease_location relationship -->
<owl:Restriction>
    <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/RO_0004026"/>
    <owl:someValuesFrom rdf:resource="[UBERON_IRI]"/>
</owl:Restriction>
```

#### Part-whole
```xml
<!-- part_of relationship -->
<owl:Restriction>
    <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/BFO_0000050"/>
    <owl:someValuesFrom rdf:resource="[WHOLE_IRI]"/>
</owl:Restriction>
```

### Handling Cross-Ontology Relationships

When linking terms from different ontologies (e.g., CL term → OBA parent):

1. **Always import the external term first** via @CL-importer
2. Check if relationship exists in source ontology (if yes, DO NOT add to subclasses.csv)
3. If relationship is cross-ontology and new, add to `src/templates/subclasses.csv`:
   ```
   ID_OF_CL_TERM,ID_OF_EXTERNAL_PARENT_TERM
   ```
4. Rebuild component:
   ```bash
   cd src/ontology
   make components/subclasses.owl
   ```