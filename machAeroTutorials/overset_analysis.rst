.. _overset_analysis:

*******************************************************
CFD Analysis
*******************************************************

Introduction
============

This part will help guide you through the analysis part. We will setup the run script, let ADflow compute the 
solution and finally take a look at the output with ParaView. From :cite:`nasaM6real` we know the flow conditions:

+-------------------+---------+
| Mach              | 0.8395  |
+-------------------+---------+
| Reynolds Number   | 11.72e6 |
+-------------------+---------+
| Reference Chord   | 0.646m  |
+-------------------+---------+
| Angle of Attack   | 3.06°   |
+-------------------+---------+
| Angle of Sideslip | 0.0°    |
+-------------------+---------+

I developed a convenience package for ADflow called 
`adflow_util <https://github.com/DavidAnderegg/adflow_util>`_\. It allows to plot the ADflow state variables live in the console and 
handles some annoying stuff like creating the ``output`` folder for ADflow automatically. I will use this 
utility here, but the regular python API, that is detailed in other tutorials, would work aswell.


Files
=====
If you want to use ``adflow_util`` download and install it first:
::

    $ pip install git+https://github.com/DavidAnderegg/adflow_util.git

