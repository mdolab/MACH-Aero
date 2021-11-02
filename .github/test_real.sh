#!/bin/bash
set -e

# all tests should pass on private
if [[ $IMAGE == "private" ]] && [[ $OS == "ubuntu" ]]; then
    EXTRA_FLAGS='--disallow_skipped'
fi

# Hack to print out memory usage every 2 seconds
free -s 2 &
testflo -v -n 1 $EXTRA_FLAGS
