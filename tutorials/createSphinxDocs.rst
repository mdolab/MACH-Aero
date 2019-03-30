.. Instructions on how to set up create a new documentation site for an
   existing repository
   Author: Eirikur Jonsson (eirikurj@umich.edu)


.. _createSphinxDocs:

Adding documentation to a package
=================================

Creating Sphinx documentation for a package is easy! To create
documentation and have it included on the MDOlab website use the
following guidelines:

#. Install ``sphinx`` and ``numpy-doc`` using::

    sudo apt-get install python-sphinx
    sudo apt-get install python-pip
    sudo pip install numpydoc

#. Create a ``doc`` folder in the root of the repository you want to
   document using::

     mkdir doc

#. Run the command (from the doc folder)::

     sphinx-quickstart

#. Use all defaults except for ``Project name``, ``Author name`` and
   ``Project version``. Enter ``y`` for the ``viewcode`` question.

#. After the quick-start has completed, open ``conf.py`` find the line
   starting with ``extensions =`` and replace it with::

    extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'numpydoc']
    numpydoc_show_class_members = False

#. A documentation shell is now created. It can be built using::

     make html

#. The result can be viewed using::

     firefox _build/html/index.html

#. **Optional** To use the MDOlab theme copy theme ``themes`` directory
   from an existing repository and add the following lines to the
   ``conf.py`` file (and comment out the ``html_theme='default'``
   line)::

     html_theme_path = ['themes']
     html_theme = 'mdolab_theme'

#. To include the documentation on the website, first ensure you have
   the ``documentation`` repository checked out::

     git clone https://bitbucket.org/mdolab/documentation

#. Modify the ``repos`` dictionary in the ``build_all_docs.py`` file
   to point to the name of your repository.

#. Modify the ``index.rst`` to include the index of the new
   documentation. It should look like::

    packages/<package_name>/doc/index

#. Finally, the module must be cloned automatically onto the
   server. Contact the admin to check if this is case.


For more information refer to the Sphinx documentation site http://www.sphinx-doc.org/
