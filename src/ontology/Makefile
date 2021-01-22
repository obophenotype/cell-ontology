# ----------------------------------------
# Makefile for cl
# Generated using ontology-starter-kit
# ODK Version: v1.2.25
# ----------------------------------------
# <do not edit above this line>

# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

URIBASE=                    http://purl.obolibrary.org/obo
ONT=                        cl
ONTBASE=                    $(URIBASE)/$(ONT)
EDIT_FORMAT=                owl
SRC =                       $(ONT)-edit.$(EDIT_FORMAT)
CATALOG=                    catalog-v001.xml
ROBOT=                      robot --catalog $(CATALOG)
RELEASEDIR=                 ../..
REPORTDIR=                  reports
TMPDIR=                     tmp
SPARQLDIR =                 ../sparql
ROBOT_PROFILE =             profile.txt
REPORT_FAIL_ON =            None
REPORT_LABEL =              -l true
REPORT_PROFILE_OPTS =       
OBO_FORMAT_OPTIONS =        
SPARQL_VALIDATION_CHECKS =  equivalent-classes trailing-whitespace owldef-self-reference xref-syntax nolabels
SPARQL_EXPORTS =            basic-report class-count-by-prefix edges xrefs obsoletes synonyms
ODK_VERSION_MAKEFILE =      v1.2.25

TODAY ?= $(shell date +%Y-%m-%d)
OBODATE ?= $(shell date +'%d:%m:%Y %H:%M')
VERSION=$(TODAY)
ANNOTATE_ONTOLOGY_VERSION = annotate -V $(ONTBASE)/releases/$(VERSION)/$@ --annotation owl:versionInfo $(VERSION)
PATTERNDIR=                 ../patterns
DOSDP_SCHEMA=                http:// # change to PURL when ready.
PATTERN_TESTER=              simple_pattern_tester.py
DOSDPT=                      dosdp-tools
PATTERN_RELEASE_FILES=       $(PATTERNDIR)/definitions.owl $(PATTERNDIR)/pattern.owl

# seed.txt contains all referenced entities
IMPORTSEED=seed.txt
SRCMERGED=tmp/merged-$(SRC)
SIMPLESEED=simple_seed.txt
PRESEED=tmp/pre_seed.txt

FORMATS = $(sort  owl obo json owl)
FORMATS_INCL_TSV = $(sort $(FORMAT) tsv)
RELEASE_ARTEFACTS = $(sort  base full simple basic non-classified base full)

# ----------------------------------------
# Top-level targets
# ----------------------------------------

.PHONY: .FORCE
all: odkversion all_imports patterns all_main all_subsets sparql_test all_reports all_assets
test: odkversion sparql_test all_reports
	$(ROBOT) reason --input $(SRC) --reasoner ELK  --equivalent-classes-allowed all --exclude-tautologies structural --output test.owl && rm test.owl && echo "Success"

odkversion:
	echo "ODK Makefile version: $(ODK_VERSION_MAKEFILE) (this is the version of the ODK with which this Makefile was generated, not the version of the ODK you are running)" &&\
	echo "ROBOT version (ODK): " && $(ROBOT) --version

$TMPDIR:
	mkdir -p $@

## -- main targets --
##
## By default this is the cross-product of {ont, ont-base} x FORMATS

MAIN_PRODUCTS = $(sort $(foreach r,$(RELEASE_ARTEFACTS), $(ONT)-$(r)) $(ONT))
MAIN_GZIPPED = 
MAIN_FILES = $(foreach n,$(MAIN_PRODUCTS), $(foreach f,$(FORMATS), $(n).$(f))) $(MAIN_GZIPPED)

all_main: $(MAIN_FILES)

## -- import targets --
##
## By default this is the cross-product of IMPORT_MODULES x FORMATS


IMPORTS =  pr go uberon ro chebi clo pato ncbitaxon

IMPORT_ROOTS = $(patsubst %, imports/%_import, $(IMPORTS))
IMPORT_OWL_FILES = $(foreach n,$(IMPORT_ROOTS), $(n).owl)
IMPORT_FILES = $(IMPORT_OWL_FILES)


all_imports: $(IMPORT_FILES)

## -- subset targets --
##
## By default this is the cross-product of SUBSETS x FORMATS
## Note we also include TSV as a format


SUBSETS = 

