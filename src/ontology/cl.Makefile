## Customize Makefile settings for cl
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile
# railing-whitespace  xref-syntax

non_native_classes.txt: $(SRC)
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/non-native-classes.sparql $@.tmp &&\
	cat $@.tmp | sort | uniq >  $@
	rm -f $@.tmp

# TODO add back: 		remove --term-file non_native_classes.txt \

#####################################################################################
### Run ontology-release-runner instead of ROBOT as long as ROBOT is broken.      ###
#####################################################################################

# The reason command (and the reduce command) removed some of the very crucial asserted axioms at this point.
# That is why we first need to extract all logical axioms (i.e. subsumptions) and merge them back in after
# The reasoning step is completed. This will be a big problem when we switch to ROBOT completely..

tmp/cl_terms.txt: $(SRC)
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/cl_terms.sparql $@

tmp/asserted-subclass-of-axioms.obo: $(SRC) tmp/cl_terms.txt
	$(ROBOT) merge --input $< \
		filter --term-file tmp/cl_terms.txt --axioms "logical" --preserve-structure false \
		convert --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && mv $@.tmp.obo $@

# All this terrible OBO file hacking is necessary to make sure downstream tools can actually compile something resembling valid OBO (oort!).
#http://purl.obolibrary.org/obo/UBERON_0004370 EquivalentTo basement membrane needs fixing
# Removing drains CARO relationship is a necessary hack because of an OBO bug that turns universals
# into existentials on roundtrip

tmp/source-merged.obo: $(SRC) tmp/asserted-subclass-of-axioms.obo config/remove_annotations.txt
	$(ROBOT) merge --input $(SRC) \
		reason --reasoner ELK \
		relax \
		remove --axioms equivalent \
		merge -i tmp/asserted-subclass-of-axioms.obo \
		remove -T config/remove_annotations.txt --axioms annotation \
		query --update ../sparql/remove-op-definitions.ru \
		convert --check false -f obo $(OBO_FORMAT_OPTIONS) -o tmp/source-merged.owl.obo &&\
		grep -v ^owl-axioms tmp/source-merged.owl.obo > tmp/source-stripped2.obo &&\
		grep -v '^def[:][ ]["]x[ ]only[ ]in[ ]taxon' tmp/source-stripped2.obo > tmp/source-stripped3.obo &&\
		grep -v '^relationship[:][ ]drains[ ]CARO' tmp/source-stripped3.obo > tmp/source-stripped.obo &&\
		cat tmp/source-stripped.obo | perl -0777 -e '$$_ = <>; s/name[:].*\nname[:]/name:/g; print' | perl -0777 -e '$$_ = <>; s/range[:].*\nrange[:]/range:/g; print' | perl -0777 -e '$$_ = <>; s/domain[:].*\ndomain[:]/domain:/g; print' | perl -0777 -e '$$_ = <>; s/comment[:].*\ncomment[:]/comment:/g; print' | perl -0777 -e '$$_ = <>; s/created_by[:].*\ncreated_by[:]/created_by:/g; print' | perl -0777 -e '$$_ = <>; s/def[:].*\ndef[:]/def:/g; print' > $@ &&\
		rm tmp/source-merged.owl.obo tmp/source-stripped.obo tmp/source-stripped2.obo tmp/source-stripped3.obo

oort: tmp/source-merged.obo
	ontology-release-runner --reasoner elk tmp/source-merged.obo --no-subsets --skip-ontology-checks --allow-equivalent-pairs --simple --relaxed --asserted --allow-overwrite --outdir oort

# With the new OWLAPI 4.5.26, which allows arbitrary annotation properties in the OBO parser and oort using a previous OWLAPI version, 
# we are having conflicts when converting it. Also, the oort step is not used in any release artefact.
#test: oort

tmp/$(ONT)-stripped.owl: oort
	$(ROBOT) filter --input oort/$(ONT)-simple.owl --term-file tmp/cl_terms.txt --trim false \
		convert -o $@

# cl_signature.txt should contain all CL terms and all properties (and subsets) used by the ontology.
# It serves like a proper signature, but including annotation properties
tmp/cl_signature.txt: tmp/$(ONT)-stripped.owl tmp/cl_terms.txt
	$(ROBOT) query -f csv -i $< --query ../sparql/object-properties.sparql $@_prop.tmp &&\
	cat tmp/cl_terms.txt $@_prop.tmp | sort | uniq > $@ &&\
	rm $@_prop.tmp

