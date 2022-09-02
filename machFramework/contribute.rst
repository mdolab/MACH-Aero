How to Contribute to MACH-Aero
==============================
The codes in the MACH-Aero framework are open-source tools, so we welcome users to submit additions or fixes to improve them for everyone.

Issues
------
If you have an issue, a bug to report, or a feature to request, submit an issue on the GitHub repository for that specific code.
This lets other users know about the issue.
If you are comfortable fixing the issue, please do so and submit a pull request from a branch on your own fork of that repo.

Coding style
------------
We use formatters specific to different programming languages to increase readability and standardization of code. 
We run continuous integration with these tools on all pull requests submitted.
For an easier workflow, we recommend integrating these tools with your code editor.

Python
^^^^^^

We use `black <https://github.com/psf/black>`_ for formatting Python codes.
Please install it following its documentation and run it at the project root with:

.. prompt:: bash

    black . -l 120

This will automatically format all Python files.

We use `flake8 <https://flake8.pycqa.org/en/latest/>`_ for linting in Python.
Please install it following its instructions and run it at the project root with:

.. prompt:: bash

    flake8 .

The configuration file we use for ``flake8`` is a combination of `this .flake8 file <https://github.com/mdolab/.github/blob/main/.flake8>`__ and the one at the root of the respective repository.
If there are any PEP-8 violations, ``flake8`` will print out the nature of the violation.

Fortran
^^^^^^^

We use `fprettify <https://github.com/pseewald/fprettify>`_ for formatting Fortran codes. 
Please install it following its documentation and run it at the project root with:

.. prompt:: bash

    fprettify -i=4 -l=120 --whitespace-multdiv=True --strict-indent

The configuration file for ``fprettify`` is a combination of `this .fprettify.rc file <https://github.com/mdolab/.github/blob/main/.fprettify.rc>`_ and the one at the root of the respective repository.

C/C++
^^^^^

We use `ClangFormat <https://clang.llvm.org/>`_ to format C/C++ codes. 
Please install it following its documentation and run at the project root with:

.. prompt:: bash

    clang-format

The configuration file for ``ClangFormat`` is a combination of `this .clang-format file <https://github.com/mdolab/.github/blob/main/.clang-format>`_ and the one at the root of the respective repository.

.. warning::
    For a PR to be accepted it must pass formatting checks with the relevant formatter and/or linter.

Documentation
-------------
When you add or modify code, make sure to provide relevant documentation that explains the new code.
This should be done in code via docstrings and comments as well as in the Sphinx documentation if you add a new feature or capability.
Look at the ``.rst`` files in the ``doc`` section of each repo.

Building the documentation requires ``sphinx`` and ``numpydoc``, as well as the Sphinx RTD theme.
To install these dependencies, type:

.. prompt:: bash

    pip install sphinx numpydoc sphinx-rtd-theme

To build documentation locally, go to the ``doc`` folder and type: 

.. prompt:: bash

    make html

The HTML files are then generated in ``_build/html`` and can be viewed in a web browser.

Testing
-------
When you add code or functionality, add tests that cover the new or modified code.
These may be units tests for individual components or regression tests for entire models that use the new functionality.
All the existing tests can be found under the ``test`` folder.
Running tests requires additional packages in some repos, to install these you can go to the root of that repo and type:

.. prompt:: bash 

    pip install .[testing]

We use `Codecov <https://about.codecov.io/>`_ to monitor the percentage of the code covered by tests. 
Coverage can be difficult to determine locally, so it is recommended to look for the check automatically run in the pull request. 

.. warning::
    For a PR to be accepted all existing tests must pass and new code should meet coverage requirements.

Pull requests
-------------
Finally, after adding or modifying code and making sure the steps above are followed, submit a pull request via the GitHub interface.
This will automatically go through every test in the repo to make sure everything is functioning properly as well as check the formatting and the code coverage.
The main developers of the respective repo will then merge in the request or provide feedback on how to improve the contribution.
