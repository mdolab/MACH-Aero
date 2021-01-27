from sphinx_mdolab_theme.config import *

# -- Project information -----------------------------------------------------
project = "MACH-Aero Documentation"

# -- General configuration -----------------------------------------------------
# Built-in Sphinx extensions are already contained in the imported variable
# here we add external extensions, which must also be added to requirements.txt
# so that RTD can import and use them
extensions.extend(["sphinxcontrib.bibtex"])

# Specify the baseurls for the projects I want to link to
intersphinx_mapping = {
    "pyoptsparse": ("https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest", None),
    "pygeo": ("https://mdolab-pygeo.readthedocs-hosted.com/en/latest", None),
}

# bibtex
bibtex_bibfiles = ["machFramework/references.bib"]
