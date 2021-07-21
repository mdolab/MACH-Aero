.. _dockerInstructions:

Using Docker
============

This guide assumes you are working with Ubuntu 20.04 LTS and have Docker installed and running.
The commands may differ depending on the operating system.
If you need to install Docker on your machine, you can follow the Docker guide for `Installing the Docker Engine <https://docs.docker.com/engine/install/>`_.

Pull MDO Lab Docker Image
-------------------------

Pull one of the MDO Lab Docker images.
The available images are listed in the table below:

======================== ================
Tag                      Operating System
======================== ================
c7-intel-impi-latest     CentOS 7
u20-gcc-ompi-latest      Ubuntu 20.04
u20-gcc-ompi-stable      Ubuntu 20.04
tacc-u18-gcc-impi-stable Ubuntu 18.04
======================== ================

To pull an image, use the ``docker pull`` command:

.. code-block:: bash

    $ docker pull mdolab/public:<TAG>


Check that the Docker image is pulled successfully by running:

.. code-block:: bash

    $ docker image ls

You should see the image you just pulled.

Initialize Docker Container
---------------------------
Navigate to the directory containing the case you would like to run and initialize the Docker image you downloaded into a container, running interactively:

.. code-block:: bash

    $ docker run -it --name <NAME> --mount "type=bind,src=<HOST_DIR>,target=<MOUNT_DIR>" <IMAGE> /bin/bash

Replace ``<NAME>`` with the name you would like to give the container, set ``<HOST_DIR>`` to the absolute path to the current directory, and set ``<MOUNT_DIR>`` to ``/home/mdolabuser/mount/``.
Then provide the image tag as ``<IMAGE>``, matching the one downloaded previously: ``mdolab/public:<TAG>``.

When you run this command, you will enter the container and have access to the MACH framework in your specified case directory.

Exiting and Restarting the Container
------------------------------------
At any point you can exit the container with the command:

.. code-block:: bash

    $ exit

You can restart the container by running `start` and `exec`, using:

.. code-block:: bash

    $ docker start <NAME>
    $ docker exec -it --name <NAME> /bin/bash
