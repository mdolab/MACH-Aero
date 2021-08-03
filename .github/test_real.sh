#!/bin/bash
set -e

CHANGED_FILES=$(git --no-pager diff --name-only FETCH_HEAD $(git merge-base FETCH_HEAD master))
echo "The following files have changed:"
echo $CHANGED_FILES

# only run MACH tests if any files under tests/ or tutorial/ have changed
if [[ $CH == "tests/"* ]] || [[ $CH == "tutorial/"* ]]; then
    testflo -v -n 1
fi
