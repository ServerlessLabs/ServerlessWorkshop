
# Serverless Workshop - OpenFaaS

![](images/OpenFaaS_logo.png)

## Installing OpenFaaS

The OpenFaaS **source code repository** at https://github.com/openfaas/faas has already been cloned in your VM at ~/src/git/openfaas/faas.

The **faas-cli** command-line client has already been downloaded from https://github.com/openfaas/faas-cli/releases and place in /usr/local/bin.

Docker has already be installed within the VM.

Verify that docker is installed and available to your user using the ```docker version``` command, you should see something similar to
```
> docker version
Client:
 Version:           18.09.1
 API version:       1.39
 Go version:        go1.10.6
 Git commit:        4c52b90
 Built:             Wed Jan  9 19:35:31 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.1
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.6
  Git commit:       4c52b90
  Built:            Wed Jan  9 19:02:44 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```

### Enabling the Swarm cluster

We need to enable Swarm mode, by performing ```docker swarm init```, you should see output similar to
```
> docker swarm init
Swarm initialized: current node (g4wrzwsej0gmkou7iqf4asqrt) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-0urdp54xbjqt72jeuj9amet9ci4ketyntmx2l6a4qsbvg3g9yl-avy6vll481mozpzdgbi4xxbf4 172.31.21.116:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

There are no other nodes to add to the swarm.

We can verify that we are in swarm mode with the ```docker node ls``` command, you should see output like
```
> docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
g4wrzwsej0gmkou7iqf4asqrt *   ip-172-31-21-116    Ready               Active              Leader              18.09.1
```

### Starting OpenFaaS

Now it is sufficient to run the ```deploy_stack.sh``` script, you should see output similar to
```
user1@ip-172-31-21-116 ~/src/git/openfaas.faas> ./deploy_stack.sh
Attempting to create credentials for gateway..
fruu7z64jvkymnidv5bb85ith
w8eyz6n1z4vo9xvcg4i5mgi30
[Credentials]
 username: admin
 password: 1548be044d6ac4741abdc3ed2139f63321d4b7954a1397e0f9f082c860bac480
 echo -n 1548be044d6ac4741abdc3ed2139f63321d4b7954a1397e0f9f082c860bac480 | faas-cli login --username=admin --password-stdin

Enabling basic authentication for gateway..

Deploying OpenFaaS core services
Creating network func_functions
Creating config func_alertmanager_config
Creating config func_prometheus_config
Creating config func_prometheus_rules
Creating service func_nats
Creating service func_queue-worker
Creating service func_prometheus
Creating service func_alertmanager
Creating service func_gateway
Creating service func_faas-swarm
```

Note that an admin password has been auto-generated for you, in the above example it is *1548be044d6ac4741abdc3ed2139f63321d4b7954a1397e0f9f082c860bac480*.

You must **save away** the password to be able to login to the OpenFaaS portal.

**NOTE**: If you had previously run OpenFaaS but not saved the password, see '*Problems starting OpenFaaS*' below.

You should now be able to login to the OpenFaaS portal.

Obtain the public_ip address of the VM (the same which is present in the ssh_nodeX_user1.sh script) using the provided (in ~/.bash_profile) function public_ip, e.g.
```
user1@ip-172-31-21-116 ~/src/git/openfaas.faas> public_ip
54.67.51.193
```

Connect to the OpenFaaS portal at (**replacing with your ip address**):

 [http://54.67.51.193:8080/](http://54.67.51.193:8080/)
    

You will be prompted to login.

Login with user name '*admin*' and the password which you saved earlier - you did save it didn't you?

You should now see the OpenFaaS portal as below

![OpenFaaSPortal](images/Portal0.JPG)

**NOTE:** It is not necessary to run the curl command shown in the image as the VM already has the faas-cli utility installed.

You can verify that OpenFaaS is running from the command-line with
```docker stack ls``` and ```docker stack ps func``` which should produce

```
mjb@carbon ~/src/git/openfaas.faas> docker stack ls
NAME                SERVICES            ORCHESTRATOR
func                6                   Swarm
mjb@carbon ~/src/git/openfaas.faas> docker stack ps func
ID                  NAME                  IMAGE                         NODE                    DESIRED STATE       CURRENT STATE            ERROR                       PORTS
uecw8el7p8ty        func_gateway.1        openfaas/gateway:0.9.14       linuxkit-00155d00106c   Running             Running 23 seconds ago
26v7l74rsye6        func_prometheus.1     prom/prometheus:v2.3.1        linuxkit-00155d00106c   Running             Running 30 seconds ago
n9s9tgr1rq4n        func_queue-worker.1   openfaas/queue-worker:0.5.4   linuxkit-00155d00106c   Running             Running 44 seconds ago
z5laddw4fqvf        func_nats.1           nats-streaming:0.11.2         linuxkit-00155d00106c   Running             Running 49 seconds ago
xzob41l44s7g        func_faas-swarm.1     openfaas/faas-swarm:0.6.1     linuxkit-00155d00106c   Running             Running 57 seconds ago
yweg7nxftaml        func_gateway.1        openfaas/gateway:0.9.14       linuxkit-00155d00106c   Running             Running 44 seconds ago
6enobzg56p14        func_alertmanager.1   prom/alertmanager:v0.15.0     linuxkit-00155d00106c   Running             Running 58 seconds ago

```

You can verify that you have *faas-cli* installed by running the ```faas-cli``` command, e.g.:

```
user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaas> faas-cli version
  ___                   _____           ____
 / _ \ _ __   ___ _ __ |  ___|_ _  __ _/ ___|
