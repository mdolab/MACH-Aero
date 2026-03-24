.. _dockerInstructions:

Using Docker
============

The MACH framework is packaged within Docker images that can be used to run the software without installing it natively on your machine.
If you are using MACH for the first time, we encourage you to try Docker to avoid installation issues or other inconveniences caused by natively installing the tools.

This guide assumes you are have Docker installed and running on your machine.
If you need to install Docker, you can follow the Docker guide for `Installing the Docker Engine <https://docs.docker.com/engine/install/>`_.
The commands used in this guide may differ depending on your operating system, so refer to the Docker documentation for more details for specific use cases.

Pull MDO Lab Docker Image
-------------------------

Pull one of the `MDO Lab Docker images from Docker Hub <https://hub.docker.com/r/mdolab/public/tags>`_.
The available maintained images are listed in the table below:

=========================  ============  ===================  =====================  ======  =======  ========  =======  =======  ==========
Tag                        OS            Compiler             MPI                    CGNS    PETSc    Python    NumPy    SciPy    OpenMDAO
=========================  ============  ===================  =====================  ======  =======  ========  =======  =======  ==========
u22-gcc-ompi-latest        Ubuntu 22.04  gcc                  OpenMPI 5.0.9          4.5.0   3.21.6   3.12.12   2.3.5    1.17.1   3.42.0
u22-gcc-ompi-stable        Ubuntu 22.04  gcc                  OpenMPI 4.1.6          4.3.0   3.18.5   3.11.14   1.25.2   1.11.2   3.37
u22-intel-impi-latest      Ubuntu 22.04  intel 2024.2.1-1079  intel 2021.11.0-49493  4.5.0   3.21.6   3.12.12   2.3.5    1.17.1   3.42.0
u24-gcc-ompi-latest        Ubuntu 24.04  gcc                  OpenMPI 5.0.9          4.5.0   3.21.6   3.12.12   2.3.5    1.17.1   3.42.0
u24-gcc-ompi-stable        Ubuntu 24.04  gcc                  OpenMPI 4.1.6          4.3.0   3.18.5   3.11.14   1.25.2   1.11.2   3.37
u24-intel-impi-latest      Ubuntu 24.04  intel 2024.2.1-1079  intel 2021.11.0-49493  4.5.0   3.21.6   3.12.12   2.3.5    1.17.1   3.42.0
=========================  ============  ===================  =====================  ======  =======  ========  =======  =======  ==========

To pull an image, use the ``docker pull`` command:

.. prompt:: bash

    docker pull mdolab/public:<TAG>

.. note::
    If you have a Mac with an Apple Silicon CPU (M1, M2, etc.) you will need to pull an image specifically built for ARM architecture, currently the only image with an `arm64` tag is ``mdolab/public:u24-gcc-ompi-stable``.

Check that the Docker image is pulled successfully by running:

.. prompt:: bash

    docker image ls

You should see the image you just pulled.

Initialize Docker Container
---------------------------
Navigate to the directory containing the case you would like to run and initialize the Docker image you downloaded into a container, running interactively:

.. prompt:: bash

    docker run -it --name <NAME> --mount "type=bind,src=<HOST_DIR>,target=<MOUNT_DIR>" <IMAGE> /bin/bash

Replace ``<NAME>`` with the name you would like to give the container, set ``<HOST_DIR>`` to the absolute path to the current directory, and set ``<MOUNT_DIR>`` to ``/home/mdolabuser/mount/``.
Then provide the image tag as ``<IMAGE>``, matching the one downloaded previously: ``mdolab/public:<TAG>``.

When you run this command, you will enter the container and have access to the MACH framework in your specified case directory.

.. note::

    If you are running the MACH tutorials included in this guide using Docker, set the ``<HOST_DIR>`` parameter to the path to the directory where you have cloned the tutorial files.

Exiting and Restarting the Container
------------------------------------
At any point you can exit the container with the command:

.. prompt:: bash

    exit

You can restart the container by running ``start``:

.. prompt:: bash

    docker start <NAME>

Run ``exec`` to enter the container:

.. prompt:: bash

    docker exec -it <NAME> /bin/bash

.. note::
    Running system commands or installing system software inside the container, e.g. using ``apt-get`` requires running ``sudo``, followed by a password.
    The following password can be used in all images, ``temppass``.

Developing in Docker with VS Code
---------------------------------

The VS Code extension ``Remote - Containers`` provides a way for you to spin up a docker container for your projects with the click of a button.
The extension automatically mounts the project folder to the container, so all the changes to the project will persist outside of the container.
Because the containers that are created are based on a configuration file local to your project you will have everything you need for a project defined in one place.
Furthermore, you can share the project with others and they will have an easy way of running your project.
You could also save the image to ensure you can run your project in the future.
Finally, you can use the same docker file to create a singularity image that can be used to run your project on an HPC, how neat is that!

To get started, follow `this tutorial <https://code.visualstudio.com/docs/remote/containers-tutorial>`__.

.. warning::
    If installing on an Ubuntu distro, make sure you use a package manager to install docker, not the ``snap`` install.
    The latter will cause issues with the VS Code extension.
