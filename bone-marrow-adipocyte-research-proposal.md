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

## Literature Search - SUCCESSFUL UPDATE

### Search Method:
**artl-mcp MCP server tools** - Successfully used on second attempt!

### Search Results:
Successfully retrieved **10 highly relevant papers** on bone marrow adipocytes from Europe PMC database using `artl-mcp-search_europepmc_papers` and `artl-mcp-get_europepmc_full_text` tools.

### Key Papers Retrieved:

1. **PMID:37926488** - Wang et al. (2024)
   - Title: "Bone marrow adipocyte: Origin, biology and relationship with hematological malignancy"
   - Journal: International Journal of Laboratory Hematology
   - Type: Review article
   - Abstract summary: "BMAds is distinct from extramedullary adipose tissues and maintains a routine but dynamic accumulation throughout an individual's life... Bone marrow adipocytes (BMAds) are also contradictorily involved in normal hematopoiesis, and positively participate in the occurrence and progression of hematologic malignancies."

2. **PMID:34235494** (PMC8246640) - Attané et al. (2021)
   - Title: "A protocol for human bone marrow adipocyte isolation and purification"
   - Journal: STAR Protocols
   - Key finding: "Primary human bone marrow adipocytes (BM-Ads) display a specific metabolism that is not recapitulated by in vitro differentiated bone marrow mesenchymal stromal cells."

3. **PMID:38961077** (PMC11222446) - Xie et al. (2024)
   - Title: "PCLAF induces bone marrow adipocyte senescence and contributes to skeletal aging"
   - Journal: Bone Research
   - Abstract: "Bone marrow adipocytes (BMAds) affect bone homeostasis... The accumulated BMAds during aging impaired bone homeostasis, which increased the risks of fracture and osteoporosis."

4. **PMID:41214690** (PMC12604269) - Dong et al. (2025)
   - Title: "Targeting bone marrow adipocyte-driven fatty acid metabolism to overcome drug resistance in lung cancer bone metastasis"
   - Journal: Journal of Nanobiotechnology

5. **PMID:40170099** (PMC11959767) - Herranz et al. (2025)
   - Title: "C3G promotes bone marrow adipocyte expansion and hematopoietic regeneration after myeloablation"
   - Journal: Journal of Hematology & Oncology

6. **PMID:38904042** (PMC11188307) - Rinne et al. (2024)
   - Title: "Caloric restriction reduces trabecular bone loss during aging and improves bone marrow adipocyte endocrine function in male mice"
   - Journal: Frontiers in Endocrinology

7. **PMID:38465622** - Jia et al. (2024)
   - Title: "Dynamic evolution of bone marrow adipocyte in B cell acute lymphoblastic leukemia"
   - Journal: Cancer Biology & Therapy

8. **PMID:37957155** (PMC10643445) - Wan et al. (2023)
   - Title: "Pathological roles of bone marrow adipocyte-derived monocyte chemotactic protein-1 in type 2 diabetic mice"
   - Journal: Cell Death Discovery

9. **PMID:36506047** (PMC9727239) - Tratwal et al. (2022)
   - Title: "Raman microspectroscopy reveals unsaturation heterogeneity at the lipid droplet level and validates an in vitro model of bone marrow adipocyte subtypes"
   - Journal: Frontiers in Endocrinology

### Previous Attempt (First Session):
In the initial attempt, aurelian CLI had compatibility issues. However, using the artl-mcp MCP server tools directly (as requested by @dosumis) successfully accessed the literature.

## Literature-Based Definition for Bone Marrow Adipocyte

### Term Information:
- **Proposed Label**: bone marrow adipocyte
- **Proposed ID**: CL_99XXXXX (following NTR guidelines in idrange:81)

### Proposed Definition (Literature-Based):
"An adipocyte that is part of the bone marrow and is derived from bone marrow mesenchymal stromal cells. Bone marrow adipocytes are distinct from extramedullary adipose tissues and display a specific metabolism that is not recapitulated by in vitro differentiated bone marrow mesenchymal stromal cells. These cells accumulate dynamically throughout an individual's life, interact with hematopoietic cells, and contribute to bone marrow homeostasis, hematopoietic regulation, and skeletal health."

**Definition References:**
- PMID:37926488 (Wang et al., 2024) - Review on BMAds origin, biology and hematological relationships
- PMID:34235494 (Attané et al., 2021) - BMAds isolation protocol and metabolic distinctiveness
- PMID:38961077 (Xie et al., 2024) - BMAds role in bone homeostasis and aging

