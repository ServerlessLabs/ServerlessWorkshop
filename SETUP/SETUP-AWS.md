
# Setup choices for AWS parts of Lab

This page describes how to perform the setup of your environment to be able to use AWS features such as S3, Lambda for use in the Lab.

You may either:
- Use your own PC and your own AWS account (recommended but you will need to install *aws* cli tool and some Python or npm modules - see [Using your own PC](#SETUP_PC_AWS) below).
- Use the provided VM with your own AWS account

## Using the provided VM with your own AWS account
You will need to use your own AWS login, if you do not have an account you can create an account at https://portal.aws.amazon.com/billing/signup.

**Note** that the lab exercises described here fall within the Free Tier usage [aws.amazon.com/free].

### Storing your credentials in standard location
Once you have created your account you should place your AWS credentials in ~/.aws/credentials in the following format:

```
[default]
aws_access_key_id     = <Your access key id>
aws_secret_access_key = <Your secret access key>
region                = us-west-1
```

These credentials will be used automatically by the *aws* cli tool (already installed in the VM).


### Storing you credentials as Environment Variables
or if you prefer in ~/.aws/credentials.rc (or some *hidden* location) in the following format:

```
export AWS_ACCESS_KEY_ID="<Your access key id>"
export AWS_SECRET_ACCESS_KEY="<Your secret access key>"
export AWS_DEFAULT_REGION=us-west-1
```

You will need to source this file in each shell from which you wish to use the *aws* cli tool.

**Note**: This VM will be deleted shortly after the lab session but you may want to delete the ~/.aws directory anyway, so that your credentials do not persist.

<div id="SETUP_PC_AWS" />
## Using your own PC

The provided VMs provide the following components in a Ubuntu 18.04 LTS VM, you will need most of these packages.
**Note** that package names may differ on other Linux distributions.

**Note** You are advised to install Python packages using pip in a virtualenv.

- python3, python3-pip
- wget, curl, nodejs, npm
- npm: claudia, serverless, serverless-s3-deploy
- pip: awscli, chalice, docker, gspread, oauth2client
- docker, docker-compose

github:
- https://github.com/ServerlessLabs/ServerlessWorkshop/ on branch 2019-Jan-DevConf.cz

Other optional packages:
- tmux, pelican, snap, virtualenv

The Bash scripts and Ansible playbooks use to perform setup are stored in the '[*scripts*](scripts)' and '[*playbooks*](playbooks)' directories.

Other packages may be required in other sections of the Lab.


