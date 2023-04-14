#!/usr/bin/env python
import argparse
import csv
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, List

UBERGRAPH_ENDPOINT = "https://ubergraph.apps.renci.org/sparql"


def calculate_coverage(_scope_dict: Dict[str, str], _term_leaves_dict: Dict[str, Dict[str, str]]):
    """Calculates coverage and returns list that contains coverage status of terms under the scope. Also returns
    not covered term list and a report that shows the percentage of the coverage

    Args:
        _scope_dict (Dict[str, str]): Terms that are subclass of the scope
        _term_leaves_dict (Dict[str, Dict[str, str]): Dictionary of terms with their subclasses

    Returns:
        * A coverage report with number of total terms and percentage of the covered terms
    """
    covered_tissue_number = 0
    _not_covered_list = []
    for scope_iri, scope_label in _scope_dict.items():
        covered = False
        for organ, tissue in _term_leaves_dict.items():
            # Coverage % calculation part and creating not_covered list
            if tissue.get(scope_iri) and not covered:
                covered_tissue_number = covered_tissue_number + 1
                covered = True
        if not covered and [scope_iri, scope_label] not in _not_covered_list:
            _not_covered_list.append([scope_iri, scope_label])
    return f"{100 * (covered_tissue_number / len(_scope_dict)):.2f}%", covered_tissue_number, _not_covered_list


def generate_scope_dict(ontologies: str, _term_dict: Dict[str, str], _scope: str) -> Dict[str, str]:
    # Retrieve terms under scope in 'ontologies' with IRIs and labels from Ubergraph.
    # Remove all superclasses of terms on the term list (via subClassOf/ and part_of)
    mas_dict = get_scope_terms(ontologies, _scope)
    return clean_up_scope_terms(_term_dict, mas_dict, _scope)


def get_scope_terms(ontologies: str, _scope: str) -> Dict[str, str]:
    # Get multicellular anatomical structure terms with IRIs and labels from Ubergraph
    sparql.setQuery(get_scope_query(ontologies, _scope))
    mas_query_response = sparql.queryAndConvert()
    mas_dict: Dict[str, str] = {}
    for mas in mas_query_response["results"]["bindings"]:
        mas_dict.update({mas['mas']['value']: mas['label']['value']})
    return mas_dict


def clean_up_scope_terms(_term_dict: Dict[str, str], mas_dict: Dict[str, str], _scope: str) -> Dict[str, str]:
    # Remove all superclasses of terms on the scope list (via subClassOf/ and part_of)
    sparql.setQuery(get_superclass_value_query(list(_term_dict.values()), _scope))
    super_ret = sparql.queryAndConvert()
    for super_class in super_ret["results"]["bindings"]:
        mas_dict.pop(super_class['super']['value'], None)
    return mas_dict


def get_term_leaves(term_list: List[str], _scope: str) -> Dict[str, Dict[str, str]]:
    # Get terms under, connected with 'subClassOf' relation, given the term list via template file from Ubergraph
    _term_leaves_dict = {}
    sparql.setQuery(get_tissue_list_query(term_list, _scope))
    ret = sparql.queryAndConvert()
    for row in ret["results"]["bindings"]:
        if row['organ_label']['value'] not in _term_leaves_dict.keys():
            _term_leaves_dict.update(
                {row['organ_label']['value']: {row['tissue']['value']: row['tissue_label']['value']}})
        else:
            _term_leaves_dict[row['organ_label']['value']].update(
                {row['tissue']['value']: row['tissue_label']['value']})
    return _term_leaves_dict


def get_invalid_subclass_list(_term_dict: Dict[str, Dict[str, str]]) -> List[str]:
    merged_subset = {k: v for key, value in _term_dict.items() for k, v in value.items() if key != value.get(k)}
    invalid_subclass_list = []
    for term, term_subset in _term_dict.items():
        if term in merged_subset.values():
            invalid_subclass_list.append(term)
    return invalid_subclass_list


