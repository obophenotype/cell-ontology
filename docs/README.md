# EFO Agent System - Overview

This directory contains the specifications for three specialized agents that work together to manage the Experimental Factor Ontology (EFO).

## Agent Architecture v1.1

### Three-Agent System with Workflow Orchestration

```
                    ┌─────────────────┐
                    │  User Request   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────────┐
                    │copilot-instructions │ ◄─── Workflow Orchestrator
                    │  (Decision Logic)   │      & Decision Maker
                    └────┬───────┬────────┘
                         │       │
         ┌───────────────┼───────┼──────────────┐
         │               │       │              │
    ┌────▼─────┐  ┌────-─▼─-─┐ ┌─▼──────────┐   │
    │   EFO-   │  │   EFO-   │ │    EFO-    │   │
    │ontologist│  │ curator  │ │  importer  │   │
    │(Editor)  │  │(Research)│ │  (Import)  │   │
    └──────────┘  └────────-─┘ └────────────┘   │
         │               │            │         │
         └───────────────┴────────────┴─────────┘
                         │
                    Shared Context
```

**Key Changes in v1.1**:
- Workflow orchestration moved to `copilot-instructions.md`
- Decision logic (ontology placement, agent routing) centralized
- Agents are now narrow specialists with clear boundaries
- No agent-to-agent orchestration - all coordinated by instructions

## The Agents

### 1. EFO-ontologist (Specialist Editor) v1.1
**File**: `.github/agents/EFO-ontologist.md`

**Role**: OWL/XML editing specialist
- Handles all direct manipulation of `efo-edit.owl`
- Adds new terms (with pre-validated information)
- Edits existing terms
- Obsoletes terms following proper workflow
- Manages logical definitions and relationships
- Maintains ontology consistency

**What it does NOT do**:
- Literature research (→ EFO-curator)
- External term imports (→ EFO-importer)
- Workflow orchestration (→ copilot-instructions)
- Architectural decisions (→ copilot-instructions)

**When to invoke**: 
- Add/edit/obsolete terms in efo-edit.owl
- Fix OWL/XML syntax issues
- Update relationships or metadata

**Prerequisites**:
- New terms need pre-validated information
- External terms must be pre-imported

**Key capabilities**:
- OWL/XML formatting
- Term integration
- Logical definitions
- Relationship management
- Git workflow

### 2. EFO-curator (Research Specialist)
**File**: `.github/agents/EFO-curator.md`

**Role**: Literature research and validation
- Deep literature searches using artl-mcp
- Validates term components (label, definition, xrefs, parent)
- Generates comprehensive validation reports
- Provides evidence-based recommendations
- Domain-specific expertise

**When to invoke**:
- New term needs research/validation
- Definition requires literature support
- Parent term relationship unclear
- Ontology placement needs research

**Key capabilities**:
- Europe PMC full-text search
- Citation validation
- Evidence gathering
- Domain expertise
- Structured reporting

### 3. EFO-importer (Import Specialist)
**File**: `.github/agents/EFO-importer.md`

**Role**: External ontology term importer
- Searches OLS for terms in external ontologies
- Bidirectional verification of term identity
- Adds IRIs to dependency files
- Updates mirrors and regenerates imports

**When to invoke**:
- Parent term exists in external ontology
- Need to import related terms
- Cross-ontology relationships needed

**Key capabilities**:
- OLS search
- IRI validation
- Dependency file management
- Import generation

## Workflow Orchestration

**Location**: `.github/copilot-instructions.md`

The copilot instructions file now handles:
- Initial request triage
- Ontology placement decisions (EFO vs MONDO vs OBA vs CL, etc.)
- Agent invocation routing
- Workflow sequencing
- Quality assurance checks

**Decision patterns**:
- Standard diseases → MONDO import
- General measurements → OBA consideration
- Experimental assays → EFO
- Cell types → CL import
- Anatomical entities → UBERON import

## Handoff Protocol

**File**: `HANDOFF-PROTOCOL.md`

