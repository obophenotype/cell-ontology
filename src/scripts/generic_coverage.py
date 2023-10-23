#!/usr/bin/env python
import argparse
import csv
import os
import subprocess
from typing import Dict, List

from rdflib import Graph


def calculate_coverage(
    _scope_dict: Dict[str, str], _term_leaves_dict: Dict[str, Dict[str, str]]
):
    """Calculates coverage and returns list that contains coverage status of terms under the scope. Also returns
    not covered term list and a report that shows the percentage of the coverage

    Args:
        _scope_dict (Dict[str, str]): Terms that are subclass of the scope
        _term_leaves_dict (Dict[str, Dict[str, str]): Dictionary of terms with their subclasses

    Returns:
        * A coverage report with number of total terms and percentage of the covered terms
    """
    _covered_term_count_by_each_term = [
        [term, len(scope_members)] for term, scope_members in _term_leaves_dict.items()
    ]
    sort_term_count = sorted(_covered_term_count_by_each_term, key=lambda x: x[1])
    covered_term = set(
        [
            member
            for scope_members in _term_leaves_dict.values()
            for member in scope_members
            if member in _scope_dict.keys()
        ]
    )
    _not_covered_list = [
        [scope_iri, scope_label]
        for scope_iri, scope_label in _scope_dict.items()
        if scope_iri not in covered_term
    ]
    return (
        f"{100 * (len(covered_term) / len(_scope_dict)):.2f}%",
        sort_term_count,
        _not_covered_list,
    )


def generate_scope_dict(_term_dict: Dict[str, str], _scope: str) -> Dict[str, str]:
    # Retrieve terms under scope with IRIs and labels from Ubergraph.
    # Remove all superclasses of terms on the term list (via subClassOf/ and part_of)
    _scope_dict = get_scope_terms(_scope)
    return clean_up_scope_terms(_term_dict, _scope_dict, _scope)


def get_scope_terms(_scope: str) -> Dict[str, str]:
    # Get terms under the scope with IRIs and labels from Ubergraph
    query = get_scope_query(_scope)
    _scope_dict: Dict[str, str] = {}

    for _result in cl.query(query):
        _scope_dict.update({_result.scope_member.toPython(): _result.label.toPython()})
    return _scope_dict


def clean_up_scope_terms(
    _term_dict: Dict[str, str], _scope_dict: Dict[str, str], _scope: str
) -> Dict[str, str]:
    # Remove all superclasses of terms on the scope list (via subClassOf/ and part_of)
    query = get_superclass_value_query(list(_term_dict.values()), _scope)

    for _result in cl.query(query):
        _scope_dict.pop(_result.super.toPython(), None)
    return _scope_dict


def get_term_leaves(term_list: List[str], _scope: str) -> Dict[str, Dict[str, str]]:
    # Get terms under, connected with 'subClassOf' relation, given the term list via template file from Ubergraph
    # Prepare the SPARQL query
    query = get_term_leaves_list_query(term_list, _scope)

    _term_leaves_dict = {}
    for _result in cl.query(query):
        term_label = _result.term_label.toPython()
        term_leaf = _result.term_leaf.toPython()
        term_leaf_label = _result.term_leaf_label.toPython()

        if term_label not in _term_leaves_dict:
            _term_leaves_dict[term_label] = {term_leaf: term_leaf_label}
        else:
            _term_leaves_dict[term_label][term_leaf] = term_leaf_label

    return _term_leaves_dict


def get_invalid_subclass_list(term_list: List[str]) -> List[List[str]]:
    # Get slim terms that are subclasses of other slim terms
    query = get_invalid_subclass_list_query(term_list)

    return [
        [
            f"{_result.sub.toPython()} {_result.sub_label.toPython()}",
            "rdfs:subClassOf",
            f"{_result.obj.toPython()} {_result.obj_label.toPython()}",
        ]
        for _result in cl.query(query)
    ]


