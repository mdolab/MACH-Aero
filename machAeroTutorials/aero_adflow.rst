.. _aero_adflow:

********************
Analysis with ADflow
********************

Introduction
============
Now that we have a valid structured volume mesh, we can start our aerodynamics analysis with ADflow.
There is no graphical user interface for ADflow.
The cases are prepared with python scripts and run from the command line.
In this section of the tutorial, we will explain the nuts and bolts of a basic ADflow runscript.
You will find a complete introduction to ADflow in the :doc:`docs <adflow:introduction>`.
For this tutorial we will use the L3 mesh that we generated in the previous step.
L1 meshes are what is typically used for analysis but we want to limit computational time for the purpose of this tutorial.

Files
=====
Navigate to the directory ``aero/analysis`` in your tutorial folder.
Copy the following file from the volume meshing directory:

.. prompt:: bash

    cp ../meshing/volume/wing_vol_L3.cgns .

Create the following empty runscript in the current directory:

- ``aero_run.py``


Dissecting the ADflow runscript
===============================
Open the file ``aero_run.py`` with your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :start-after: # rst Imports
   :end-before: # rst ADflow options

This section is identical to the one shown in :ref:`the airfoil analysis tutorial <airfoilanalysis_adflow>`.
We import ADflow and baseclasses among several other things.

Adding command line arguments
-----------------------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Args
    :end-before: # rst ADflow options

This is a convenience feature that allows the user to pass in command line arguments to the script.
Three options are provided:

-  Output directory
-  Grid file to be used
-  Task to execute

ADflow options
--------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :start-after: # rst ADflow options
   :end-before: # rst Start ADflow

We will use the same ADflow solver settings that we used in the :ref:`the airfoil analysis tutorial <airfoilanalysis_adflow>`.
An exhaustive list of the ADflow options and their descriptions can be found `in the docs <https://mdolab-adflow.readthedocs-hosted.com/en/latest/options.html>`_.
We strongly recommend going over the descriptions and tips on solvers and solver options in the ADflow :doc:`solvers docs <adflow:solvers>`.
A basic overview of the options used in this example are provided here.

`I/O Parameters`
    We include the mesh file, the output directory, and the variables that will be printed as the solver runs.

`Physics Parameters`
    We set the equation type that ADflow will solve which in this case will be RANS.

`Solver Parameters`
    We typically select the smoother (RK or DADI) and multigrid settings for the explicit solver.
    However we will be using the implicit solver in this example so we just set the number of turburlence sub-iterations to 10 and turn off multigrid.
    For most practical problems we use the Approximate Newton-Krylov (ANK) and Newton-Krylov (NK) solvers to speed up convergence and increase the robustness of the solver.

`ANK Solver Parameters`
    We will simply turn on the ANK solver

`NK Solver Parameters`
    We will turn on the NK solver and request that ADflow switch to it from ANK at a specific relative tolerance.

`Termination Criteria`
    We set the termination criteria of the solver based on relative convergence of the norm of the residuals or maximum number of iterations.

Create solver
-------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :start-after: # rst Start ADflow
   :end-before: # rst Create AeroProblem

When ADflow is instantiated, it reads in the mesh and then waits for the user to dictate further operations.
Before running the case, we can choose to set up some additional output options.
First, ADflow can write a file containing distribution data over the extent of the wing (e.g. lift, drag, twist) using ``addLiftDistribution``.
Also, ADflow can write airfoil data for a given set of slices along the wing using `addSlices`.

Set flow conditions
-------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Create AeroProblem
    :end-before: # rst Run ADflow

The flow conditions and any auxiliary information about the geometry (such as reference dimensions) are provided to ADflow by way of an AeroProblem.
The AeroProblem automatically generates complete flow state information from the Mach number and altitude based on the 1976 U.S. Standard Atmosphere.
The ``alpha`` parameter is used to rotate the flow in the far-field to simulate angle-of-attack.
The ``evalFuncs`` parameter stipulates which functions the user would like to compute from the converged flow solution.
Some available functions include ``'cl'``, ``'cd'``, ``'cmz'``, ``'lift'``, and ``'drag'``.

