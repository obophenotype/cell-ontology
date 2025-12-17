# Bone Marrow Adipocyte - Literature Search and Definition Proposal

## Research Task
This document contains findings from literature search for bone marrow adipocyte and proposes a referenced definition for potential inclusion in the Cell Ontology.

## Current Status
**Note:** This is a research proposal only. No ontology edits have been made per issue instructions.

## Background from Cell Ontology

### Existing Related Terms:
1. **CL_0000136 (adipocyte)**: "A fat-storing cell found mostly in the abdominal cavity and subcutaneous tissue of mammals. Fat is usually stored in the form of triglycerides." [MESH:D017667]

2. **CL_0000448 (white adipocyte)**: Subclass of adipocyte, part of white adipose tissue (UBERON_0001347)

3. **CL_0000449 (brown adipocyte)**: "A cell from the thermogenic form of adipose tissue found in many species, particularly in newborns and hibernating mammals, but also in lesser amounts in adults of other mammals including humans. Brown fat is capable of rapid liberation of energy and seems to important in the maintenance of body temperature immediately after birth and upon waking from hibernation." [MESH:D002001]

4. **CL_0001070 (beige adipocyte)**: Another adipocyte subtype

5. **CL_0002521 (subcutaneous adipocyte)**: Adipocyte of subcutaneous tissue

6. Bone marrow-related terms:
   - CL_0002092 (bone marrow cell)
   - CL_0002540 (mesenchymal stem cell of the bone marrow)
   - CL_0010001 (stromal cell of bone marrow)

## Literature Search Attempts

### Methods Tried:
1. **aurelian/artl-mcp tool**: 
   - Successfully installed aurelian package (v0.4.2)
   - Encountered runtime error: pydantic-ai version compatibility issue
   - Error: `pydantic_ai.exceptions.UserError: Unknown keyword arguments: result_type`
   
2. **PubMed access (browser)**:
   - Status: ERR_BLOCKED_BY_CLIENT
   - Unable to access pubmed.ncbi.nlm.nih.gov
   
3. **Google Scholar (browser)**:
   - Status: ERR_BLOCKED_BY_CLIENT
   - Unable to access scholar.google.com
   
4. **Semantic Scholar API (curl)**:
   - Status: DNS resolution failed
   - Unable to resolve api.semanticscholar.org
   
5. **Europe PMC API (curl)**:
   - Status: DNS resolution failed
   - Unable to resolve www.ebi.ac.uk
   
6. **Wikipedia (browser and Python library)**:
   - Browser: ERR_BLOCKED_BY_CLIENT
   - Python library: DNS resolution failed for en.wikipedia.org

### Network Environment Limitations:
The sandboxed environment has significant network restrictions with DNS resolution failures and blocked client connections. Direct literature access was not possible through any tested method.

### Approach Taken:
Given the constraints, this proposal synthesizes information from:
- Existing Cell Ontology structure and definitions
- Standard cell biology knowledge of bone marrow adipocytes
- Patterns observed in related adipocyte term definitions

## Proposed Definition for Bone Marrow Adipocyte

### Term Information:
- **Proposed Label**: bone marrow adipocyte
- **Proposed ID**: CL_99XXXXX (following NTR guidelines in idrange:81)

### Proposed Definition:
"An adipocyte located in the bone marrow cavity that is derived from bone marrow mesenchymal stromal cells. Bone marrow adipocytes form a distinct adipocyte subtype characterized by their unique microenvironment within the bone marrow, where they interact with hematopoietic cells and contribute to bone marrow homeostasis and hematopoietic regulation."

### Ontological Relationships:
- **is_a**: CL_0000136 (adipocyte)
- **part_of**: UBERON_0002371 (bone marrow) [suggested, need to verify UBERON term]
- **develops_from**: CL_0002540 (mesenchymal stem cell of the bone marrow) [potential relationship]

### Key Characteristics (to be verified with literature):
1. Location-specific: Found in bone marrow cavity
2. Distinct from white and brown adipocytes in metabolic properties
3. Role in hematopoietic niche regulation
4. Derived from bone marrow mesenchymal stromal cells (BM-MSCs)
5. Unique marker expression profile compared to peripheral adipocytes

### Suggested References to Obtain:
Key research areas to explore for definitive references:
1. **Bone marrow adipose tissue (BMAT) characterization studies**
2. **Marrow adipocyte origin and differentiation** (e.g., studies on MSC differentiation)
3. **Functional roles in hematopoiesis** (interaction with hematopoietic stem cells)
4. **Metabolic characteristics** distinguishing marrow adipocytes from peripheral fat
5. **Clinical relevance** (obesity, aging, osteoporosis)

### Recommended PMIDs to Search:
Based on typical key papers in this field (these need to be verified):
- Studies on bone marrow adipose tissue (BMAT)
- Scheller et al. papers on marrow adipocytes
- Craft et al. on adipocyte progenitors in bone marrow
- Studies differentiating constitutive vs regulated marrow adipocytes

## Next Steps

To complete this definition properly, the following actions are recommended:

1. **Access primary literature** using functional aurelian/artl-mcp or direct PubMed access
2. **Identify 2-3 key review papers** on bone marrow adipocytes
3. **Extract specific PMIDs** for definition references
4. **Verify anatomical location** term (UBERON ID for bone marrow)
5. **Confirm developmental origin** relationships
6. **Add species-specific information** if relevant
7. **Review recent single-cell studies** that may have characterized bone marrow adipocytes at molecular level

## Conclusion

This proposal provides a framework for a bone marrow adipocyte definition based on the structure of existing adipocyte terms in CL. However, **proper literature references are essential** before adding this term to the ontology. The definition should be refined based on recent primary literature, particularly review articles that synthesize the field's understanding of this cell type.

**Status: RESEARCH PROPOSAL ONLY - NO ONTOLOGY EDITS MADE**
