
# ----------------------------------------
# Sync with main repo in CVS (temporary)
# ----------------------------------------

# the primary editors version
# (todo - make this live)
cl-edit.obo:
	wget http://obo.cvs.sourceforge.net/viewvc/obo/obo/ontology/anatomy/cell_type/cell.edit.obo -O $@ && perl -i ../tools/fix-obo-header.pl cl-edit.obo $@

# ----------------------------------------
# Reasoning
# ----------------------------------------
# currently this is done via the OE reasoner, in future it
# will be via an OWL reasoner and OWLTools

# first classify the ontology
%-reasoned.obo: %.obo
	obo2obo -o -saveimpliedlinks $@ $<
.PRECIOUS: %-reasoned.obo

# ----------------------------------------
# De-mireoting and filtering dangling links
# ----------------------------------------

# for the basic built, we want to get rid of all classes that are not CL classes
%-demireot.obo: %.obo
	obo-grep.pl -r '(id:\s*CL|Typedef)' $< > $@
.PRECIOUS: %-demireot.obo

# remove references to non-CL classes
# also remove all relations - add these later
%-filtered.obo: %.obo
	obo-filter-external.pl -v --idspace CL $< > $@.tmp && obo-filter-unused.pl $@.tmp | obo-grep.pl --neg -r Typedef - > $@.tmp2 && obo2obo -o $@ $@.tmp2 cl-basic-relations.obo
.PRECIOUS: %-filtered.obo

# ----------------------------------------
# Release
# ----------------------------------------

release: cl-basic.owl cl.owl

cl.obo: cl-edit-reasoned.obo
	cp $< $@
.PRECIOUS: cl.obo

cl-basic.obo: cl-edit-reasoned-demireot-filtered.obo
	cp $< $@
.PRECIOUS: cl-basic.obo

CVS_DIR = ../../../obo/ontology/anatomy/cell_type/
publish_to_cvs: release
	cp cell.obo $(CVS_DIR) && cd $(CVS_DIR) && cvs commit -m 'new release' cell.obo

# ----------------------------------------
# OBO to OWL conversion
# ----------------------------------------
%.owl: %.obo
	obolib-obo2owl $< -o $@

%-legacy-owl: %.obo
	go2owl $< > $@
