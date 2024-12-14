.. _intersection_opt:

Aerodynamic Shape Optimization
==============================

Now that we have set up the geometry parameterization, the top-level run script, ``aero_opt.py``, closely resembles a wing-only aerodynamic shape optimization case.
We set up the MACH modules by calling the setup functions in sequence.

.. literalinclude:: ../tutorial/intersection/aero_opt.py
   :start-after: # rst MACH (start)
   :end-before: # rst MACH (end)

One difference from a more conventional optimization is that we pass ``CFDPointSetKwargs`` to the ADflow object when setting the DVGeometry object.
This dictionary is defined in ``SETUP/setup_adflow.py``.

.. literalinclude:: ../tutorial/intersection/SETUP/setup_adflow.py
   :start-after: # rst CFDPointSetKwargs (start)
   :end-before: # rst CFDPointSetKwargs (end)

.. important::
   You must set ``applyIC`` if you want the intersection method to work!
   It is ``False`` by default so the DVConstraints do not get affected by the intersection method.

Setting ``applyIC`` tells DVGeometryMulti that the CFD surface mesh must follow the intersection curves.
This ensures that the outer mold line remains watertight when the intersection is updated.
The ``comm`` argument tells DVGeometryMulti that the CFD point set is distributed across the processors on the specified communicator object.

We can run the optimization with several combinations of geometric design variables by passing the ``dvs`` argument to ``aero_opt.py``.
The possible values for the argument are defined with ``permutations``  from the ``itertools`` module in Python.

.. literalinclude:: ../tutorial/intersection/aero_opt.py
   :start-after: # rst dvs (start)
   :end-before: # rst dvs (end)

For example, we can optimize with fuselage and twist variables using ``python aero_opt.py --dvs=ft``.
Running an optimization with this configuration in a reasonable time will most likely require using HPC resources.
