import sys, os

# Diretories with documentations:
repos = {
        'adflow':'../../adflow',
        'baseclasses':'../../baseclasses',
        'idwarp':'../../idwarp',
        'multipoint':'../../multipoint',
        'pygeo':'../../pygeo',
        'pyhyp':'../../pyhyp',
        'pyoptsparse':'../../pyoptsparse',
        'pyspline':'../../pyspline',
        'mach_aero_tutorials':'../../mach_aero_tutorials'
}

cur_dir = os.path.abspath(os.getcwd())
os.chdir('packages')
for repo in repos:
    os.system('ln -sf %s'%repos[repo])

os.chdir(cur_dir)

# Now build the master:
os.system('make html')

# Build depencencies that are needed in docs
os.system('cd ../adflow/doc/ && doxygen Doxyfile && cp -r _static {0:s}/_build/html/packages/adflow/doc/'.format(cur_dir))

# And copy...should only actually work on the server:
os.system('cp -fr _build/html/* ~/doc_website_public')
