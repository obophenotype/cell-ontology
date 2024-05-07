from rdflib import Graph
from mdutils import MdUtils
from datetime import datetime

class OntologyContentReport:
    """Generic class for summarize content in an ontology"""

    def __init__(self, ontology_iri, ont_namespace):
        self.ontology_iri = ontology_iri
        self.ont_namespace = ont_namespace
        self.g = self._init_graph(ontology_iri)
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.nb_subclass_root = None
        self.nb_annotations = None
        self.nb_synonyms = None
        self.nb_references = None
        self.nb_relationships = None
        self.nb_cxg = None
        self.nb_hra = None

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
                                               ?ont rdf:type owl:Ontology .
                                               ?ont <http://purl.obolibrary.org/obo/IAO_0000700> ?root .
                                               ?class rdfs:subClassOf* ?root .
                                               FILTER (STRSTARTS(STR(?class), "http://purl.obolibrary.org/obo/CL_"))
                                           }
                                           """)
        self.nb_annotations = self.query("""
                                         SELECT (COUNT (?annotation) AS ?nb_annotations)
                                         WHERE {
                                             ?annotation rdf:type owl:AnnotationProperty .
                                             ?class rdf:type owl:Class .
                                             ?class ?annotation ?value .
                                             FILTER (STRSTARTS(STR(?class), "http://purl.obolibrary.org/obo/CL_"))
                                         }
                                         """)
        self.nb_cxg = self.query("""
                                 SELECT (COUNT (?cxg) AS ?nb_cxg)
                                 WHERE {
                                    ?cxg rdf:type owl:Class .
                                    ?cxg <http://www.geneontology.org/formats/oboInOwl#inSubset> <http://purl.obolibrary.org/obo/cl#cellxgene_subset> .
                                    FILTER (STRSTARTS(STR(?class), "http://purl.obolibrary.org/obo/CL_"))
                                 }
                                 """)

    def prepare_report(self, filename):
        md_report = MdUtils(filename=filename, title=f"Release Notes {self.date}")

        md_report.new_header(level=1, title="Ontology content summary")
        md_report.new_line()

        summary_table = [["Metric", "Value"],
                         ["Number of root classes", self.nb_subclass_root],
                         ["Number of annotations", self.nb_annotations],
                         ["Number of synonyms", self.nb_synonyms],
                         ["Number of references", self.nb_references],
                         ["Number of relationships", self.nb_relationships]]
        md_report.new_table(columns=2, rows=summary_table, text_align="center")

        md_report.new_line()
        md_report.create_md_file()

        return md_report
if __name__ == "__main__":
    report = OntologyContentReport("http://purl.obolibrary.org/obo/cl/cl-simple.owl", "CL")
    report.get_content_summary()
