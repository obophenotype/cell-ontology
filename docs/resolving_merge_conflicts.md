## A guide to resolving merge conflicts

When you come to merge your pull request, you may find that conflicts prevent automated merging back into the master.  In some cases, GitHub supports resolution of these through its web interface. However, probably due to file size, this is not currently supported for cl-edit.owl.

The majority of the time, the conflict is trivial - due to addition of new terms to the same point in the file. Because terms are ordered in the file by ID, this happens whenever two edits add terms without any intervening IDs. Trivial clashes are easy to spot - they involve whole term stanzas + declarations.  

Occassionally non-trivial clashes will happen when two pull requests include edits to the same term or even the same axiom. Ask an editor for help if you don't feel confident resolving these.  

### SOP.

1. Reserialise the Master file using the Ontology Development Kit (ODK). This requires setting up Docker and ODK. If not already set up, follow [the instructions here](https://oboacademy.github.io/obook/howto/odk-setup/).

2. Open Docker.

3. At the line command (PC) or Terminal (Mac), use the cd (change directory) command to navigate to the repository's src/ontology/ directory.
 For example,

 '''
 cd PATH_TO_ONTOLOGY/src/ontology/
 '''

 Replace "PATH_TO_ONTOLOGY" with the actual file path to the ontology. If you need to orient yourself, use the '''pwd''' (present working directory) or '''ls''' (list) line commands.

 3. If you are resolving a conflict in an .owl file, run:

 '''
sh run.sh make normalize_src
 '''

 If you are resolving a conflict in an .obo file, run:

 '''
sh run.sh make normalize_obo_src
 '''

4. In CL, edits sometimes result in creating a large amount of uninteded differences involving ^^xsd:string. If you see these differences after running the command above, they can be resolved by following [the instructions here](https://obophenotype.github.io/cell-ontology/Fixing_xsdstring_diffs/).

5. Resolving conflicts in GitHub Desktop and VSCode:
   
  > 1) **Update Branches in GitHub Desktop:**
   >
   >    * **Checkout Master** and pull to make sure your Master branch is up to date.
   >    * **Checkout the branch** for the pull request and make sure it is up to date.
   >    * Choose `Branch > Update from Master` to integrate the latest changes from the master branch.
   >     
   >      ![Update from Master](https://user-images.githubusercontent.com/112839/112127621-89af9f00-8bbd-11eb-8613-f3a2b8166085.png)
   >    
   >    * GitHub Desktop will detect the clash and suggest opening it in your text editor of choice (e.g., Atom, VSCode).
   > 
   > 2) **Resolve Conflicts in VSCode:**
   >
   >    * Open the conflicting file in VSCode.
   >    * VSCode will highlight the conflicting areas with markers:
   >      
   >      <img width="603" alt="image" src="https://github.com/user-attachments/assets/345a9671-f3bf-4d69-a534-2995b19a09ab">
   >      
   >    * For trivial ordering problems, either manually delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) and ensure all necessary declarations are retained, or click on **Accept Both Changes**. This will automatically merge all term declarations from both the HEAD and incoming changes, removing the conflict markers.
   >    * **Important** - Always check that the change does look trivial before making any changes.
   >
   > 3) **Reserialise OWL Files:**
   >
   >    * It is essential to reserialise after resolving conflicts to ensure consistency and proper formatting:
   >
   >      ```
   >      sh run.sh make normalize_src
   >      ```
   >
   > 4) **Complete the Resolution Process:**
   >
   >    * In GitHub Desktop, review the changes, commit the resolved conflict, and push the updates back to GitHub.
   >    * Check the resulting diffs on the Pull Request on GitHub.
   >    * Once the checks have run and are successful, merge and delete the branch.
