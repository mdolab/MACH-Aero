#! /bin/bash
version= # TODO: PUT THE VERSION OF PETSC YOU WANT TO BUILD HERE (e.g 3.19.5)

# If the user doesn't have an OPT_FLAGS environment variable, define the optimization flags here
if [ -z ${var+x} ]; then
    OPT_FLAGS="-O3 -xCORE-AVX2" # TODO: PUT YOUR DESIRED OPTIMIZATION FLAGS HERE OR SAVE THEM IN AN ENVIRONMENT VARIABLE CALLED OPT_FLAGS
fi

cd petsc-${version}

for buildType in "opt" "debug"; do
    for scalarType in "real" "complex"; do

        archName="${scalarType}-${buildType}"
        echo "Configuring $archName PETSc"
        export PETSC_ARCH=$archName

        PETSC_DIR=`pwd`; export PETSC_DIR

        if [[ buildType == "debug" ]]; then
            debug=1
        else
            debug=0
        fi

        rm -rf $PETSC_ARCH
        ./configure \
        --with-debugging=$debug \
        --with-scalar-type=$scalarType \
        --PETSC_ARCH=$PETSC_ARCH \
        # TODO: PUT YOUR REMAINING CONFIG OPTIONS HERE

        status=$?

        # Build PETSc if configuration was successful
        if [[ $status == 0 ]]; then
            make PETSC_DIR=$PETSC_DIR PETSC_ARCH=$PETSC_ARCH all
            status=$?
        else
            echo "Configuring $archName PETSc failed"
            exit 1
        fi

        # Test PETSc if build was successful
        if [[ $status == 0 ]]; then
            make PETSC_DIR=$PETSC_DIR PETSC_ARCH=$PETSC_ARCH test
            status=$?
        else
            echo "Building $archName PETSc failed"
            exit 1
        fi

        if [[ $status != 0 ]]; then
            echo "Testing $archName PETSc failed"
            exit 1
        fi
    done
done
