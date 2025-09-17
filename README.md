<img src="_assets/AMD-Pensando-White.png" alt="AMD Pensando" width="350"/>


ELK based analytics for AMD Pensando DPUs in the Aruba CX10K

This repository is the starting point for building and utlizing the Elasticstack for monitoring and analyzing
data, both about and traversing, the AMD Pensando DPU(s) within your environment. By default, it is an Elastic Common
Schema (ECS) compliant install that will support AMD Pensando DPU telemetry from any Aruba CX10K with AOSCX 10.12, 10.13,
10.14 or 10.15. The main purpose is to consolidate the applications and tools used for said monitoring and analysis and
deploy them in an easy fashion to get a demo/poc up and running in very little time.

</br>

**NOTE**
</br>

<mark>Please *fully* read the Support Policy below if you have any issues/questions with the installation</mark>

  #### System Requirements
  This is a POC/demo implementation only.  Some aspects (configurations and schemas) can be used for production, but the
   underlying infra (Elasticstack) should only be used in a lab situation.  It is not built to scale to anything past a
   couple switches with paltry amounts of workloads.  The AMD Pensando Technical Business Development team is more than
   happy to help when a production instance is needed and can advise on how the AMD Pensando configurations and settings
    need to be applied to a production instance of Elasticstack.

  There are 2 recommended requirements because each deals with different scenarios.  The "minimum" is what you will need
   for 1 CX10K and no more than 12 workloads attached just doing basic connectivity tests, web tier apps and the like.
   The "large" is what you would use for 1 CX10K with more than 12, but less than 48, workloads or multiple CX10Ks
   (again with no more than 48 workloads total) doing connectivity tests along with a more "normal" DC traffic pattern
   (i.e. hundreds of flows/sec).

  The HDD recommendations will allow for each to store both syslog and ipfix data for a total of 30 days before deletion.
  This can be adjusted on your data retention requirements and whether or not both telemetry systems are sending to the ELK stack.

  **Minimum Requirements**
  > 4 vCPU <br/>
  > 16GB RAM  <br/>
  > 256GB HDD  <br/>
  > Ubuntu 22.04 or newer <br/>

  <br/>

  **Large Requirements**
  > 6 vCPU  <br/>
  > 32GB RAM  <br/>
  > 512GB HDD  <br/>
  > Ubuntu 22.04 or newer <br/>

  <br/>

#### Installation and running
There are two options to install this repository.  Please read the options below and decide which is best for you.


> #### OPTION 1 - Mostly Automated <br/>

This option will download and run an all-in-one script that will install not only this repository, but will also install
all of the necessary pre-requisites (docker, docker-compose, etc.) and configure your Ubuntu based system for Elasticstack.

