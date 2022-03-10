.. _download-pensando-elk:

**********************
Download
**********************

To download Pensando ELK, login to your system as a non-root user [1]_ and issue the following
command:

.. code-block:: bash

    git clone https://gitlab.com/pensando/tbd/elastic/pensando-elk.git


This will clone the repository into the pensando-elk directory.

Once you have the repo cloned, there are a few, one-time setup tasks that need to be performed before starting the containers

1. Change into the directory where it is stored

2. Create the file '.env' and add the following to it (change 8.0.0 if the version of ELK you want is different):

  .. code-block:: none

    TAG=8.0.0


3. Create the following 2 directories and give them full write permissions (777 works)

  .. code-block:: none

    mkdir -p ./data/es_backups
    mkdir -p ./data/pensando_es


4. Ensure that you update ```vm.max_map_count``` on your system so that elasticsearch can store it's inidices correctly

  .. code-block:: none

    sudo sysctl -w vm.max_map_count=262144
    sudo echo vm.max_map_count=262144 >> /etc/sysctl.conf


Now you can :ref:`running-pensando-elk` pensando-elk


.. [1] This is the same user that you will be running the containers as.  Doing this as root can complicate it.