# The standard simple artefacts keeps a bunch of irrelevant Typedefs which are a result of the merge. The following steps takes the result
# of the oort simple version, and then removes them. A second problem is that oort does not deal well with cycles and removes some of the
# asserted CL subsumptions. This can hopefully be solved once we can move all the way to ROBOT, but for now, it requires merging in
# the asserted hierarchy and reducing again.


# Note that right now, TypeDefs that are CL native (like has_age) are included in the release!


##############################################
##### CL Template pipeline ###################
##############################################

TEMPLATESDIR=../templates
DEPENDENCY_TEMPLATE=dependencies.tsv
TEMPLATES=$(filter-out $(DEPENDENCY_TEMPLATE), $(notdir $(wildcard $(TEMPLATESDIR)/*.tsv)))
TEMPLATES_OWL=$(patsubst %.tsv, $(TEMPLATESDIR)/%.owl, $(TEMPLATES))
TEMPLATES_TSV=$(patsubst %.tsv, $(TEMPLATESDIR)/%.tsv, $(TEMPLATES))

p:
	echo $(TEMPLATES)
	echo $(TEMPLATES_TSV)
	echo $(TEMPLATES_OWL)

templates: prepare_templates $(TEMPLATES_OWL)

remove_template_classes_from_edit.txt: $(TEMPLATES_TSV)
	for f in $^; do \
			cut -f1 $${f} >> tmp.txt; \
			cat tmp.txt | grep 'CL:' | sort | uniq > $@; \
	done \
	rm tmp.txt

remove_template_classes_from_edit: remove_template_classes_from_edit.txt $(SRC)
	$(ROBOT) remove -i $(SRC) -T $< --preserve-structure false -o $(SRC).ofn && mv $(SRC).ofn $(SRC)

prepare_templates: ../templates/config.txt
	sh ../scripts/download_templates.sh $<

#components/all_templates.owl: $(TEMPLATES_OWL)
#	$(ROBOT) merge $(patsubst %, -i %, $^) \
#		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ \
#		--output $@.tmp.owl && mv $@.tmp.owl $@

$(TEMPLATESDIR)/dependencies.owl: $(TEMPLATESDIR)/dependencies.tsv
	$(ROBOT) merge -i $(SRC) template --template $< --prefix "CP: http://purl.obolibrary.org/obo/CP_" --output $@ && \
	$(ROBOT) annotate --input $@ --ontology-iri $(ONTBASE)/components/$*.owl -o $@

$(TEMPLATESDIR)/%.owl: $(TEMPLATESDIR)/%.tsv $(SRC) $(TEMPLATESDIR)/dependencies.owl
	$(ROBOT) merge -i $(SRC) -i $(TEMPLATESDIR)/dependencies.owl template --template $< --output $@ && \
	$(ROBOT) annotate --input $@ --ontology-iri $(ONTBASE)/components/$*.owl -o $@

CL_EDIT_GITHUB_MASTER=https://raw.githubusercontent.com/obophenotype/cell-ontology/master/src/ontology/cl-edit.owl

tmp/src-noimports.owl: $(SRC)
	$(ROBOT) remove -i $< --select imports -o $@

tmp/src-imports.owl: $(SRC)
	$(ROBOT) merge -i $< -o $@

tmp/src-master-noimports.owl:
	$(ROBOT) remove -I $(CL_EDIT_GITHUB_MASTER) --select imports -o $@

tmp/src-master-imports.owl:
	$(ROBOT) merge -I $(CL_EDIT_GITHUB_MASTER) -o $@

reports/diff_edit_%.md: tmp/src-master-%.owl tmp/src-%.owl
	$(ROBOT) diff --left tmp/src-master-$*.owl --right tmp/src-$*.owl -f markdown -o $@

reports/diff_edit_%.txt: tmp/src-master-%.owl tmp/src-%.owl
	$(ROBOT) diff --left tmp/src-master-$*.owl --right tmp/src-$*.owl -o $@

branch_diffs: reports/diff_edit_imports.md reports/diff_edit_noimports.md reports/diff_edit_imports.txt reports/diff_edit_noimports.txt

tmp/cl-current.owl: $(ONT).owl
	$(ROBOT) remove -i $< --term rdfs:label --select complement --select annotation-properties \
		remove --base-iri $(URIBASE)/CL_ --axioms external -o $@

tmp/cl-lastbuild.owl: .FORCE
	$(ROBOT) remove -I $(URIBASE)/$(ONT).owl --term rdfs:label --select complement --select annotation-properties \
		remove --base-iri $(URIBASE)/CL_ --axioms external -o $@

reports/obo-diff.txt: tmp/cl-lastbuild.owl tmp/cl-current.owl
	$(ROBOT) diff --left $< --right tmp/cl-current.owl -f markdown -o $@
	#perl ../scripts/obo-simple-diff.pl $^ > $@.tmp && mv $@.tmp $@

all_reports: reports/obo-diff.txt


normalise_xsd_string: $(SRC)
	sed -i.bak -E "s/Annotation[(](oboInOwl[:]hasDbXref [\"][^\"]*[\"])[)]/Annotation(\1^^xsd:string)/g" $<
	rm $<.bak

rm-altid:
	$(ROBOT) query -i cl-edit.owl --format ttl --query ../sparql/rm-obsolete-alt-id.ru tmp/cl-updated.ttl
	$(ROBOT) unmerge -i cl-edit.owl -i tmp/cl-updated.ttl convert -f ofn -o cl-edit.owl

merge-constructed:
	$(ROBOT) merge -i $(SRC) -i tmp/cl-construct-replaced-by.ttl --collapse-import-closure false convert -f ofn -o $(SRC)

construct-replaced-by:
	$(ROBOT) query -i cl-edit.owl --format ttl --query ../sparql/construct-replaced-by.sparql tmp/cl-construct-replaced-by.ttl

ALL_PATTERNS=$(patsubst ../patterns/dosdp-patterns/%.yaml,%,$(wildcard ../patterns/dosdp-patterns/[a-z]*.yaml))
DOSDPT=dosdp-tools

tmp/edit-merged.owl: $(SRC)
	$(ROBOT) merge -i $< -o $@

.PHONY: matches
matches: tmp/edit-merged.owl
	$(DOSDPT) query --ontology=$< --catalog=catalog-v001.xml --reasoner=elk --obo-prefixes=true --batch-patterns="$(ALL_PATTERNS)" --template="../patterns/dosdp-patterns" --outfile="../patterns/data/matches/"

.PHONY: install_dosdp
install_dosdp:
	pip install -i https://test.pypi.org/simple/ dosdp==0.1.7.dev1

.PHONY: pattern_docs
pattern_docs:
	dosdp document -i ../patterns/dosdp-patterns/ -o ../../docs/patterns/ -d ../patterns/data/matches/

.PHONY: obocheck
obocheck:
	$(ROBOT) merge -i cl-edit.owl remove --base-iri http://purl.obolibrary.org/obo/CL_ --axioms external --trim false convert -f obo --check false -o cl-check.obo
	fastobo-validator cl-check.obo
	
test: obocheck

test_obsolete: cl.obo
	! grep "! obsolete" cl.obo

test: test_obsolete

## DOSDP on Google Sheets

DOSDP_URL=https://docs.google.com/spreadsheets/d/e/2PACX-1vQpgUhGLXgSov-w4xu_7jaI-e5AS0MNLVVhd6omHBEh20UHcBbZHOM4m8lepzBPN4ErD6TjxaKRTX4A/pub?gid=0&single=true&output=tsv

.PHONY: gs_dosdp_%
gs_dosdp_%:
	wget "$(DOSDP_URL)" -O ../patterns/data/default/$*.tsv

gs_dosdp: gs_dosdp_cellPartOfAnatomicalEntity


## FBbt mappings component

# Download the FBbt mapping file
.PHONY: $(TMPDIR)/fbbt-mappings.sssom.tsv
$(TMPDIR)/fbbt-mappings.sssom.tsv:
	if [ $(IMP) = true ]; then wget -O $@ http://purl.obolibrary.org/obo/fbbt/fbbt-mappings.sssom.tsv ; fi

# Attempt to update the canonical FBbt mapping file from a freshly downloaded one
# (no update if the downloaded file is absent or identical to the one we already have)
mappings/fbbt-mappings.sssom.tsv: $(TMPDIR)/fbbt-mappings.sssom.tsv
	if [ -f $< ]; then if ! cmp $< $@ ; then cat $< > $@ ; fi ; fi

# Generate cross-reference component from the FBbt mapping file
$(COMPONENTSDIR)/mappings.owl: mappings/fbbt-mappings.sssom.tsv ../scripts/sssom2xrefs.awk
	awk -f ../scripts/sssom2xrefs.awk $< > $@

## Download human reference atlas subset

HRA_SUBSET_URL="https://raw.githubusercontent.com/hubmapconsortium/ccf-validation-tools/master/owl/CL_ASCTB_subset.owl"
$(TMPDIR)/hra_subset.owl:
	wget $(HRA_SUBSET_URL) -O $@

$(COMPONENTSDIR)/hra_subset.owl: $(TMPDIR)/hra_subset.owl
	$(ROBOT) merge -i $< annotate --ontology-iri $(ONTBASE)/$@ --output $@

## Download CellXGene reference subset

CELLXGENE_SUBSET_URL="https://raw.githubusercontent.com/hkir-dev/cellxgene-cell-reporter/main/templates/cellxgene_subset.tsv"
$(TEMPLATEDIR)/cellxgene_subset.tsv:
	wget $(CELLXGENE_SUBSET_URL) -O $@

# Make CL-plus (CL + PCL product)

cl-plus.owl: $(ONT)-full.owl
	$(ROBOT) merge --input-iri http://purl.obolibrary.org/obo/pcl/pcl-base.owl --input $(ONT)-full.owl \
		reason --reasoner ELK --equivalent-classes-allowed asserted-only --exclude-tautologies structural \
		relax \
		reduce -r ELK \
		$(SHARED_ROBOT_COMMANDS) annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@

# ----------------------------------------
# RELEASE DEPLOYMENT
# ----------------------------------------

DEPLOY_GH=true

.PHONY: cl
cl:
	$(MAKE) prepare_release IMP=false PAT=false 
	$(MAKE) release-simple-diff
	if [ $(DEPLOY_GH) = true ]; then 	$(MAKE) deploy_release GHVERSION="v$(TODAY)"; fi

.PHONY: release-simple-diff
release-simple-diff:
	$(ROBOT) diff --labels True -f markdown --left-iri http://purl.obolibrary.org/obo/cl-simple.owl --right ../../cl-simple.owl --output reports/$(ONT)-simple-diff.md
		
FILTER_OUT=../patterns/definitions.owl ../patterns/pattern.owl reports/cl-edit.owl-obo-report.tsv
MAIN_FILES_RELEASE = $(foreach n, $(filter-out $(FILTER_OUT), $(RELEASE_ASSETS)), ../../$(n))

deploy_release:
	@test $(GHVERSION)
	ls -alt $(MAIN_FILES_RELEASE)
	gh release create $(GHVERSION) --notes "TBD." --title "$(GHVERSION)" --draft $(MAIN_FILES_RELEASE)  --generate-notes

# -------------------------------------------
# UPPER SLIM VALIDATION AND COVERAGE REPORTS
# -------------------------------------------

TERM_hematopoietic= CL:0000988
TERM_eye= UBERON:0000970
TERM_general = CL:0000000
TERM_kidney= UBERON:0002113

SLIM_TEMPLATES= blood_and_immune eye general_cell_types kidney
SLIM_REPORTS = $(foreach n,$(SLIM_TEMPLATES),$(REPORTDIR)/$(n)_upper_slim.csv)

.PHONY: slim_coverage
slim_coverage: $(SLIM_REPORTS)

COVERAGECMD= ./$(SCRIPTSDIR)/generic_coverage.py -s $(TERM_ID) -f $< -o $@ -c makefile

$(REPORTDIR)/blood_and_immune_upper_slim_report.csv: $(TEMPLATEDIR)/blood_and_immune_upper_slim.csv
	$(eval TERM_ID := $(TERM_hematopoietic))
	$(COVERAGECMD)

$(REPORTDIR)/eye_upper_slim_report.csv: $(TEMPLATEDIR)/eye_upper_slim.csv
	$(eval TERM_ID := $(TERM_eye))
	$(COVERAGECMD)

$(REPORTDIR)/general_cell_types_upper_slim_report.csv: $(TEMPLATEDIR)/general_cell_types_upper_slim.csv
	$(eval TERM_ID := $(TERM_general))
	$(COVERAGECMD)

$(REPORTDIR)/kidney_upper_slim_report.csv: $(TEMPLATEDIR)/kidney_upper_slim.csv
	$(eval TERM_ID := $(TERM_kidney))
	$(COVERAGECMD)