def get_scope_query(ontology: str, scope_term: str) -> str:
    """Returns the SPARQL query to retrieve multicellular anatomical structure terms with IRIs and labels

    Args:
        ontology (str): Ontology name, can be either "uberon" or "all"
        scope_term (str): Scope of the slim

    Returns:
        output (str): Multicellular anatomical structure SPARQL query
    """
    # ?mas rdfs:isDefinedBy 'obo:uberon.owl'
    filter_str = "FILTER(strstarts(str(?mas),'http://purl.obolibrary.org/obo/UBERON_'))" if ontology == 'uberon' else ""
    _scope = scope_term if ":" in scope_term else f"<{scope_term}>"
    return f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
        PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
        SELECT ?mas ?label
        WHERE
        {{
          ?mas <http://www.w3.org/2000/01/rdf-schema#subClassOf>|<http://purl.obolibrary.org/obo/BFO_0000050> {_scope} .
          ?mas rdfs:isDefinedBy <http://purl.obolibrary.org/obo/cl.owl> .
          ?mas rdfs:label ?label. 
          ?s <http://www.w3.org/2000/01/rdf-schema#subClassOf>|<http://purl.obolibrary.org/obo/BFO_0000050> ?mas.
          FILTER(?s != ?mas)
          {filter_str}
        }}
    """


def get_superclass_value_query(term_iri_list: List[str], _scope: str) -> str:
    """Returns the SPARQL query to retrieve superclasses of given term list

    Args:
        term_iri_list (List[str]): Term IRI list
        _scope (str): Scope term

    Returns:
        output (str): Terms superclass SPARQL query
    """
    return f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
            PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
            SELECT DISTINCT ?super ?label
            WHERE
            {{
              ?organ <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?super. ?super rdfs:label ?label. 
              ?super <http://www.w3.org/2000/01/rdf-schema#subClassOf>|<http://purl.obolibrary.org/obo/BFO_0000050> {_scope}
              VALUES ?organ {{{' '.join(term_iri_list)}}}
            FILTER(?organ != ?super)
            }}
        """


def get_tissue_list_query(term_iri_list: List[str], scope_term: str) -> str:
    """Returns the SPARQL query to retrieve ontology terms that are under the given term

    Args:
        term_iri_list (List[str]): Term IRI list
        scope_term (str): Scope term

    Returns:
        output (str): TIssue list SPARQL query
    """
    _scope = scope_term if ":" in scope_term else f"<{scope_term}>"
    return f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
        PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
        SELECT ?organ_label ?tissue ?tissue_label
        WHERE
        {{
          ?tissue <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?organ.
          ?tissue rdfs:label ?tissue_label. 
          ?tissue <http://www.w3.org/2000/01/rdf-schema#subClassOf>|<http://purl.obolibrary.org/obo/BFO_0000050> {_scope}. 
          ?organ rdfs:label ?organ_label.
          VALUES ?organ {{{' '.join(term_iri_list)}}}
        }}
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scope', help='''Upper class term that you want to calculate coverage of your slim''')
    parser.add_argument('-f', '--file', help='''File path of your slim's template file''')
    parser.add_argument('-o', '--output', help='''Output file name''')
    args = parser.parse_args()

    file_name = str(args.file)
    scope = str(args.scope)
    output_file = str(args.output)

    # SPARQLWrapper init
    sparql = SPARQLWrapper(UBERGRAPH_ENDPOINT)
    sparql.setReturnFormat(JSON)

    term_dict = pd.read_csv(file_name, usecols=["ID", "label"], index_col=1).iloc[1:, :].squeeze().to_dict()

    term_leaves_dict = get_term_leaves(list(term_dict.values()), scope)
    invalid_slim_term_list = get_invalid_subclass_list(term_leaves_dict)
    if invalid_slim_term_list:
        raise Exception(f"{file_name} is invalid! {','.join(invalid_slim_term_list)} are subClassOf another slim term!")
    scope_dict = generate_scope_dict("", term_dict, scope)
    report_str,  total_covered_number, not_covered_list = calculate_coverage(scope_dict, term_leaves_dict)
    result = list()
    result.append([report_str])
    result.append([total_covered_number])
    result.extend(not_covered_list)
    file = open(output_file, 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(result)
    print(f"{file_name} has {report_str} coverage over {scope}")