SUBSET_ROOTS = $(patsubst %, subsets/%, $(SUBSETS))
SUBSET_FILES = $(foreach n,$(SUBSET_ROOTS), $(foreach f,$(FORMATS_INCL_TSV), $(n).$(f)))

all_subsets: $(SUBSET_FILES)

OBO_REPORT =  $(SRC)-obo-report $(ONT).owl-obo-report
REPORTS = $(OBO_REPORT)
REPORT_FILES = $(patsubst %, $(REPORTDIR)/%.tsv, $(REPORTS))

all_reports: all_reports_onestep $(REPORT_FILES)

## -- all files/assets --

ASSETS = \
  $(IMPORT_FILES) \
  $(MAIN_FILES) \
  $(REPORT_FILES) \
  $(SUBSET_FILES)

all_assets: $(ASSETS)

show_assets:
	echo $(ASSETS)
	du -sh $(ASSETS)


# ----------------------------------------
# Release Management
# ----------------------------------------

KEEPRELATIONS=keeprelations.txt
ONTOLOGYTERMS=ontologyterms.txt

# This should be executed by the release manager whenever time comes to make a release.
# It will ensure that all assets/files are fresh, and will copy to release folder
prepare_release: $(ASSETS) $(PATTERN_RELEASE_FILES)
	rsync -R $(ASSETS) $(RELEASEDIR) &&\
  mkdir -p $(RELEASEDIR)/patterns &&\
  cp $(PATTERN_RELEASE_FILES) $(RELEASEDIR)/patterns &&\
  rm -f $(MAIN_FILES) $(SRCMERGED) &&\
  echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

prepare_initial_release: prepare_release
	cd $(RELEASEDIR) && git add $(ASSETS)

# ----------------------------------------
# Export formats
# ----------------------------------------


$(ONT)-base.obo: $(ONT)-base.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT)-base.json: $(ONT)-base.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@
$(ONT)-full.obo: $(ONT)-full.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT)-full.json: $(ONT)-full.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@
$(ONT)-simple.obo: $(ONT)-simple.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT)-simple.json: $(ONT)-simple.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@
$(ONT)-basic.obo: $(ONT)-basic.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT)-basic.json: $(ONT)-basic.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@
$(ONT)-non-classified.obo: $(ONT)-non-classified.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT)-non-classified.json: $(ONT)-non-classified.owl
	$(ROBOT) annotate --input $< --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@
# Main release artefacts
$(ONT).owl: $(ONT)-full.owl
	$(ROBOT) annotate --input $< --ontology-iri $(URIBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(ONT).obo: $(ONT).owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT).json: $(ONT)-full.owl
	$(ROBOT) annotate --input $< --ontology-iri $(URIBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		convert --check false -f json -o $@.tmp.json && mv $@.tmp.json $@
# ----------------------------------------
# Initiating Step: Reason over source
# ----------------------------------------

# by default we use ELK to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo

OTHER_SRC = $(PATTERNDIR)/definitions.owl 


$(ONTOLOGYTERMS): $(SRC) $(OTHER_SRC)
	touch $(ONTOLOGYTERMS) && \
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/cl_terms.sparql $@










# base: OTHER sources of interest, such as definitions owl
$(ONT)-base.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) remove --input $< --select imports --trim false \
		merge $(patsubst %, -i %, $(OTHER_SRC)) \
		annotate --link-annotation http://purl.org/dc/elements/1.1/type http://purl.obolibrary.org/obo/IAO_8000001 \
		--ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) \
		--output $@.tmp.owl && mv $@.tmp.owl $@

# Full: The full artefacts with imports merged, reasoned
$(ONT)-full.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) merge --input $< \
		reason --reasoner ELK --equivalent-classes-allowed all --exclude-tautologies structural \
		relax \
		reduce -r ELK \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@

# foo-non-classified: (edit->imports-merged)
$(ONT)-non-classified.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) merge --input $< \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@
# foo-simple: (edit->reason,relax,reduce,drop imports, drop every axiom which contains an entity outside the "namespaces of interest")
# drop every axiom: filter --term-file keep_terms.txt --trim true
#	remove --select imports --trim false \

$(ONT)-simple.owl: $(SRC) $(OTHER_SRC) $(SIMPLESEED)
	$(ROBOT) merge --input $< $(patsubst %, -i %, $(OTHER_SRC)) \
		reason --reasoner ELK --equivalent-classes-allowed all --exclude-tautologies structural \
		relax \
		remove --axioms equivalent \
		relax \
		filter --term-file $(SIMPLESEED) --select "annotations ontology anonymous self" --trim true --signature true \
		reduce -r ELK \
		query --update ../sparql/inject-subset-declaration.ru \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@
