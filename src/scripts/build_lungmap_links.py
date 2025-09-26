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

def extract_lung_related_cl_terms(cl_edit_path: str) -> List[Dict]:
    """
    Extract lung-related CL terms from the ontology file.
    
    Args:
        cl_edit_path: Path to cl-edit.owl file
        
    Returns:
        List of dictionaries with cl_id, cl_label for lung-related terms
    """
    lung_terms = []
    
    with open(cl_edit_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all label assertions for lung-related terms
    import re
    label_pattern = r'AnnotationAssertion\(rdfs:label (obo:CL_\d+) "([^"]*(?:lung|pulmonary|alveolar|bronchial|pneumocyte)[^"]*)"\)'
    
    matches = re.findall(label_pattern, content, re.IGNORECASE)
    
    for cl_iri, label in matches:
        cl_id = cl_iri.replace('obo:CL_', 'CL:')
        lung_terms.append({
            'cl_id': cl_id,
            'cl_label': label,
            'cl_iri': cl_iri
        })
    
    return lung_terms

def discover_potential_lungmap_matches(lung_terms: List[Dict]) -> List[Dict]:
    """
    Create potential LungMap matches based on lung-related CL terms.
    
    Since we can't access LungMap directly, this creates a framework for
    potential matches that could be validated when access becomes available.
    
    Args:
        lung_terms: List of lung-related CL terms
        
    Returns:
        List of potential cell card matches (currently hypothetical)
    """
    # Start with the known exact match
    known_matches = [
        {
            "id": "LMCC0000000003",
            "name": "alveolar type 1 epithelial cell",
            "cl_id": "CL:0002062",
            "cl_label": "pulmonary alveolar type 1 cell",
            "match_type": "Exact"
        }
    ]
    
    # Add potential matches based on common lung cell types
    # These are hypothetical LungMap IDs that would need to be verified
    potential_matches = []
    
    for term in lung_terms:
        # Skip the known match
        if term['cl_id'] == 'CL:0002062':
            continue
            
        # Create hypothetical matches for common lung cell types
        # In reality, these would be discovered by browsing LungMap
        if 'alveolar type 2' in term['cl_label'].lower() or 'type ii pneumocyte' in term['cl_label'].lower():
            potential_matches.append({
                "id": f"LMCC_HYPOTHETICAL_AT2",  # Would need to find actual ID
                "name": term['cl_label'].replace('pulmonary ', ''),
                "cl_id": term['cl_id'],
                "cl_label": term['cl_label'],
                "match_type": "Potential"  # Mark as potential until verified
            })
        elif 'club cell' in term['cl_label'].lower():
            potential_matches.append({
                "id": f"LMCC_HYPOTHETICAL_CLUB",
                "name": term['cl_label'],
                "cl_id": term['cl_id'],
                "cl_label": term['cl_label'],
                "match_type": "Potential"
            })
        elif 'lung endothelial' in term['cl_label'].lower():
            potential_matches.append({
                "id": f"LMCC_HYPOTHETICAL_ENDO",
                "name": term['cl_label'],
                "cl_id": term['cl_id'],
                "cl_label": term['cl_label'],
                "match_type": "Potential"
            })
    
    return known_matches + potential_matches

def create_lungmap_browsing_guide(lung_terms: List[Dict]) -> str:
    """
    Create a guide for manually browsing LungMap to find more matches.
    
    Args:
        lung_terms: List of lung-related CL terms
        
    Returns:
        String with browsing instructions
    """
    guide = """
# LungMap Browsing Guide

To find more CL term matches in LungMap Cell Cards:

1. Visit https://www.lungmap.net/research/cell-cards/
2. Browse through the cell cards or use search functionality
3. For each cell card, check if it has a "Cell Ontology" section
4. Look for "Cell Ontology Match Type: Exact" entries
5. Record the mapping between:
   - LungMap Cell Card ID (e.g., LMCC0000000003)
   - Cell name in LungMap
   - CL term ID (e.g., CL:0002062)

## Candidate CL terms to look for:
"""
    
    # Add the most likely candidates
    priority_terms = []
    for term in lung_terms:
        label_lower = term['cl_label'].lower()
        if any(keyword in label_lower for keyword in [
            'alveolar', 'pneumocyte', 'club cell', 'endothelial',
            'fibroblast', 'macrophage', 'epithelial', 'goblet'
        ]):
            priority_terms.append(term)
    
    for term in sorted(priority_terms, key=lambda x: x['cl_label']):
        guide += f"- {term['cl_id']}: {term['cl_label']}\n"
    
    guide += f"""
## All {len(lung_terms)} lung-related CL terms:
"""
    
    for term in sorted(lung_terms, key=lambda x: x['cl_label']):
        guide += f"- {term['cl_id']}: {term['cl_label']}\n"
    
    return guide

def browse_lungmap_for_matches(lung_terms: List[Dict]) -> List[Dict]:
    """
    Browse LungMap website to find additional cell card matches.
    
    This function would implement web scraping or API calls to discover
    more LungMap cell cards that match CL terms.
    
    Args:
        lung_terms: List of lung-related CL terms to search for
        
    Returns:
        List of discovered cell card matches
    """
    # TODO: When LungMap access becomes available, implement:
    # 
    # import requests
    # from bs4 import BeautifulSoup
    # 
    # discovered_matches = []
    # base_url = "https://www.lungmap.net/research/cell-cards/"
    # 
    # try:
    #     # Get the main cell cards page
    #     response = requests.get(base_url, timeout=30)
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     
    #     # Find all cell card links
    #     card_links = soup.find_all('a', href=re.compile(r'cell_cards_id='))
    #     
    #     for link in card_links:
    #         card_url = link.get('href')
    #         if not card_url.startswith('http'):
    #             card_url = "https://www.lungmap.net" + card_url
    #             
    #         # Visit each cell card page
    #         card_response = requests.get(card_url, timeout=30)
    #         card_soup = BeautifulSoup(card_response.content, 'html.parser')
    #         
    #         # Look for Cell Ontology section
    #         ontology_section = card_soup.find(text=re.compile(r'Cell Ontology'))
    #         if ontology_section:
    #             # Extract CL term and match type
    #             cl_link = card_soup.find('a', href=re.compile(r'CL_\d+'))
    #             if cl_link:
    #                 cl_id_match = re.search(r'CL_(\d+)', cl_link.get('href'))
    #                 if cl_id_match:
    #                     cl_id = f"CL:{cl_id_match.group(1)}"
    #                     
    #                     # Check if it's an exact match
    #                     exact_match = card_soup.find(text=re.compile(r'Match Type.*Exact'))
    #                     if exact_match:
    #                         # Extract cell card ID from URL
    #                         card_id_match = re.search(r'cell_cards_id=([^&]+)', card_url)
    #                         if card_id_match:
    #                             card_id = card_id_match.group(1)
    #                             
    #                             # Find the cell name
    #                             cell_name = card_soup.find('h1') or card_soup.find('title')
    #                             cell_name_text = cell_name.get_text().strip() if cell_name else ""
    #                             
    #                             # Find corresponding CL term
    #                             matching_term = next((t for t in lung_terms if t['cl_id'] == cl_id), None)
    #                             if matching_term:
    #                                 discovered_matches.append({
    #                                     "id": card_id,
    #                                     "name": cell_name_text,
    #                                     "cl_id": cl_id,
    #                                     "cl_label": matching_term['cl_label'],
    #                                     "match_type": "Exact"
    #                                 })
    #     
    #     return discovered_matches
    #     
    # except Exception as e:
    #     print(f"Error browsing LungMap: {e}")
    #     return []
    
    print("Warning: Cannot access LungMap website directly due to network restrictions.")
    print("Using discovery based on known CL lung terms instead.")
    print("\nTo manually discover more matches, use --browsing-guide option.")
    
    # For now, return the potential matches we can discover
    return discover_potential_lungmap_matches(lung_terms)

def fetch_lungmap_data(cl_edit_path: str = None) -> List[Dict]:
    """
    Fetch LungMap Cell Cards data by browsing the website or using known mappings.
    
    Args:
        cl_edit_path: Path to cl-edit.owl file for extracting lung terms
        
    Returns:
        List of cell card dictionaries containing id, name, cl_id, cl_label, match_type
    """
    if cl_edit_path and os.path.exists(cl_edit_path):
        # Extract lung-related CL terms from the ontology
        lung_terms = extract_lung_related_cl_terms(cl_edit_path)
        print(f"Found {len(lung_terms)} lung-related CL terms")
        
        # Try to discover more matches by browsing LungMap
        try:
            return browse_lungmap_for_matches(lung_terms)
        except Exception as e:
            print(f"Warning: Could not browse LungMap: {e}")
    
    # Fallback to known data
    return [
        {
            "id": "LMCC0000000003",
            "name": "alveolar type 1 epithelial cell",
            "cl_id": "CL:0002062",
            "cl_label": "pulmonary alveolar type 1 cell",
            "match_type": "Exact"
        }
    ]

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
        "--show-potential",
        action="store_true",
        help="Also show potential matches that need verification"
    )
    parser.add_argument(
        "--browsing-guide",
        action="store_true",
        help="Generate a guide for manually browsing LungMap to find more matches"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing LungMap annotations before adding new ones"
    )
    
    args = parser.parse_args()
    
    # Fetch LungMap data
    print("Fetching LungMap Cell Cards data...")
    lungmap_data = fetch_lungmap_data(args.cl_edit_path)
    print(f"Found {len(lungmap_data)} cell cards")
    
    # If browsing guide requested, generate and show it
    if args.browsing_guide:
        if os.path.exists(args.cl_edit_path):
            lung_terms = extract_lung_related_cl_terms(args.cl_edit_path)
            guide = create_lungmap_browsing_guide(lung_terms)
            print(guide)
        return
    
    # Filter for exact matches only
    exact_matches = [card for card in lungmap_data if card["match_type"] == "Exact"]
    potential_matches = [card for card in lungmap_data if card["match_type"] == "Potential"]
    
    print(f"Found {len(exact_matches)} exact matches")
    if potential_matches:
        print(f"Found {len(potential_matches)} potential matches")
        
    # Show potential matches if requested
    if args.show_potential and potential_matches:
        print("\nPotential matches (need verification on LungMap):")
        for card in potential_matches:
            print(f"  {card['cl_id']} ({card['cl_label']}) -> {card['name']}")
        print("\nTo use these, verify the matches on LungMap and update the script with actual cell card IDs.")
    
    if not exact_matches:
        if potential_matches and not args.show_potential:
            print("No exact matches found. Use --show-potential to see potential matches.")
        else:
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