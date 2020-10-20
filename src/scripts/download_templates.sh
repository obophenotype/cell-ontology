#!/bin/bash

set -e

file=$1

echo $file

sed -i 's/\r$//g' $file
sed -i -e '$a\' $file
rm -rf ../templates/*_do_no_edit.tsv
rm -rf ../templates/*_do_no_edit.owl

while IFS=',' read -r sheet url
do 
	wget "$url" -O ../templates/"$sheet"_do_no_edit.tsv
done <$file
