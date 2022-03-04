## A guide to resolving merge conflicts

When you come to merge your pull request, you may find that conflicts prevent automated merging back into the master.  In some cases, GitHub supports resolution of these through its web interface. However, probably due to file size, this is not currently supported for cl-edit.owl.

The majority of the time, the conflict is trivial - due to addition of new terms to the same point in the file. Because terms are ordered in the file by ID, this happens whenever two edits add terms without any intervening IDs. Trivial clashes are easy to spot - they involve whole term stanzas + declarations.  

Occassionally non-trivial clashes will happen when two pull requests include edits to the same term or even the same axiom. Ask an editor for help if you don't feel confident resolving these.  

### SOP.

1. Reserialise the Master file using ROBOT. This will fix any odd orderings that may have been introduced during previous merges.
    ```sh
    sh ./run.sh ROBOT convert --input cl-edit.owl -f ofn --output cl-edit.owl
   ```
4. In GitHub Desktop:

   * Checkout Master and pull to make sure your Master is up to date.
   * Checkout the branch for the pull request & make sure it is up to date.
   * Choose Branch > Update from master: ![image](https://user-images.githubusercontent.com/112839/112127621-89af9f00-8bbd-11eb-8613-f3a2b8166085.png)

   * GitHub desktop should detect the clash and ask you if you want to open in your text editor of choice (Atom is a good choice)
   * If clashes are due to trivial ordering problems, delete conflict marks, commit and push back to GitHub.
   * Check the resulting diffs on the Pull Request on GitHub
   * Once tests have run, if successful you can merge and delete the branch.
  
  
