<img src="https://pensando.io/wp-content/themes/pensando/assets/images/logo.svg" alt="My cool logo" width="350"/>


ELK based analytics for Pensado Systems

This repository is the starting point for building and utlizing the Elasticstack for monitoring and analyzing
data, both about and traversing, the Pensando DSC(s) and DSS(es) within your environment.  The purpose is to consolidate the
applications and tools used for said monitoring and analysis and deploy them in an automated fashion.

Instantiation can be done on any system with docker and docker-compose installed.

## Running Pensando-ELK

1. Clone this repository
2. Change into the directory where it is stored
3. Edit a file called '.env' and add the following to it - changing the 7.14.1 to the version of ELK you want to use:
    ```
    TAG=7.14.1
    ```
4. Run 'docker-compose up'

## Support Policy
The code and templates in the repo are released under an as-is, best effort, support policy. These scripts should be seen as community supported and Pensando will contribute our expertise as and when possible. We do not provide technical support or help in using or troubleshooting the components of the project through our normal support options. Unless explicitly tagged, all projects or work posted in our GitHub repository (at https://github.com/Pensando) or sites other than our official Downloads page on https://support.pensando.io are provided under the best effort policy.