Defines:
- Communication patterns between agents
- Request/response formats
- Multi-agent workflows
- Error handling
- State tracking

**Key patterns**:
1. **New term (needs research)**: copilot-instructions → Curator → Ontologist
2. **New term (pre-validated)**: copilot-instructions → Ontologist
3. **Import needed**: copilot-instructions → Importer → Ontologist
4. **External ontology**: Curator → User (no integration)
5. **Simple edit**: Ontologist only

## Quick Start

### For New Term Requests

For basic requests, describe what you need:

```markdown
Please add a new term:
- Label: [term name]
- Definition: [if you have one]
- Parent: [if you know it]
- References: [if you have any]
```

The workflow will:
1. Assess what you've provided (copilot-instructions)
2. Call @EFO-curator to fill gaps or validate
3. Call @EFO-importer if external terms needed
4. Call @EFO-ontologist to integrate into EFO
5. Create a PR for review

Or invoke agents directly:

```markdown
@EFO-curator please research [term name]
@EFO-importer please import [term name] from MONDO
@EFO-ontologist please add this validated term to efo-edit.owl
```

### For Editing Existing Terms

```markdown
Please edit [term name] (EFO:XXXXXXX):
- [Describe the change needed]
```

Or directly:
```markdown
@EFO-ontologist edit EFO:XXXXXXX to update the definition
```

### For Obsoleting Terms

```markdown
Please obsolete [term name] (EFO:XXXXXXX)
Replacement: [term name] (EFO:YYYYYYY)
Reason: [why obsoleting]
```

Or directly:
```markdown
@EFO-ontologist obsolete EFO:XXXXXXX, replaced by EFO:YYYYYYY
```

## Agent Capabilities Matrix

| Capability | Ontologist | Curator | Importer |
|-----------|-----------|---------|----------|
| Literature search | ❌ | ✅ | ❌ |
| OWL/XML editing | ✅ | ❌ | ❌ |
| OLS search | Limited | Limited | ✅ |
| Definition validation | ❌ | ✅ | ❌ |
| Parent term import | ❌ | ❌ | ✅ |
| Ontology placement advisory | ❌ | ✅ | ❌ |
| Git workflow | ✅ | ❌ | ❌ |
| Term integration | ✅ | ❌ | ❌ |
| Workflow orchestration | ❌ | ❌ | ❌ |

**Note**: Workflow orchestration and architectural decisions now handled by `copilot-instructions.md`

## Tools Used

### artl-mcp (Literature Research)
Used by: **Curator**
- `search_europepmc_papers`: Find papers by keywords
- `get_europepmc_paper_by_id`: Get metadata for specific papers
- `get_all_identifiers_from_europepmc`: Get PMIDs, DOIs, PMCIDs
- `get_europepmc_full_text`: Get full text as Markdown
- `get_europepmc_pdf_as_markdown`: Convert PDF to Markdown

### ols4-mcp (Ontology Lookup)
Used by: **All agents**
- `mcp_ols4_search`: Search all ontologies
- `mcp_ols4_searchClasses`: Search specific ontology
- `mcp_ols4_fetch`: Get term details
- `mcp_ols4_getAncestors`: Get term hierarchy
- `mcp_ols4_getDescendants`: Get child terms

### Standard Tools
- `grep_search`, `file_search`: Find terms in files
- `read_file`, `replace_string_in_file`: Edit ontology
- `run_in_terminal`: Execute make commands
- `manage_todo_list`: Track multi-step workflows

## Workflow Examples

### Example 1: Minimal Information
```
User: "Add term: ATAC-seq"
    ↓
copilot-instructions: Triage → Call curator for research
    ↓
Curator: Research literature → Generate report
    ↓ 
copilot-instructions: Decide parent needs import → Call importer
    ↓
Importer: Import parent from OBI
    ↓
copilot-instructions: Call ontologist to integrate
    ↓
Ontologist: Add to efo-edit.owl → Create PR
```

