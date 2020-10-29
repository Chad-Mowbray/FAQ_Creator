#!/bin/bash

# FOLDER="$PWD/files/output"
# rm -v `$FOLDER/frequency*`

function run_linter {
    linterrating=`pylint components/ \
    --disable=C0103 --disable=C0321 --disable=C0116 --disable=C0114 --disable=R0903 --disable=E0401 \
    | grep 'rated at'\
    | awk '{print $7}'`\
    && num=${linterrating:0:1} \
    && echo "Linter score: " $linterrating; \
    if [ "$num" -lt 9 ]; 
        then echo "linter failed" && exit 1; 
        else echo "linter passed"; 
    fi;
}

function run_program {
    python main.py -quick || exit 1
}

function check_output_files {
    FOLDER="$PWD/files/output"
    NUM_FILES=`ls -1 $FOLDER | wc -l`
    if [ "$NUM_FILES" -lt 5 ];
        then echo "Generated files don't exist";
        else echo "Generated files exist";
    fi;
}


function main {
    echo "running quick testing script..."
    # run_linter
    run_program
    check_output_files
}

main