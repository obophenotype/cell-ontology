# How to contribute to CL

We welcome your contributions to CL! Generally, you can follow the editors workflow instructions [here](odk-workflows/EditorsWorklow.md).

However, if you aren't confident in directly editing the ontology, you can contribute by writing up an issue and one of our curators/developers will pick it up and address it.

## Writing up an issue

If you want a new term added, or want edits to a current term, or spot any mistakes/issues with CL, or you have any other CL related issues, you can write up a ticket using the following steps:

1. Go to the [issues tab](https://github.com/obophenotype/cell-ontology/issues) in CL.
2. Click the 'New issue' tab on the top right corner and select the most appropriate category for your issue. (Note: blank issues can be created if none of the categories fit, but we recommend using the categories as they are designed to be more comprehensive).
3. Fill up the form as best you can, giving a descriptive title to your issue name and leaving the bracketed [] tag in the title: eg.`Add new term` is bad name, while `[NTR] larval stage X` is good name.
4. When writing up more complex issues that include multiple items or steps, make sure you include the use of `- [ ]` to denote action items. These turn into checkboxes which makes it much faster to assess which comments have been addressed. (Note: it is better to write up multiple issues than one big one with multiple items, e.g. write up one issue for each term you want added rather than an issue with all the terms you want added.)
5. If you know a specific curator/editor that you want handling your ticket, you can assign them to your ticket in the assignee tab on the right, if not, someone from our team will assign an appropriate person to handle your ticket. If, however, your ticket has not been looked at in more than 10 days, and you suspect that it might have been missed, please assign it to `gouttegd` and they will assign it appropriately.
6. If you know how to edit the ontology directly, please then proceed to making a Pull request with the guidelines below, following the editors workflow instructions [here](odk-workflows/EditorsWorklow.md).

## Pull request guidelines

- Give your pull requests good names: `Add new terms` is bad. `Adding larval stage X term #332` is ok.
- Make sure pull requests have someone assigned to review them and remind them once in a while. Do not let them go dormant
- Assign yourself to be the Assignee
- Make sure to use `- [ ]` to denote action items in issues and pull requests, not just comments. These turn into checkboxes which makes it much faster to assess which comments have been addressed and can be ignored.
- Give a short summary of the pull request - that way we can find suitable reviewers much quicker. Say which terms you are adding or what kinds of changes you are proposing.
- It is most of the time a good idea to use `squash merge` rather than `merge` for your pull request, to keep the git history short and useful.

## Pull requests that require imports to be refreshed

If your pull request references foreign terms from an external ontology that are not yet present in the import module for that ontology (for example, you’re adding a logical definition that makes use of a GO term for the first time), imports needs to be refreshed for the foreign terms to be available to use.

If you have the technical skills and/or the required computer resources (refreshing imports can be a memory-intensive task), you may refresh the imports yourself before submitting the pull request, by following the [appropriate procedure](odk-workflows/UpdateImports.md).

If you can’t apply the imports refreshing procedure for any reason, you may instead opt for using “bare IRIs” when editing the ontology, everywhere you need a reference to a foreign term. Then, when submitting your pull request, label it with the tag `update-imports-required` to ask that a member of the tech support group refresh the imports before the pull request can be merged.

People reviewing pull requests must 1) make sure that if a pull request is referencing bare IRIs, the request is tagged with `update-imports-required` (adding the label themselves if needed); and 2) make sure that imports have indeed been updated (either by the author of the pull request, or by someone from the tech support group if requested) before allowing the request to be merged.