### Ontological Relationships:
- **is_a**: CL_0000136 (adipocyte)
- **part_of**: UBERON_0002371 (bone marrow)
- **develops_from**: CL_0002540 (mesenchymal stem cell of the bone marrow)
- **capable_of**: hematopoietic regulation (based on literature findings)

### Key Characteristics (Literature-Confirmed):
1. **Location-specific**: Found in bone marrow cavity, distinct from peripheral adipose depots
2. **Metabolic distinctiveness**: Display specific metabolism not recapitulated by in vitro differentiated MSCs [PMID:34235494]
3. **Dynamic accumulation**: Routine but dynamic accumulation throughout life, increasing with age [PMID:37926488]
4. **Hematopoietic interactions**: Involved in normal hematopoiesis and hematopoietic niche function [PMID:37926488, PMID:40170099]
5. **Skeletal homeostasis**: Affect bone homeostasis and bone remodeling [PMID:38961077]
6. **Developmental origin**: Derived from bone marrow mesenchymal stromal cells (BM-MSCs) [PMID:37926488]
7. **Disease associations**: Involved in hematologic malignancies, osteoporosis, and metabolic disorders [PMID:37926488, PMID:38961077, PMID:37957155]
8. **Functional heterogeneity**: Evidence for bone marrow adipocyte subtypes with different properties [PMID:36506047]

## Summary of Literature Findings

### Evidence for Bone Marrow Adipocyte as Distinct Cell Type:

1. **Metabolic Distinctiveness**: Primary bone marrow adipocytes have unique metabolism not replicated by in vitro differentiated MSCs [PMID:34235494]

2. **Functional Roles**:
   - Hematopoietic regulation and regeneration [PMID:40170099]
   - Bone homeostasis and skeletal aging [PMID:38961077]
   - Metabolic disease involvement [PMID:37957155]
   - Cancer microenvironment interactions [PMID:41214690]

3. **Cellular Heterogeneity**: Evidence for constitutive and regulated bone marrow adipocyte subtypes [PMID:36506047]

4. **Age-Related Changes**: Dynamic accumulation during aging with impacts on fracture risk and osteoporosis [PMID:38961077, PMID:37926488]

### Comparison with Existing Adipocyte Terms:

- Unlike **white adipocytes (CL_0000448)**: Found in subcutaneous/visceral depots
- Unlike **brown adipocytes (CL_0000449)**: Thermogenic function
- Unlike **beige adipocytes (CL_0001070)**: Inducible thermogenic function
- Parallel to **subcutaneous adipocyte (CL_0002521)**: Location-specific adipocyte subtype

Bone marrow adipocytes represent a functionally distinct, location-specific adipocyte population with unique roles in hematopoiesis and skeletal biology.

## Next Steps for Ontology Implementation

To add this term to the Cell Ontology, the following steps are recommended:

1. **Assign term ID**: Use next available ID in CL_99xxxxx range (idrange:81)
2. **Add core metadata**:
   - Label: "bone marrow adipocyte"
   - Definition with PMIDs: [PMID:37926488, PMID:34235494, PMID:38961077]
   - Exact synonyms: "BMAd", "bone marrow adipose cell"
   - Related synonyms: "marrow adipocyte"
3. **Add relationships**:
   - SubClassOf: CL_0000136 (adipocyte)
   - part_of: UBERON_0002371 (bone marrow)
   - develops_from: CL_0002540 (mesenchymal stem cell of the bone marrow)
4. **Add provenance**:
   - terms:date with timestamp
   - terms:contributor with ORCID (if provided)
   - oboInOwl:hasDbXref links to key PMIDs
5. **Link to issue**: Add term_tracker_item annotation

## Conclusion

**Literature search using artl-mcp tools was SUCCESSFUL.** Retrieved 10+ relevant papers from Europe PMC providing comprehensive evidence for bone marrow adipocytes as a distinct cell type.

### Key Findings:
- Bone marrow adipocytes are metabolically distinct from other adipocyte types
- They play crucial roles in hematopoiesis, bone homeostasis, and aging
- Multiple high-quality references support their unique characteristics
- Clear evidence distinguishes them from peripheral adipose tissues

### Proposed Definition Ready for Review:
The literature-based definition includes proper PMID references and can be implemented in the ontology following the standard CL term addition workflow.

**Status: RESEARCH COMPLETE WITH LITERATURE SUPPORT - NO ONTOLOGY EDITS MADE (as requested)**
