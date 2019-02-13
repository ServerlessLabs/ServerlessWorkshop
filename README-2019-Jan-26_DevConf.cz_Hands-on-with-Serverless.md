# Welcome to the "*Hands-on with Serverless*" Workshop, 26th Jan, DevConf.cz.

In this workshop we will explore the concept of *Serverless* looking at several Serverless platforms, including
- AWS Lambda,
- OpenFaaS
- and *possibly* Apache OpenWhisk.

The workshop is hands-on and so you will be provided with pre-configured VMs with the necessary tools pre-installed.

Although slides will not be shown, there is an associated slide-set, a general presentation on Serverless at [https://mjbright.github.io/Talks/#201901_devconfcz_2019_1](https://mjbright.github.io/Talks/#201901_devconfcz_2019_1).

## Pre-requisites
You will need a PC or Mac to be able to access the VMs to run the lab (browser + ssh access).
Your instructor will provide you with credentials to connect to your VM once you have entered your e-mail details in the **sign up form** at [**http://bit.ly/20190126SIGNUP**](http://bit.ly/20190126SIGNUP) on the "**USER Registration**" tab.
(if using Google Sheets is a problem, then just pop by to tell me your e-mail).

You may also run the workshop completely on your own PC though there is some tooling to install - described in the setup pages at 
[https://github.com/ServerlessLabs/ServerlessWorkshop/tree/2019-Jan-DevConf.cz/SETUP](https://github.com/ServerlessLabs/ServerlessWorkshop/tree/2019-Jan-DevConf.cz/SETUP).

You will be required to use your own AWS account, all usage will fall within the "Free Tier" usage.

**NOTE**: The Provided VMs will be deleted at the end of the Workshop.

## Agenda
- This Overview, and presentation of Serverless concept
- [Setup for AWS](/SETUP/SETUP-AWS.md)
- [AWS S3 Object Store](AWS-S3-Lambda/README-S3.md) (or minio) for static site hosting
- [AWS Lambda](AWS-S3-Lambda/README-Lambda.md)
  - About AWS Lambda
  - Implementing a REST api
  - Sending SMS or E-Mail
  - Responding to S3 file upload
  - Webhooks
- Scenario Ideas
  - Auto-mailer
  - Aggregator
  - Image processor: colorizer, thumbnail generator
  - OCR/Machine Learning
  - URL Shortener
  - Collaborative Booksmarks site
- [OpenFaaS](OpenFaaS/README.md)
  - About Apache OpenFaaS
  [Setup for OpenFaaS](/SETUP/SETUP-OPENFAAS.md)
  
- [Apache OpenWhisk](Apache-OpenFaaS/README.md)
  - About Apache OpenWhisk
  [Setup for OpenWhisk](/SETUP/SETUP-OPENWHISK.md)

## Learning Paths

See below for a matrix of elements in this tutorial.

It is suggested that you follow one of these paths.

If time allows it is recommended that you first follow one path, then follow the others building upon the knowledge gained in the other paths.

#### Legend

Strong colors: Tutorial elements

Weak colors: Suggested optional elements

Other: Not yet implemented

### Path1 - S3, Lambda+Python
 <table> <tbody> <tr>
  <th><img src='./images/Technology_270x30_808080_000000.svg'/></th>  <th><img src='./images/Step_180x30_808080_000000.svg'/></th>  <th><img src='./images/Step_315x30_808080_000000.svg'/></th>  <th><img src='./images/Step_255x30_808080_000000.svg'/></th>  <th><img src='./images/Step_270x30_808080_000000.svg'/></th>  <th><img src='./images/Step_120x30_808080_000000.svg'/></th>
</tr>
<tr>
  <td><img src='./images/S3+Static+Site_270x30_808080_000000.svg'/></td>  <td><a href=S3.md> <img src='./images/Basic+S3+Static+Site_180x30_339966_ffffff.svg'/> </a></td>  <td><img src='./images/Site+Gen+React_315x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Site+Gen+Hugo_255x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Site+Gen+Pelican_270x30_ccffcc_000000.svg'/></td>  <td><img src='./images/DNS+Routing_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/AWS+Lambda+Python_270x30_808080_000000.svg'/></td>  <td><img src='./images/Using+aws+cli_180x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Using+Chalice_315x30_339966_ffffff.svg'/></td>  <td><img src='./images/Using+Serverless+BRpa-sls-_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Terraform_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/AWS+Lambda+Node.js_270x30_808080_000000.svg'/></td>  <td><img src='./images/Using+aws+cli_180x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Using+Claudia_315x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Using+Serverless+BRpa-sls-_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Terraform_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/OpenFaaS_270x30_808080_000000.svg'/></td>  <td><a href=OpenFaaS.md> <img src='./images/OpenFaaS+Setup_180x30_ffffff_000000.svg'/> </a></td>  <td><img src='./images/Investigate+Store_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Investigate+cliBRcn-+faasBR-cli_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Creating+functions+from+templates_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/OpenWhisk_270x30_808080_000000.svg'/></td>  <td><img src='./images/OpenWhisk+Setup_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Investigate+cliBRcn-+wsk,+wskdeploy_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/Capabilities_270x30_808080_000000.svg'/></td>  <td><img src='./images/Send+SMS_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Send+EBR-Mail_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Read+Config+from+S3+file_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Read+Config+from+DB_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/Scenarii_270x30_808080_000000.svg'/></td>  <td><img src='./images/Informer+Tool_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Scooper+BRpa-Content+Aggregator-_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Bookmark+Manager_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Image+Processor_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
 </tbody> </table> 




### Path2 - S3, Lambda+Node.js
 <table> <tbody> <tr>
  <th><img src='./images/Technology_270x30_808080_000000.svg'/></th>  <th><img src='./images/Step_180x30_808080_000000.svg'/></th>  <th><img src='./images/Step_315x30_808080_000000.svg'/></th>  <th><img src='./images/Step_255x30_808080_000000.svg'/></th>  <th><img src='./images/Step_270x30_808080_000000.svg'/></th>  <th><img src='./images/Step_120x30_808080_000000.svg'/></th>
</tr>
<tr>
  <td><img src='./images/S3+Static+Site_270x30_808080_000000.svg'/></td>  <td><a href=S3.md> <img src='./images/Basic+S3+Static+Site_180x30_339966_ffffff.svg'/> </a></td>  <td><img src='./images/Site+Gen+React_315x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Site+Gen+Hugo_255x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Site+Gen+Pelican_270x30_ccffcc_000000.svg'/></td>  <td><img src='./images/DNS+Routing_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/AWS+Lambda+Python_270x30_808080_000000.svg'/></td>  <td><img src='./images/Using+aws+cli_180x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Using+Chalice_315x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Using+Serverless+BRpa-sls-_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Terraform_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/AWS+Lambda+Node.js_270x30_808080_000000.svg'/></td>  <td><img src='./images/Using+aws+cli_180x30_ccffcc_000000.svg'/></td>  <td><img src='./images/Using+Claudia_315x30_339966_ffffff.svg'/></td>  <td><img src='./images/Using+Serverless+BRpa-sls-_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Terraform_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/OpenFaaS_270x30_808080_000000.svg'/></td>  <td><a href=OpenFaaS.md> <img src='./images/OpenFaaS+Setup_180x30_ffffff_000000.svg'/> </a></td>  <td><img src='./images/Investigate+Store_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Investigate+cliBRcn-+faasBR-cli_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Creating+functions+from+templates_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/OpenWhisk_270x30_808080_000000.svg'/></td>  <td><img src='./images/OpenWhisk+Setup_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Investigate+cliBRcn-+wsk,+wskdeploy_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/Capabilities_270x30_808080_000000.svg'/></td>  <td><img src='./images/Send+SMS_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Send+EBR-Mail_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Read+Config+from+S3+file_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Read+Config+from+DB_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/Scenarii_270x30_808080_000000.svg'/></td>  <td><img src='./images/Informer+Tool_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Scooper+BRpa-Content+Aggregator-_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Bookmark+Manager_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Image+Processor_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
 </tbody> </table> 




### Path3 - OpenFaaS
 <table> <tbody> <tr>
  <th><img src='./images/Technology_270x30_808080_000000.svg'/></th>  <th><img src='./images/Step_180x30_808080_000000.svg'/></th>  <th><img src='./images/Step_315x30_808080_000000.svg'/></th>  <th><img src='./images/Step_255x30_808080_000000.svg'/></th>  <th><img src='./images/Step_270x30_808080_000000.svg'/></th>  <th><img src='./images/Step_120x30_808080_000000.svg'/></th>
</tr>
<tr>
  <td><img src='./images/S3+Static+Site_270x30_808080_000000.svg'/></td>  <td><a href=S3.md> <img src='./images/Basic+S3+Static+Site_180x30_ffffff_000000.svg'/> </a></td>  <td><img src='./images/Site+Gen+React_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Site+Gen+Hugo_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Site+Gen+Pelican_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/DNS+Routing_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/AWS+Lambda+Python_270x30_808080_000000.svg'/></td>  <td><img src='./images/Using+aws+cli_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Chalice_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Serverless+BRpa-sls-_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Terraform_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/AWS+Lambda+Node.js_270x30_808080_000000.svg'/></td>  <td><img src='./images/Using+aws+cli_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Claudia_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Serverless+BRpa-sls-_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Using+Terraform_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/OpenFaaS_270x30_808080_000000.svg'/></td>  <td><a href=OpenFaaS.md> <img src='./images/OpenFaaS+Setup_180x30_339966_ffffff.svg'/> </a></td>  <td><img src='./images/Investigate+Store_315x30_339966_ffffff.svg'/></td>  <td><img src='./images/Investigate+cliBRcn-+faasBR-cli_255x30_339966_ffffff.svg'/></td>  <td><img src='./images/Creating+functions+from+templates_270x30_339966_ffffff.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/OpenWhisk_270x30_808080_000000.svg'/></td>  <td><img src='./images/OpenWhisk+Setup_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Investigate+cliBRcn-+wsk,+wskdeploy_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/Capabilities_270x30_808080_000000.svg'/></td>  <td><img src='./images/Send+SMS_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Send+EBR-Mail_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Read+Config+from+S3+file_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Read+Config+from+DB_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
<tr>
  <td><img src='./images/Scenarii_270x30_808080_000000.svg'/></td>  <td><img src='./images/Informer+Tool_180x30_ffffff_000000.svg'/></td>  <td><img src='./images/Scooper+BRpa-Content+Aggregator-_315x30_ffffff_000000.svg'/></td>  <td><img src='./images/Bookmark+Manager_255x30_ffffff_000000.svg'/></td>  <td><img src='./images/Image+Processor_270x30_ffffff_000000.svg'/></td>  <td><img src='./images/_120x30_ffffff_000000.svg'/></td>
</tr>
 </tbody> </table> 

### Path4: OpenWhisk

## Serverless

![images/ServerlessEvents.PNG](images/ServerlessEvents.PNG)

## Resources






