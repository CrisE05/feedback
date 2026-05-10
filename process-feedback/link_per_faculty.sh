#!/bin/bash

if test $# -ne 2; then
    echo "Usage: $0 <data-folder> <output-folder>" 1>&2
    exit 1
fi

data_dir="$1"
output_dir="$2"

if test ! -d "$data_dir"; then
    echo "Error: Folder $data_dir does not exist or is not a folder." 1>&2
    exit 1
fi

if test ! -d "$output_dir"; then
    echo "Error: Folder $output_dir does not exist or is not a folder." 1>&2
    exit 1
fi

declare -A category_ids
category_ids["01-ELECTRO"]=2
category_ids["02-ENERG"]=3
category_ids["03-ACS"]=4
category_ids["04-ELECTRONICA"]=5
category_ids["05-FIMM"]=7
category_ids["06-FIIR"]=8
category_ids["07-ISB"]=9
category_ids["08-Transp"]=10
category_ids["09-AERO"]=11
category_ids["10-SIM"]=12
category_ids["11-CHIM"]=13
category_ids["12-FILS"]=14
category_ids["13-FSA"]=15
category_ids["14-FIM"]=16
category_ids["15-FAIMA"]=17
category_ids["16-DPPD"]=18

for key in ${!category_ids[@]}; do
    ./link_users.py -g "${category_ids[$key]}" -d "$data_dir" -o "$output_dir"/"$key"/user-json/raw/
    ./link_feedbacks.py -g "${category_ids[$key]}" -d "$data_dir" -o "$output_dir"/"$key"/json/raw/
done
