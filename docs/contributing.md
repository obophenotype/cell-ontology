# How to contribute to CL

We welcome your contributions to CL! Generally, you can follow the editors workflow instructions [here](odk-workflows/EditorsWorkflow.md).

However, if you aren't confident in directly editing the ontology, you can contribute by writing up an issue and one of our curators/developers will pick it up and address it.

## Writing up an issue

If you want a new term added, or want edits to a current term, or spot any mistakes/issues with CL, or you have any other CL related issues, you can write up a ticket using the following steps:

1. Go to the [issues tab](https://github.com/obophenotype/cell-ontology/issues) in CL.
2. Click the 'New issue' tab on the top right corner and select the most appropriate category for your issue. (Note: blank issues can be created if none of the categories fit, but we recommend using the categories as they are designed to be more comprehensive).
3. Fill up the form as best you can, giving a descriptive title to your issue name and leaving the bracketed [] tag in the title: eg.`Add new term` is bad name, while `[NTR] larval stage X` is good name.
4. When writing up more complex issues that include multiple items or steps, make sure you include the use of `- [ ]` to denote action items. These turn into checkboxes which makes it much faster to assess which comments have been addressed. (Note: it is better to write up multiple issues than one big one with multiple items, e.g. write up one issue for each term you want added rather than an issue with all the terms you want added.)
5. If you know a specific curator/editor that you want handling your ticket, you can assign them to your ticket in the assignee tab on the right, if not, someone from our team will assign an appropriate person to handle your ticket. If, however, your ticket has not been looked at in more than 10 days, and you suspect that it might have been missed, please assign it to `gouttegd` and they will assign it appropriately.
6. If you know how to edit the ontology directly, please then proceed to making a Pull request with the guidelines below, following the editors workflow instructions [here](odk-workflows/EditorsWorkflow.md).

## Pull request guidelines

- Give your pull requests good names: `Add new terms` is bad. `Adding larval stage X term #332` is ok.
- Make sure pull requests have someone assigned to review them and remind them once in a while. Do not let them go dormant
- Assign yourself to be the Assignee
- Make sure to use `- [ ]` to denote action items in issues and pull requests, not just comments. These turn into checkboxes which makes it much faster to assess which comments have been addressed and can be ignored.
- Give a short summary of the pull request - that way we can find suitable reviewers much quicker. Say which terms you are adding or what kinds of changes you are proposing.
- It is most of the time a good idea to use `squash merge` rather than `merge` for your pull request, to keep the git history short and useful.

## Contributions that use terms from other ontologies not yet referenced in CL

(in jargon, PRs that need imports to be refreshed)

Pull requests to the Cell Ontology often include terms from other external ontologies, such as [UBERON](https://github.com/obophenotype/uberon) or the [Gene Ontology](https://github.com/geneontology/go-ontology). If these terms do not yet exist, they need to be proposed, created, and released by the external source. 

If the foreign term exists but is not yet present in the import module of CL (for example, you’re adding a logical definition that makes use of a GO term for the first time), it is necessary to make them available. This requires ''refreshing the imports'', a technical task. 
The easiest way to add the imports is by using what is called a Protége-based declaration, or a “bare IRIs” approach. Details on how to do so are available in the [OBO Training documentation](https://oboacademy.github.io/obook/howto/update-import/?h=import#protege-based-declaration). When submitting your pull request, you should label it with the tag `update-imports-required` to ask a member of the tech support group to refresh the imports before the pull request can be merged.

If you have the technical skills and/or the required computer resources (refreshing imports can be a memory-intensive task), you may refresh the imports yourself before submitting the pull request by following the [appropriate procedure](odk-workflows/UpdateImports.md). This approach is generally preferred, as it streamlines updates and reviews, but either is acceptable.

People reviewing pull requests must:
1. Make sure that if a pull request is referencing bare IRIs, the request is tagged with `update-imports-required` .
2. Make sure that imports have indeed been updated (either by the author of the pull request or by someone from the tech support group if requested) before allowing the request to be merged.

Additional details on imports are available in:
* the general CL guideline called ["Adding classes from another ontology"](https://obophenotype.github.io/cell-ontology/Adding_classes_from_another_ontology/).
* [OBO Training docs](https://oboacademy.github.io/obook/howto/update-import/) 
* the [CL-specific ODK workflow documentation](odk-workflows/UpdateImports.md).

### Why the Cell Ontology does not pull all terms by default?

If the Cell Ontology pulled all terms by default (from UBERON or the Gene Ontology, for example), that would lead to a tremendous increase in ontology size and the resources needed to run it. Thus, it is necessary to import only a subset of terms from each foreign resource. 

