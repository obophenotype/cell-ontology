# Generate a OWL file of cross-references from a SSSOM TSV file.
# Warning: This script assumes a valid SSSOM TSV file.

# Minimal OWL boilerplate
BEGIN {
  FS = "\t";
  print "<?xml version=\"1.0\"?>";
  print "<rdf:RDF xmlns=\"http://www.w3.org/2002/07/owl#\"";
  print "  xml:base=\"http://www.w3.org/2002/07/owl\"";
  print "  xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"";
  print "  xmlns:oboInOwl=\"http://www.geneontology.org/formats/oboInOwl#\">";
  print "  <Ontology rdf:about=\"http://purl.obolibrary.org/obo/cl/components/mappings.owl\"/>";
}

END {
  print "</rdf:RDF>";
}

# Find the column containing the object ID
# (We do not need to do that for the subject ID, as the SSSOM
#  specification says the subject_id is always the first column)
/^subject_id/ {
  for ( i = 1; i < NF; i++ ) {
    if ( $i == "object_id" ) {
      object_index = i;
    }
  }  
}

# We only generate cross-references for "exact" mappings
/(skos:exactMatch|semapv:crossSpeciesExactMatch)/ {
  split($object_index, object, ":");
  # Only process mappings where the object term belongs to Uberon
  if ( object[1] == "CL" ) {
    print "  <Class rdf:about=\"http://purl.obolibrary.org/obo/CL_"object[2]"\">";
    print "    <oboInOwl:hasDbXref rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"$1"</oboInOwl:hasDbXref>";
    print "  </Class>";
  }
}
