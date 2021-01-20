#!/bin/sh
# this is temporary!
# will be replaced when https://github.com/ontodev/robot/issues/432
# this is adopted from Mondo
echo \#\# New Classes
echo
grep ^\+id: cl-diff.txt | perl -npe 's@...: CL:(\d+) . @ * [CL:$1](http://purl.obolibrary.org/obo/CL_$1) @'
echo
echo \#\# Obsoletions
echo
grep '\--> obsolete' cl-diff.txt | perl -npe 's@id: CL:(\d+) . @ * [CL:$1](http://purl.obolibrary.org/obo/CL_$1) @'
echo
echo \#\# Renaming
echo
grep '\-->' cl-diff.txt | perl -npe 's@id: cl-diff:(\d+) . @ * [CL:$1](http://purl.obolibrary.org/obo/CL_$1) @'
echo
