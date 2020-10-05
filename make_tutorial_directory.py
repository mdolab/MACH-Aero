"""
This script can be used to generate a directory structure identical to that
found in ./tutorial, except without any of the files. The user can then follow
the tutorial, creating each python script from scratch as recommended in the
introduction to the tutorial. Basically, this script saves you some time making
a bunch of directories.
"""
import os
import fnmatch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('writedir', type=str)
args = parser.parse_args()

tutorial_directory = 'tutorial/'
write_directory = args.writedir

for root, dirnames, filenames in os.walk(tutorial_directory):
    for dirname in dirnames:
        fullpath = os.path.join(root, dirname)
        endpath = fullpath.split(tutorial_directory)[-1]
        newdir = os.path.join(write_directory, endpath)
        os.system('mkdir -p %s'%newdir)
