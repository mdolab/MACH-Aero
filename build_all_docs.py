import sys, os

# Diretories with documentations:
repos = {'pyhyp':'../../pyhyp',
         'multipoint':'../../multipoint',
         'pyoptsparse':'../../pyoptsparse',
         'baseclasses':'../../baseclasses',
         'pyspline':'../../pyspline',
         'idwarp':'../../idwarp',
         'pygeo':'../../pygeo',
         'adflow':'../../adflow',
         'pylayout':'../../pylayout',
         'machtutorial':'../../machtutorial'
}

cur_dir = os.path.abspath(os.getcwd())
os.chdir('packages')
for repo in repos:
    os.system('ln -sf %s'%repos[repo])

os.chdir(cur_dir)

# Now build the master:
os.system('make html')

# And copy...should only actually work on the server:
os.system('cp -fr _build/html/* ~/doc_website_public')