Single analysis
---------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Run ADflow
    :end-before: # rst Create polar arrays

The solver is run the same way it was for the airfoil analysis.
We print out the requested functions on the root proc.

Generating Drag Polars
----------------------
The other task is to generate a drag polar, which shares the same ADflow setup as the previous task.
The only difference is that the analysis is now done within a loop.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Create polar arrays
    :end-before: # rst Start loop

We start by creating a list of the angle of attack values that we wish to analyze.
In this case we use the ``numpy.linspace`` function to create a uniformly-spaced array with six whole number entries from 0 -- 5.
We also create the empty lists for storing the lift and drag coefficients.
The lift and drag data will be appended to these lists as the flow solutions are completed.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Start loop
    :end-before: # rst update AP

Having created the input array and data storage lists, we can now loop over the desired angles of attack to evaluate the polar.
We accomplish this by using the builtin ``for`` loop structure in python.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst update AP
    :end-before: # rst Run ADflow polar

Now for each angle of attack, we update two attributes of the aero problem.
We update the name to include the current angle of attack.
This allow the filenames of the lift distribution, slices, volume solution and surface solution to be updated with the current angle of attack, making it easier to keep track of the output files.
We also update the alpha parameter, which is the attribute of the AeroProblem that represents the angle of attack.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Run ADflow polar
    :end-before: # rst Print polar

Running the solver is identical to the simple single point example.
We simply call the ``CFDSolver`` instance with the current AeroProblem.
This causes the CFD solver to be updated with the values of that AeroProblem prior to solving the flow.
We then use the same ``EvalFunctions`` call to integrate the surface forces to get the lift and drag coefficients.
The difference is that here, we append the coefficients from ``funcs`` into the ``CLList`` and ``CDList`` variables, so that they can be used later.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Print polar

Once we complete the loop and evaluate all of the desired flow conditions, we can print the completed data set to the screen.



Run it yourself!
================
First we run the analysis task, which is the default ``task``:

.. prompt:: bash

    mpirun -np 4 python aero_run.py


