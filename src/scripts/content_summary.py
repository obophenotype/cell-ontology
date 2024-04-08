from rdflib import Graph


class OntologyContentReport:
    """Generic class for summarize content in an ontology"""

    def __init__(self, ontology_iri, ont_namespace):
        self.ontology_iri = ontology_iri
        self.ont_namespace = ont_namespace
        self.g = self._init_graph(ontology_iri)
        self.nb_subclass_root = None
        self.nb_annotations = None
        self.nb_synonyms = None
        self.nb_references = None
        self.nb_relationships = None

    def _init_graph(self, ontology_iri):
        """Load given ontology into Graph"""
        g = Graph()
        g.parse(ontology_iri, format="xml")
        return g

    def query(self, query):
        """Query graph"""
        response = self.g.query(query)
        print(response.bindings[0])
        return response.bindings[0]

    def get_content_summary(self):
        """Query graph to get summary"""
        self.nb_subclass_root = self.query("""
                                           SELECT (COUNT (DISTINCT ?class) AS ?nb_subclass_root)
                                           WHERE {
                                               ?class rdfs:subClassOf* <http://purl.obolibrary.org/obo/CL_0000000>
                                           }
                                           """)
        self.nb_annotations = self.query("""
                                         SELECT (COUNT (?annotation) AS ?nb_annotations)
                                         WHERE {
                                             ?annotation rdf:type owl:AnnotationProperty .
                                             ?class rdf:type owl:Class .
                                             ?class ?annotation ?value .
                                         }
                                         """)


if __name__ == "__main__":
    report = OntologyContentReport("http://purl.obolibrary.org/obo/cl/cl-simple.owl", "CL")
    report.get_content_summary()
