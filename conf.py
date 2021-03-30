from sphinx_mdolab_theme.config import *

# -- Project information -----------------------------------------------------
project = "MACH-Aero Documentation"

# -- General configuration -----------------------------------------------------
# Specify the baseurls for the projects I want to link to
repos = [
    "pygeo",
    "pyoptsparse",
    "baseclasses",
    "idwarp",
    "adflow",
    "pyhyp",
    "multipoint",
    "pyspline",
]
intersphinx_mapping = {r: (f"https://mdolab-{r}.readthedocs-hosted.com/en/latest", None) for r in repos}

# bibtex
bibtex_bibfiles = [
    "machFramework/references.bib",
    "machAeroTutorials/overset.bib",
]
