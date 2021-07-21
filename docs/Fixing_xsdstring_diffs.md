# Fixing ^^xsd:string Diffs
When you make edits, sometimes there will be large amounts of unintended differences that show up that involves the removal of ^^xsd:string. If so, you can resolve them by following normalising your cl-edit.owl file.

## SOP

1. Update your file from Master (see 'How to resolve merge conflicts' for instructions on how to do this including how to resolve clashes while doing this).

2. in the terminal, set directory to the ontology folder in CL: ```cd .../GitHub/cell-ontology/src/ontology```

3. Run the normaliser in terminal

*If you have docker installed: ```sh run.sh make normalise_xsd_string```

*If you do not have docker installed: ```make normalise_xsd_string```

*If "make" is not installed: ``` sed -i -E "s/Annotation[(](oboInOwl[:]hasDbXref [\"][^\"]*[\"])[)]/Annotation(\1^^xsd:string)/" cl-edit.owl ```

4. This should resolve your ^^xsd:string issue, after which, you can handle your pull request as per usual.
