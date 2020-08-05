# MDO Lab Documentation #

MDO Lab public documentation repository
Most of the docs in this repo are in reStructuredText (.rst) format and made with Sphinx.
Some docs live in this repo, whereas others live in their respective code's repo.

# How to access the docs online #

These docs are continuously built and published online to http://mdolab.engin.umich.edu/docs/.

# How to locally make the docs #

To locally compile these docs, clone the rpeo, then type `make html` at the base folder.
The built docs will live in the `_build/html` folder.
Open up `index.html` within there to see the main doc page.

The docs for the code repos will only be compiled if those repos live at the same level as this documentation repo.
However, to make the rest of the docs, including the installation instructions, and tutorials, you don't need those code repos at that same level.

# Maintainer #

John Jasa, johnjasa@umich.edu
