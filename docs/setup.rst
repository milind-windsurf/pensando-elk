.. _setup-pensando-elk:

Setup
======================

From the install directory, load the elasticsearch schema (mappings) for the Pensando DSS Firewall index-pattern using the following cli:

.. code-block:: bash

  `curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_index_template/pensando-fwlog?pretty' -d @./elasticsearch/pensando_fwlog_mapping.json`


The index-patterns, visualizations and dashboards require that they are manually loaded via the Kibana UI:

1.) Click the "Hamburger Menu" button in the top left corner and under **Management** select "Stack Management"

.. image:: _static/stackmgmt.png
    :scale: 50 %

2.) Under the Kibana section, select the **Saved Objects** link and click **Import** in the upper right hand corner

.. image:: _static/importobject.png

That will bring up the import screen on the right side.

3.) Click the Import icon and select the file from your install directory located here:

.. code-block:: bash

    <install-dir>/kibana/pensando-dss-elk.ndjson
                        and/or  (you need to install both)
    <install-dir>/kibana/elastiflow-7.14.x-ecs-dark.ndjson

4.) Once the file is selected, click the blue Import button at the bottom of the page

.. image:: _static/importndjson.png
    :scale: 50 %

If it works (*and why wouldn't it?*) you should see something similar to the below:

.. image:: _static/hopethisworks.png
    :scale: 50 %


Now from the Dashboard menu you should be able to see the AMD Pensando DPU dashboards and the Elastiflow dashboards for IPFix from the AMD Pensando DPU
