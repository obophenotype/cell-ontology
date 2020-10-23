# Annotation Properties

_Note- this page is currently under development._

The Cell Ontology has the following annotation properties:

Annotation property	| 	Description	|	Example term	|	Example annotation | Must have? | Only one use per term is allowed?
-- | -- | -- | --  | -- | --
consider	|	To be used on obsoleted classes, to point to a term that should be considered by curators for use in place of the obsoleted term.  Multiple consider terms are allowed.  It can be useful to combine this with a comment to indicate when replacement would be appropriate.	|	CL:0000610 `obsolete plant cell`	|	PO:0009002 | No | No
created_by	|	Added automatically on term creation with standard Protege settings. Ideally, this should use the "supplied user name" in the Protege User Details preference pane. This has been inconsistently applied in the past.	|	CL:0002518 | tmeehan | Should | Yes
creation_date	|	Added automatically on term creation with standard Protege settings.	|	CL:0002518 |	2011-02-08T10:46:34Z | Should | Yes
database_cross_reference	|	Citable references that have helped generate the term and term's definition. Includes PubMed IDs (in the format PMID:XXXXXXXX).	|	CL:0011005 `GABAergic interneuron` | PMID:29724907 | Should | No
dc:contributor	|	Use this to annotate a whole ontology file with the identifier of a contributor.  ORCID preferred.	|	N/A	|	https://orcid.org/0000-0001-9990-8331 | Nice to have, if applicable | No
dc:creator	|	Coming Soon	|	CL:0001201 `B cell, CD19-positive`	|	https://orcid.org/0000-0001-9990-8331 | No | Yes
dc:date	|	Coming soon	|	CL:0001065 `innate lymphoid cell` | 2017-01-30T20:20:48Z | No | Yes
dc:description	|	Use this to annotate a whole ontology file with a brief description of the ontology.	| N/A |	An ontology of cell types. | No | No
dc:title	|	Use this to annotate an ontology, giving it a human readable title.	| N/A |	Cell Ontology | No | No
dcterms:license	|	Use to attach a license to an ontology	|	N/A | http://creativecommons.org/licenses/by/4.0/ | No | No
definition	|	Coming soon	|	Coming soon	|	Coming soon | Must | Yes
'expand expression to'	|	Coming soon	|	Coming soon	|	Coming soon | No | No
foaf:depicted_by	|	Use this to add a link to an image that depicts an example of an entity referred to by the term	|	Coming soon	|	Coming soon | No | No
has_alternative_id	|	In CL this is a legacy property. Do not use.	|	CL:0000059 `ameloblast`	|	CL:0000053 | No | No
has_broad_synonym	|	Used for synonyms where the primary definition accurately describes the synonym, but the definition of the synonym may encompass other structures as well. In some cases where a broad synonym is given, it will be a broad synonym for more than one ontology term.  You are encouraged to add a reference that uses the term in this way.	|	CL:0000365 `animal zygote`	|	zygote | No | No
has_exact_synonym	|	Used for synonyms where the definition of the synonym is exactly the same as primary term definition. This is used when the same class can have more than one name.  You are encouraged to add a reference that uses the term in this way. |	CL:0000622	`acinar cell` |	acinic cell | Nice to have, if applicable | No
has_narrow_synonym	|	Used for synonyms where the definition of the synonym is the same as the primary definition, but has additional qualifiers. You are encouraged to add a reference that uses the term in this way.	|	CL:0000362 `epidermal cell`	| epithelial cell of skin | No | No
has_obo_namespace	|	This is a legacy annotation property.  Do not add this manually.	|	CL:0001061 `abnormal cell`	|	cell | No | No
has_related_synonym	|	This scope is applied when a word of phrase has been used synonymously with the primary term name in the literature, but the usage is not strictly correct. That is, the synonym in fact has a slightly different meaning than the primary term name. Since users may not be aware that the synonym was being used incorrectly when searching for a term, related synonyms are included.	|	Coming soon	|	Coming soon | No | No
has_synonym_type	|	  The target of this relation must be an annotation property of type 'synonym_type_property'.	| Coming soon	 |	Coming sooon | No | No
IAO_0000116	|	Coming soon	|	Coming soon	|	Coming soon | No | No
id	|	Automatically added by some pathways.  Do not add manually.  If duplicating a term (with the duplicate getting a new ID), it should be deleted.	|	CL:2000074	`splenocyte` |	CL:2000074 | Yes | Yes
in_subset	|	Used to add subset tags, used in conjunction with subset_property	|	CL:0000039 `germ line cell`	|	\_upper_level | No | No
is_inferred	|	This annotation property is used in some automated pipelines.  Do not add manually	|	Coming soon	|	Coming soon | No | No
rdfs:comment	|	Use to add a clarifying comment to a term.  This can be useful for adding examples and for clarifying terminological confusions	|	Coming soon	|	Coming soon | No | Yes
rdfs:isDefinedBy	|	Do not add manually.	|	Coming soon	|	Coming soon | No | Yes
rdfs:label	|	Primary name - used as a display name by Protege (with standard settings) and most downstream consumers. Add only one of these.  It must be unique within an ontology.	|	Coming soon	|	Coming soon | Must | Yes
RO_0002161	|	Coming soon	|	Coming soon	|	Coming soon | No | No
'see also'	|	Used to link to a webpage, such as a GitHub ticket.	|	CL:0000134 `mesenchymal stem cell`	| https://github.com/obophenotype/cell-ontology/issues/474 | No | No
shorthand	|	Added automatically by some pipelines.  Do not add manually	|	Coming soon	|	Coming soon | No | No
subset_property	|	A grouping class for subset tags.	| N/A |	N/A | No | No
synonym_type_property	|  A grouping class for synonym tags.	|	N/A	|	N/A | No | No
'term replaced by'	|	To be used on obsolete terms to indicate a term that can be automatically substituted for the obsoleted term. |	Coming soon	|	Coming soon | No | No
