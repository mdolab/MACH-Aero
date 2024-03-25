#!/bin/bash
set -e

# All tests should pass on private images with non-Intel MPI
if [[ $IMAGE == "private" ]] && [[ -z $I_MPI_ROOT ]]; then
    EXTRA_FLAGS='--disallow_skipped'
fi

testflo -v -n 1 $EXTRA_FLAGS
