.. _running-pensando-elk:

Run
======================

These run instructions can be run numerous times since you may start and :ref:`stop-pensando-elk` ad-hoc.

The docker containers should survive reboots, so if the system is restarted, they should restart on their own.  If not you can refer to the instrcutions below.

To start Pensando ELK, run docker-compose up while in the directory where the docker-compose.yml file is located

.. code-block:: bash

    `cd <install-dir>`

    If using docker-compose v1 (standalone)

     `docker-compose up`

     Or if using docker-compose v2 (docker plug-in)

     `docker compose up`


Give it a few minutes and, using your browser, try to login to the IP address of your system running docker at port 5601

EXAMPLE:

.. code-block:: bash

  https://localhost:5601

If you get an error message in your browser, you can `check the logs <https://www.shellhacks.com/docker-container-logs-how-to-check/>`_ for elasticsearch and kibana using the following
commands:

.. code-block:: bash

  docker logs pensando-elasticsearch
  docker logs pensando-kibana



If this is the first time you are starting Pensando ELK, refer to the :ref:`setup-pensando-elk` section
for a one time setup procedure to install the correct dashboards.
