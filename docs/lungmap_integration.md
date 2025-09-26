# LungMap Cell Cards Integration

This document describes the integration between the Cell Ontology (CL) and LungMap Cell Cards.

## Overview

The LungMap Cell Cards (https://www.lungmap.net/research/cell-cards/) provide detailed information about lung cell types. Many of these cell cards have been mapped to CL terms with "Exact" matches. For each exact match, we add an `rdfs:seeAlso` annotation to the CL term that links to the corresponding LungMap cell card.

## Enhanced Discovery Features

The integration now includes automated discovery of lung-related CL terms and potential matches:

- **47 lung-related CL terms** automatically extracted from the ontology
- **Potential match identification** for common lung cell types
- **Browsing guide generation** for manual verification of additional matches

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

- `make lungmap_preview` - Show exact and potential matches
- `make lungmap_links` - Add LungMap annotations to the ontology
- `make lungmap_guide` - Generate a manual browsing guide for finding more matches

## Discovery Process

The enhanced script now:

1. **Extracts lung-related terms**: Automatically finds CL terms with lung-related labels
2. **Identifies candidates**: Suggests potential matches for common lung cell types
3. **Provides browsing guide**: Generates instructions for manual verification
4. **Shows potential matches**: Lists terms that likely have LungMap equivalents

### Example Discovery Output

```bash
$ make lungmap_preview
Found 47 lung-related CL terms
Found 1 exact matches
Found 2 potential matches

Potential matches (need verification on LungMap):
  CL:0002063 (pulmonary alveolar type 2 cell) -> alveolar type 2 cell
  CL:1001567 (lung endothelial cell) -> lung endothelial cell
```

## Data Source Strategy

1. **Known exact matches**: Currently includes CL:0002062 → LMCC0000000003
2. **Automated discovery**: Extracts lung-related CL terms from the ontology
3. **Potential matches**: Identifies likely candidates for manual verification
4. **Future expansion**: Ready for direct API access when LungMap provides it

## Manual Verification Process

To expand the integration:

1. Run `make lungmap_guide` to get a browsing guide
2. Visit https://www.lungmap.net/research/cell-cards/
3. Search for potential matches from the candidate list
4. Record any "Cell Ontology Match Type: Exact" entries
5. Update the script with new exact matches

## Maintenance

When new LungMap cell cards are created or existing mappings change:
1. Update the exact matches in `build_lungmap_links.py`
2. Run `make lungmap_links` to refresh the annotations
3. Commit the changes to the ontology

## Technical Details

- **47 lung-related CL terms** automatically discovered
- Only "Exact" matches are included as `rdfs:seeAlso` annotations
- Potential matches are flagged for manual verification
- Existing LungMap annotations are cleaned and replaced when the script runs
- The script validates CL term IDs and formats URLs consistently
- The integration preserves the functional syntax format of the CL edit file

## Candidate Terms for Verification

The script automatically identifies high-priority lung cell types including:
- Alveolar cells (type 1, type 2, macrophages)
- Pneumocytes and club cells
- Lung endothelial and epithelial cells
- Bronchial and tracheal cell types
- Lung fibroblasts and other stromal cells