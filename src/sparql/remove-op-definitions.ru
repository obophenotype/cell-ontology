PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX description: <http://purl.obolibrary.org/obo/IAO_0000115>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


DELETE {
  ?sub description: ?obj .
  ?relax a owl:Axiom ;
         owl:annotatedSource ?sub ;
         owl:annotatedProperty description: ;
         owl:annotatedTarget ?obj ;
         ?a ?b .
}
WHERE {
  {
    ?sub description: ?obj .
    ?relax a owl:Axiom ;
           owl:annotatedSource ?sub ;
           owl:annotatedProperty description: ;
           owl:annotatedTarget ?obj ;
           ?a ?b .
    FILTER (ISIRI(?sub) && STRSTARTS(STR(?sub), "http://purl.obolibrary.org/obo/RO_"))
  }
}