### Example 2: Complete Information
```
User: "Add cardiac measurement with definition, PMID, parent"
    ↓
copilot-instructions: Triage → Call curator to verify
    ↓
Curator: Verify citations → Validate parent → Confirm EFO placement
    ↓
copilot-instructions: Call ontologist to integrate
    ↓
Ontologist: Add term → Create PR
```

### Example 3: Should Be External
```
User: "Add general disease term"
    ↓
copilot-instructions: Triage → Call curator for research
    ↓
Curator: Research → Recommend MONDO (not EFO)
    ↓
copilot-instructions: Acknowledge → Inform user (no integration)
    ↓
User: Submit to MONDO with curator's report
```

## Decision Trees

### Should I create one agent or two?

**Two agents is better because**:
✅ Separation of concerns (research vs integration)
✅ Curator can be called for external submissions too
✅ Different expertise required (literature vs OWL/XML)
✅ Easier to maintain and improve each
✅ Clear handoff points

### Which agent do I call?

```
Are you a user? → @EFO-ontologist
Are you the ontologist needing validation? → @EFO-curator  
Are you the ontologist needing imports? → @EFO-importer
Are you the curator? → Response to @EFO-ontologist
Are you the importer? → Response to @EFO-ontologist
```

## File Structure

```
.github/agents/
├── EFO-ontologist.md      ← Main orchestrator agent
├── EFO-curator.md         ← Research & validation agent
├── EFO-importer.md        ← Import specialist agent (existing)
└── HANDOFF-PROTOCOL.md    ← Communication protocols
```

## Maintenance

### Updating Agent Specifications

When updating an agent:
1. Edit the relevant agent's `.md` file
2. Update `HANDOFF-PROTOCOL.md` if communication patterns change
3. Update this README if capabilities change
4. Test the workflow with a sample issue

### Adding New Capabilities

When adding new tools or workflows:
1. Determine which agent should handle it
2. Update that agent's specification
3. Update handoff protocol if involves multiple agents
4. Add to capabilities matrix in this README

### Common Issues

**Agent not finding terms**:
- Check OLS is accessible
- Verify term exists in expected ontology
- Try alternative search terms

**Literature search returns nothing**:
- Try broader search terms
- Search for related concepts
- Check alternative spellings/synonyms

**Import fails**:
- Verify term exists in source ontology
- Check IRI format
- Ensure mirrors are up to date

## Best Practices

### For Users
- Provide as much information as you have
- Include relevant PMIDs or papers if known
- Mention domain context (disease, measurement, etc.)
- Reference related existing terms if applicable

### For Agent Development
- Keep agents focused on their core competency
- Use structured communication formats
- Always validate before integrating
- Document decisions in commit messages and PRs
- Use TODO lists for multi-step workflows

### For Ontology Curation
- Always require literature support
- Verify parent relationships make sense
- Check for existing terms before creating new ones
- Consider external ontologies for general concepts
- Maintain consistency with existing patterns

## Testing the System

To test the agent system:

1. **Simple test**: "Add synonym 'XYZ' to term ABC"
   - Should: Ontologist only

2. **Medium test**: "Add new term: [label only]"
   - Should: Ontologist → Curator → (maybe Importer) → Ontologist

3. **Complex test**: "Add new measurement with is_about relationship"
   - Should: All three agents, full validation, logical definition

4. **Edge test**: "Add general anatomical term"
   - Should: Ontologist → Curator → Recommend UBERON

## Support

For questions about:
- **Agent behavior**: See individual agent `.md` files
- **Communication**: See `HANDOFF-PROTOCOL.md`
- **Ontology editing**: See main `copilot-instructions.md`
- **Import process**: See `docs/Import_terms_from_another_ontology.md`

## Version History

- **v1.0** (2025-01-06): Initial three-agent system
  - EFO-ontologist (orchestrator)
  - EFO-curator (researcher)
  - EFO-importer (existing, connector)
  - Handoff protocol established
