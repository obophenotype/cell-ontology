# Update Imports Workflow

This page details the import workflows mostly used by CL editors. 

There are several different ways of importing terms, though, and the details of the different approaches not covered here (such as the "Base Module approach") are available at the general [OBO Training Update Imports Workflow with ODK](https://oboacademy.github.io/obook/howto/update-import/). 

There are some also notes available on the current practice of imports in CL at ["Adding classes from another ontology"](https://obophenotype.github.io/cell-ontology/Adding_classes_from_another_ontology/).

## Importing a new term

Importing a new term is split into two sub-phases:

1. Declaring the terms to be imported (always done by the author of the PR)
2. Refreshing imports dynamically (may be done by the author or _post-hoc_ by the tech team )

### Declaring terms to be imported
There are three ways to declare terms that are to be imported from an external ontology

1. Protégé-based declaration
2. Using term files
3. Using the custom import template (described only in the [OBO general docs](https://oboacademy.github.io/obook/howto/update-import/))

#### Protégé-based declaration

This workflow is the simplest, but will require an update by the tech team. 

1. Open your ontology (edit file) in Protégé (5.5+).
1. Select 'owl:Thing'
1. Add a new class as usual.
1. Paste the _full iri_ in the 'Name:' field, for example, http://purl.obolibrary.org/obo/CHEBI_50906.
1. Click 'OK'

<img src="https://raw.githubusercontent.com/INCATools/ontology-development-kit/master/docs/img/AddingClasses.png" alt="Adding Classes" />

Now you can use this term for example to construct logical definitions. The next time the imports are refreshed (see how to refresh [here](#refresh-imports)), the metadata (labels, definitions, etc.) for this term are imported from the respective external source ontology and becomes visible in your ontology.

Make sure that if a pull request is using Protégé-based declarations and using bare IRIs, the request is tagged with `update-imports-required`.


#### Using term files

The Cell Ontology has several term files associated with each ontology it imports, which can be found in the imports directory ([`cell-ontology/src/ontology/imports/`](https://github.com/obophenotype/cell-ontology/tree/master/src/ontology/imports)). 

For example, you may add a Gene Ontology term to the end of the list at `src/ontology/imports/go_terms.txt`, for example:

```
GO:0008150
GO:0008151
GO:0004990
GO:0070278
```

Now you can run the [refresh imports workflow](#refresh-imports)) and the new terms will be imported.


### Refresh imports

If you want to refresh the import yourself, and you have the ODK installed, you can do the following (using GO as an example):

First, you navigate in your terminal to the ontology directory. 

```
cd src/ontology
```

Then, you regenerate the import that will now include any new terms you have added. Note: You must have [docker installed](SettingUpDockerForODK.md).

```
sh run.sh make PAT=false imports/go_import.owl -B
```

Since ODK 1.2.27, it is also possible to simply run the following, which is the same as the above:

```
sh run.sh make refresh-go
```

Note that in case you changed the defaults, you need to add `IMP=true` and/or `MIR=true` to the command below:

```
sh run.sh make IMP=true MIR=true PAT=false imports/go_import.owl -B
```

If you wish to skip refreshing the mirror, i.e. skip downloading the latest version of the source ontology for your import (e.g. `go.owl` for your go import) you can set `MIR=false` instead, which will do the exact same thing as the above, but is easier to remember:

```
sh run.sh make IMP=true MIR=false PAT=false imports/go_import.owl -B
```