ADflow will print to the terminal various information during the initialization stages before starting the solution process.
Once the solution process starts the terminal should show information about the convergence history of the variables specified in ``monitorvariables``, in addition to the total residual.
The solver terminates either by reaching the maximum number of iterations or a reduction in the total residual is specified by the ``L2Convergence`` option::

    #
    # Grid 1: Performing 1000 iterations, unless converged earlier. Minimum required iteration before NK switch:      5. Switch to NK at totalR of:   8.57E+02
    #
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  Grid  | Iter | Iter |  Iter  |   CFL   | Step | Lin  |        Res rho         |         C_lift         |        C_drag          |        totalRes        |
    #  level |      | Tot  |  Type  |         |      | Res  |                        |                        |                        |                        |
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
        1       0      0     None     ----    ----   ----   4.5760880850983540E+03   9.4948769161599597E-04   1.2173162187172898E-01   8.5728159111749921E+06 
        1       1      3     *ANK   5.00E+00  0.14  0.002   3.9679631958491655E+03   1.7537610979047276E-02   1.4288470429589364E-01   7.5050033612243887E+06 
        1       2      8      ANK   5.00E+00  0.26  0.009   3.1171223433649261E+03   4.3716865105597892E-02   1.7353266092650765E-01   5.9157234909154158E+06 
        1       3     13      ANK   5.00E+00  0.32  0.035   2.3699050613709455E+03   6.8010731519896200E-02   2.0044710639367061E-01   4.4974285684760632E+06 
        1       4     19      ANK   5.00E+00  0.34  0.034   1.8029132070105472E+03   8.6179435819707995E-02   2.1934689225220694E-01   3.4149124881035890E+06 
        1       5     22     *ANK   5.00E+00  0.38  0.002   1.3206410159977643E+03   9.9537161344425903E-02   2.3219335667643443E-01   2.4831543544889279E+06 
        1       6     26      ANK   5.00E+00  0.46  0.014   9.0889949792115658E+02   1.0958023297824177E-01   2.4064582104444554E-01   1.6937163734136217E+06 
        1       7     29     *ANK   1.60E+01  0.24  0.007   6.9909664261075181E+02   1.1185473627720038E-01   2.3836667159480979E-01   1.3015605402722002E+06 
        1       8     33      ANK   1.60E+01  0.30  0.027   5.0423804442511863E+02   1.1419212425389599E-01   2.3484525594643657E-01   9.3550673644135345E+05 
        1       9     38      ANK   1.60E+01  0.37  0.033   3.3109178764540275E+02   1.1633909479884250E-01   2.2933056623741732E-01   6.1090855258631264E+05 
        1      10     41     *ANK   1.60E+01  0.75  0.013   1.1836781896183199E+02   1.1857390476257375E-01   2.1466090801128215E-01   2.1746268220285341E+05 
        1      11     45     *ANK   7.03E+01  0.27  0.026   9.1125429870865901E+01   1.2455620187572600E-01   1.9609187028311442E-01   1.6613907954926230E+05 
        1      12     49      ANK   7.03E+01  0.29  0.046   7.2854203357871413E+01   1.3096330845423412E-01   1.7861879775152983E-01   1.3179027480889054E+05 
        1      13     54      ANK   7.03E+01  0.28  0.045   6.1691847950250988E+01   1.3797506810648708E-01   1.6287468478337511E-01   1.1114028085404509E+05 
        1      14     60      ANK   7.03E+01  0.32  0.029   5.3812892251593532E+01   1.4743178315984540E-01   1.4663574635008658E-01   9.7243041620139658E+04 
        1      15     64     *ANK   7.03E+01  0.46  0.034   4.6325044295277344E+01   1.6191818379650993E-01   1.2723126806585017E-01   8.5340123378121061E+04 
        1      16     68      ANK   7.03E+01  0.65  0.044   3.7813558075872201E+01   1.8306104497612510E-01   1.0458483596385845E-01   7.3807101680342530E+04 
        1      17     73      ANK   7.03E+01  1.00  0.022   2.6252660248899119E+01   2.2191338460882476E-01   7.6898300173845704E-02   5.8536992385465470E+04 
        1      18     78      ANK   7.03E+01  1.00  0.028   1.6250470715938114E+01   2.6358639835798969E-01   6.0246136161691256E-02   4.1865570325607812E+04 
        1      19     83     *ANK   2.61E+02  1.00  0.043   1.3717127706500461E+01   3.4574372192704905E-01   3.5464974788251162E-02   4.1815825205397021E+04 
        1      20     88      ANK   2.61E+02  1.00  0.040   9.5563171634005748E+00   4.0484491791222060E-01   2.4292741356896130E-02   3.0330365462563317E+04 
        1      21     94      ANK   2.61E+02  1.00  0.034   7.4712098349400264E+00   4.4321417662451390E-01   2.1553708434763591E-02   2.1674050900269729E+04 
        1      22    101      ANK   2.61E+02  1.00  0.044   6.5109626351731889E+00   4.5951615580281946E-01   2.2087812854262506E-02   1.6756648041082062E+04 
        1      23    120     *ANK   1.04E+03  0.01  0.044   6.5071096403318567E+00   4.5957533691744179E-01   2.2059882651482687E-02   1.6737580178263084E+04 
        1      24    135      ANK   1.04E+03  0.06  0.043   6.4942544198878158E+00   4.5981634065269644E-01   2.1946442997196725E-02   1.6743643580330863E+04 
        1      25    150      ANK   1.04E+03  0.06  0.042   6.4832165791516587E+00   4.6004261924428214E-01   2.1836774484840112E-02   1.6750146713744234E+04 
        1      26    164      ANK   1.04E+03  0.08  0.040   6.4711342957866851E+00   4.6034768125010705E-01   2.1684736160627306E-02   1.6762298914109168E+04 
        1      27    177      ANK   1.04E+03  0.12  0.037   6.4613422238276073E+00   4.6075060015755698E-01   2.1476668711852869E-02   1.6779638731460818E+04 
        1      28    190      ANK   1.04E+03  0.12  0.034   6.4606614830799574E+00   4.6111097564347614E-01   2.1282006566616767E-02   1.6788067449240807E+04 
        1      29    202      ANK   1.04E+03  0.17  0.031   6.4736950901517858E+00   4.6156913229454327E-01   2.1023974628519349E-02   1.6792803608832848E+04 
        1      30    212      ANK   1.04E+03  0.34  0.029   6.5662660084598654E+00   4.6234631450599406E-01   2.0554699440536166E-02   1.6826229846384926E+04 
        1      31    220      ANK   1.04E+03  0.70  0.027   6.8266118433162442E+00   4.6333609537501030E-01   1.9819811184226648E-02   1.6703831009060345E+04 
        1      32    227      ANK   1.04E+03  1.00  0.033   6.6864869810165448E+00   4.6340585576159532E-01   1.9294241993376891E-02   1.5133773873503615E+04 
        1      33    232     *ANK   1.30E+03  1.00  0.046   5.9416081378350816E+00   4.6229165389361937E-01   1.9047801044987822E-02   1.2762251914357010E+04 
        1      34    237      ANK   1.30E+03  1.00  0.033   4.7429528427361252E+00   4.6119152365733074E-01   1.9086602567357329E-02   1.0117133670527639E+04 
        1      35    242      ANK   1.30E+03  1.00  0.046   3.9365570522451669E+00   4.5992160517078251E-01   1.9175019948332352E-02   8.5106428019587256E+03 
        1      36    248      ANK   1.30E+03  1.00  0.045   3.9370842460083981E+00   4.5792531659306207E-01   1.9122895930275486E-02   8.5620897860534915E+03 
        1      37    254      ANK   1.30E+03  1.00  0.045   3.6141129284594760E+00   4.5562242000904740E-01   1.9030451823249361E-02   7.8387657851526501E+03 
        1      38    260      ANK   1.30E+03  1.00  0.047   3.1231316588682017E+00   4.5319001087354782E-01   1.8889286949177790E-02   6.7332314379643785E+03 
        1      39    266     *ANK   4.66E+03  1.00  0.042   2.7990460500382648E+00   4.5021645139500999E-01   1.8541917448272726E-02   6.0521223620195424E+03 
        1      40    272      ANK   4.66E+03  1.00  0.046   2.5158523690883947E+00   4.4676965980407507E-01   1.8260399142678692E-02   5.4084605812692216E+03 
        1      41    278      ANK   4.66E+03  1.00  0.043   2.0484935116594376E+00   4.4338628675383307E-01   1.8046795319939395E-02   4.5490626899207300E+03 
        1      42    284      ANK   4.66E+03  1.00  0.039   1.5421434236634035E+00   4.4018180601766554E-01   1.7886210428336727E-02   3.6197597850599914E+03 
        1      43    290      ANK   4.66E+03  1.00  0.039   1.2812321653201908E+00   4.3724440234215106E-01   1.7772222091637063E-02   2.9144114355022693E+03 
        1      44    296     *ANK   1.72E+04  1.00  0.037   1.1852510246941101E+00   4.3459739618028531E-01   1.7676856600067712E-02   2.5020449627126800E+03 
        1      45    303      ANK   1.72E+04  1.00  0.022   1.0945623485429916E+00   4.3168394332416110E-01   1.7578373573632504E-02   2.3644997771821381E+03 
        1      46    309      ANK   1.72E+04  1.00  0.047   8.6484955978338218E-01   4.2961818408796204E-01   1.7535093061909309E-02   2.0178315702726600E+03 
        1      47    315      ANK   1.72E+04  1.00  0.039   7.3487342662398769E-01   4.2805316500733970E-01   1.7490930659281839E-02   1.7612763302510132E+03 
        1      48    321      ANK   1.72E+04  1.00  0.040   6.6478547609931393E-01   4.2692117426185555E-01   1.7452822293910309E-02   1.4971609458654380E+03 
        1      49    327      ANK   1.72E+04  1.00  0.043   5.8292974814115939E-01   4.2608649291580714E-01   1.7419952545412679E-02   1.2372705914316994E+03 
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  Grid  | Iter | Iter |  Iter  |   CFL   | Step | Lin  |        Res rho         |         C_lift         |        C_drag          |        totalRes        |
    #  level |      | Tot  |  Type  |         |      | Res  |                        |                        |                        |                        |
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
        1      50    333     *ANK   6.47E+04  1.00  0.043   4.7831463269643004E-01   4.2543592168424560E-01   1.7390435805140249E-02   1.0057155399695830E+03 
        1      51    339      ANK   6.47E+04  1.00  0.047   3.6926569897752548E-01   4.2491669813999461E-01   1.7366998838599695E-02   8.1748852939009623E+02 
        1      52    349      *NK     ----    0.16  0.285   3.1463424290774855E-01   4.2478397671579232E-01   1.7359055140522262E-02   7.0008955777128620E+02 
        1      53    353       NK     ----    0.22  0.630   2.7411283735301312E-01   4.2474909652992932E-01   1.7361051793538109E-02   6.1173005820145602E+02 
        1      54    357       NK     ----    0.33  0.684   2.2865359465126406E-01   4.2469684770627930E-01   1.7362499189754826E-02   5.1287529715733911E+02 
        1      55    361       NK     ----    1.00  0.700   1.6939197915889270E-01   4.2445349377345443E-01   1.7349848235219442E-02   3.5968072596233537E+02 
        1      56    367       NK     ----    1.00  0.598   1.0823270187253292E-01   4.2398190900333566E-01   1.7310271175799030E-02   2.1750453405571128E+02 
        1      57    375       NK     ----    1.00  0.388   3.9803477756788809E-02   4.2371811630298661E-01   1.7294054488295844E-02   8.5092973277057425E+01 
        1      58    389       NK     ----    1.00  0.273   1.1476810178887591E-02   4.2347679059913895E-01   1.7275728060226571E-02   2.5322003178368682E+01 
        1      59    409       NK     ----    1.00  0.138   2.4309321438236520E-03   4.2348492120367293E-01   1.7282272025832192E-02   3.7021505779273607E+00


