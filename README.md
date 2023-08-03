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