# foo-basic: A version of -simple containing only relationships using relations on a configurable whitelist (default = BFO:0000050 (?)). See above (David comment) for explanation.
# removes any axioms that contains one of the ops that not in the whitelist file

$(ONT)-basic.owl: $(SRC) $(OTHER_SRC) $(SIMPLESEED) $(KEEPRELATIONS)
	$(ROBOT) merge --input $< $(patsubst %, -i %, $(OTHER_SRC)) \
		reason --reasoner ELK --equivalent-classes-allowed all --exclude-tautologies structural \
		relax \
		remove --axioms equivalent \
		remove --axioms disjoint \
		remove --term-file $(KEEPRELATIONS) --select complement --select object-properties --trim true \
		relax \
		filter --term-file $(SIMPLESEED) --select "annotations ontology anonymous self" --trim true --signature true \
		reduce -r ELK \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@
# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder

$(SRCMERGED): $(SRC)
	$(ROBOT) remove --input $< --select imports --trim false \
		merge  $(patsubst %, -i %, $(OTHER_SRC)) -o $@

$(PRESEED): $(SRCMERGED)
	$(ROBOT) query -f csv -i $< --query ../sparql/terms.sparql $@.tmp &&\
	cat $@.tmp | sort | uniq >  $@

$(SIMPLESEED): $(SRCMERGED) $(ONTOLOGYTERMS)
	$(ROBOT) query -f csv -i $< --query ../sparql/simple-seed.sparql $@.tmp &&\
	cat $@.tmp $(ONTOLOGYTERMS) | sort | uniq >  $@ &&\
	echo "http://www.geneontology.org/formats/oboInOwl#SubsetProperty" >> $@ &&\
	echo "http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty" >> $@


# Ugly hack which should be replaced by the dynamic import revision pipeline
$(IMPORTSEED): $(PRESEED) prepare_patterns $(PATTERNDIR)/all_pattern_terms.txt 
	if [ $(IMP) = true ]; then cat $(PRESEED) $(PATTERNDIR)/all_pattern_terms.txt | sort | uniq > $@; fi


# Generate terms.txt for each import.  (Assume OBO-style Possibly hacky step?)
# Should be able to drop this if robot can just take a big messy list of terms as input.

imports/%_terms_combined.txt: $(IMPORTSEED) imports/%_terms.txt
	if [ $(IMP) = true ]; then cat $^ | grep -v ^# | sort | uniq >  $@; fi

# -- Generate Import Modules --
#
# This pattern uses ROBOT to generate an import module
imports/%_import.owl: mirror/%.owl imports/%_terms_combined.txt
	if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T imports/$*_terms_combined.txt --force true --method BOT \
		query --update ../sparql/inject-subset-declaration.ru \
		annotate --ontology-iri $(ONTBASE)/$@ $(ANNOTATE_ONTOLOGY_VERSION) --output $@.tmp.owl && mv $@.tmp.owl $@; fi
.PRECIOUS: imports/%_import.owl

# convert imports to obo.
# this can be useful for spot-checks and diffs.
# we set strict mode to false by default. For discussion see https://github.com/owlcs/owlapi/issues/752
imports/%_import.obo: imports/%_import.owl
	if [ $(IMP) = true ]; then $(ROBOT) convert --check false -i $< -f obo -o $@.tmp.obo && mv $@.tmp.obo $@; fi
imports/%_import.json: imports/%_import.owl
	if [ $(IMP) = true ]; then $(ROBOT) convert --check false -i $< -f json -o $@.tmp.json && mv $@.tmp.json $@; fi


# ----------------------------------------
# Mirroring upstream ontologies
# ----------------------------------------
#

IMP=true # Global parameter to bypass import generation
MIR=true # Global parameter to bypass mirror generation
PAT=true # Global parameter to bypass pattern generation

## ONTOLOGY: pr
## Copy of pr is re-downloaded whenever source changes
mirror/pr.trigger: $(SRC)

mirror/pr.owl: mirror/pr.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pr.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: go
## Copy of go is re-downloaded whenever source changes
mirror/go.trigger: $(SRC)

