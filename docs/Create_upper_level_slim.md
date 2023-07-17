
# SOP for adding a new slim:
## Intro

An upper slim is a set of terms for summarising annotations.  CL has both a general slim and domain-specific slims allowing for the generation of general summaries or for domain specific ones.  All slims have a context that covers all cells in the domain of interest. In order to fullfil the summarising use-case, a slim should have good % coverage of the domain and, if possible, avoid excluding major cell types.  The following are potentially a problem for the grouping use-case:

* Classes in the slim with very small numbers of subclasses: Having 0-1 subclass => no capacity to summarise.
* Classes with disproportionately large numbers of subclasses.
* Overlapping classes - these clash with some types of summary - e.g. pie charts.

Potential clashing concerns: It seems reasonable to want to make sure that very important cell types are covered and are not obscured in generating summaries, but this desire can clash with the considerations above. Some judgement is needed to balance these concerns.

There is no perfect solution, but some solutions are better (at fulfilling the use case) than others.

## Name and definition

It is important that the name of the slim accurately reflects the content it covers. Specifically, if the intention is to cover all cell types that are specific for an organ, the slim's name should be in the format of "organ_upper_slim". This ensures clarity and helps users understand the scope of the slim.

Furthermore, the description of the slim should follow a consistent pattern. It is recommended to use the following structure: "a subset of general classes related to specific cell types in the [organ or specific context]". This format provides a concise and informative description of the slim, helping users identify its purpose and content.

## What files to create and edit


### 1. Preparing the subset:
- Create XXX_upper_slim in Protege (change "XXX" to the subset label). [See *Adding a new Subset*](https://oboacademy.github.io/obook/howto/add-new-slim/).
- Create a CSV table with the following characteristics (Find examples in [src/templates](https://github.com/obophenotype/cell-ontology/tree/master/src/templates)):
  - 3 columns

ID | subset | label
--| --- | ---
ID | AI oboInOwl:inSubset| 
CL:####### | 	http://purl.obolibrary.org/obo/cl#XXX_upper_slim | CL term
... | 	http://purl.obolibrary.org/obo/cl#XXX_upper_slim | ...

   - Save csv file with name XXX_upper_slim.csv in src/templates

- Modify src/ontology/cl-odk.yaml introducing new lines for the new slim:
   - ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/bf8af4ca-80b0-4dd0-ab11-d9ce1afa2939)
   - ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/f26e7ae5-c2b4-4509-828f-7d5a49c2874e)

### 2. Generating the slim owl file:
- Open the src/ontology file in the terminal with Docker opened.
- Run the command: `sh run.sh make update_repo`.

### 3. Modifying the Catalog:
- Open the src/ontology/catalog-v001.xml file.
- Add the following line: `<uri name="http://purl.obolibrary.org/obo/cl/components/XXX_upper_slim.owl" uri="components/XXX_upper_slim.owl"/>` (change "XXX" to the subset label).
   - ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/9fed5519-aca2-4a87-999f-8ac44b361f37)


### 4. Importing the Upper Level Slim in CL:
- Open src/ontology/cl-edit.owl.
- Add the following import statement: `Import(<http://purl.obolibrary.org/obo/cl/components/XXX_upper_slim.owl>)`. (change "XXX" to the subset label).
   - ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/b0da114e-4df6-4fee-93f3-2733fea4b4cf)


### 5. Updating the slim owl file:
- Run the command: `sh run.sh make all_subsets`.
   - Alternatively, run the command: `sh run.sh make components/XXX_upper_slim.owl -B` (to run it anyway even if it says it is up to date) (change "XXX" to the subset label).

### 6. Testing Slim Coverage:
- Open src/ontology/cl.Makefile.
- Add the subset label to SLIM_TEMPLATES (without _upper_slim!!!).
    
    ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/874da667-bfb6-4f46-abc0-fdd798553d48)
- Add the term that will be used to test coverage
     
     ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/c7ec5b9f-3deb-43f4-a68e-b07c1eff4fbe)
   - Add:

   ```
   $(REPORTDIR)/XXX_upper_slim.csv: $(TEMPLATEDIR)/XXX_upper_slim.csv
	$(eval TERM_ID := $(YYY))
	$(COVERAGECMD)
   ```
   (substitute "XXX" to the subset label and YYY for the tested label)


     ![image](https://github.com/aleixpuigb/Protocols/assets/94959119/96619a7f-0c81-40b2-ada7-2829703b500c)
- Using the terminal, navigate to src/ontology.
- Run the command: `sh run.sh make slim_coverage`.


### Understanding reports 

The reports can be accessed at src/ontology/reports/XXX_upper_slim.csv. First, the coverage percentage is displayed, indicating the proportion of cells covered. Secondly, the number of cells covered by each term of the subset is provided. Finally, a list is presented, indicating all the terms that were expected to be covered but are not currently included.

Ideally, terms would have more than 1 cell covered, but not too many, as that might indicate the term is too general. Furthermore, a term covering hundreds of cells might indicate that it is too general, and a more specific term (or multiple) should be evaluated, specially if it overlaps with other terms of the subset. Example: For the eye_upper_slim, 'retinal cell' is a (too) general term that overlaps other grouping terms such as 'retinal bipolar neuron', 'retina horizontal cell' or 'amacrine cell'.

In the case that there is overlapping of terms (term A in the subset covers term B of the subset), a coverage file will be created and it can be accessed at src/ontology/reports/overlapping_terms_XXX_upper_slim.csv.