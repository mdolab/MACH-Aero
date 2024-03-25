from sphinx_mdolab_theme.config import *

# -- Project information -----------------------------------------------------
project = "MACH-Aero Documentation"

# -- General configuration -----------------------------------------------------
# autolink
extensions.extend(["sphinx_codeautolink"])
codeautolink_concat_default = True
codeautolink_warn_on_missing_inventory = True
codeautolink_warn_on_failed_resolve = True

# bibtex
bibtex_bibfiles = [
    "machAeroTutorials/overset.bib",
]