This is recommended for most users.  It takes care of the heavy lifting and is for those that don't need/want to
understand the undelying complexities of getting this up and running
</br>
To run this, please [use the ELK_single_script repository](https://github.com/tdmakepeace/ELK_Single_script/tree/main) and
make sure to read the README before starting.


> #### OPTION 2 - Manual Installation <br/>

This option is for those that want to run the AMD Pensando Elasticstack but also have an interest in how it's actually
built and how things are configured.  It is suggested that you use this installation method if you plan on administering
your Elasticstack "cluster" in your demo/poc environment.

Instantiation can be done on any system with docker and docker-compose installed.

:warning: <span style="color:yellow">**WARNING**</span> :warning:

<mark>DO NOT RUN THE INSTALL OR CONFIGURATION AS ROOT  -  IT WILL NOT WORK. </mark>

<br/>
If you don't know how to run docker as a non-root user, simply add the user to the docker group, then log out and log back in.

```
sudo usermod -aG docker ${USER}
```
<br/>

---

This branch works with the following software. <br/>

CXOS: 10.15.x <br/>
PSM:  1.100.2-T-8 or later

This is backwards compatible with CXOS software 10.13.x and 10.14.x as well (and applicable PSM versions).  If this is not what you are running,
 [ check one of the other branches](https://github.com/amd/pensando-elk/branches)

---
  ### Please fully read the Support Policy below if you are having problems installing or configuring this

  #### Installation and running
</br>

  1. Clone this repository and cd into the directory where it was cloned
        ```
        git clone https://github.com/amd/pensando-elk.git
        cd pensando-elk
        ```

  2. Verify you are on the correct branch before starting  (you want to be on main or aoscx_10.15.x)
        ```
        git branch
        ```
</br>

  3. If you are not on the correct branch, use the following command to switch to the correct branch:
        ```
        git checkout main
        ```
</br>

  4. Run the following command to set up the ELK version to run:
      ```
      echo "TAG=8.16.1" >.env
      ```
</br>

  5. Create the following directories and give them full write permissions (777 works)
      ```
      ./data/es_backups
      ./data/pensando_es
      ./data/elastiflow
      chmod -R 777 ./data
      ```
</br>

  6. Ensure that you update ```vm.max_map_count``` on your system so that elasticsearch can store it's inidices correctly
      ```
      sudo sysctl -w vm.max_map_count=262144
      echo vm.max_map_count=262144 | sudo tee -a /etc/sysctl.conf
      ```
</br>

  7. If you are going to collect IPFix packets.  If not, then skip to step 7.

      ```
      localip=`hostname -I | cut -d " " -f1`
      sed -i.bak  's/EF_OUTPUT_ELASTICSEARCH_ENABLE: '\''false'\''/EF_OUTPUT_ELASTICSEARCH_ENABLE: '\''true'\''/' docker-compose.yml
      sed -i.bak -r "s/EF_OUTPUT_ELASTICSEARCH_ADDRESSES: 'CHANGEME:9200'/EF_OUTPUT_ELASTICSEARCH_ADDRESSES: '$localip:9200'/" docker-compose.yml
      sed -i.bak -r "s/#EF_OUTPUT_ELASTICSEARCH_INDEX_PERIOD: 'daily'/EF_OUTPUT_ELASTICSEARCH_INDEX_PERIOD: 'daily'/" docker-compose.yml
      ```

      The previous commands do the following in the docker-compose.yml file for Elastiflow:
        - Enables Elasticsearch output for Elastiflow:                EF_OUTPUT_ELASTICSEARCH_ENABLE: 'true'
        - Change the "CHANGEME" to the IP address of your system:     EF_OUTPUT_ELASTICSEARCH_ADDRESSES: 'CHANGEME:9200'
        - Enable daily log file rotation:                             EF_OUTPUT_ELASTICSEARCH_INDEX_PERIOD: 'daily'
</br></br>

  8. Using PSM, point your DSS firewall syslog (RFC5424) at the IP of your ELK cluster, UDP port 5514  (this number can be changed in the logstash/dss_syslog.conf file in the input section at the top)
</br></br>

  9. If collecting IPFix (else skip to step 9), use PSM point your DSS IPFix flows (flow export policy) at the IP of your ELK cluster, UDP port 9995  (this port number can be changed in the docker-compose file using the EF_FLOW_SERVER_UDP_PORT parameter)*

</br>

  10. Run

     If using docker-compose v1 (standalone)

     `docker-compose -d up`

     Or if using docker-compose v2 (docker plug-in)

     `docker compose up --detach`
  </br>

      **NOTE:** Give it about 5 minutes to start up

  </br>

  11. From the install directory, load the elasticsearch schema (mappings) for the Pensando DSS Firewall index-pattern using the following cli:
        ```
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_index_template/pensando-fwlog-session-end?pretty' -d @./elasticsearch/template/pensando-fwlog-session-end.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_index_template/pensando-fwlog-create-allow?pretty' -d @./elasticsearch/template/pensando-fwlog-create-allow.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_index_template/pensando-fwlog-empty-delete?pretty' -d @./elasticsearch/template/pensando-fwlog-empty-delete.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_index_template/pensando-fwlog-create-deny?pretty' -d @./elasticsearch/template/pensando-fwlog-create-deny.json
        ```



  12. From the install directory, load the elasticsearch index retention settings for the Pensando DSS Firewall index-pattern using the following cli:
        ```
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_ilm/policy/pensando_empty_delete' -d @./elasticsearch/policy/pensando_empty_delete.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_ilm/policy/pensando_create_allow' -d @./elasticsearch/policy/pensando_create_allow.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_ilm/policy/pensando_session_end' -d @./elasticsearch/policy/pensando_session_end.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_ilm/policy/pensando_create_deny' -d @./elasticsearch/policy/pensando_create_deny.json
        curl -XPUT -H'Content-Type: application/json' 'http://localhost:9200/_ilm/policy/elastiflow' -d @./elasticsearch/policy/elastiflow.json
        ```


  13. From the install directory, load the Kibana dashboard for syslog:
        ```
        curl -X POST "http://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" -H "securitytenant: global" --form file=@./kibana/pensando-dss-10.15.x-syslog.ndjson
        ```
  </br>

  14. From the install directory, load the Kibana dashboard IPFIX:
        ```
        curl -X POST "http://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" -H "securitytenant: global" --form file=@./kibana/kibana-8.2.x-flow-codex.ndjson
        ```
  </br>

  15. Use basic docker commands to monitor the ELK stack:
      - ```docker ps``` - View running container status
      - ```docker logs <container name>``` - View container logs
      - ```docker stats``` - Monitor resource usage
  </br>

  16. Access the Kibana web interface:
      - Point your browser to the IP of your ELK cluster, port 5601
      - Default URL for local installations: http://localhost:5601 </br>
      **NOTE:**
      It could take about 5 mins for visualizations to become populated in both the DSS and IPFix dashboards.


  </br>

</br>

## Support Policy
The code and templates in the repo are released under an as-is, best effort, support policy. These scripts should be seen as community supported and AMD Pensando will contribute our expertise as and when possible. The absolute best (and quickest) way to get help/support is to [file an issue](https://github.com/amd/pensando-elk/issues).  Any other attempts at contact will probably be lost in the ether and you will rarely, if ever, hear back.
