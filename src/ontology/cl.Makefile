## Customize Makefile settings for cl
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

mirror/pr.owl: mirror/pr.trigger
#	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pr.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi
	pass

imports/pr_import.owl:
	pass


mirror/ncbitaxon.owl: mirror/pr.trigger
#	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pr.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi
	pass

imports/ncbitaxon_import.owl:
	pass

object_properties.txt: $(SRC)
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/object-properties-in-signature.sparql $@