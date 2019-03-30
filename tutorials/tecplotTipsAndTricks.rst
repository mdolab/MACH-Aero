.. Various tips and trick using tecplot. Most are small features that might improve the user experience.
   Author: Eirikur Jonsson (eirikurj@umich.edu)


.. _tecplotTipsAndTricks:

Tecplot
=======


Using Custom Color Maps
"""""""""""""""""""""""

For most Tecplot versions a custom color map can be loaded for contour plots. 
Tecplot 2014 R1 does not offer custom color plot option. 


Download
########
You can download the colormaps here (right click -> Save Link As)

Tecplot 2014 R2 and newer:

- :download:`Viridis <./files/viridis_map_tecplot.map>` 
- :download:`Parula <./files/parula_map_tecplot.map>`  

Tecplot 2013 R2 and older:

- :download:`Viridis <./files/viridis_map_tecplot_old.map>` 
- :download:`Parula <./files/parula_map_tecplot_old.map>`  


Install
#######
To use the colormap 

- Run Tecplot and load your data.
- Click the ``Details`` button next to the Contour checkbox.
- Click the setting icon as highlighted in the figure below

     .. image:: ./images/tecplot-custom-color-map.png
        :scale: 50 %

- Select ``Import Color Maps`` and select the downloaded color map
- Once imported select the color map from the adjacent dropdown list

Tips and Tricks
"""""""""""""""

Resetting view
##############

When opening up a CGNS file in tecplot the geometry might be shown in an awkward way all stretched.
This is due the axis settings, scaling and dependencies between axes. To fix this the common solution is to go into ``Plot -> Axis``.

Then set:

- *Dependency* to *XYZ dependent*
- *X to Y ratio* to 1
- *X to Z ratio* to 1

The size factors should automatically be set to one when this is done. This should reset the view.


Resetting view using a macro
############################

When the above procedure is done repeatedly it can become irritating and slow down the user. By making a macro the above steps can be executed quickly with a double click from the *Quick Macro Panel*. To enable the *Quick Macro Panel* in tecplot click ``Scripting -> Quick Macros``

To create the actual macro, edit ``/usr/local/tecplot360ex/tecplot.mcr`` (using *sudo*) with your favorite text editor, for example::

   sudo vi /usr/local/tecplot360ex/tecplot.mcr

Copy the following code block and paste it at the end of file, save and close::

   ############## MDOLAB MACROS ###############
   $!MACROFUNCTION NAME = "MDOLAB - Reset view"
   $!THREEDAXIS AXISMODE = XYZDEPENDENT
   $!THREEDAXIS DEPXTOYRATIO = 1
   $!THREEDAXIS DEPXTOZRATIO = 1
   $!VIEW FITSURFACES
   $!ENDMACROFUNCTION

Restart tecplot and you should see the *MDOLAB - Reset view* macro in the *Quick Macro Panel*.


Partial Border Display on Exported Images
#########################################

Possible fix
$$$$$$$$$$$$

When exporting a single tecplot frame to a .png figure from tecplot gray borders on the right/bottom edges may appear. To fix this issue one can edit the ``/usr/local/tecplot360ex/tecplot.cfg`` file (using *sudo*) and add the following lines to the end of the::

   # To prevent gray boundary when exporting to png
   $!Interface OpenGLConfig {ScreenRendering {AdjustRectangleRightAndBottom = yes}}
   $!Interface OpenGLConfig {ImageRendering {AdjustRectangleRightAndBottom = yes}}

For more information visit https://www.tecplot.com/knowledgebase/2015/02/10/partial-border-display-exported-images-tecplot-360-ex/

Latex workaround
$$$$$$$$$$$$$$$$

Exporting multiple frames may still show these gray borders. A workaround when importing a figure into latex is shown below::

   \begin{figure}
         \includegraphics[width=\linewidth,clip,trim={0cm 0cm 0.1cm 0cm}]{figure.png}
   \end{figure}

This will trim of 0.1cm of the figures right edge.

Inserting LaTex Text
####################

Tecplot now supports LaTex. With tecplot2018 (or a later version), you should be able to insert a LaTex text.
Tecplot has tested the ability against MikTeX and TeXLive, but should be compatible with other LaTex engines.

Adding packages
$$$$$$$$$$$$$$$

Some packages are not pre-intalled with tecplot. To initialize the package in the preamble, edit ``/usr/local/tecplot360ex/tecplot_latex.mcr`` (using *sudo*) with your favorite text editor. For example, if one wants to use ``color``, add ``\usepackage{color}`` to the end of the preamble in the ``tecplot_latex.mcr``::
  
   Preamble=R"(\usepackage{amsfonts}
              \usepackage{amsmath}
              \usepackage{amssymb}
              \usepackage{amsthm}
	      \usepackage{color}
              % replace this LaTeX comment with any additions
             )"

Restart tecplot.
	     
Configure a Licensing Server
""""""""""""""""""""""""""""
To use Tecplot you must specify a license server. To configure, open tecplot and go to ``Help -> Tecplot 360 EX Licensing``, select the ``Network license server`` and fill in the license server name and port number::

    License server name:: license-tecplot.engin.umich.edu
    Port :: 29001

Once you have typed in the information the window should look like

    .. image:: images/tecplotLicense.png
        :scale: 80 %

Tecplot off campus
""""""""""""""""""
In case you are off campus you need to connect using the VPN. Please follow the instructions, :ref:`settingUpUMVPN`. to set up and use the UM VPN. 

For those frequently using Tecplot off campus or have a laptop and do not want to connect using the VPN all the time, a roaming license can be requested. To request a roaming license open Tecplot (either on campus or using the VPN) and go to ``Help -> License roaming...`` and specify the date when the roaming license should expire and click OK. If the request is successful Tecplot can now be used off campus **without** connecting the VPN.




