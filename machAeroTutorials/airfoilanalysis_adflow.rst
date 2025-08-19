.. _airfoilanalysis_adflow:


*************************
Analysis with ADflow
*************************

Introduction
============
Now that we have a valid structured volume mesh, we can start our aerodynamics analysis with ADflow.
There is no graphical user interface for ADflow.
The cases are prepared with python scripts and run from the command line.
In this section of the tutorial, we will explain the nuts and bolts of a basic ADflow runscript.
You will find a complete introduction to ADflow in the :doc:`docs <adflow:introduction>`.

Files
=====

Navigate to the directory ``airfoil/analysis`` in your tutorial folder. 
Copy the CGNS mesh file, ``n0012.cgns``, generated previously, into the directory:

.. prompt:: bash

    cp ../mesh/n0012.cgns . 

Create the following empty runscript in the current directory:

- ``airfoil_run.py``


Dissecting the airfoil analysis script
==============================================
Open the file ``airfoil_run.py`` in your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Imports
    :end-before: # rst Args

First we import ADflow.
We also need to import ``baseclasses``, which is a library of problem and solver classes used to encourage a common API within the MACH suite.
In this case we will be using the AeroProblem, which is a container for the flow conditions that we want to analyze.
Finally, it is convenient to import the mpi4py library to prevent printing multiple times if we are running on multiple processors.
Importing mpi4py is not entirely necessary in the runscript because ADflow does it internally if necessary.

Adding command line arguments
-----------------------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Args
    :end-before: # rst ADflow options

This is a convenience feature that allows the user to pass in command line arguments to the script.
Four options are provided:

-  Output directory
-  Grid file to be used
-  Task to execute

ADflow options
-------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst ADflow options
    :end-before: # rst Start ADflow

Now we set the ADflow solver configuration dictionary.
In this example, we only set the bare essential settings.
In reality, ADflow has a huge number of settings and any that do not appear in the options dictionary will be left to their defaults.
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
------------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Start ADflow
    :end-before: # rst Create AeroProblem

We now initialize ADflow as a object and pass it the options dictionary.
When ADflow is instantiated, it reads in the mesh and then waits for the user to dictate further operations.


Set flow conditions
------------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Create AeroProblem
    :end-before: # rst Run ADflow

The flow conditions and any auxiliary information about the geometry (such as reference dimensions) are provided to ADflow by way of an AeroProblem.
The AeroProblem automatically generates complete flow state information from the Mach number and altitude based on the 1976 U.S. Standard Atmosphere.
The ``alpha`` parameter is used to rotate the flow in the far-field to simulate angle-of-attack.
The ``evalFuncs`` parameter stipulates which functions the user would like to compute from the converged flow solution.
Some available functions include ``'cl'``, ``'cd'``, ``'cmz'``, ``'lift'``, and ``'drag'``.


Single analysis
---------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Run ADflow
    :end-before: # rst Create polar arrays

Running the solver is very simple, it only requires an AeroProblem to run.
The function evaluation is done separately from the solution.
We pass a dictionary to ADflow and it will populate it with the prescribed functions.
We can request additional functions with the ``evalFuncs`` parameter.
Finally we print out the requested functions on the root proc.

Generating Drag Polars
----------------------
The other task is to generate a drag polar, which shares the same ADflow setup as the previous task.
The only difference is that the analysis is now done within a loop.


.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Create polar arrays
    :end-before: # rst Start loop

We start by creating a list of the angle of attack values that we wish to analyze.
In this case we use the ``numpy.linspace`` function to create a uniformly-spaced array with six whole number entries from 0 -- 5.
We also create the empty lists for storing the lift and drag coefficients. 
The lift and drag data will be appended to these lists as the flow solutions are completed.


.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Start loop
    :end-before: # rst update AP

Having created the input array and data storage lists, we can now loop over the desired angles of attack to evaluate the polar.
We accomplish this by using the builtin ``for`` loop structure in python.


.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst update AP
    :end-before: # rst Run ADflow polar

Now for each angle of attack, we update two attributes of the aero problem.
We update the name to include the current angle of attack.
This allow the filenames of the lift distribution, slices, volume solution and surface solution to be updated with the current angle of attack, making it easier to keep track of the output files.
We also update the alpha parameter, which is the attribute of the AeroProblem that represents the angle of attack.


.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Run ADflow polar
    :end-before: # rst Print polar

Running the solver is identical to the simple single point example. 
We simply call the ``CFDSolver`` instance with the current AeroProblem.
This causes the CFD solver to be updated with the values of that AeroProblem prior to solving the flow.
We then use the same ``EvalFunctions`` call to integrate the surface forces to get the lift and drag coefficients.
The difference is that here, we append the coefficients from ``funcs`` into the ``CLList`` and ``CDList`` variables, so that they can be used later.


