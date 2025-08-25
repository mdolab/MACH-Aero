#!/bin/bash
set -e

# Set OpenMPI env variables only on non-Intel MPI
if [[ -z $I_MPI_ROOT ]]; then
    # Set these to allow MPI oversubscription because the tests need to run on specific number of procs but the test runner may have fewer
    export OMPI_MCA_rmaps_base_oversubscribe=1 # This works for OpenMPI <= 4
    export PRTE_MCA_rmaps_default_mapping_policy=:oversubscribe # This works from OpenMPI >= 5
fi

# All tests should pass on private images with non-Intel MPI
if [[ $IMAGE == "private" ]] && [[ -z $I_MPI_ROOT ]]; then
    EXTRA_FLAGS='--disallow_skipped'
fi

testflo -v -n 1 $EXTRA_FLAGS