mirror/go.owl: mirror/go.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/go.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: uberon
## Copy of uberon is re-downloaded whenever source changes
mirror/uberon.trigger: $(SRC)

mirror/uberon.owl: mirror/uberon.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/uberon.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: ro
## Copy of ro is re-downloaded whenever source changes
mirror/ro.trigger: $(SRC)

mirror/ro.owl: mirror/ro.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/ro.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: chebi
## Copy of chebi is re-downloaded whenever source changes
mirror/chebi.trigger: $(SRC)

mirror/chebi.owl: mirror/chebi.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/chebi.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: clo
## Copy of clo is re-downloaded whenever source changes
mirror/clo.trigger: $(SRC)

mirror/clo.owl: mirror/clo.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/clo.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: pato
## Copy of pato is re-downloaded whenever source changes
mirror/pato.trigger: $(SRC)

mirror/pato.owl: mirror/pato.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pato.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: ncbitaxon
## Copy of ncbitaxon is re-downloaded whenever source changes
mirror/ncbitaxon.trigger: $(SRC)

mirror/ncbitaxon.owl: mirror/ncbitaxon.trigger
	if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/ncbitaxon.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl



# ----------------------------------------
# Subsets
# ----------------------------------------
subsets/%.tsv: subsets/%.owl
	$(ROBOT) query -f tsv -i $< -s ../sparql/labels.sparql $@
subsets/%.owl: $(ONT).owl
	owltools --use-catalog $< --extract-ontology-subset --fill-gaps --subset $* -o $@.tmp.owl && mv $@.tmp.owl $@


# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl $(ONT).obo
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live.
# NOTE: these will soon be phased out and replaced by robot-report

