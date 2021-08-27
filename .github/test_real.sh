#!/bin/bash
set -e

# all tests should pass on private
if [[ $IMAGE == "private" ]] && [[ $OS == "ubuntu" ]]; then
    EXTRA_FLAGS='--disallow_skipped'
fi

testflo -v -n 1 $EXTRA_FLAGS
