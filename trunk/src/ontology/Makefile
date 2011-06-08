# todo - make this live:
cl-edit.obo:
	wget http://obo.cvs.sourceforge.net/viewvc/obo/obo/ontology/anatomy/cell_type/cell.edit.obo -O $@

cl-xp-obol.obo:
	obol qobol -ontology CL -r uberonp -i cl-xp.obo -tag generic -tag cell -undefined_only true -export obo > $@

cl-new-ext.txt:
	obol -r obol_av qobol-newterms -ontology CL -i cl-xp.obo -r uberonp -i cl-xp.obo -tag generic -tag cell -undefined_only true -export obo > $@

