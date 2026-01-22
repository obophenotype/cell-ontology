# Standard Operating Procedure: CellGuide Definitions Review & Integration

This document outlines the workflow for reviewing CellGuide definitions, processing them into the Cell Ontology (CL) source format, and generating the final ontology patterns.

## 1. Prerequisites

- Access to the cell-ontology GitHub repository.
- A Python virtual environment configured with necessary dependencies.
- The source Excel file containing CellGuide descriptions to be reviewed.

## 2. Curatorial Review

Before running the pipeline, the descriptions must be manually validated in the source Excel spreadsheet.

1. Open the source Excel file (e.g., `CellGuide_Validated_Descriptions.xlsx`).
2. Filter **For CL inclusion** column by blanks 
3. Review the content and add comments in the provided column **Notes (CL Ed)** if needed to document any concerns, such as:
   - Incorrect or inaccurate definitions
   - Definitions that are too broad or vague
   - Terms that may need further refinement
   - References to similar reviewed cases

The way I have assessed the defs:
- excluded descriptions that contradicts CL core definition and are wrong (ie. endothelial cell of pericentral hepatic sinusoid, cardiac muscle myoblast)
- included the descriptions of grouping terms - only  if 
1) there are no cellguide defs for child terms 
2) Includes a nice summary rather than detailed description of child terms
3) CL terms that barely include any details in their core definition 


4. **Determine Inclusion**: Use the **For CL inclusion** column to indicate if the definition should be imported:
   - `1`: Include in Cell Ontology.
   - `0`: Exclude.
   - `[Blank]`: Not reviewed or strictly for future consideration.

5. **Save the file** after completing your review session.



## 3. Data Processing Pipeline

### Step 1: File Setup & Environment

Create a new branch.

Ensure you are working within the local repository and have your environment active.

Activate your Python virtual environment:

```bash
source venv/bin/activate
```

Navigate to the source data directory within the repository:

```bash
cd src/patterns/data/source_data/CellGuide
```

Copy your reviewed Excel file into this directory.

**Note**: Ensure the filename matches what the Python script expects (CellGuide Validated Descriptions for CL Review.xlsx).

### Step 2: Generate Source TSV

Run the processing script to convert the Excel data into the TSV format required by the ontology pipeline.

Execute the processing script:

```bash
python3 src/patterns/data/source_data/CellGuide/CG_desc_proc.py
```

**Verify Output**: This process generates or updates the following TSV file. Open it to ensure the data was parsed correctly:

```
src/patterns/data/default/ExtendedDescription.tsv
```

### Step 3: Build Ontology Patterns

Once the TSV is generated, use the ontology build tools to create the OWL definition file.

Navigate to the ontology source directory `src/ontology`:

```bash
cd ../../../../ontology
# You should now be in the src/ontology directory
```

Run the build command:

```bash
./run.sh make ../patterns/definitions.owl
```

## 4. Summary of File Locations

| Component | Generic Path / Location |
|-----------|------------------------|
| Python Script | `src/patterns/data/source_data/CellGuide/CG_desc_proc.py` |
| Source Data Dir | `src/patterns/data/source_data/CellGuide/` |
| Output TSV | `src/patterns/data/default/ExtendedDescription.tsv` |
| Build Command | `src/ontology/run.sh` |
