from sphinx_mdolab_theme.config import *

# -- Project information -----------------------------------------------------
project = "MACH-Aero Documentation"

# -- General configuration -----------------------------------------------------
# Built-in Sphinx extensions are already contained in the imported variable
# here we add external extensions, which must also be added to requirements.txt
# so that RTD can import and use them
extensions.extend(["sphinxcontrib.bibtex"])

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