| | | | '_ \ / _ \ '_ \| |_ / _` |/ _` \___ \
| |_| | |_) |  __/ | | |  _| (_| | (_| |___) |
 \___/| .__/ \___|_| |_|_|  \__,_|\__,_|____/
      |_|

CLI:
 commit:  a141dedf94ffeed84412365fd591bdc8999c5a1b
 version: 0.8.3
```

If everything is OK, skip to the '*Getting Started with OpenFaaS*' section below.


## Problems starting OpenFaaS

If you need to retry starting OpenFaaS, perform the following steps to cleanup

- Remove the OpenFaaS '*func*' stack using command ```docker stack remove func```
- Verify that the stack is no longer running using command ```docker stack ls```
- Wait/Verify that all containers have been stopped/removed using command ```docker ps```
- Remove secrets using
  ```
    docker secret ls
    docker secret remove basic-auth-user
    docker secret remove basic-auth-password
    docker secret ls
  ```
- Redeploy the stack using ```deploy_stack.sh``` or ```bash -x deploy_stack.sh```

## Getting Started with OpenFaaS

### Using the OpenFaaS Portal

Click on the '*Deploy a New Function*' button and deploy an existing function.

Experiment with this interface.

But we will continue using command-line ...

### Using the faas-cli command

```
user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaas> faas-cli help

Manage your OpenFaaS functions from the command line

Usage:
  faas-cli [flags]
  faas-cli [command]

Available Commands:
  build          Builds OpenFaaS function containers
  cloud          OpenFaaS Cloud commands
  deploy         Deploy OpenFaaS functions
  describe       Describe an OpenFaaS function
  generate       Generate Kubernetes CRD YAML file
  help           Help about any command
  invoke         Invoke an OpenFaaS function
  list           List OpenFaaS functions
  login          Log in to OpenFaaS gateway
  logout         Log out from OpenFaaS gateway
  new            Create a new template in the current folder with the name given as name
  push           Push OpenFaaS functions to remote registry (Docker Hub)
  remove         Remove deployed OpenFaaS functions
  secret         OpenFaaS secret commands
  store          OpenFaaS store commands
  template       OpenFaaS template store and pull commands
  up             Builds, pushes and deploys OpenFaaS function containers
  version        Display the clients version information

Flags:
      --filter string   Wildcard to match with function names in YAML file
  -h, --help            help for faas-cli
      --regex string    Regex to match with function names in YAML file
  -f, --yaml string     Path to YAML file describing function(s)

Use "faas-cli [command] --help" for more information about a command.
```
Let's list any functions locally available using ```faas-cli list``` (*or ls*) command.

If you already deployed functions using the portal  you will see them here, e.g.
```
user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaaS> faas-cli ls
Function                        Invocations     Replicas
nodeinfo                        0               1
```

### Deploying from the store using faas-cli

**NOTE:** If not already deployed we can deploy from the store using the command-line

First lets's look at the available '*store*' commands:

```
user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaaS> faas-cli store
Allows browsing and deploying OpenFaaS functions from a store

Usage:
  faas-cli store [command]

Available Commands:
  deploy      Deploy OpenFaaS functions from a store
  inspect     Show details of OpenFaaS function from a store
  list        List available OpenFaaS functions in a store

Flags:
  -h, --help         help for store
  -u, --url string   Alternative Store URL starting with http(s):// (default "https://cdn.rawgit.com/openfaas/store/master/store.json")

Global Flags:
      --filter string   Wildcard to match with function names in YAML file
      --regex string    Regex to match with function names in YAML file
  -f, --yaml string     Path to YAML file describing function(s)

Use "faas-cli store [command] --help" for more information about a command.
```

Let's list the functions available in the store:

```
user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaaS> faas-cli store  ls

FUNCTION                    DESCRIPTION
Colorization                Turn black and white photos to color ...
Inception                   This is a forked version of the work ...
Have I Been Pwned           The Have I Been Pwned function lets y...
SSL/TLS cert info           Returns SSL/TLS certificate informati...
Face Detection with Pigo    Detect faces in images using the Pigo...
SentimentAnalysis           Python function provides a rating on ...
Figlet                      OpenFaaS Figlet image. This repositor...
Business Strategy Generator Generates a Business Strategy (using ...
NodeInfo                    Get info about the machine that you'r...
Tesseract OCR               This function brings OCR - Optical Ch...
Dockerhub Stats             Golang function gives the count of re...
QR Code Generator - Go      QR Code generator using Go
Nmap Security Scanner       Tool for network discovery and securi...
ASCII Cows                  Generate cartoons of ASCII cows
YouTube Video Downloader    Download YouTube videos as a function
OpenFaaS Text-to-Speech     Generate an MP3 of text using Google'...
nslookup                    Uses nslookup to return any IP addres...
Docker Image Manifest Query Query an image on the Docker Hub for ...
face-detect with OpenCV     Detect faces in images. Send a URL as...
Left-Pad                    left-pad on OpenFaaS
mememachine                 Turn any image into a meme.
```

Now we can deploy the '*nodeinfo*' function:

```user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaaS> faas-cli store deploy nodeinfo

Deployed. 202 Accepted.
URL: http://127.0.0.1:8080/function/nodeinfo

user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaaS> faas-cli ls
Function                        Invocations     Replicas
nodeinfo                        0               1
```

### Invoking the function using faas-cli

We can now invoke our function using ```faas-cli invoke``` e.g.

```
user1@ip-172-31-21-116 ~/src/git/ServerlessLabs/ServerlessWorkshop/OpenFaaS> echo | faas-cli invoke nodeinfo
Hostname: 522725a5d800

Platform: linux
Arch: x64
CPU count: 2
Uptime: 183867
```

Note the use of '*echo* |' because ```faas-cli invoke``` always reads input from stdin.


```bash

```


```bash

```


```bash

```


```bash


```
