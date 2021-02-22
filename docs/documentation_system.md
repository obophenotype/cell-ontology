# Documentation System

The intended audience for this page is the maintainers of CL.

The CL documentation system is mkdocs. The documentation is maintained
in the `docs/` folder in the CL repo.

They are deployed using github pages here: https://obophenotype.github.io/cell-ontology/

In the future, changes made here will automatically deploy to github pages once we set up github actions

For now it is necessary to manually deploy. This currently requires the command line.

First set up a virtual environment:

```bash
. environment.sh
```

Then install mkdocs:

```bash
pip install -r requirements.txt
```

The above steps should only need doing once

once mkdocs is installed, do this:

```bash
mkdocs gh-deploy
```

Changes will automatically deploy to:

https://obophenotype.github.io/cell-ontology/