.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Print polar

Once we complete the loop and evaluate all of the desired flow conditions, we can print the completed data set to the screen.


Run it yourself!
================
First we run the analysis task, which is the default ``task``:

.. prompt:: bash

    mpirun -np 4 python airfoil_run.py


ADflow will print to the terminal various information during the initialization stages before starting the solution process.
Once the solution process starts the terminal should show information about the convergence history of the variables specified in ``monitorvariables``, in addition to the total residual.
The solver terminates either by reaching the maximum number of iterations or a reduction in the total residual is specified by the ``L2Convergence`` option::

    #
    # Grid 1: Performing 1000 iterations, unless converged earlier. Minimum required iteration before NK switch:      5. Switch to NK at totalR of:   6.18E+02
    #
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  Grid  | Iter | Iter |  Iter  |   CFL   | Step | Lin  |        Res rho         |         C_lift         |        C_drag          |        totalRes        |
    #  level |      | Tot  |  Type  |         |      | Res  |                        |                        |                        |                        |
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
        1       0      0     None     ----    ----   ----   7.7435230845577107E+03   3.5011993069732554E-03   4.3195197788935208E-01   6.1844676631565355E+06 
        1       1      3     *ANK   5.00E+00  0.14  0.002   6.7945187231395375E+03   1.9219926068650264E-02   4.4816264291116603E-01   5.4829557821402745E+06 
        1       2      8      ANK   5.00E+00  0.24  0.012   5.5226898609721093E+03   4.3558605608723461E-02   4.6739663346390026E-01   4.4824534098928915E+06 
        1       3     14      ANK   5.00E+00  0.33  0.015   4.2696552026427880E+03   6.9922598388306001E-02   4.8200465163751222E-01   3.4717353703403827E+06 
        1       4     21      ANK   5.00E+00  0.36  0.025   3.3684086266089989E+03   8.9660704465998123E-02   4.8618681812154535E-01   2.7404984226656561E+06 
        1       5     24     *ANK   5.00E+00  0.41  0.002   2.6723093737622539E+03   1.0424159093415895E-01   4.8173893557085712E-01   2.1744745862484900E+06 
        1       6     28      ANK   5.00E+00  0.49  0.035   2.0944506662304429E+03   1.1519855884106124E-01   4.6969914659287670E-01   1.7088810555934941E+06 
        1       7     34      ANK   5.00E+00  0.53  0.020   1.6627378795251541E+03   1.2134687502813479E-01   4.5233845013799778E-01   1.3663470695925625E+06 
        1       8     37     *ANK   1.59E+01  0.19  0.016   1.3909675309529173E+03   1.2253679979394382E-01   4.3752608026325468E-01   1.1592292712072381E+06 
        1       9     42      ANK   1.59E+01  0.26  0.027   1.1018301791444205E+03   1.2380490860652416E-01   4.1954537559996141E-01   9.3083826935877977E+05 
        1      10     48      ANK   1.59E+01  0.33  0.047   8.3333839070697195E+02   1.2504688676930392E-01   3.9953208997557921E-01   7.0997724832861568E+05 
        1      11     56      ANK   1.59E+01  0.36  0.031   6.1971541521071833E+02   1.2609214574286817E-01   3.7982220151850465E-01   5.2986333302179212E+05 
        1      12     59     *ANK   1.59E+01  0.43  0.019   4.3863172391842227E+02   1.2706394874047972E-01   3.5943046643297011E-01   3.7466389115405828E+05 
        1      13     63      ANK   1.59E+01  0.42  0.034   3.1832975430121587E+02   1.2765618615213475E-01   3.4336971000148553E-01   2.7227531180866656E+05 
        1      14     68      ANK   1.59E+01  0.43  0.045   2.3048765487442645E+02   1.2807151962281899E-01   3.2955236795579484E-01   1.9882730564546149E+05 
        1      15     72     *ANK   6.69E+01  0.18  0.028   1.8939187879358792E+02   1.2745868348693445E-01   3.1498457137361363E-01   1.6598119170463725E+05 
        1      16     77      ANK   6.69E+01  0.28  0.042   1.3875193988748788E+02   1.2622950939887778E-01   2.9337803361021114E-01   1.2646396583243270E+05 
        1      17     85      ANK   6.69E+01  0.28  0.029   1.0601764702615763E+02   1.2458283384644310E-01   2.7270445313002917E-01   1.0165916803021115E+05 
        1      18     94      ANK   6.69E+01  0.30  0.037   8.8968499847853920E+01   1.2270705344290511E-01   2.5260667382692864E-01   8.8577981662129081E+04 
        1      19     99     *ANK   6.69E+01  0.36  0.034   8.2699878724372908E+01   1.2048211883596763E-01   2.3031139747204735E-01   8.2974084038077897E+04 
        1      20    104      ANK   6.69E+01  0.44  0.044   8.4168663841265683E+01   1.1810912354771165E-01   2.0453003000336448E-01   8.2724649857764220E+04 
        1      21    110      ANK   6.69E+01  0.50  0.022   8.6541510290806045E+01   1.1672084108227974E-01   1.7812314491530568E-01   8.3029327612322275E+04 
        1      22    116      ANK   6.69E+01  0.59  0.029   8.5431720228366387E+01   1.1636482700813880E-01   1.5155624087205083E-01   8.0102676511803191E+04 
        1      23    122      ANK   6.69E+01  0.69  0.032   7.8699422365489013E+01   1.1728177489086072E-01   1.2596307675063051E-01   7.2265445402101555E+04 
        1      24    128      ANK   6.69E+01  0.93  0.029   6.4181205697680298E+01   1.1987670131934980E-01   1.0025648766008335E-01   5.7927940527841114E+04 
        1      25    134      ANK   6.69E+01  1.00  0.035   4.6594670792423450E+01   1.2438102726425990E-01   8.2849204608775012E-02   4.2024497784053718E+04 
        1      26    141     *ANK   2.24E+02  1.00  0.019   2.5051574522809734E+01   1.5021649973751730E-01   5.9366457927657906E-02   2.7712314035092593E+04 
        1      27    147      ANK   2.24E+02  1.00  0.041   1.6837157198117083E+01   1.6574432714219445E-01   5.0752621821674684E-02   1.9273867535826979E+04 
        1      28    154     *ANK   7.80E+02  1.00  0.041   1.2222447662745466E+01   1.9198098002486857E-01   3.3115459604629402E-02   1.6471098460525489E+04 
        1      29    161      ANK   7.80E+02  1.00  0.038   1.6298221794987683E+01   2.1817808024518348E-01   1.9916373723001368E-02   1.6117019753865288E+04 
        1      30    170      ANK   7.80E+02  0.46  0.046   1.7483597596386318E+01   2.2693692610711541E-01   1.6114813491608371E-02   1.6367030955945766E+04 
        1      31    177      ANK   7.80E+02  0.95  0.041   1.8859198998587665E+01   2.4420237169550635E-01   9.8244572761843375E-03   1.6707781485365093E+04 
        1      32    185      ANK   7.80E+02  0.83  0.038   1.8243993107672559E+01   2.5647230543613209E-01   7.4947229999616019E-03   1.5932372842353589E+04 
        1      33    193      ANK   7.80E+02  0.90  0.042   1.6327537195967320E+01   2.6348011695855783E-01   7.5833432472369733E-03   1.4220177711256705E+04 
        1      34    201      ANK   7.80E+02  0.97  0.046   1.3881397469236283E+01   2.6579712037133796E-01   9.8255521513757951E-03   1.2110929001647592E+04 
        1      35    209      ANK   7.80E+02  1.00  0.050   1.1376742921573351E+01   2.6324563761472725E-01   1.3008315684452775E-02   9.9254784009444138E+03 
        1      36    218      ANK   7.80E+02  1.00  0.043   9.3579731823862762E+00   2.5559487867915387E-01   1.5515068640028124E-02   8.1270660856133900E+03 
        1      37    226     *ANK   2.95E+03  1.00  0.045   8.7058134500720605E+00   2.5167425083604200E-01   1.3910571753710469E-02   7.7544286087581404E+03 
        1      38    234      ANK   2.95E+03  1.00  0.033   7.1231305054949976E+00   2.5958381932995617E-01   1.2566056091901260E-02   6.2287595591438767E+03 
        1      39    242      ANK   2.95E+03  1.00  0.038   5.4345342251514879E+00   2.6828020439819683E-01   1.1789693982527575E-02   4.7377508087922251E+03 
        1      40    250      ANK   2.95E+03  1.00  0.040   4.4470623607932129E+00   2.7295682671165628E-01   1.1693356793751811E-02   3.8564721770505312E+03 
        1      41    274     *ANK   9.91E+03  0.00  0.033   4.4470623607932147E+00   2.7295682671165628E-01   1.1693356793751811E-02   3.8564721770505321E+03 
        1      42    297     *ANK   4.95E+03  0.00  0.045   4.4470623607932147E+00   2.7295682671165628E-01   1.1693356793751811E-02   3.8564721770505334E+03 
        1      43    307     *ANK   2.48E+03  1.00  0.035   4.3728850864902391E+00   2.7133221181466410E-01   1.2946920642176403E-02   3.7329213874421835E+03 
        1      44    316      ANK   2.48E+03  1.00  0.042   3.3361274315554237E+00   2.7253948112577131E-01   1.3459527035483979E-02   2.8526996944618113E+03 
        1      45    324      ANK   2.48E+03  1.00  0.049   2.0309290942899292E+00   2.7461037544593914E-01   1.3424276880490499E-02   1.7681794293682603E+03 
        1      46    347     *ANK   8.62E+03  0.00  0.032   2.0309290942899287E+00   2.7461037544593914E-01   1.3424276880490499E-02   1.7681794293682606E+03 
        1      47    360     *ANK   4.31E+03  0.34  0.026   2.0420851586365902E+00   2.7632031459267725E-01   1.3147915051498817E-02   1.7666697465702259E+03 
        1      48    368      ANK   4.31E+03  1.00  0.050   1.5428329907363620E+00   2.7855924039852420E-01   1.2805031695477559E-02   1.3449150780587775E+03 
        1      49    377      ANK   4.31E+03  1.00  0.041   1.1358694377521008E+00   2.7936222772424990E-01   1.2949433960464142E-02   9.9095701565099387E+02 
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  Grid  | Iter | Iter |  Iter  |   CFL   | Step | Lin  |        Res rho         |         C_lift         |        C_drag          |        totalRes        |
    #  level |      | Tot  |  Type  |         |      | Res  |                        |                        |                        |                        |
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
        1      50    385      ANK   4.31E+03  1.00  0.045   7.0215345675828134E-01   2.7941565347725977E-01   1.3146512708582180E-02   6.1390272598944034E+02 
        1      51    394      *NK     ----    1.00  0.254   1.9275996836673603E-01   2.8029832556924711E-01   1.3263112273449125E-02   1.5776583192012410E+02 
        1      52    417       NK     ----    1.00  0.134   4.5057579197132040E-02   2.8474135492109282E-01   1.3201658852899634E-02   2.6909898679162541E+01 
        1      53    479       NK     ----    1.00  0.078   9.1573840687545448E-03   2.8648745539602416E-01   1.3257641727754146E-02   3.7981315399189892E+00 
        1      54    539       NK     ----    1.00  0.041   7.1478713945336881E-04   2.8674410534033962E-01   1.3261722813129513E-02   4.2226225454601196E-01 
        1      55    601       NK     ----    1.00  0.044   6.6493084467565187E-05   2.8672831762181628E-01   1.3262876751834766E-02   1.8754020905752102E-02 
        1      56    663       NK     ----    1.00  0.095   5.5211815099735919E-06   2.8672389259050796E-01   1.3262710510837175E-02   1.7890839595500301E-03 
        1      57    725       NK     ----    1.00  0.063   4.0029492865346096E-07   2.8672450857594478E-01   1.3262723174075756E-02   1.1301764706676297E-04 
        1      58    787       NK     ----    1.00  0.045   1.7256278256408886E-08   2.8672448823756219E-01   1.3262722837467619E-02   5.1141474331540129E-06 
        1      59    849       NK     ----    1.00  0.091   1.6525462096100757E-09   2.8672448921188942E-01   1.3262722851025950E-02   4.6522577057575730E-07 
        1      60    911       NK     ----    1.00  0.101   1.5582220887448603E-10   2.8672448931881295E-01   1.3262722856165147E-02   4.7136065512343082E-08 
        1      61    973       NK     ----    1.00  0.060   1.0440088849389754E-11   2.8672448930210082E-01   1.3262722855760446E-02   4.5210454775745827E-09 
        
A the end of the terminal output the functions defined in ``evalFuncs``  are printed to the screen::

    {'airfoil_cd': 0.013262722855760448, 'airfoil_cl': 0.28672448930210087}

Next, run the ``polar`` task:

.. prompt:: bash

    mpirun -np 4 python aero_run.py --task polar --output polar


The final table should look something like::

     Alpha       CL       CD
    ========================
        0.0   0.0000   0.0088
        1.0   0.1930   0.0103
        2.0   0.3750   0.0179
        3.0   0.5108   0.0310
        4.0   0.5453   0.0443
        5.0   0.5347   0.0568

Postprocessing the solution output
==================================
All output is found in the ``output`` directory.
The solutions file (``.dat``, ``.cgns`` or ``.plt``) can be viewed in Tecplot.
