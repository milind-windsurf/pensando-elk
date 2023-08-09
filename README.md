<img src="https://th.bing.com/th/id/OIP.CwPiU5tKuxQpL4ZMRSoVIQAAAA?pid=ImgDet&rs=1" alt="AMD Pensando" width="350"/>


ELK based analytics for Pensado Systems

This repository is the starting point for building and utlizing the Elasticstack for monitoring and analyzing
data, both about and traversing, the Pensando DSS(es) within your environment.  The purpose is to consolidate the
applications and tools used for said monitoring and analysis and deploy them in an automated fashion.

Instantiation can be done on any system with docker and docker-compose installed.

## Running ELK-Pensando


:warning: <span style="color:yellow">**WARNING**</span> :warning:

<mark>DO NOT RUN *ANTHING* AS ROOT DURING INSTALL OR CONFIGURATION!!!  IT WILL NOT WORK. </mark>

<br/>

---
**NOTE**

Each branch has it's own README that has release specific information and configuration.  Please select the branch that you will use from the dropdown in github or checkout the correct branch and view that README for any information pertaining to that particular release.  

The latest branch is aoscx_10.12 and supports the following <br/>
CXOS: 10.12.x <br/>
PSM:  1.59.0-50 or later

If these do not match your current install, [check one of the other branches](https://github.com/amd/cx10000-elastic/branches)

---

<mark>Please *fully* read the Support Policy below if you have any issues/questions with the installation</mark>

  #### System Requirements
  This is a POC/demo implementation only.  Some aspects (configurations and schemas) can be used for production, but the underlying infra (ELK) should only be used in a lab situation.  It is not built to scale to anything past a couple switches with paltry amounts of workloads.  The AMD Pensando Technical Business Development team is more than happy to help when a production instance is needed and can advise on how the AMD Pensando configurations and settings need to be applied.
  
  There are 2 recommended requirements because each deals with different scenarios.  The "minimum" is what you will need for 1 CX10K and no more than 12 workloads attached just doing basic connectivity tests, web tier apps and the like.  The "large" is what you would use for 1 CX10K with more than 12, but less than 48, workloads or multiple CX10Ks (again with no more than 48 workloads total) doing connectivity tests along with a more "normal" DC traffic pattern (i.e. hundreds of flows/sec).  
  
  The HDD recommendations will allow for each to store both syslog and ipfix data for a total of 30 days before deletion.  This can be adjusted on your data retention requirements and whether or not both telemetry systems are sending to the ELK stack.

  **Minimum Requirements**
  > 4 vCPU <br/>
  > 16GB RAM  <br/>
  > 512GB HDD  <br/>

  <br/>

  **Large Requirements**
  > 6 vCPU  <br/>
  > 32GB RAM  <br/>
  > 1TB HDD  <br/>

  <br/>
  
  #### Installation and running
 
  1. Clone this repository

  2. Change into the directory where it is stored

  3. Checkout the branch that you need
     ```
     git checkout <branch name>
     ```
     
  4. Follow the instructions in the README for your particular branch 

  
## Support Policy
The code and templates in the repo are released under an as-is, best effort, support policy. These scripts should be seen as community supported and AMD Pensando will contribute our expertise as and when possible. The absolute best (and quickest) way to get help/support is to [file an issue](https://github.com/amd/cx10000-elastic/issues).  Any other attempts at contact will probably be lost in the ether and you will rarely, if ever, hear back. 
