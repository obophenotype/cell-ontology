# Update Imports Workflow

This page discusses how to update the contents of your imports, like adding or removing terms. If you are looking to customise imports, like changing the module type, see [here](RepoManagement.md).

## Importing a new term

Importing a new term is split into to sub-phases:

1. Declaring the terms to be imported
2. Refreshing imports dynamically

### Declaring terms to be imported
There are three ways to declare terms that are to be imported from an external ontology. Choose the appropriate one for your particular scenario (all three can be used in parallel if need be):

1. Protege-based declaration
2. Using term files
3. Using the custom import template

#### Protege-based declaration

This workflow is to be avoided, but may be appropriate if the editor _does not have access to the ODK docker container_.

1. Open your ontology (edit file) in Protege (5.5+).
1. Select 'owl:Thing'
1. Add a new class as usual.
1. Paste the _full iri_ in the 'Name:' field, for example, http://purl.obolibrary.org/obo/CHEBI_50906.
1. Click 'OK'

<img src="https://raw.githubusercontent.com/INCATools/ontology-development-kit/master/docs/img/AddingClasses.png" alt="Adding Classes" />

Now you can use this term for example to construct logical definitions. The next time the imports are refreshed (see how to refresh [here](#Refresh-imports)), the metadata (labels, definitions, etc) for this term are imported from the respective external source ontology and becomes visible in your ontology.


#### Using term files

Every import has, by default a term file associated with it, which can be found in the imports directory. For example, if you have a GO import in `src/ontology/go_import.owl`, you will also have an associated term file `src/ontology/go_terms.txt`. You can add terms in there simply as a list:

```
GO:0008150
GO:0008151
```

Now you can run the [refresh imports workflow](#Refresh-imports)) and the two terms will be imported.

#### Using the custom import template 

This workflow is appropriate if:

1. You prefer to manage all your imported terms in a single file (rather than multiple files like in the "Using term files" workflow above).
2. You wish to augment your imported ontologies with additional information. This requires a cautionary discussion.

To enable this workflow, you add the following to your ODK config file (`src/ontology/cl-odk.yaml`), and [update the repository](RepoManagement.md):

```
use_custom_import_module: TRUE
```

Now you can manage your imported terms directly in the custom external terms template, which is located at `src/templates/external_import.owl`. Note that this file is a [ROBOT template](http://robot.obolibrary.org/template), and can, in principle, be extended to include any axioms you like. Before extending the template, however, read the following carefully.

The main purpose of the custom import template is to enable the management off all terms to be imported in a centralised place. To enable that, you do not have to do anything other than maintaining the template. So if you, say current import `APOLLO_SV:00000480`, and you wish to import `APOLLO_SV:00000532`, you simply add a row like this:

```
ID	Entity Type
ID	TYPE
APOLLO_SV:00000480	owl:Class
APOLLO_SV:00000532	owl:Class
```

When the imports are refreshed [see imports refresh workflow](#Refresh-imports), the term(s) will simply be imported from the configured ontologies.

Now, if you wish to extent the Makefile (which is beyond these instructions) and add, say, synonyms to the imported terms, you can do that, but you need to (a) preserve the `ID` and `ENTITY` columns and (b) ensure that the ROBOT template is valid otherwise, [see here](http://robot.obolibrary.org/template).

_WARNING_. Note that doing this is a _widespread antipattern_ (see related [issue](https://github.com/OBOFoundry/OBOFoundry.github.io/issues/1443)). You should not change the axioms of terms that do not belong into your ontology unless necessary - such changes should always be pushed into the ontology where they belong. However, since people are doing it, whether the OBO Foundry likes it or not, at least using the _custom imports module_ as described here localises the changes to a single simple template and ensures that none of the annotations added this way are merged into the [base file](https://github.com/INCATools/ontology-development-kit/blob/master/docs/ReleaseArtefacts.md#release-artefact-1-base-required).  

### Refresh imports

If you want to refresh the import yourself (this may be necessary to pass the travis tests), and you have the ODK installed, you can do the following (using go as an example):

First, you navigate in your terminal to the ontology directory (underneath src in your hpo root directory). 
```
cd src/ontology
```

Then, you regenerate the import that will now include any new terms you have added.

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