#  run all violation checks
SPARQL_VALIDATION_QUERIES = $(foreach V,$(SPARQL_VALIDATION_CHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	$(ROBOT) verify  --catalog catalog-v001.xml -i $< --queries $(SPARQL_VALIDATION_QUERIES) -O reports/

# ----------------------------------------
# ROBOT report
# ----------------------------------------
reports/%-obo-report.tsv: %
	$(ROBOT) report -i $< $(REPORT_LABEL) $(REPORT_PROFILE_OPTS) --fail-on $(REPORT_FAIL_ON) --print 5 -o $@

# ----------------------------------------
# Sparql queries: Exports
# ----------------------------------------

SPARQL_EXPORTS_ARGS = $(foreach V,$(SPARQL_EXPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
# This combines all into one single command
all_reports_onestep: $(SRC)
	$(ROBOT) query -f tsv -i $< $(SPARQL_EXPORTS_ARGS)


# ----------------------------------------
# Docker (experimental)
# ----------------------------------------
IM=build-$(ONT)
build-docker:
	docker build -t $(ONT) .
# ----------------------------------------
# Patterns (experimental)
# ----------------------------------------

# Test patterns for schema compliance:

.PHONY: patterns
patterns: all_imports $(PATTERNDIR)/pattern.owl $(PATTERNDIR)/definitions.owl

.PHONY: pattern_clean
pattern_clean:
	echo "Not implemented"

pattern_schema_checks: update_patterns
	if [ $(PAT) = true ]; then $(PATTERN_TESTER) $(PATTERNDIR)/dosdp-patterns/; fi

#This command is a workaround for the absence of -N and -i in wget of alpine (the one ODK depend on now). It downloads all patterns specified in external.txt
update_patterns: .FORCE
	if [ $(PAT) = true ]; then rm -f $(PATTERNDIR)/dosdp-patterns/*.yaml.1 || true; fi
	if [ $(PAT) = true ]; then wget -i $(PATTERNDIR)/dosdp-patterns/external.txt --backups=1 -P $(PATTERNDIR)/dosdp-patterns; fi
	if [ $(PAT) = true ]; then rm -f $(PATTERNDIR)/dosdp-patterns/*.yaml.1 || true; fi


$(PATTERNDIR)/pattern.owl: pattern_schema_checks update_patterns
	if [ $(PAT) = true ]; then $(DOSDPT) prototype --obo-prefixes --template=$(PATTERNDIR)/dosdp-patterns --outfile=$@; fi

individual_patterns_default := $(patsubst %.tsv, $(PATTERNDIR)/data/default/%.ofn, $(notdir $(wildcard $(PATTERNDIR)/data/default/*.tsv)))
pattern_term_lists_default := $(patsubst %.tsv, $(PATTERNDIR)/data/default/%.txt, $(notdir $(wildcard $(PATTERNDIR)/data/default/*.tsv)))



individual_patterns_clustering := $(patsubst %.tsv, $(PATTERNDIR)/data/clustering/%.ofn, $(notdir $(wildcard $(PATTERNDIR)/data/clustering/*.tsv)))
pattern_term_lists_clustering := $(patsubst %.tsv, $(PATTERNDIR)/data/clustering/%.txt, $(notdir $(wildcard $(PATTERNDIR)/data/clustering/*.tsv)))



# Generating the individual pattern modules and merging them into definitions.owl
$(PATTERNDIR)/definitions.owl: prepare_patterns update_patterns dosdp_patterns_default   dosdp_patterns_clustering
	if [ $(PAT) = true ]; then $(ROBOT) merge $(addprefix -i , $(individual_patterns_default))   $(addprefix -i , $(individual_patterns_clustering)) annotate --ontology-iri $(ONTBASE)/patterns/definitions.owl  --version-iri $(ONTBASE)/releases/$(TODAY)/patterns/definitions.owl --annotation owl:versionInfo $(VERSION) -o definitions.ofn && mv definitions.ofn $@; fi

individual_patterns_names_default := $(strip $(patsubst %.tsv,%, $(notdir $(wildcard $(PATTERNDIR)/data/default/*.tsv))))
dosdp_patterns_default: $(SRC) all_imports .FORCE
	if [ $(PAT) = true ] && [ "${individual_patterns_names_default}" ]; then $(DOSDPT) generate --catalog=catalog-v001.xml --infile=$(PATTERNDIR)/data/default/ --template=$(PATTERNDIR)/dosdp-patterns --batch-patterns="$(individual_patterns_names_default)" --ontology=$< --obo-prefixes=true --outfile=$(PATTERNDIR)/data/default; fi



individual_patterns_names_clustering := $(strip $(patsubst %.tsv,%, $(notdir $(wildcard $(PATTERNDIR)/data/clustering/*.tsv))))
dosdp_patterns_clustering: $(SRC) all_imports .FORCE
	if [ $(PAT) = true ] && [ "${individual_patterns_names_clustering}" ]; then $(DOSDPT) generate --catalog=catalog-v001.xml --infile=$(PATTERNDIR)/data/clustering --template=$(PATTERNDIR)/dosdp-patterns/ --batch-patterns="$(individual_patterns_names_clustering)" --ontology=$< --obo-prefixes=true --outfile=$(PATTERNDIR)/data/clustering; fi



# Generating the seed file from all the TSVs. If Pattern generation is deactivated, we still extract a seed from definitions.owl
$(PATTERNDIR)/all_pattern_terms.txt: $(pattern_term_lists_default)   $(pattern_term_lists_clustering) $(PATTERNDIR)/pattern_owl_seed.txt
	if [ $(PAT) = true ]; then cat $^ | sort | uniq > $@; else $(ROBOT) query --use-graphs true -f csv -i ../patterns/definitions.owl --query ../sparql/terms.sparql $@; fi

$(PATTERNDIR)/pattern_owl_seed.txt: $(PATTERNDIR)/pattern.owl
	if [ $(PAT) = true ]; then $(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/terms.sparql $@; fi

$(PATTERNDIR)/data/default/%.txt: $(PATTERNDIR)/dosdp-patterns/%.yaml $(PATTERNDIR)/data/default/%.tsv .FORCE
	if [ $(PAT) = true ]; then $(DOSDPT) terms --infile=$(word 2, $^) --template=$< --obo-prefixes=true --outfile=$@; fi

.PHONY: prepare_patterns
prepare_patterns:
	if [ $(PAT) = true ]; then touch $(PATTERNDIR)/data $(pattern_term_lists_default)   $(pattern_term_lists_clustering); fi
	if [ $(PAT) = true ]; then touch $(PATTERNDIR)/data $(individual_patterns_default)   $(individual_patterns_clustering); fi



$(PATTERNDIR)/data/clustering/%.txt: $(PATTERNDIR)/dosdp-patterns/%.yaml $(PATTERNDIR)/data/clustering/%.tsv .FORCE
	if [ $(PAT) = true ]; then $(DOSDPT) terms --infile=$(word 2, $^) --template=$< --obo-prefixes=true --outfile=$@; fi





update_repo:
	sh ../scripts/update_repo.sh

include cl.Makefile