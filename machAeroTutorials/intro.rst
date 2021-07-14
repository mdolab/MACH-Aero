.. _mach-aero-tutorial-intro:

############
Introduction
############

The `MDO Lab <http://mdolab.engin.umich.edu>`_ at the University of Michigan has developed the MDO of aircraft configurations with high fidelity (MACH) framework.
This tutorial was written to help new users become familiar with the tools and workflow of MACH for aerodynamic shape optimization and a few common practices of more experienced users.
Most of the tools in the MACH framework are written with Python, although many of the tools incorporate Fortran code to handle operations that require speed.
The user does not need to know Fortran to complete this tutorial, but if Python is not your strong suit, we recommend a refresher with one of the many online Python tutorials.

.. warning:: Please view this tutorial as a *bare-minimum* tutorial and not as a comprehensive tutorial. To gain proficiency and flexibility with the MACH tools, it is necessary to explore the dedicated documentation, source code, docstrings, and code comments of each tool. 

This tutorial starts from scratch and leads the user through the steps necessary to conduct aerodynamic shape optimization of a B717 wing.
The tutorial files are located on `GitHub <https://github.com/mdolab/MACH-Aero/>`__.
The scripts referenced in the tutorial can be found in the tutorial directory, organized according to section.
Although these scripts should be executable without any modifications, **we highly recommend that you create a separate directory and type out the lines of code by yourself.**
As you do this, ask yourself, "Do I understand why the code is written this way?"
This will result in a much deeper understanding of how to use the tools and eventually will help you develop code in a consistent manner.
To make this easier for you, we provide a basic script that will create the directory structure in your desired location so that all you have to do is create the files themselves.
To run this script, go to the mach_aero_tutorials root folder and run the following:
::

    python make_tutorial_directory.py my_tutorial

where ``my_tutorial`` is the name of the folder in which you will build your scripts.
The directory structures for each section of the tutorial, including all files, are displayed at the beginning of each section.
Throughout the tutorial, we will refer to the location of your developing tutorial as ``my_tutorial``, so if you chose a different name make sure to adjust your commands accordingly.

Before continuing with the tutorial, make sure that the MDOLab framework is already installed on your machine.
If you set up your machine using an MDOLab iso, then the required packages should already be installed.
If not, follow the instructions for installing the MDOLab framework from :ref:`scratch <installFromScratch>`.

This tutorial requires the following software.

**Made in the MDO Lab**

- `pyHyp <https://github.com/mdolab/pyhyp>`_
- `cgnsUtilities <https://github.com/mdolab/cgnsutilities>`_
- `baseclasses <https://github.com/mdolab/baseclasses>`_
- `pySpline <https://github.com/mdolab/pyspline>`_
- `pyGeo <https://github.com/mdolab/pygeo>`_
- `IDWarp <https://github.com/mdolab/idwarp>`_
- `ADflow <https://github.com/mdolab/adflow>`_
- `pyOptSparse <https://github.com/mdolab/pyoptsparse>`_
- `multipoint <https://github.com/mdolab/multipoint.git>`_

.. note:: These links take you to the GitHub repositories.
   To see their documentation, follow the link in the README for each GitHub repository.


**External Software**

- ICEM CFD (for surface mesh generation)
- Tecplot (for flow visualization)

Documentation strategy
======================
The tutorial resides on `GitHub <https://github.com/mdolab/MACH-Aero-tutorial/>`__, but it is a living tutorial, which means that it is constantly updated with corrections and improvements.
We invite you, especially as a new user, to take notes of the parts that you find confusing and bring them to the attention of an admin to the tutorial repository so that changes can be made.

The rst files in the doc directory contain direct links to the python scripts in the tutorial directory to avoid code duplication.
This is done using the ``start-after`` and ``end-before`` options of Sphinx's native ``literalinclude`` directive.
We adopt the convention of using ``#rst <section subject>`` as the marker for the start and end of each ``literalinclude`` section, like so:
::

    #rst Simple addition (begin)
    a = 2
    b = 3
    c = a + b
    #rst Simple addition (end)

Please adopt this same convention for any future developments to the tutorial.