def get_scope_query(scope_term: str) -> str:
    """Returns the SPARQL query to retrieve terms under the scope with IRIs and labels

    Args:
        scope_term (str): Scope of the slim

    Returns:
        output (str): Scope members SPARQL query
    """
    _scope = scope_term if ":" in scope_term else f"<{scope_term}>"
    return f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
        PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
        PREFIX BFO: <http://purl.obolibrary.org/obo/BFO_>
        PREFIX RO: <http://purl.obolibrary.org/obo/RO_>
        SELECT ?scope_member ?label
        WHERE
        {{
          ?scope_member rdfs:subClassOf|BFO:0000050|RO:0002100 {_scope} .
          ?scope_member rdfs:label ?label. 
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
            PREFIX BFO: <http://purl.obolibrary.org/obo/BFO_>
            SELECT DISTINCT ?super ?label
            WHERE
            {{
              ?term rdfs:subClassOf ?super. ?super rdfs:label ?label. 
              ?super rdfs:subClassOf|BFO:0000050 {_scope}.
              VALUES ?term {{{' '.join(term_iri_list)}}}
            FILTER(?term != ?super)      
            }}
        """


def get_term_leaves_list_query(term_iri_list: List[str], scope_term: str) -> str:
    """Returns the SPARQL query to retrieve ontology terms that are under the given term

    Args:
        term_iri_list (List[str]): Term IRI list
        scope_term (str): Scope term

    Returns:
        output (str): Term leaves SPARQL query
    """
    _scope = scope_term if ":" in scope_term else f"<{scope_term}>"
    return f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
        PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_>
        PREFIX BFO: <http://purl.obolibrary.org/obo/BFO_>
        SELECT ?term_label ?term_leaf ?term_leaf_label
        WHERE
        {{
          ?term_leaf rdfs:subClassOf ?term.
          ?term_leaf rdfs:label ?term_leaf_label.
          ?term_leaf rdfs:subClassOf|BFO:0000050 {_scope}. 
          ?term rdfs:label ?term_label.
          VALUES ?term {{{' '.join(term_iri_list)}}}
        }}
    """


def get_invalid_subclass_list_query(term_iri_list: List[str]) -> str:
    """Returns the SPARQL query to retrieve slim terms that are subclasses of other slim terms

    Args:
        term_iri_list (List[str]): Term IRI list

    Returns:
        output (str): Invalid subclass list SPARQL query
    """
    return f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX CL: <http://purl.obolibrary.org/obo/CL_>
        SELECT DISTINCT ?sub ?sub_label ?obj ?obj_label WHERE {{
        VALUES ?sub {{{' '.join(term_iri_list)}}}
        VALUES ?obj {{{' '.join(term_iri_list)}}}
        ?sub rdfs:subClassOf ?obj .
        ?sub rdfs:label ?sub_label .
        ?obj rdfs:label ?obj_label .
        FILTER(?sub != ?obj)
        }}
    """


def run_command(command, wd):
    """
    Execute a command in a specified working directory.

    Args:
        command (list): A list containing the command and its arguments.
        wd (str): The working directory in which to execute the command.

    Returns:
        None

    Prints the command's standard output and standard error.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    try:
        completed_process = subprocess.run(
            command,
            cwd=wd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        print(f"{command[0]} command executed successfully")
        print("Standard Output:")
        print(completed_process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {command[0]} command: {e}")
        print("Standard Error:")
        print(e.stderr)


def modify_docker_script(input_file, _output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Make the change in the content
    lines[69] = lines[69].replace("-ti", "-t")

    with open(_output_file, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--scope",
        help="""Upper class term that you want to calculate coverage of your slim""",
    )
    parser.add_argument(
        "-f", "--file", help="""File path of your slim's template file"""
    )
    parser.add_argument("-o", "--output", help="""Output file name""")
    parser.add_argument(
        "-c",
        "--caller",
        default="user",
        help="""Caller of the path. It is used to determine how to use the make 
        command""",
    )
    args = parser.parse_args()

    file_name = str(args.file)
    scope = str(args.scope)
    output_file = str(args.output)
    caller = str(args.caller)

    # Define the working directory where you want to run the command
    working_directory = "../ontology/"

    if caller == "user":
        # Change -ti flag to -t in the run.sh
        modify_docker_script("../ontology/run.sh", "../ontology/run_temp.sh")
        make_command = [
            "sh",
            "run_temp.sh",
            "make",
            "cl-full.owl",
            "MIR=false",
            "IMP=false",
        ]
    else:
        make_command = [
            "make",
            "cl-full.owl",
            "MIR=false",
            "IMP=false",
        ]

    relation_graph_command = [
        "relation-graph",
        "--ontology-file",
        "cl-full.owl",
        "--output-file",
        "test.ttl",
        "--output-subclasses",
        "true",
        "--reflexive-subclasses",
        "false",
        "--property",
        "http://purl.obolibrary.org/obo/BFO_0000050",
        "--property",
        "http://purl.obolibrary.org/obo/RO_0002100",
    ]

    run_command(make_command, working_directory)
    if caller == "user":
        os.remove("../ontology/run_temp.sh")
    run_command(relation_graph_command, working_directory)

    cl_base = Graph().parse("../ontology/cl-full.owl", format="xml")
    cl_rel = Graph().parse("../ontology/test.ttl", format="ttl")
    cl = cl_base + cl_rel

    term_dict = {}
    with open(file_name, mode="r", encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        # Skip the first line
        next(reader)
        for _row in reader:
            term_dict[_row["label"]] = _row["ID"]

    term_leaves_dict = get_term_leaves(list(term_dict.values()), scope)
    invalid_slim_term_list = get_invalid_subclass_list(list(term_dict.values()))
    if invalid_slim_term_list:
        invalid_report_file = output_file.replace(
            "reports/", "reports/overlapping_terms_", 1
        )
        with open(invalid_report_file, "w+", newline="") as invalid_file:
            write = csv.writer(invalid_file)
            write.writerows(invalid_slim_term_list)
        # Disabling the exception for now
        # raise Exception(f"{file_name} is invalid! {invalid_report_file} report for more details")
    scope_dict = generate_scope_dict(term_dict, scope)
    report_str, covered_term_count_by_each_term, not_covered_list = calculate_coverage(
        scope_dict, term_leaves_dict
    )
    result = list()
    result.append(["#####Coverage percentage#####"])
    result.append([report_str])
    result.append(["#####Number of terms covered by each term in the slim#####"])
    result.extend(covered_term_count_by_each_term)
    result.append(
        [f"#####Terms that are not covered by {file_name} under {scope}#####"]
    )
    result.extend(not_covered_list)
    if output_file:
        with open(output_file, "w+", newline="") as file:
            write = csv.writer(file)
            write.writerows(result)
    print(f"{file_name} has {report_str} coverage over {scope}")
