# LungMap Cell Cards Integration

This document describes the integration between the Cell Ontology (CL) and LungMap Cell Cards.

## Overview

The LungMap Cell Cards (https://www.lungmap.net/research/cell-cards/) provide detailed information about lung cell types. Many of these cell cards have been mapped to CL terms with "Exact" matches. For each exact match, we add an `rdfs:seeAlso` annotation to the CL term that links to the corresponding LungMap cell card.

## Annotation Format

The annotations follow this format:
```
AnnotationAssertion(
  Annotation(rdfs:label "cell name on LungMap") 
  rdfs:seeAlso 
  obo:CL_NNNNNNN 
  "https://www.lungmap.net/research/cell-cards/?cell_cards_id=LMCC..."
)
```

Where:
- `CL_NNNNNNN` is the CL term ID (in OBO IRI format)
- The annotation on the annotation provides the cell name as used in LungMap
- The URL points to the specific LungMap cell card

## Example

For CL:0002062 (pulmonary alveolar type 1 cell), the annotation is:
```
AnnotationAssertion(
  Annotation(rdfs:label "alveolar type 1 epithelial cell on LungMap") 
  rdfs:seeAlso 
  obo:CL_0002062 
  "https://www.lungmap.net/research/cell-cards/?cell_cards_id=LMCC0000000003"
)
```

## Build Integration

The LungMap integration is handled by the `build_lungmap_links.py` script and integrated into the Makefile:

- `make lungmap_preview` - Show what annotations would be added
- `make lungmap_links` - Add LungMap annotations to the ontology

## Data Source

Currently, the script uses mock data based on the known example. In the future, this should be replaced with:
1. Direct API access to LungMap (if available)
2. Scraping of the LungMap website 
3. Manual curation of a mapping file

## Maintenance

When new LungMap cell cards are created or existing mappings change:
1. Update the data source in `build_lungmap_links.py`
2. Run `make lungmap_links` to refresh the annotations
3. Commit the changes to the ontology

## Technical Details

- Only "Exact" matches are included as `rdfs:seeAlso` annotations
- Existing LungMap annotations are cleaned and replaced when the script runs
- The script validates CL term IDs and formats URLs consistently
- The integration preserves the functional syntax format of the CL edit file