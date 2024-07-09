PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

DELETE {
    ?sub rdfs:subClassOf ?super .
    
    ?axiom a owl:Axiom ;
        owl:annotatedSource ?sub ;
        owl:annotatedProperty rdfs:subClassOf ;
        owl:annotatedTarget ?super ;
        oboInOwl:is_inferred "true" .
    
}
WHERE {
    ?sub rdfs:subClassOf ?super .
    ?axiom a owl:Axiom ;
        owl:annotatedSource ?sub ;
        owl:annotatedProperty rdfs:subClassOf ;
        owl:annotatedTarget ?super ;
        oboInOwl:is_inferred "true" .
    FILTER (ISIRI(?sub) && (STRSTARTS(STR(?sub), "http://purl.obolibrary.org/obo/CL_")))
}