A the end of the terminal output the functions defined in ``evalFuncs``  are printed to the screen::

    {'wing_cd': 0.0172822720258322, 'wing_cl': 0.423484921203673}

Next, run the ``polar`` task:

.. prompt:: bash

    mpirun -np 4 python aero_run.py --task polar --output polar


The final table should look something like::

     Alpha       CL       CD
    ========================
        0.0   0.2320   0.0113
        1.0   0.3607   0.0147
        2.0   0.4819   0.0207
        3.0   0.5777   0.0292
        4.0   0.6460   0.0397
        5.0   0.6971   0.0523


Postprocessing the solution output
==================================
All output is found in the ``output`` directory.
The solutions file (``.dat``, ``.cgns`` or ``.plt``) can be viewed in the Tecplot.
A contour plot of the pressure coefficient using the surface ``.plt`` is shown below.

.. figure:: images/aero_wing_analysis_cp_contour.png
    :scale: 20
    :align: center
    :alt: Pressure coefficient
    :figclass: align-center

The lift and slice files (``.dat``) can also be viewed in tecplot or parsed directly and plotted e.g. matplotlib.
From the lift file we show the spanwise normalized lift, compared to elliptical lift, as well as the twist distribution and t/c.

.. figure:: images/aero_wing_analysis_lift.png
    :scale: 50
    :align: center
    :alt: Lift file
    :figclass: align-center

For the slice file, here the normalized airfoil shape and pressure coefficient are shown.

.. figure:: images/aero_wing_analysis_slices.png
    :scale: 50
    :align: center
    :alt: Slice file
    :figclass: align-center
