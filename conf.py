from sphinx_mdolab_theme.config import *

# -- Project information -----------------------------------------------------
project = "MACH-Aero Documentation"

# -- General configuration -----------------------------------------------------
# Built-in Sphinx extensions are already contained in the imported variable
# here we add external extensions, which must also be added to requirements.txt
# so that RTD can import and use them
extensions.extend(["sphinxcontrib.bibtex"])
