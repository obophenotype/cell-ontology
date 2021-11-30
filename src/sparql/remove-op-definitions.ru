PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX definition: <http://purl.obolibrary.org/obo/IAO_0000115>
DELETE {
   ?term definition: ?def .
   ?ax a owl:Axiom ;
          owl:annotatedSource ?term ;
          owl:annotatedProperty definition: ;
   	 	  owl:annotatedTarget ?def .
}
WHERE {
    ?term definition: ?def .
    OPTIONAL {
    	?ax a owl:Axiom ;
        owl:annotatedSource ?term ;
        owl:annotatedProperty definition: ;
   	 	  owl:annotatedTarget ?def .
    }
    FILTER (ISIRI(?term) && (STRSTARTS(STR(?term), "http://purl.obolibrary.org/obo/RO_") || STRSTARTS(STR(?term), "http://purl.obolibrary.org/obo/BFO_")))
}