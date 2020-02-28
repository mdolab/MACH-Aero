.. Some helpful tips or common pitfalls when using Tapenade to differentiate code.
Please add or modify as you see fit.


.. _tapenadeTips:

Automatic Differentiation (AD) with Tapenade
============================================

`Tapenade <http://www-sop.inria.fr/tropics/tapenade.html>`_ is an
Automatic Differentiation (AD) tool developed at INRIA Sophia-Antipolis.

The basic idea of AD is straightforward:
you provide source code that compute outputs from a set of inputs and
you then receive code to obtain both forward- and reverse-mode derivatives.
However, the actual implementation and process to obtain this code may
be challenging due to code complexity.

Tapenade does this through source code transformation, which breaks down
each line of code into individual math operations (addition,
division, log, etc) and calculates the derivatives of these operations.
By combining each of these derivatives via the chain rule, a total
derivative for the subroutine can be computed.

Getting Started
---------------

Here is a helpful `blog post about AD <https://justindomke.wordpress.com/2009/02/17/automatic-differentiation-the-most-criminally-underused-tool-in-the-potential-machine-learning-toolbox/>`_
and here is another `post that explains reverse-mode AD <https://justindomke.wordpress.com/2009/03/24/a-simple-explanation-of-reverse-mode-automatic-differentiation/>`_. Note that these are just one person's explanation of AD.

The Tapenade website has a great
`tutorial <http://www-sop.inria.fr/tropics/tapenade/tutorial.html>`_,
but the basic steps and other issues to note are outlined below.
If you are new to Tapenade or AD, reading through the online tutorial
and trying the commands yourself is highly recommended.

Basic Setup for Tapenade Differentiation
----------------------------------------

#.  `Download Tapenade <http://www-sop.inria.fr/tropics/tapenade/downloading.html>`_
    and install it locally or navigate to the `online differentiation tool
    <http://www-tapenade.inria.fr:8080/tapenade/>`_.
    For simple subroutines, the online tool will be sufficient.

#.  Run Tapenade on the source code file. Locally, this is done as::

      tapenade SOURCE_FILE.F90 -d -b

    The `-d` and `-b` options create forward- and reverse-mode code respectively.

    For the online version, you simply upload your source code and choose
    to differentiate in tangent (forward) or adjoint (reverse) mode.

#.  Examine the code produced by Tapenade.

    You should have obtained `SOURCE_FILE_d.F90` and `SOURCE_FILE_b.F90`,
    which contain the forward- and reverse-mode differentiated subroutines
    respectively.

    Note that Tapenade also creates `.msg` files which contain warnings and error
    messages related to the AD results. You should inspect these and ensure
    that your code was correctly differentiated without fatal errors.

    Also note that if your code contains logical branches (e.g. if/then statements)
    or relies on previous calculations for the reverse-mode, the AD First-Aid
    Kit will have to be compiled with your code. This kit defines the push/pop
    routines and is available from the `Tapenade FAQ <https://www-sop.inria.fr/tropics/tapenade/faq.html>`_.


Common Pitfalls and Items to Note
----------------------------------

This is an assuredly incomplete list of possible issues that may occur
when running Tapenade. Please check their `FAQ and Bugs <http://www-sop.inria.fr/tropics/tapenade.html>`_ webpage for a more
exhaustive list.



Push-pop errors in reverse mode: "popping from an empty stack"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When using user-defined sizes for variable sizing, the reverse-mode code
sometimes fails due to Tapenade incorrectly storing the byte length of the variables.
This only occurs in the reverse-mode because of the way pushing and popping variables
is handled.

One error that you might see is "Error: popping from an empty stack!"
This means that Tapenade tried to retrieve data it incorrectly thought
was pushed previously.

This error might be caused by the following snippet in your reverse-mode code::

  call pushinteger4array(i-1, inttype/4)
  ...
  call popinteger4(ad_to)

Here, inttype is 4 bytes (integer4).
The code is pushing an integer array of length 1 (inttype/4) and then
trying to pop an integer.
This causes the stack error because the bytes of the stack do not line up correctly.

This problem was seen especially with index variables within Fortran loops.
For example, using the index `i` in a `do` loop with a specified `inttype`.

One fix for this problem is use `integer*4` instead of `integer(kind=inttype)`
when instantiating the index variable.
Note that the index variable is only used as a placeholder in the do loop;
its value is never actually accessed.


Seeds are overwritten in reverse mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note that the `_b` routines produced by Tapenade take in derivative seed
values and then modify them in place.
That is, if you have the `coordinate` variable and provide the seeds
`coordinateb`, these seeds will be treated as an in-out variable.
This is especially important if using f2py to wrap the Fortran code.
Make sure that the intents match what you expect - f2py does not
always automatically produce correct intents when using Tapenade.


External callbacks might have incorrect intents when using f2py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Also related to f2py and Tapenade: if you are using an external
callback function to Python, you may have to manually set the intents
in the auto-generated `.pyf` file.
Here is an example of the unmodified code::

  python module march__user__routines
      interface march_user_interface
          subroutine py_projection(rstart,rnext,nnext,numnodes) ! in :hypsurfAPI:hypsurfAPI.F90:hypsurfapi:march:unknown_interface
              real(kind=realtype) dimension(3 * numnodes),intent(in) :: rstart
              real(kind=realtype) dimension(3 * numnodes),depend(numnodes) :: rnext
              real(kind=realtype) dimension(3,numnodes),depend(numnodes) :: nnext
              integer(kind=inttype), optional,intent(in),check((len(rstart))/(3)>=numnodes),depend(rstart) :: numnodes=(len(rstart))/(3)
          end subroutine py_projection
      end interface march_user_interface
  end python module march__user__routines

Here we need `rnext` and `nnext` to also have `intent(out)`, so the final
version would look like::

  python module march__user__routines
      interface march_user_interface
          subroutine py_projection(rstart,rnext,nnext,numnodes) ! in :hypsurfAPI:hypsurfAPI.F90:hypsurfapi:march:unknown_interface
              real(kind=realtype) dimension(3 * numnodes),intent(in) :: rstart
              real(kind=realtype) dimension(3 * numnodes),depend(numnodes),intent(out) :: rnext
              real(kind=realtype) dimension(3,numnodes),depend(numnodes),intent(out) :: nnext
              integer(kind=inttype), optional,intent(in),check((len(rstart))/(3)>=numnodes),depend(rstart) :: numnodes=(len(rstart))/(3)
          end subroutine py_projection
      end interface march_user_interface
  end python module march__user__routines

Do not use functions; use subroutines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is really only relevant if you are using f2py to wrap your differentiated code.
However, we do this often enough that is included here.
Fortran functions are not correctly processed by f2py; only subroutines
can be reliably converted correctly into Python functions.

Even if you are calling the Fortran functions only from within Fortran,
those should still be subroutines as f2py will run into issues when
attempting to run the top-level Python function.

Avoid providing the same object twice to a subroutine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say you're trying to find the dot product of a vector with itself and you use the following line::

  call dot(vec, vec, out_vec)

Tapenade will not differentiate this code correctly because of the way that seeds are zeroed within a differentiated subroutine.
To circumvent this issue, create a dummy vector to pass into the subroutine, like so::

  vec_dummy = vec
  call dot(vec, vec_dummy, out_vec)

This way when the seeds passed into the `dot_b` or `dot_d` subroutine are zeroed, it does not cause the `out_vec` seeds to be accumulated incorrectly.
