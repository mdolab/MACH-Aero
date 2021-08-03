#!/bin/bash
set -e

# files changed by this PR
CHANGED_FILES=$(git --no-pager diff --name-only FETCH_HEAD $(git merge-base FETCH_HEAD master))
echo "The following files were changed in this PR:"
echo $CHANGED_FILES

# only run MACH tests if any files under tests/ or tutorial/ have changed
# or if it's not a PR build
if [[ $BUILD_REASON != "PullRequest" ]] || [[ $CH == *"tests/"* ]] || [[ $CH == *"tutorial/"* ]]; then
    testflo -v -n 1
fi
