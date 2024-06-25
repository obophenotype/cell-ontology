""" Script to summarize content in an ontology """
import argparse
from datetime import datetime

import pandas as pd
from rdflib import Graph


class OntologyContentReport:
    """Generic class for summarizing content in an ontology"""

    def __init__(self, ontology_iri, ont_namespace):
        """
        Initialize the OntologyContentReport object.

        Args:
            ontology_iri (str): The IRI or filepath of the ontology to summarize.
            ont_namespace (str): The namespace of the ontology.
        """
        self.ontology_iri = ontology_iri
        self.ont_namespace = ont_namespace
        self.g = self._init_graph(ontology_iri)
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.nb_subclass_root = None
        self.nb_annotations = None
        self.nb_synonyms = None
        self.nb_references = None
        self.nb_def_references = None
        self.nb_relationships = None
        self.nb_cxg = None
        self.nb_hra = None

    def _init_graph(self, ontology_iri):
        """
        Load the given ontology into a Graph object.

        Args:
            ontology_iri (str): The IRI or filepath of the ontology.

        Returns:
            rdflib.Graph: The loaded ontology graph.
        """
        g = Graph()
        g.parse(ontology_iri, format="xml")
        return g

    def query(self, query):
        """
        Execute a SPARQL query on the ontology graph.

        Args:
            query (str): The SPARQL query to execute.

        Returns:
            int: The count of query results.
        """
        response = self.g.query(query)
        return response.bindings[0]["count"]

    def get_content_summary(self):
        """
        Query the ontology graph to get the content summary.
        """
        self.nb_subclass_root = self.query(f"""
            SELECT (COUNT (DISTINCT ?class) AS ?count)
            WHERE {{
                ?ont rdf:type owl:Ontology .
                ?ont <http://purl.obolibrary.org/obo/IAO_0000700> ?root .
                ?class rdfs:subClassOf* ?root .
                FILTER (STRSTARTS(STR(?class), "http://purl.obolibrary.org/obo/{self.ont_namespace}_"))
            }}
            """)

        self.nb_annotations = self.query(f"""
            SELECT (COUNT (?annotation) AS ?count)
            WHERE {{
                ?annotation rdf:type owl:AnnotationProperty .
                ?class rdf:type owl:Class .
                ?class ?annotation ?value .
                FILTER (STRSTARTS(STR(?class), "http://purl.obolibrary.org/obo/{self.ont_namespace}_"))
            }}
            """)

        self.nb_cxg = self.query(f"""
            SELECT (COUNT (?cxg) AS ?count)
            WHERE {{
                ?cxg rdf:type owl:Class .
                ?cxg <http://www.geneontology.org/formats/oboInOwl#inSubset> <http://purl.obolibrary.org/obo/cl#cellxgene_subset> .
                FILTER (STRSTARTS(STR(?cxg), "http://purl.obolibrary.org/obo/{self.ont_namespace}_"))
            }}
            """)

        self.nb_hra = self.query(f"""
            SELECT (COUNT (?hra) AS ?count)
            WHERE {{
                ?hra rdf:type owl:Class .
                ?hra <http://www.geneontology.org/formats/oboInOwl#inSubset> <http://purl.obolibrary.org/obo/uberon/core#human_reference_atlas> .
                FILTER (STRSTARTS(STR(?hra), "http://purl.obolibrary.org/obo/{self.ont_namespace}_"))
            }}
            """)

        self.nb_synonyms = self.count_report(
            self.load_report(f"{self.ont_namespace.lower()}-synonyms")
        )

        self.nb_relationships = self.count_report(
            self.load_report(f"{self.ont_namespace.lower()}-edges")
        )

        self.nb_references = self.count_report(self.load_report(
            f"{self.ont_namespace.lower()}-xrefs")["?xref"].unique()
        )

        self.nb_def_references = self.count_report(
            self.load_report(
                f"{self.ont_namespace.lower()}-def-xrefs"
            )["?xref"].unique()
        )

    def load_report(self, report_type):
        """
        Load a report from a file.

        Args:
            report_type (str): The type of report to load.

        Returns:
            pandas.DataFrame: The loaded report data.
        """
        return pd.read_csv(f"reports/{report_type}.tsv", sep="\t")

    def count_report(self, data):
        """
        Count the number of rows in a report.

        Args:
            data (pandas.DataFrame): The report data.

        Returns:
            int: The number of rows in the report.
        """
        return len(data)

    def prepare_report(self):
        """
        Prepare the content summary report for printing.
        """
        print(f"# Release Notes {self.date}")
        print("## Ontology content summary")

        summary_table = [
            {
                "Metric": "Number of subclasses of root",
                "Value": self.nb_subclass_root
            },
            {
                "Metric": f"Number of annotations on {self.ont_namespace} terms",
                "Value": self.nb_annotations
            },
            {
                "Metric": "Number of synonyms",
                "Value": self.nb_synonyms
            },
            {
                "Metric": "Number of unique references",
                "Value": self.nb_references
            },
            {
                "Metric": "Number of unique references in definitions",
                "Value": self.nb_def_references
            },
            {
                "Metric": f"Number of relationships with {self.ont_namespace} term as subject",
                "Value": self.nb_relationships
            },
            {
                "Metric": "Number of cellxgene classes",
                "Value": self.nb_cxg
                },
            {
                "Metric": "Number of HRA classes",
                "Value": self.nb_hra
            }
        ]

        print(pd.DataFrame(summary_table).to_markdown(index=False))


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--ontology_iri", type=str, help="IRI or filepath of ontology to summarize")
    cli.add_argument("--ont_namespace", type=str, help="Ontology namespace")

    args = cli.parse_args()

    report = OntologyContentReport(args.ontology_iri, args.ont_namespace)
    report.get_content_summary()
    report.prepare_report()
