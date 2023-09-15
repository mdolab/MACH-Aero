#! /bin/sh
version= # TODO: PUT THE VERSION OF PETSC YOU WANT TO BUILD HERE (e.g 4.3.0)

# If the user doesn't have an OPT_FLAGS environment variable, define the optimization flags here
if [[ ! -v OPT_FLAGS ]]; then
    OPT_FLAGS="-O3 -xCORE-AVX2" # TODO: PUT YOUR DESIRED OPTIMIZATION FLAGS HERE OR SAVE THEM IN AN ENVIRONMENT VARIABLE CALLED OPT_FLAGS
    echo "================================================================================="
    echo "OPT_FLAGS environment variable not defined. Using default flags: $OPT_FLAGS"
    echo "================================================================================="
fi

# cd CGNS-${version}
# rm CMakeCache.txt

# cmake -D CGNS_ENABLE_FORTRAN=ON \
# -D CMAKE_INSTALL_PREFIX=$CGNS_HOME \
# -D CGNS_ENABLE_64BIT=OFF \
# -D CGNS_ENABLE_HDF5=OFF \
# -D CGNS_BUILD_CGNSTOOLS=OFF \
# -D CMAKE_C_FLAGS="-fPIC ${OPT_FLAGS}" \
# -D CMAKE_Fortran_FLAGS="-fPIC ${OPT_FLAGS}" .
# # TODO: EDIT THE CONFIGURATION OPTIONS ABOVE IF NECESSARY

# status=$?

# # Build CGNS if configuration was successful
# if [[ $status == 0 ]]; then
#     make install
#     status=$?
# else
#     echo "Configuring CGNS-$version failed"
#     exit 1
# fi
# if [[ $status != 0 ]]; then
#     echo "Building/installing CGNS-$version failed"
#     exit 1
# fi
