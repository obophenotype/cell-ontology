## Customize Makefile settings for cl
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

mirror/pr.owl: mirror/pr.trigger
#	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pr.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi
	echo "skipped pr"

imports/pr_import.owl:
	echo "skipped pr import"


mirror/ncbitaxon.owl: mirror/pr.trigger
#	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pr.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi
	echo "skipped ncbitaxon mirror"

imports/ncbitaxon_import.owl:
	echo "skipped ncbitaxon import"

object_properties.txt: $(SRC)
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/object-properties-in-signature.sparql $@

$(ONT)-simple.obo: $(ONT)-simple.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo &&\
	grep -v ^owl-axioms $@.tmp.obo > $@.tmp &&\
	cat $@.tmp | perl -0777 -e '$$_ = <>; s/^name[:].*?\nname[:]/name:/g; print' | perl -0777 -e '$$_ = <>; s/def[:].*?\ndef[:]/def:/g; print' > $@
	rm -f $@.tmp.obo $@.tmp

simple_seed.txt: $(SRC) #$(ONTOLOGYTERMS) #prepare_patterns
	$(ROBOT) query --use-graphs false -f csv -i $< --query ../sparql/object-properties.sparql $@.tmp &&\
	cat $@.tmp $(ONTOLOGYTERMS) | sort | uniq >  $@ &&\
	echo "http://www.geneontology.org/formats/oboInOwl#SubsetProperty" >> $@ &&\
	echo "http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty" >> $@
#rm -f $@.tmp

non_native_classes.txt: $(SRC)
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/non-native-classes.sparql $@.tmp &&\
	cat $@.tmp | sort | uniq >  $@
	rm -f $@.tmp

$(ONT)-simple.owl: $(SRC) $(OTHER_SRC) simple_seed.txt non_native_classes.txt $(ONTOLOGYTERMS)
	$(ROBOT) merge --input $< $(patsubst %, -i %, $(OTHER_SRC)) --collapse-import-closure true \
		reason --reasoner ELK \
		relax \
		remove --axioms equivalent \
		relax \
		filter --term-file simple_seed.txt --trim true --select "annotations ontology anonymous parents object-properties self" --preserve-structure false \
		remove --term-file non_native_classes.txt --preserve-structure false \
		reduce -r ELK \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@

# TODO add back: 		remove --term-file non_native_classes.txt \


$(ONT).obo: $(ONT)-basic.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo

$(PATTERNDIR)/dosdp-patterns: .FORCE
	echo "WARNING WARNING Skipped until fixed: delete from cl.Makefile"

$(ONT)-basic.owl: $(SRC) $(OTHER_SRC) $(ONTOLOGYTERMS) $(KEEPRELATIONS) simple_seed.txt non_native_classes.txt
	$(ROBOT) merge --input $< $(patsubst %, -i %, $(OTHER_SRC)) --collapse-import-closure true \
		reason --reasoner ELK \
		relax \
		remove --axioms equivalent \
		relax \
		filter --term-file simple_seed.txt --trim true --select "annotations ontology anonymous parents object-properties self" --preserve-structure false \
		remove --term-file non_native_classes.txt --preserve-structure false \
		remove --term-file $(KEEPRELATIONS) --select complement --select object-properties --trim true \
		reduce -r ELK \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@

oort: $(SRC)
	ontology-release-runner --reasoner elk $< --no-subsets --allow-equivalent-pairs --simple --relaxed --asserted --allow-overwrite --outdir oort

KEEPRS= RO:0002202

$(ONT)-basic.owl: $(ONT)-simple.owl
	owltools $< --make-subset-by-properties $(KEEPRS) --remove-axioms -t DisjointClasses -o -f owl $@

$(ONT)-simple.owl: oort
	cp oort/$@ $@

$(ONT)-basic.obo: $(ONT)-simple.obo
	owltools $< --make-subset-by-properties $(KEEPRS) --remove-axioms -t DisjointClasses -o -f obo $@

$(ONT)-simple.obo: oort
	cp oort/$@ $@

# TODO add BACK remove --term-file $(KEEPRELATIONS) --select complement --select object-properties --trim true \
# TODO add BACK remove --term-file non_native_classes.txt \

#				remove --term-file $(KEEPRELATIONS) --select complement --select object-properties --trim true \



fail_seed_by_entity_type_cl:
	robot query --use-graphs false -f csv -i cl-edit.owl --query ../sparql/object-properties.sparql $@.tmp &&\
	cat $@.tmp | sort | uniq >  $@.txt && rm -f $@.tmp 

works_seed_by_entity_type_cl:
	robot query --use-graphs false -f csv -i cl-edit.owl --query ../sparql/object-properties-in-signature.sparql $@.tmp &&\
	cat $@.tmp | sort | uniq >  $@.txt && rm -f $@.tmp 
