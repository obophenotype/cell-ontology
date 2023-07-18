
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
- Create a CSV table with the following characteristics (Find examples in `src/templates`):
  - 3 columns

ID | subset | label
--| --- | ---
ID | AI oboInOwl:inSubset| 
CL:####### | 	http://purl.obolibrary.org/obo/cl#XXX_upper_slim | CL term
... | 	http://purl.obolibrary.org/obo/cl#XXX_upper_slim | ...

   - Save the CSV file with the name 'XXX_upper_slim.csv' in the `src/templates` directory.

- Modify `src/ontology/cl-odk.yaml` introducing new lines for the new slim (change "XXX" to the subset label):

	```
  	- id: XXX_upper_slim
 	```

     ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/4673253e-9526-43b4-8608-8d7e7b27d988)

   ```
    - filename: XXX_upper_slim.owl
      use_template: True
      templates:
        - XXX_upper_slim.csv
   ```

    ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/254ad25f-7bf2-4ac2-afe2-9ad067d9c1ea)

### 2. Generating the Slim OWL file:
- Navigate to the `src/ontology` file in the terminal. Make sure Docker is running.
- Run the command:

  ```
  sh run.sh make update_repo
  ```

### 3. Modifying the Catalog:
- Open the `src/ontology/catalog-v001.xml` file.
- Add the following line (change "XXX" to the subset label):

  ```
  <uri name="http://purl.obolibrary.org/obo/cl/components/XXX_upper_slim.owl" uri="components/XXX_upper_slim.owl"/>`
  ```
   - ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/429a8098-9748-4e3b-a5a1-c3e178d6cb6c)



### 4. Preparing the Upper Level Slim import to CL:
- Open `src/ontology/cl-edit.owl`.
- Add the following import statement (change "XXX" to the subset label):

    ```
    Import(<http://purl.obolibrary.org/obo/cl/components/XXX_upper_slim.owl>)
    ```
    ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/0b467b48-ad94-46e9-80a1-bc473de769e8)


### 5. Updating the slim owl file:
- Run the command:

    ```
    sh run.sh make all_subsets
    ```
   - Alternatively, run the following command to run it anyway even if it says it is up to date (change "XXX" to the subset label):

     ```
     sh run.sh make components/XXX_upper_slim.owl -B
     ```

### 6. Testing Slim Coverage:
- Open `src/ontology/cl.Makefile`.
- Add the subset label to SLIM_TEMPLATES (without _upper_slim!!!).
    
    ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/18960b0b-098c-42cf-95b1-ab1f1978a8bc)

- Add the term that will be used to test coverage
     
     ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/24a0c221-da18-4754-9a45-e6b65b6cec35)

   - Add:

   ```
   $(REPORTDIR)/XXX_upper_slim.csv: $(TEMPLATEDIR)/XXX_upper_slim.csv
	$(eval TERM_ID := $(YYY))
	$(COVERAGECMD)
   ```
   (substitute "XXX" to the subset label and YYY for the tested label)


     ![image](https://github.com/obophenotype/cell-ontology/assets/94959119/7eb18255-0ef7-4fbc-9f7f-e582372165bf)

- Using the terminal, navigate to `src/ontology`.
- Run the command:

    ```
    sh run.sh make slim_coverage
    ```


## Understanding reports 

The reports can be accessed at `src/ontology/reports/XXX_upper_slim.csv`. First, the coverage percentage is displayed, indicating the proportion of cells covered. Secondly, the number of cells covered by each term of the subset is provided. Finally, a list is presented, indicating all the terms that were expected to be covered but are not currently included.

Ideally, terms would have more than 1 cell covered. Furthermore, a term covering hundreds of cells might indicate that it is too general, and a more specific term (or multiple) should be evaluated, specially if it overlaps with other terms of the subset. Example: For the eye_upper_slim, 'retinal cell' is a (too) general term that overlaps other grouping terms such as 'retinal bipolar neuron', 'retina horizontal cell' or 'amacrine cell'.

In the case that there is overlapping of terms (term A in the subset covers term B of the subset), a coverage file will be created and it can be accessed at `src/ontology/reports/overlapping_terms_XXX_upper_slim.csv`.
