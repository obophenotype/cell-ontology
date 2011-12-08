
# PR mireots CHEBI, but is not always in sync, which causes problems for Oort (e.g. different defs in two version).
# only use core PR info
# (todo: make thispart of Oort)
extsubset/pr-core.obo: extsubset/pr.obo
	obo-grep.pl  -r 'id: PR:' $< > $@
extsubset/pr.obo:
	wget http://purl.obolibrary.org/obo/pr.obo -O $@

oort:
	ontology-release-runner --allow-overwrite --outdir . --repair-cardinality --reasoner elk --asserted --simple --re-mireot cl-edit.obo http://purl.obolibrary.org/obo/uberon/basic.owl http://purl.obolibrary.org/obo/go.owl http://purl.obolibrary.org/obo/pato.owl extsubset/chebi_lite.obo extsubset/pr-core.obo
#	ontology-release-runner --outdir releases --reasoner elk --asserted --simple --re-mireot --allow-overwrite --prefix http://purl.obolibrary.org/obo/CL_ --prefix http://purl.obolibrary.org/obo/CP_ cl-edit.obo http://purl.obolibrary.org/obo/uberon/basic.owl pr-core.obo http://purl.obolibrary.org/obo/go.owl http://purl.obolibrary.org/obo/pato.owl chebi_lite.obo


# ----------------------------------------
# OBO to OWL conversion
# ----------------------------------------
# DEPRECATED - done as part of Oort now
%.owl: %.obo
	obolib-obo2owl $< -o $@

# ----------------------------------------
# Legacy copy to cvs
# ----------------------------------------

CVS_DIR = ../../../obo/ontology/anatomy/cell_type/
publish_to_cvs: release
	cp cell.obo $(CVS_DIR) && cd $(CVS_DIR) && cvs commit -m 'new release' cell.obo

# ----------------------------------------
# Sync with main repo in CVS (temporary)
# ----------------------------------------

# the primary editors version
# (todo - make this live)
cl-edit.obo:
	wget http://obo.cvs.sourceforge.net/viewvc/obo/obo/ontology/anatomy/cell_type/cell.edit.obo -O $@ && perl -i ../tools/fix-obo-header.pl cl-edit.obo $@
#	cp cell.edit.obo $@
