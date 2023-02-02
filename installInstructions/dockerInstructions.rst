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

Pull one of the MDO Lab Docker images.
The available images are listed in the table below:

======================== ================
Tag                      Operating System
======================== ================
c7-intel-impi-latest     CentOS 7
tacc-u18-gcc-impi-stable Ubuntu 18.04
u20-gcc-ompi-latest      Ubuntu 20.04
u20-gcc-ompi-stable      Ubuntu 20.04
u22-gcc-ompi-latest      Ubuntu 22.04
u22-gcc-ompi-stable      Ubuntu 22.04
======================== ================

To pull an image, use the ``docker pull`` command:

.. prompt:: bash

    docker pull mdolab/public:<TAG>


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
