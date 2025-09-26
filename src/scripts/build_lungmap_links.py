#!/usr/bin/env python3
"""
Build LungMap Cell Cards links for CL terms.

This script fetches LungMap Cell Cards data and creates rdfs:seeAlso annotations
for CL terms that have exact matches with LungMap cell cards.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Set, Tuple
import urllib.parse
import urllib.request
import re

# import pandas as pd  # Not needed for this script

# LungMap Cell Cards base URL
LUNGMAP_BASE_URL = "https://www.lungmap.net/research/cell-cards/"
LUNGMAP_API_URL = "https://www.lungmap.net/api/cell-cards/"  # Hypothetical API endpoint

def fetch_lungmap_data() -> List[Dict]:
    """
    Fetch LungMap Cell Cards data.
    
    For now, we'll use a mock data structure based on the example from the issue.
    In production, this would fetch from the actual LungMap API or scrape the website.
    
    Returns:
        List of cell card dictionaries containing id, name, cl_id, cl_label, match_type
    """
    # Mock data based on the example in the issue
    # This should be replaced with actual API calls when the LungMap API is accessible
    mock_data = [
        {
            "id": "LMCC0000000003",
            "name": "alveolar type 1 epithelial cell",
            "cl_id": "CL:0002062",
            "cl_label": "pulmonary alveolar type 1 cell",
            "match_type": "Exact"
        }
        # TODO: Add more entries from actual LungMap data
        # Additional entries would be automatically fetched from the LungMap API
        # when that becomes available. The structure should follow:
        # {
        #     "id": "LMCC...",
        #     "name": "cell type name from LungMap",
        #     "cl_id": "CL:NNNNNNN",
        #     "cl_label": "official CL term label",
        #     "match_type": "Exact" | "Related" | etc.
        # }
    ]
    
    # TODO: Replace with actual API call when LungMap provides programmatic access
    # Example implementation:
    # try:
    #     # Try different potential API endpoints
    #     api_endpoints = [
    #         LUNGMAP_API_URL,
    #         "https://www.lungmap.net/api/v1/cell-cards/",
    #         "https://lungmap.net/api/cell-cards.json"
    #     ]
    #     
    #     for endpoint in api_endpoints:
    #         try:
    #             response = urllib.request.urlopen(endpoint, timeout=30)
    #             data = json.loads(response.read().decode('utf-8'))
    #             # Process and normalize the data structure
    #             return normalize_lungmap_data(data)
    #         except:
    #             continue
    #             
    #     print("Warning: Could not access LungMap API, using mock data")
    #     return mock_data
    #     
    # except Exception as e:
    #     print(f"Warning: Could not fetch LungMap data: {e}")
    #     return mock_data
    
    return mock_data

def cl_id_to_iri(cl_id: str) -> str:
    """Convert CL:NNNNNNN to IRI format."""
    return f"obo:{cl_id.replace(':', '_')}"

def generate_lungmap_annotations(lungmap_data: List[Dict]) -> List[str]:
    """
    Generate OWL functional syntax annotations for LungMap links.
    
    Args:
        lungmap_data: List of cell card data with exact matches
        
    Returns:
        List of OWL functional syntax annotation axioms
    """
    annotations = []
    
    for card in lungmap_data:
        if card["match_type"] != "Exact":
            continue
            
        cl_iri = cl_id_to_iri(card["cl_id"])
        lungmap_url = f"{LUNGMAP_BASE_URL}?cell_cards_id={card['id']}"
        
        # Create the annotated annotation axiom
        # Format: AnnotationAssertion(Annotation(rdfs:label "cell name on LungMap") rdfs:seeAlso CL_ID "URL")
        annotation = (
            f'AnnotationAssertion('
            f'Annotation(rdfs:label "{card["name"]} on LungMap") '
            f'rdfs:seeAlso {cl_iri} "{lungmap_url}")'
        )
        
        annotations.append(annotation)
        
    return annotations

def read_cl_edit_file(cl_edit_path: str) -> List[str]:
    """Read the CL edit file and return lines."""
    with open(cl_edit_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_cl_edit_file(cl_edit_path: str, lines: List[str]) -> None:
    """Write the CL edit file with updated lines."""
    with open(cl_edit_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def insert_lungmap_annotations(cl_edit_path: str, annotations: List[str]) -> None:
    """
    Insert LungMap annotations into the CL edit file.
    
    Args:
        cl_edit_path: Path to cl-edit.owl file
        annotations: List of annotation axioms to insert
    """
    if not annotations:
        print("No LungMap annotations to insert.")
        return
        
    lines = read_cl_edit_file(cl_edit_path)
    
    # Find a good place to insert the annotations - after the ontology header
    # but before the class declarations
    insert_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('Declaration(Class('):
            insert_index = i
            break
    
    # Create comment header for the LungMap section
    lungmap_section = [
        "\n",
        "# ----------------------------------------\n",
        "# LungMap Cell Cards Links\n", 
        "# ----------------------------------------\n",
        "\n"
    ]
    
    # Add each annotation
    for annotation in annotations:
        lungmap_section.append(annotation + "\n")
    
    lungmap_section.append("\n")
    
    # Insert the new section
    lines[insert_index:insert_index] = lungmap_section
    
    write_cl_edit_file(cl_edit_path, lines)
    print(f"Inserted {len(annotations)} LungMap annotations into {cl_edit_path}")

def remove_existing_lungmap_annotations(cl_edit_path: str) -> None:
    """Remove any existing LungMap annotations from the CL edit file."""
    lines = read_cl_edit_file(cl_edit_path)
    
    # Filter out lines that contain LungMap references
    filtered_lines = []
    in_lungmap_section = False
    
    for line in lines:
        if "# LungMap Cell Cards Links" in line:
            in_lungmap_section = True
            continue
        elif in_lungmap_section and line.strip().startswith('#'):
            continue  # Skip section comments
        elif in_lungmap_section and line.strip() == "":
            continue  # Skip empty lines in section
        elif in_lungmap_section and 'lungmap.net' in line:
            continue  # Skip LungMap annotation lines
        elif in_lungmap_section and line.strip().startswith('Declaration') or line.strip().startswith('AnnotationAssertion') and 'lungmap.net' not in line:
            # End of LungMap section
            in_lungmap_section = False
            filtered_lines.append(line)
        else:
            filtered_lines.append(line)
    
    write_cl_edit_file(cl_edit_path, filtered_lines)

def main() -> None:
    """Main entry point for LungMap integration."""
    parser = argparse.ArgumentParser(
        description="Generate LungMap Cell Cards links for CL terms"
    )
    parser.add_argument(
        "--cl-edit-path", 
        default="cl-edit.owl",
        help="Path to cl-edit.owl file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="Show what would be added without modifying files"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing LungMap annotations before adding new ones"
    )
    
    args = parser.parse_args()
    
    # Fetch LungMap data
    print("Fetching LungMap Cell Cards data...")
    lungmap_data = fetch_lungmap_data()
    print(f"Found {len(lungmap_data)} cell cards")
    
    # Filter for exact matches only
    exact_matches = [card for card in lungmap_data if card["match_type"] == "Exact"]
    print(f"Found {len(exact_matches)} exact matches")
    
    if not exact_matches:
        print("No exact matches found. Nothing to do.")
        return
    
    # Generate annotations
    annotations = generate_lungmap_annotations(exact_matches)
    
    if args.dry_run:
        print("\nWould add the following annotations:")
        for annotation in annotations:
            print(f"  {annotation}")
        return
    
    # Clean existing annotations if requested
    if args.clean:
        print("Removing existing LungMap annotations...")
        remove_existing_lungmap_annotations(args.cl_edit_path)
    
    # Insert new annotations
    insert_lungmap_annotations(args.cl_edit_path, annotations)
    print("LungMap integration complete!")

if __name__ == "__main__":
    main()