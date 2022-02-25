.. _components:

************************
Pensando-ELK Components
************************

The following docker containers are used in the Pensando-ELK implementation

Elasticsearch
------------------
    - Hub Repository: docker.elastic.co/elasticsearch/elasticsearch
    - Container Name: pensando-elasticsearch
    - Port(s) Used: 9200
    - Description:
      This is the storage of all the syslog messages coming from the Pensando
      platform.  Since this is run in a container, the ./data/pensando_es dir
      will persist through container restarts so that no data is lost.



Kibana
------------------
    - Hub Repository: docker.elastic.co/kibana/kibana
    - Container Name: pensando-kibana
    - Port(s) Used: 5601
    - Description:



Logstash
------------------
    - Hub Repository: docker.elastic.co/logstash/logstash
    - Container Name: pensando-logstash
    - Port(s) Used: 5514
    - Description:
      Uses the ./logstash/pipelines file for managing how many workers are used
      to parse incoming syslog messages and also to set up where the configuration
      file is stored within the container:
      - ./logstash/taormina.conf file is used by the pipeline workers to ingest
      syslog messages as they are received from the Aruba CX10K switch, manipulate
      them and store them in a JSON format in Elasticsearch.
