#!/bin/bash
# This file will download the input files for the intersection tutorial and extract them to the right place.

DIR=$(dirname $0)
INPUT_TAR="input_files.tar.gz"
wget -O $DIR/$INPUT_TAR http://umich.edu/~mdolaboratory/repo_files/private-MACH-tutorial/intersection_input_files.tar.gz
tar -xzf $DIR/$INPUT_TAR -C $DIR
mkdir -p $DIR/meshing/surface
mv $DIR/INPUT/dlr-f6* $DIR/meshing/surface
mv $DIR/INPUT/collar_surf.cgns $DIR/meshing/volume
rm $DIR/$INPUT_TAR
