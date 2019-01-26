
# AWS Lambda

AWS Lambda is the Serverless product that AWS introduced at reInvent in November 2014.  Lambda has largely popularized the concept of Serverless and AWS continues to lead in this space.

AWS Lambda allows developers to create and deploy small functions and have the code executed without the need to provision servers.  You pay only for the resources used rather than for idle servers.

**NOTE**: However these functions (FaaS) will often be combined with backend services (BaaS) from AWS or elsewhere which may have more significant costs.  Those backend services include S3 storage, DB storage, API gateways, physical or virtual machines.

**NOTE**: Although FaaS costs themselves are minimal typically with 1mn requests/month free and very small cost per request after that limit is passed, there is a risk of high costs if your application/api goes viral.  It is therefore strongly advised to place rate limits at the API Gateway to prevent runaway costs.

A Lambda function provides a handler which is the entry point for the Lambda written for the chosen runtime such as node.js, python etc.
A Lambda function accepts JSON-formatted input and will usually return the same.

A Lambda function is invoked in response to an event, such as an S3 file upload, a change in a database table, a web request or a scheduled event.

#### Runtimes
The following languages, as well as custom runtimes, are now supported
- C#
- Go
- Java
- Node.js
- Python

## Closed-source

Unfortunately AWS Lambda itself if a proprietary service.

Nevertheless as the leader in this space it is important to understand it's capabilities and limitations.

There are many Open Source tools which allow to deploy to AWS Lambda such as
- Serverless(.com) - allows to deploy to several Serverless platforms
- Chalice (A Python Framework provided by AWS)
- Claudia (A Node.js Framework)

or even to emulate Lambda for testing purposes
- localstack
- docker-lambda (https://github.com/lambci/docker-lambda)

## Setup

To run these exercises you should first have
- installed the awscli package to provide the aws command and also
- configured either
  - the ~/.aws/configure file with your AWS account credentials or
  - created a sourceable ~/.aws/credentials.rc (can be in any location) file

```
> cat ~/.aws/credentials.rc

export AWS_ACCESS_KEY_ID="<your-access-key>"
export AWS_SECRET_ACCESS_KEY="<your-secret-access-key>"
export AWS_DEFAULT_REGION=us-west-1
```

If you have chosen to use an rc file, source it as ```source <your-aws-credentials-rc-file>```, e.g.


```bash
. ~/.aws/credentials.rc

cd ~/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda
rm -rf chalice-app scheduled-app

cleanup_functions() {
    echo "-- Functions before:"
    aws lambda list-functions | grep FunctionName

    FNS=$(aws lambda list-functions | grep FunctionName |sed -e 's/.*: //'  -e 's/"//g' -e 's/,//')
    for FN in $FNS; do aws lambda delete-function --function-name $FN; done
    echo "-- Functions after cleanup:"
    aws lambda list-functions | grep FunctionName
}
```

We can now use the aws cli utility to access lambda commands.

Let's investigate the available commands with ```aws lambda help```


```bash
cleanup_functions
```

    -- Functions before:
    -- Functions after cleanup:





```bash
aws lambda help 
```

    LAMBDA()                                                              LAMBDA()
    
    
    
    NAME
           lambda -
    
    DESCRIPTION
              Overview
    
           This  is  the AWS Lambda API Reference . The AWS Lambda Developer Guide
           provides additional information. For the service overview, see What  is
           AWS  Lambda  , and for information about how the service works, see AWS
           Lambda: How it Works in the AWS Lambda Developer Guide .
    
    AVAILABLE COMMANDS
           o add-layer-version-permission
    
           o add-permission
    
           o create-alias
    
           o create-event-source-mapping
    
           o create-function
    
           o delete-alias
    
           o delete-event-source-mapping
    
           o delete-function
    
           o delete-function-concurrency
    
           o delete-layer-version
    
           o get-account-settings
    
           o get-alias
    
           o get-event-source-mapping
    
           o get-function
    
           o get-function-configuration
    
           o get-layer-version
    
           o get-layer-version-policy
    
           o get-policy
    
           o help
    
           o invoke
    
           o list-aliases
    
           o list-event-source-mappings
    
           o list-functions
    
           o list-layer-versions
    
           o list-layers
    
           o list-tags
    
           o list-versions-by-function
    
           o publish-layer-version
    
           o publish-version
    
           o put-function-concurrency
    
           o remove-layer-version-permission
    
           o remove-permission
    
           o tag-resource
    
           o untag-resource
    
           o update-alias
    
           o update-event-source-mapping
    
           o update-function-code
    
           o update-function-configuration
    
    
    
                                                                          LAMBDA()


Let's see if we have any functions defined already using the ```aws lambda list-functions``` command.
You won't have any functions if you just created your account.


```bash
aws lambda list-functions
```

    {
        "Functions": []
    }


Note that it is possible to create functions directly using the command ```aws lambda create-function``` but it would be necessary to interact individually with several AWS services.

There exist several tools which facilitate function creation and deployment.

For information about use of ```aws lambda create-function``` refer to these articles
- https://www.tutorialspoint.com/aws_lambda/aws_lambda_creating_and_deploying_using_aws_cli.htm
- https://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html

We will continue using other frameworks.
- Chalice: A Python Serverless Micro-service framework for AWS Lambda
- Claudia: A Node.js Serverless framework for AWS Lambda
- Serverless: A Serverless platform for various platorms (AWS Lambda, Azure Functions, Google CloudFunctions and more)

## Chalice

Chalice is an open source project created by AWS, available here: https://github.com/aws/chalice

Documentation is at https://chalice.readthedocs.io/en/latest/

Chalice allows to
- deploy to a local test server
- deploy to AWS Lambda (as dev or prod stage)
- easily discover the URL of a deployed service
- recuperate '*CloudWatch*' logs of a lambda function (all print function calls go to CloudWatch logs)

Let's see what options are available using ```chalice --help``` command


```bash
chalice --help
```

    Usage: chalice [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --version             Show the version and exit.
      --project-dir TEXT    The project directory.  Defaults to CWD
      --debug / --no-debug  Print debug logs to stderr.
      --help                Show this message and exit.
    
    Commands:
      delete
      deploy
      gen-policy
      generate-pipeline  Generate a cloudformation template for a...
      generate-sdk
      invoke             Invoke the deployed lambda function NAME.
      local
      logs
      new-project
      package
      url


## Create a Chalice project

Let's start by creating a new Chalice project:


```bash
#cd ..; rm -rf chalice-app
```


```bash
pwd
chalice new-project chalice-app
cd chalice-app
ls -al
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda
    total 20
    drwxrwxr-x  3 user1 user1 4096 Jan 26 03:28 [0m[01;34m.[0m
    drwxrwxr-x 10 user1 user1 4096 Jan 26 03:28 [01;34m..[0m
    drwxrwxr-x  2 user1 user1 4096 Jan 26 03:28 [01;34m.chalice[0m
    -rw-rw-r--  1 user1 user1   37 Jan 26 03:28 .gitignore
    -rw-rw-r--  1 user1 user1  736 Jan 26 03:28 app.py
    -rw-rw-r--  1 user1 user1    0 Jan 26 03:28 requirements.txt


We see that Chalice had created a template project for us.

Looking at the app.py file we see that we have a Python application to run a REST API server with just one route for '/'.


```bash
cp -a app.py app.py.0; cat app.py
```

    from chalice import Chalice
    
    app = Chalice(app_name='chalice-app')
    
    
    @app.route('/')
    def index():
        return {'hello': 'world'}
    
    
    # The view function above will return {"hello": "world"}
    # whenever you make an HTTP GET request to '/'.
    #
    # Here are a few more examples:
    #
    # @app.route('/hello/{name}')
    # def hello_name(name):
    #    # '/hello/james' -> {"hello": "james"}
    #    return {'hello': name}
    #
    # @app.route('/users', methods=['POST'])
    # def create_user():
    #     # This is the JSON body the user sent in their POST request.
    #     user_as_json = app.current_request.json_body
    #     # We'll echo the json body back to the user in a 'user' key.
    #     return {'user': user_as_json}
    #
    # See the README documentation for more examples.
    #


## Run the function locally

Run the command ```chalice local``` to deploy a local test server

```> chalice local
Serving on http://127.0.0.1:8000
```


```bash
http 127.0.0.1:8000
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m17[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:29:14 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"hello"[39;49;00m: [33m"world"[39;49;00m
    }
    


We see that chalice has allowed us to very quickly
- create an application skeleton and to
- test it locally.

Note that Chalice uses @app.route decoration to declare routes, similarly to the Flask micro-framework.

This whole process is greatly simplified compared with deploying Lambda functions directly which would require
- manually creating a zip file of all sources
- uploading the zip file
- creating appropriate policies
- linking the API Gateway to our Lambda function

### Updates

Try making a change to to app.py file and saving it.

Notice that chalice detects the change and redeploys the server to take into account the changes:
```
user1@ip-172-31-21-116:~/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/chalice-app$ chalice local
Serving on http://127.0.0.1:8000
127.0.0.1 - - [25/Jan/2019 00:45:04] "GET / HTTP/1.1" 200 -
Restarting local dev server.
Serving on http://127.0.0.1:8000
Restarting local dev server.
Serving on http://127.0.0.1:8000
```

## Deploying a function to AWS Lambda
Now let's deploy this to AWS Lambda using the ```chalice deploy``` command.

First let's check if any functions are already deployed or not

**NOTE**: So far we have launched a function on a local test server, we have not deployed in to AWS Lambbda.


```bash
aws lambda list-functions
```

    {
        "Functions": []
    }


then let's look at the options to ```chalice deploy```


```bash
chalice deploy --help
```

    Usage: chalice deploy [OPTIONS]
    
    Options:
      --autogen-policy / --no-autogen-policy
                                      Automatically generate IAM policy for app
                                      code.
      --profile TEXT                  Override profile at deploy time.
      --api-gateway-stage TEXT        Name of the API gateway stage to deploy to.
      --stage TEXT                    Name of the Chalice stage to deploy to.
                                      Specifying a new chalice stage will create
                                      an entirely new set of AWS resources.
      --connection-timeout INTEGER    Overrides the default botocore connection
                                      timeout.
      --help                          Show this message and exit.


Now let's deploy our function


```bash
chalice deploy
```

    /usr/share/python-wheels/requests-2.18.4-py2.py3-none-any.whl/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
    Creating deployment package.
    Updating policy for IAM role: chalice-app-dev
    Creating lambda function: chalice-app-dev
    Creating Rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-1:568285458700:function:chalice-app-dev
      - Rest API URL: https://gxan5eptj8.execute-api.us-west-1.amazonaws.com/api/


We see above the URL on which our API is available, otherwise the ```chalice url``` command provides us with the url.

We can click on that url to open in the browser or access it from the command-line as below.


```bash
chalice url
```

    https://gxan5eptj8.execute-api.us-west-1.amazonaws.com/api/



```bash
http $(chalice url)
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mConnection[39;49;00m: [33mkeep-alive[39;49;00m
    [36mContent-Length[39;49;00m: [33m17[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:29:56 GMT[39;49;00m
    [36mVia[39;49;00m: [33m1.1 34ecd2fc8d142d6781982cb32e3d84bf.cloudfront.net (CloudFront)[39;49;00m
    [36mX-Amz-Cf-Id[39;49;00m: [33mT7UWEHpVgW8Q7SZoO23cIQzCzS4QZiYzOV6Dl6dJLL5BDuVThsRHng==[39;49;00m
    [36mX-Amzn-Trace-Id[39;49;00m: [33mRoot=1-5c4bd433-c8d0a66daeb62bf3ff72f42b;Sampled=0[39;49;00m
    [36mX-Cache[39;49;00m: [33mMiss from cloudfront[39;49;00m
    [36mx-amz-apigw-id[39;49;00m: [33mUF4YHH8zSK4Ffaw=[39;49;00m
    [36mx-amzn-RequestId[39;49;00m: [33ma6972411-211a-11e9-9265-b7cb00312a65[39;49;00m
    
    {
        [34;01m"hello"[39;49;00m: [33m"world"[39;49;00m
    }
    


In just a few commands we've been able to create a project template, run a local test server and deploy our skeleton app to AWS Lambda.

Chalice greatly simplifies the deployment of Python functions.

Note that we can list deployed functions using ```aws lambda list-functions```.

Note also that the function name is chalice-app-dev, by default chalice deploys in '*dev*' mode.


```bash
aws lambda list-functions
```

    {
        "Functions": [
            {
                "FunctionName": "chalice-app-dev",
                "FunctionArn": "arn:aws:lambda:us-west-1:568285458700:function:chalice-app-dev",
                "Runtime": "python3.6",
                "Role": "arn:aws:iam::568285458700:role/chalice-app-dev",
                "Handler": "app.app",
                "CodeSize": 10518,
                "Description": "",
                "Timeout": 60,
                "MemorySize": 128,
                "LastModified": "2019-01-26T03:29:43.294+0000",
                "CodeSha256": "Uba16QADvw213FT3PyeqJhSxrDsDnym6JnMqYWZXysU=",
                "Version": "$LATEST",
                "VpcConfig": {
                    "SubnetIds": [],
                    "SecurityGroupIds": [],
                    "VpcId": ""
                },
                "Environment": {
                    "Variables": {}
                },
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": "23d15802-cfa7-4a72-8a61-68fc131d700e"
            }
        ]
    }



```bash
cat > app.py <<EOF

from chalice import Chalice

app = Chalice(app_name='chalice-app')

@app.route('/')
def index():
    print("Looks like we got a request!") ## Should appear in CloudWatch logs
    return {'hello': 'world'}
    
EOF
```

Now let's redeploy our function and make a request to it


```bash
chalice deploy
```

    /usr/share/python-wheels/requests-2.18.4-py2.py3-none-any.whl/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
    Creating deployment package.
    Updating policy for IAM role: chalice-app-dev
    Updating lambda function: chalice-app-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-1:568285458700:function:chalice-app-dev
      - Rest API URL: https://gxan5eptj8.execute-api.us-west-1.amazonaws.com/api/



```bash
http $(chalice url)
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mConnection[39;49;00m: [33mkeep-alive[39;49;00m
    [36mContent-Length[39;49;00m: [33m17[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:30:43 GMT[39;49;00m
    [36mVia[39;49;00m: [33m1.1 e75f5fedf935ed2a4a49debe6c78d172.cloudfront.net (CloudFront)[39;49;00m
    [36mX-Amz-Cf-Id[39;49;00m: [33mFh_dlKn3cOKAx_mcoMLfVl97SMMzm2wOc5Dr9U7QAEJj6lm07OhavQ==[39;49;00m
    [36mX-Amzn-Trace-Id[39;49;00m: [33mRoot=1-5c4bd463-4d76411edd93fea6b81f166c;Sampled=0[39;49;00m
    [36mX-Cache[39;49;00m: [33mMiss from cloudfront[39;49;00m
    [36mx-amz-apigw-id[39;49;00m: [33mUF4feElUSK4FlTA=[39;49;00m
    [36mx-amzn-RequestId[39;49;00m: [33mc2b2e128-211a-11e9-8589-d30094675486[39;49;00m
    
    {
        [34;01m"hello"[39;49;00m: [33m"world"[39;49;00m
    }
    



```bash
chalice logs --include-lambda-messages | grep Looks
```

    2019-01-25 23:01:06.688000 27caab [01;31m[KLooks[m[K like we got a request!
    2019-01-26 02:52:51.463000 ebd3d5 [01;31m[KLooks[m[K like we got a request!
    2019-01-26 03:20:40.767000 cec580 [01;31m[KLooks[m[K like we got a request!



```bash
cleanup_functions
```

    -- Functions before:
                "[01;31m[KFunctionName[m[K": "chalice-app-dev",
    -- Functions after cleanup:




# Scheduled events


```bash
aws lambda list-functions 
```

    {
        "Functions": []
    }



```bash
cd ~/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda


chalice new-project scheduled-app
```


```bash
cd scheduled-app
ls -al 
```

    total 20
    drwxrwxr-x  3 user1 user1 4096 Jan 26 03:31 [0m[01;34m.[0m
    drwxrwxr-x 11 user1 user1 4096 Jan 26 03:31 [01;34m..[0m
    drwxrwxr-x  2 user1 user1 4096 Jan 26 03:31 [01;34m.chalice[0m
    -rw-rw-r--  1 user1 user1   37 Jan 26 03:31 .gitignore
    -rw-rw-r--  1 user1 user1  738 Jan 26 03:31 app.py
    -rw-rw-r--  1 user1 user1    0 Jan 26 03:31 requirements.txt



```bash
pwd
cat app.py
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/scheduled-app
    from chalice import Chalice
    
    app = Chalice(app_name='scheduled-app')
    
    
    @app.route('/')
    def index():
        return {'hello': 'world'}
    
    
    # The view function above will return {"hello": "world"}
    # whenever you make an HTTP GET request to '/'.
    #
    # Here are a few more examples:
    #
    # @app.route('/hello/{name}')
    # def hello_name(name):
    #    # '/hello/james' -> {"hello": "james"}
    #    return {'hello': name}
    #
    # @app.route('/users', methods=['POST'])
    # def create_user():
    #     # This is the JSON body the user sent in their POST request.
    #     user_as_json = app.current_request.json_body
    #     # We'll echo the json body back to the user in a 'user' key.
    #     return {'user': user_as_json}
    #
    # See the README documentation for more examples.
    #



```bash
cat > app.py <<EOF

from chalice import Chalice, Rate

app = Chalice(app_name="scheduled-app")
app.debug = True

# Automatically runs every 1 minutes
@app.schedule(Rate(1, unit=Rate.MINUTES))
def periodic_task(event):
    print("Scheduled[1 min]")
    return {"hello": "world"}
EOF
```


```bash
pwd
aws lambda list-functions
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/scheduled-app
    {
        "Functions": []
    }



```bash
chalice deploy
```

    /usr/share/python-wheels/requests-2.18.4-py2.py3-none-any.whl/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
    Creating deployment package.
    Creating IAM role: scheduled-app-dev
    Creating lambda function: scheduled-app-dev-periodic_task
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-1:568285458700:function:scheduled-app-dev-periodic_task



```bash
chalice logs --include-lambda-messages
```


```bash
aws lambda list-functions
```

    {
        "Functions": [
            {
                "FunctionName": "scheduled-app-dev-periodic_task",
                "FunctionArn": "arn:aws:lambda:us-west-1:568285458700:function:scheduled-app-dev-periodic_task",
                "Runtime": "python3.6",
                "Role": "arn:aws:iam::568285458700:role/scheduled-app-dev",
                "Handler": "app.periodic_task",
                "CodeSize": 10309,
                "Description": "",
                "Timeout": 60,
                "MemorySize": 128,
                "LastModified": "2019-01-26T03:33:52.685+0000",
                "CodeSha256": "uh3k06OKlHnGH1dTkfoSX0YTDp4Q6zT9rUWW3AWqB+w=",
                "Version": "$LATEST",
                "VpcConfig": {
                    "SubnetIds": [],
                    "SecurityGroupIds": [],
                    "VpcId": ""
                },
                "Environment": {
                    "Variables": {}
                },
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": "85b4aac2-b384-4bad-8120-4c198284ee54"
            }
        ]
    }



```bash
chalice logs --include-lambda-messages
```

    2019-01-25 00:00:11.996000 44d41c START RequestId: 969cdc86-aa85-4719-bf77-aff5d863a8a9 Version: $LATEST
    2019-01-25 00:00:11.996000 44d41c END RequestId: 969cdc86-aa85-4719-bf77-aff5d863a8a9
    2019-01-25 00:00:11.996000 44d41c REPORT RequestId: 969cdc86-aa85-4719-bf77-aff5d863a8a9	Duration: 0.57 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:07:22.639000 44d41c START RequestId: 1a0a3cdc-b023-4d69-98f5-a145f0e478ee Version: $LATEST
    2019-01-25 00:07:22.709000 44d41c END RequestId: 1a0a3cdc-b023-4d69-98f5-a145f0e478ee
    2019-01-25 00:07:22.709000 44d41c REPORT RequestId: 1a0a3cdc-b023-4d69-98f5-a145f0e478ee	Duration: 29.26 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:28:18.733000 44d41c START RequestId: 6ba33c1e-d1b2-4da5-8933-4933a5ebfff3 Version: $LATEST
    2019-01-25 00:28:18.750000 44d41c END RequestId: 6ba33c1e-d1b2-4da5-8933-4933a5ebfff3
    2019-01-25 00:28:18.751000 44d41c REPORT RequestId: 6ba33c1e-d1b2-4da5-8933-4933a5ebfff3	Duration: 14.83 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:31:45.153000 44d41c START RequestId: 072db1a5-49c1-4ac6-8ba0-78d4ad8ad7c5 Version: $LATEST
    2019-01-25 00:31:45.170000 44d41c END RequestId: 072db1a5-49c1-4ac6-8ba0-78d4ad8ad7c5
    2019-01-25 00:31:45.171000 44d41c REPORT RequestId: 072db1a5-49c1-4ac6-8ba0-78d4ad8ad7c5	Duration: 8.52 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:31:56.295000 44d41c START RequestId: c07e5a87-7bd4-4696-ba24-0466896de69f Version: $LATEST
    2019-01-25 00:31:56.299000 44d41c END RequestId: c07e5a87-7bd4-4696-ba24-0466896de69f
    2019-01-25 00:31:56.299000 44d41c REPORT RequestId: c07e5a87-7bd4-4696-ba24-0466896de69f	Duration: 0.50 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:33:03.721000 44d41c START RequestId: 3f97d0c1-4c33-4b15-9ad1-99eb1c490001 Version: $LATEST
    2019-01-25 00:33:03.730000 44d41c END RequestId: 3f97d0c1-4c33-4b15-9ad1-99eb1c490001
    2019-01-25 00:33:03.731000 44d41c REPORT RequestId: 3f97d0c1-4c33-4b15-9ad1-99eb1c490001	Duration: 6.83 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:35:22.480000 44d41c START RequestId: d2dce572-7dd2-40d7-88db-736c1dd2462d Version: $LATEST
    2019-01-25 00:35:22.491000 44d41c END RequestId: d2dce572-7dd2-40d7-88db-736c1dd2462d
    2019-01-25 00:35:22.549000 44d41c REPORT RequestId: d2dce572-7dd2-40d7-88db-736c1dd2462d	Duration: 6.59 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 00:47:21.940000 65a894 START RequestId: 53c1191a-3e3f-4271-85a5-394cb7db89a2 Version: $LATEST
    2019-01-25 00:47:21.941000 65a894 END RequestId: 53c1191a-3e3f-4271-85a5-394cb7db89a2
    2019-01-25 00:47:21.941000 65a894 REPORT RequestId: 53c1191a-3e3f-4271-85a5-394cb7db89a2	Duration: 0.67 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 02:43:26.823000 ffa2ce START RequestId: 76354301-cd04-49ad-8630-1b0acd6d4662 Version: $LATEST
    2019-01-25 02:43:26.824000 ffa2ce module initialization error: Credentials are required to create a TwilioClient
    2019-01-25 02:43:27.067000 ffa2ce END RequestId: 76354301-cd04-49ad-8630-1b0acd6d4662
    2019-01-25 02:43:27.067000 ffa2ce REPORT RequestId: 76354301-cd04-49ad-8630-1b0acd6d4662	Duration: 243.64 ms	Billed Duration: 300 ms 	Memory Size: 128 MB	Max Memory Used: 32 MB
    2019-01-25 02:43:27.067000 ffa2ce module initialization error
    Credentials are required to create a TwilioClient
    2019-01-25 22:53:22.155000 f5a0b1 START RequestId: 85df50d2-cbc9-4a1a-9beb-23770635daf9 Version: $LATEST
    2019-01-25 22:53:22.156000 f5a0b1 END RequestId: 85df50d2-cbc9-4a1a-9beb-23770635daf9
    2019-01-25 22:53:22.156000 f5a0b1 REPORT RequestId: 85df50d2-cbc9-4a1a-9beb-23770635daf9	Duration: 0.45 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 22:54:02.138000 f5a0b1 START RequestId: 33c59fb9-038b-4876-9383-388f16874b2b Version: $LATEST
    2019-01-25 22:54:02.141000 f5a0b1 END RequestId: 33c59fb9-038b-4876-9383-388f16874b2b
    2019-01-25 22:54:02.141000 f5a0b1 REPORT RequestId: 33c59fb9-038b-4876-9383-388f16874b2b	Duration: 0.50 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-25 23:01:06.688000 27caab START RequestId: af58ccc6-bbfb-4dbf-ada5-477f4b11fefe Version: $LATEST
    2019-01-25 23:01:06.688000 27caab Looks like we got a request!
    2019-01-25 23:01:06.689000 27caab END RequestId: af58ccc6-bbfb-4dbf-ada5-477f4b11fefe
    2019-01-25 23:01:06.689000 27caab REPORT RequestId: af58ccc6-bbfb-4dbf-ada5-477f4b11fefe	Duration: 29.07 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 00:22:26.050000 c313db START RequestId: 79d084f2-0565-4421-8856-1fee1f67afe5 Version: $LATEST
    2019-01-26 00:22:26.050000 c313db s3objects: <<chalice.app.Request object at 0x7ffa1f2c6940>>
    2019-01-26 00:22:26.709000 c313db END RequestId: 79d084f2-0565-4421-8856-1fee1f67afe5
    2019-01-26 00:22:26.709000 c313db REPORT RequestId: 79d084f2-0565-4421-8856-1fee1f67afe5	Duration: 657.25 ms	Billed Duration: 700 ms 	Memory Size: 128 MB	Max Memory Used: 42 MB
    2019-01-26 00:24:34.082000 a295f6 START RequestId: 8a682a39-18d3-464c-bf1b-d45257bc1c5b Version: $LATEST
    2019-01-26 00:24:34.082000 a295f6 s3objects: <<chalice.app.Request object at 0x7fa8a7cd6940>>
    2019-01-26 00:24:34.650000 a295f6 END RequestId: 8a682a39-18d3-464c-bf1b-d45257bc1c5b
    2019-01-26 00:24:34.650000 a295f6 REPORT RequestId: 8a682a39-18d3-464c-bf1b-d45257bc1c5b	Duration: 567.71 ms	Billed Duration: 600 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 00:27:26.817000 c569b0 START RequestId: 1d63580c-1dbc-42d2-9958-aad5850e6c1e Version: $LATEST
    2019-01-26 00:27:26.818000 c569b0 s3 - ERROR - Internal Error for <function s3objects at 0x7f22ac1fc730>
    2019-01-26 00:27:26.818000 c569b0 Traceback (most recent call last):
    2019-01-26 00:27:26.818000 c569b0 File "/var/task/chalice/app.py", line 731, in _get_view_function_response
    2019-01-26 00:27:26.818000 c569b0 response = view_function(**function_args)
    2019-01-26 00:27:26.818000 c569b0 File "/var/task/app.py", line 20, in s3objects
    2019-01-26 00:27:26.818000 c569b0 req = json.dumps(request, default=handle_decimals)
    2019-01-26 00:27:26.818000 c569b0 NameError: name 'handle_decimals' is not defined
    2019-01-26 00:27:26.829000 c569b0 END RequestId: 1d63580c-1dbc-42d2-9958-aad5850e6c1e
    2019-01-26 00:27:26.829000 c569b0 REPORT RequestId: 1d63580c-1dbc-42d2-9958-aad5850e6c1e	Duration: 1.46 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 35 MB
    2019-01-26 00:32:18.695000 b6528d START RequestId: 5533a0b2-d2f8-468c-81dc-2429073b668a Version: $LATEST
    2019-01-26 00:32:18.695000 b6528d s3objects: <{"query_params": null, "headers": {"accept": "*/*", "accept-encoding": "gzip, deflate", "cloudfront-forwarded-proto": "https", "cloudfront-is-desktop-viewer": "true", "cloudfront-is-mobile-viewer": "false", "cloudfront-is-smarttv-viewer": "false", "cloudfront-is-tablet-viewer": "false", "cloudfront-viewer-country": "US", "host": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "user-agent": "HTTPie/0.9.8", "via": "1.1 f1a40337a32137e1c23ceffead6a50d5.cloudfront.net (CloudFront)", "x-amz-cf-id": "Bt_hdRpgoK_u8oGdWSuYLo42AEdGxKYmJEnJjOeLbZ7og4P1kyMFZw==", "x-amzn-trace-id": "Root=1-5c4baa92-b9b2765f8181eff9ffbc7e42", "x-forwarded-for": "54.67.51.193, 54.239.134.7", "x-forwarded-port": "443", "x-forwarded-proto": "https"}, "uri_params": {"key": "test"}, "method": "GET", "context": {"resourceId": "wvdbuo", "resourcePath": "/objects/{key}", "httpMethod": "GET", "extendedRequestId": "UFeW0GbkyK4Fitg=", "requestTime": "26/Jan/2019:00:32:18 +0000", "path": "/api/objects/test", "accountId": "568285458700", "protocol": "HTTP/1.1", "stage": "api", "domainPrefix": "jlmq3ygdu1", "requestTimeEpoch": 1548462738044, "requestId": "d5feccae-2101-11e9-900f-d5ae7e711214", "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "sourceIp": "54.67.51.193", "accessKey": null, "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "HTTPie/0.9.8", "user": null}, "domainName": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "apiId": "jlmq3ygdu1"}, "stage_vars": null}>
    2019-01-26 00:32:19.330000 b6528d END RequestId: 5533a0b2-d2f8-468c-81dc-2429073b668a
    2019-01-26 00:32:19.330000 b6528d REPORT RequestId: 5533a0b2-d2f8-468c-81dc-2429073b668a	Duration: 634.91 ms	Billed Duration: 700 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 00:34:33.414000 a8ddcb START RequestId: bce9a152-cb73-4261-9bec-3c0d10582899 Version: $LATEST
    2019-01-26 00:34:33.415000 a8ddcb s3objects: SO FAR SO GOOD
    2019-01-26 00:34:33.415000 a8ddcb s3objects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 5c2ff4ca1e447265402af29264e83497.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'mQCX2b5PHSGu4WVl-i1aUxzXHg9DnMHq5hUiAspg9Cqv_DL8c9Lw_w==', 'x-amzn-trace-id': 'Root=1-5c4bab18-5c7d601bd991bc898c6db78f', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFer3HhUSK4FghQ=', 'requestTime': '26/Jan/2019:00:34:32 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548462872776, 'requestId': '264d4499-2102-11e9-9ca2-032065ee22a7', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:34:33.415000 a8ddcb s3objects: <{"query_params": null, "headers": {"accept": "*/*", "accept-encoding": "gzip, deflate", "cloudfront-forwarded-proto": "https", "cloudfront-is-desktop-viewer": "true", "cloudfront-is-mobile-viewer": "false", "cloudfront-is-smarttv-viewer": "false", "cloudfront-is-tablet-viewer": "false", "cloudfront-viewer-country": "US", "host": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "user-agent": "HTTPie/0.9.8", "via": "1.1 5c2ff4ca1e447265402af29264e83497.cloudfront.net (CloudFront)", "x-amz-cf-id": "mQCX2b5PHSGu4WVl-i1aUxzXHg9DnMHq5hUiAspg9Cqv_DL8c9Lw_w==", "x-amzn-trace-id": "Root=1-5c4bab18-5c7d601bd991bc898c6db78f", "x-forwarded-for": "54.67.51.193, 54.239.134.7", "x-forwarded-port": "443", "x-forwarded-proto": "https"}, "uri_params": {"key": "test"}, "method": "GET", "context": {"resourceId": "wvdbuo", "resourcePath": "/objects/{key}", "httpMethod": "GET", "extendedRequestId": "UFer3HhUSK4FghQ=", "requestTime": "26/Jan/2019:00:34:32 +0000", "path": "/api/objects/test", "accountId": "568285458700", "protocol": "HTTP/1.1", "stage": "api", "domainPrefix": "jlmq3ygdu1", "requestTimeEpoch": 1548462872776, "requestId": "264d4499-2102-11e9-9ca2-032065ee22a7", "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "sourceIp": "54.67.51.193", "accessKey": null, "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "HTTPie/0.9.8", "user": null}, "domainName": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "apiId": "jlmq3ygdu1"}, "stage_vars": null}>
    2019-01-26 00:34:33.989000 a8ddcb END RequestId: bce9a152-cb73-4261-9bec-3c0d10582899
    2019-01-26 00:34:33.989000 a8ddcb REPORT RequestId: bce9a152-cb73-4261-9bec-3c0d10582899	Duration: 574.42 ms	Billed Duration: 600 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 00:37:55.453000 a8ddcb START RequestId: 91b39421-4222-4d9a-8381-a3ac5ac88572 Version: $LATEST
    2019-01-26 00:37:55.489000 a8ddcb s3objects: SO FAR SO GOOD
    2019-01-26 00:37:55.489000 a8ddcb s3objects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 20f1c35f343f4b271ae8dcacfd7ea0e9.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'ruqvfTXReomBotCmWepayfZnZVp5Nln6TThdjKf8xT1oPKVTAxJUbg==', 'x-amzn-trace-id': 'Root=1-5c4babe3-d12496852222efb0d911dfa2', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFfLiFlNSK4Fmrw=', 'requestTime': '26/Jan/2019:00:37:55 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463075419, 'requestId': '9f1622b9-2102-11e9-b14b-5551fb47ff1c', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:37:55.489000 a8ddcb s3objects: <{"query_params": null, "headers": {"accept": "*/*", "accept-encoding": "gzip, deflate", "cloudfront-forwarded-proto": "https", "cloudfront-is-desktop-viewer": "true", "cloudfront-is-mobile-viewer": "false", "cloudfront-is-smarttv-viewer": "false", "cloudfront-is-tablet-viewer": "false", "cloudfront-viewer-country": "US", "host": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "user-agent": "HTTPie/0.9.8", "via": "1.1 20f1c35f343f4b271ae8dcacfd7ea0e9.cloudfront.net (CloudFront)", "x-amz-cf-id": "ruqvfTXReomBotCmWepayfZnZVp5Nln6TThdjKf8xT1oPKVTAxJUbg==", "x-amzn-trace-id": "Root=1-5c4babe3-d12496852222efb0d911dfa2", "x-forwarded-for": "54.67.51.193, 54.239.134.14", "x-forwarded-port": "443", "x-forwarded-proto": "https"}, "uri_params": {"key": "test"}, "method": "GET", "context": {"resourceId": "wvdbuo", "resourcePath": "/objects/{key}", "httpMethod": "GET", "extendedRequestId": "UFfLiFlNSK4Fmrw=", "requestTime": "26/Jan/2019:00:37:55 +0000", "path": "/api/objects/test", "accountId": "568285458700", "protocol": "HTTP/1.1", "stage": "api", "domainPrefix": "jlmq3ygdu1", "requestTimeEpoch": 1548463075419, "requestId": "9f1622b9-2102-11e9-b14b-5551fb47ff1c", "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "sourceIp": "54.67.51.193", "accessKey": null, "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "HTTPie/0.9.8", "user": null}, "domainName": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "apiId": "jlmq3ygdu1"}, "stage_vars": null}>
    2019-01-26 00:37:56.009000 a8ddcb s3 - ERROR - Internal Error for <function s3objects at 0x7f6689386730>
    2019-01-26 00:37:56.009000 a8ddcb Traceback (most recent call last):
    2019-01-26 00:37:56.009000 a8ddcb File "/var/task/chalice/app.py", line 731, in _get_view_function_response
    2019-01-26 00:37:56.009000 a8ddcb response = view_function(**function_args)
    2019-01-26 00:37:56.009000 a8ddcb File "/var/task/app.py", line 35, in s3objects
    2019-01-26 00:37:56.009000 a8ddcb return json.loads(response['Body'].read())
    2019-01-26 00:37:56.009000 a8ddcb File "/var/lang/lib/python3.6/json/__init__.py", line 354, in loads
    2019-01-26 00:37:56.009000 a8ddcb return _default_decoder.decode(s)
    2019-01-26 00:37:56.009000 a8ddcb File "/var/lang/lib/python3.6/json/decoder.py", line 339, in decode
    2019-01-26 00:37:56.009000 a8ddcb obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    2019-01-26 00:37:56.009000 a8ddcb File "/var/lang/lib/python3.6/json/decoder.py", line 357, in raw_decode
    2019-01-26 00:37:56.009000 a8ddcb raise JSONDecodeError("Expecting value", s, err.value) from None
    2019-01-26 00:37:56.009000 a8ddcb json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 1)
    2019-01-26 00:37:56.009000 a8ddcb END RequestId: 91b39421-4222-4d9a-8381-a3ac5ac88572
    2019-01-26 00:37:56.009000 a8ddcb REPORT RequestId: 91b39421-4222-4d9a-8381-a3ac5ac88572	Duration: 555.22 ms	Billed Duration: 600 ms 	Memory Size: 128 MB	Max Memory Used: 38 MB
    2019-01-26 00:39:25.506000 882ee8 START RequestId: 33e782d0-3f4f-42a3-a976-24acf9df7954 Version: $LATEST
    2019-01-26 00:39:25.506000 882ee8 s3objects: SO FAR SO GOOD -----------------------------------------------------------------
    2019-01-26 00:39:25.506000 882ee8 s3objects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 24b0e5a3429d07ef12381da50e07f70f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'jJFLYx3gAXNkB8v5_zW3OgO7IYkbvDBktrUD8hZSt2qp20QVMpXIew==', 'x-amzn-trace-id': 'Root=1-5c4bac3c-2d30962cbacf1490cf4231f6', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFfZgGp6SK4Ff-A=', 'requestTime': '26/Jan/2019:00:39:24 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463164862, 'requestId': 'd4660ebb-2102-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:39:25.506000 882ee8 GET s3://mjbright-uploads/test
    2019-01-26 00:39:26.089000 882ee8 s3 - ERROR - Internal Error for <function s3objects at 0x7f74add50730>
    2019-01-26 00:39:26.089000 882ee8 Traceback (most recent call last):
    2019-01-26 00:39:26.089000 882ee8 File "/var/task/chalice/app.py", line 731, in _get_view_function_response
    2019-01-26 00:39:26.089000 882ee8 response = view_function(**function_args)
    2019-01-26 00:39:26.089000 882ee8 File "/var/task/app.py", line 36, in s3objects
    2019-01-26 00:39:26.089000 882ee8 return json.loads(response['Body'].read())
    2019-01-26 00:39:26.089000 882ee8 File "/var/lang/lib/python3.6/json/__init__.py", line 354, in loads
    2019-01-26 00:39:26.089000 882ee8 return _default_decoder.decode(s)
    2019-01-26 00:39:26.089000 882ee8 File "/var/lang/lib/python3.6/json/decoder.py", line 339, in decode
    2019-01-26 00:39:26.089000 882ee8 obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    2019-01-26 00:39:26.089000 882ee8 File "/var/lang/lib/python3.6/json/decoder.py", line 357, in raw_decode
    2019-01-26 00:39:26.089000 882ee8 raise JSONDecodeError("Expecting value", s, err.value) from None
    2019-01-26 00:39:26.089000 882ee8 json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 1)
    2019-01-26 00:39:26.090000 882ee8 END RequestId: 33e782d0-3f4f-42a3-a976-24acf9df7954
    2019-01-26 00:39:26.090000 882ee8 REPORT RequestId: 33e782d0-3f4f-42a3-a976-24acf9df7954	Duration: 584.00 ms	Billed Duration: 600 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 00:42:38.817000 0d4318 START RequestId: def1b97f-eb01-467c-9650-a5267077b1da Version: $LATEST
    2019-01-26 00:42:38.817000 0d4318 s3objects: SO FAR SO GOOD -----------------------------------------------------------------
    2019-01-26 00:42:38.817000 0d4318 s3objects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 1b52a5dd431f9e3c81753e61dfdf467a.cloudfront.net (CloudFront)', 'x-amz-cf-id': '66biLrXpMrvpM4V03J1OvKfbPVXicEW22C7uQ6u9oItwQAHGgMDUCg==', 'x-amzn-trace-id': 'Root=1-5c4bacfe-36903ca282508f579135cda1', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFf3tEdCyK4Fp6w=', 'requestTime': '26/Jan/2019:00:42:38 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463358168, 'requestId': '479e35bd-2103-11e9-b75a-8fe56bba7a8e', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:42:38.817000 0d4318 GET s3://mjbright-uploads/test
    2019-01-26 00:42:39.449000 0d4318 s3 - ERROR - Internal Error for <function s3objects at 0x7fb703c83730>
    2019-01-26 00:42:39.449000 0d4318 Traceback (most recent call last):
    2019-01-26 00:42:39.449000 0d4318 File "/var/task/chalice/app.py", line 731, in _get_view_function_response
    2019-01-26 00:42:39.449000 0d4318 response = view_function(**function_args)
    2019-01-26 00:42:39.449000 0d4318 File "/var/task/app.py", line 36, in s3objects
    2019-01-26 00:42:39.449000 0d4318 return json.loads(response['Body'].read())
    2019-01-26 00:42:39.449000 0d4318 File "/var/lang/lib/python3.6/json/__init__.py", line 354, in loads
    2019-01-26 00:42:39.449000 0d4318 return _default_decoder.decode(s)
    2019-01-26 00:42:39.449000 0d4318 File "/var/lang/lib/python3.6/json/decoder.py", line 339, in decode
    2019-01-26 00:42:39.449000 0d4318 obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    2019-01-26 00:42:39.449000 0d4318 File "/var/lang/lib/python3.6/json/decoder.py", line 355, in raw_decode
    2019-01-26 00:42:39.449000 0d4318 obj, end = self.scan_once(s, idx)
    2019-01-26 00:42:39.449000 0d4318 json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
    2019-01-26 00:42:39.469000 0d4318 END RequestId: def1b97f-eb01-467c-9650-a5267077b1da
    2019-01-26 00:42:39.469000 0d4318 REPORT RequestId: def1b97f-eb01-467c-9650-a5267077b1da	Duration: 632.66 ms	Billed Duration: 700 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 00:46:09.357000 830682 START RequestId: 7a774729-e5d8-4279-97ca-67ef720318d2 Version: $LATEST
    2019-01-26 00:46:09.358000 830682 s3objects: SO FAR SO GOOD -----------------------------------------------------------------
    2019-01-26 00:46:09.358000 830682 s3objects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 24b0e5a3429d07ef12381da50e07f70f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'O2lh0HapYLq_0y5dVOfrUFBbkwRLoamPEqLGPzNn7rkgHm9z34tbJg==', 'x-amzn-trace-id': 'Root=1-5c4badd0-12c28bf8272ed3db0745db70', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFgYnGv6yK4Fitg=', 'requestTime': '26/Jan/2019:00:46:08 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463568702, 'requestId': 'c51b26d3-2103-11e9-900f-d5ae7e711214', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:46:09.358000 830682 GET s3://mjbright-uploads/test
    2019-01-26 00:46:10.009000 830682 END RequestId: 7a774729-e5d8-4279-97ca-67ef720318d2
    2019-01-26 00:46:10.009000 830682 REPORT RequestId: 7a774729-e5d8-4279-97ca-67ef720318d2	Duration: 632.71 ms	Billed Duration: 700 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 01:03:44.795000 189dfc START RequestId: 049afcfb-6aca-4f20-9bc9-022e42bbd3a5 Version: $LATEST
    2019-01-26 01:03:44.809000 189dfc s3text: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 e2af8a85927835558866752f53562ecd.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'pc2_vVu5MLKAg72qL6zQ9Fj-Y9UHZS8R-gBq76TbPcrAIvrVKzhS6g==', 'x-amzn-trace-id': 'Root=1-5c4bb1f0-4a683a7b7d0b5cf1ac91e237', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFi9hGfnyK4FUUQ=', 'requestTime': '26/Jan/2019:01:03:44 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464624139, 'requestId': '3a320e6d-2106-11e9-b04b-6deecaeee351', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:03:44.809000 189dfc s3text: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 e2af8a85927835558866752f53562ecd.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'pc2_vVu5MLKAg72qL6zQ9Fj-Y9UHZS8R-gBq76TbPcrAIvrVKzhS6g==', 'x-amzn-trace-id': 'Root=1-5c4bb1f0-4a683a7b7d0b5cf1ac91e237', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFi9hGfnyK4FUUQ=', 'requestTime': '26/Jan/2019:01:03:44 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464624139, 'requestId': '3a320e6d-2106-11e9-b04b-6deecaeee351', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:03:44.810000 189dfc {   'context': {   'accountId': '568285458700',
    2019-01-26 01:03:44.810000 189dfc 'apiId': 'jlmq3ygdu1',
    2019-01-26 01:03:44.810000 189dfc 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:03:44.810000 189dfc 'domainPrefix': 'jlmq3ygdu1',
    2019-01-26 01:03:44.810000 189dfc 'extendedRequestId': 'UFi9hGfnyK4FUUQ=',
    2019-01-26 01:03:44.810000 189dfc 'httpMethod': 'GET',
    2019-01-26 01:03:44.810000 189dfc 'identity': {   'accessKey': None,
    2019-01-26 01:03:44.810000 189dfc 'accountId': None,
    2019-01-26 01:03:44.810000 189dfc 'caller': None,
    2019-01-26 01:03:44.810000 189dfc 'cognitoAuthenticationProvider': None,
    2019-01-26 01:03:44.810000 189dfc 'cognitoAuthenticationType': None,
    2019-01-26 01:03:44.811000 189dfc 'cognitoIdentityId': None,
    2019-01-26 01:03:44.811000 189dfc 'cognitoIdentityPoolId': None,
    2019-01-26 01:03:44.811000 189dfc 'sourceIp': '54.67.51.193',
    2019-01-26 01:03:44.811000 189dfc 'user': None,
    2019-01-26 01:03:44.811000 189dfc 'userAgent': 'HTTPie/0.9.8',
    2019-01-26 01:03:44.811000 189dfc 'userArn': None},
    2019-01-26 01:03:44.811000 189dfc 'path': '/api/text/test',
    2019-01-26 01:03:44.811000 189dfc 'protocol': 'HTTP/1.1',
    2019-01-26 01:03:44.811000 189dfc 'requestId': '3a320e6d-2106-11e9-b04b-6deecaeee351',
    2019-01-26 01:03:44.811000 189dfc 'requestTime': '26/Jan/2019:01:03:44 +0000',
    2019-01-26 01:03:44.811000 189dfc 'requestTimeEpoch': 1548464624139,
    2019-01-26 01:03:44.811000 189dfc 'resourceId': 'ezap0f',
    2019-01-26 01:03:44.811000 189dfc 'resourcePath': '/text/{key}',
    2019-01-26 01:03:44.811000 189dfc 'stage': 'api'},
    2019-01-26 01:03:44.849000 189dfc 'headers': {   'accept': '*/*',
    2019-01-26 01:03:44.849000 189dfc 'accept-encoding': 'gzip, deflate',
    2019-01-26 01:03:44.849000 189dfc 'cloudfront-forwarded-proto': 'https',
    2019-01-26 01:03:44.849000 189dfc 'cloudfront-is-desktop-viewer': 'true',
    2019-01-26 01:03:44.849000 189dfc 'cloudfront-is-mobile-viewer': 'false',
    2019-01-26 01:03:44.849000 189dfc 'cloudfront-is-smarttv-viewer': 'false',
    2019-01-26 01:03:44.849000 189dfc 'cloudfront-is-tablet-viewer': 'false',
    2019-01-26 01:03:44.849000 189dfc 'cloudfront-viewer-country': 'US',
    2019-01-26 01:03:44.849000 189dfc 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:03:44.849000 189dfc 'user-agent': 'HTTPie/0.9.8',
    2019-01-26 01:03:44.849000 189dfc 'via': '1.1 e2af8a85927835558866752f53562ecd.cloudfront.net '
    2019-01-26 01:03:44.849000 189dfc '(CloudFront)',
    2019-01-26 01:03:44.849000 189dfc 'x-amz-cf-id': 'pc2_vVu5MLKAg72qL6zQ9Fj-Y9UHZS8R-gBq76TbPcrAIvrVKzhS6g==',
    2019-01-26 01:03:44.849000 189dfc 'x-amzn-trace-id': 'Root=1-5c4bb1f0-4a683a7b7d0b5cf1ac91e237',
    2019-01-26 01:03:44.850000 189dfc 'x-forwarded-for': '54.67.51.193, 54.239.134.14',
    2019-01-26 01:03:44.850000 189dfc 'x-forwarded-port': '443',
    2019-01-26 01:03:44.850000 189dfc 'x-forwarded-proto': 'https'},
    2019-01-26 01:03:44.850000 189dfc 'method': 'GET',
    2019-01-26 01:03:44.850000 189dfc 'query_params': None,
    2019-01-26 01:03:44.850000 189dfc 'stage_vars': None,
    2019-01-26 01:03:44.850000 189dfc 'uri_params': {'key': 'test'}}
    2019-01-26 01:03:44.869000 189dfc GET s3://mjbright-uploads/test
    2019-01-26 01:03:45.490000 189dfc END RequestId: 049afcfb-6aca-4f20-9bc9-022e42bbd3a5
    2019-01-26 01:03:45.509000 189dfc REPORT RequestId: 049afcfb-6aca-4f20-9bc9-022e42bbd3a5	Duration: 695.59 ms	Billed Duration: 700 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 01:04:01.427000 189dfc START RequestId: 9788080c-6ed5-49bb-a096-0e869f307417 Version: $LATEST
    2019-01-26 01:04:01.431000 189dfc s3text: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 49c80a47c1441dd194a8337982f1cd7e.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'THP5eRWQ4cEezLBbXU-2vT4VzPDF4-mCFcMy6JMGOQTUd367pcvL4w==', 'x-amzn-trace-id': 'Root=1-5c4bb201-b56313b28f6fdc1ce3892232', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAOGudyK4FSUw=', 'requestTime': '26/Jan/2019:01:04:01 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464641414, 'requestId': '447e02ca-2106-11e9-86ac-6596e4f7f276', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:01.431000 189dfc s3text: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 49c80a47c1441dd194a8337982f1cd7e.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'THP5eRWQ4cEezLBbXU-2vT4VzPDF4-mCFcMy6JMGOQTUd367pcvL4w==', 'x-amzn-trace-id': 'Root=1-5c4bb201-b56313b28f6fdc1ce3892232', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAOGudyK4FSUw=', 'requestTime': '26/Jan/2019:01:04:01 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464641414, 'requestId': '447e02ca-2106-11e9-86ac-6596e4f7f276', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:01.431000 189dfc {   'context': {   'accountId': '568285458700',
    2019-01-26 01:04:01.432000 189dfc 'apiId': 'jlmq3ygdu1',
    2019-01-26 01:04:01.432000 189dfc 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:04:01.432000 189dfc 'domainPrefix': 'jlmq3ygdu1',
    2019-01-26 01:04:01.432000 189dfc 'extendedRequestId': 'UFjAOGudyK4FSUw=',
    2019-01-26 01:04:01.432000 189dfc 'httpMethod': 'GET',
    2019-01-26 01:04:01.432000 189dfc 'identity': {   'accessKey': None,
    2019-01-26 01:04:01.432000 189dfc 'accountId': None,
    2019-01-26 01:04:01.432000 189dfc 'caller': None,
    2019-01-26 01:04:01.432000 189dfc 'cognitoAuthenticationProvider': None,
    2019-01-26 01:04:01.432000 189dfc 'cognitoAuthenticationType': None,
    2019-01-26 01:04:01.432000 189dfc 'cognitoIdentityId': None,
    2019-01-26 01:04:01.432000 189dfc 'cognitoIdentityPoolId': None,
    2019-01-26 01:04:01.432000 189dfc 'sourceIp': '54.67.51.193',
    2019-01-26 01:04:01.432000 189dfc 'user': None,
    2019-01-26 01:04:01.432000 189dfc 'userAgent': 'HTTPie/0.9.8',
    2019-01-26 01:04:01.432000 189dfc 'userArn': None},
    2019-01-26 01:04:01.432000 189dfc 'path': '/api/text/test',
    2019-01-26 01:04:01.432000 189dfc 'protocol': 'HTTP/1.1',
    2019-01-26 01:04:01.432000 189dfc 'requestId': '447e02ca-2106-11e9-86ac-6596e4f7f276',
    2019-01-26 01:04:01.432000 189dfc 'requestTime': '26/Jan/2019:01:04:01 +0000',
    2019-01-26 01:04:01.432000 189dfc 'requestTimeEpoch': 1548464641414,
    2019-01-26 01:04:01.432000 189dfc 'resourceId': 'ezap0f',
    2019-01-26 01:04:01.433000 189dfc 'resourcePath': '/text/{key}',
    2019-01-26 01:04:01.449000 189dfc 'stage': 'api'},
    2019-01-26 01:04:01.449000 189dfc 'headers': {   'accept': '*/*',
    2019-01-26 01:04:01.449000 189dfc 'accept-encoding': 'gzip, deflate',
    2019-01-26 01:04:01.449000 189dfc 'cloudfront-forwarded-proto': 'https',
    2019-01-26 01:04:01.449000 189dfc 'cloudfront-is-desktop-viewer': 'true',
    2019-01-26 01:04:01.449000 189dfc 'cloudfront-is-mobile-viewer': 'false',
    2019-01-26 01:04:01.449000 189dfc 'cloudfront-is-smarttv-viewer': 'false',
    2019-01-26 01:04:01.449000 189dfc 'cloudfront-is-tablet-viewer': 'false',
    2019-01-26 01:04:01.449000 189dfc 'cloudfront-viewer-country': 'US',
    2019-01-26 01:04:01.449000 189dfc 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:04:01.449000 189dfc 'user-agent': 'HTTPie/0.9.8',
    2019-01-26 01:04:01.449000 189dfc 'via': '1.1 49c80a47c1441dd194a8337982f1cd7e.cloudfront.net '
    2019-01-26 01:04:01.449000 189dfc '(CloudFront)',
    2019-01-26 01:04:01.449000 189dfc 'x-amz-cf-id': 'THP5eRWQ4cEezLBbXU-2vT4VzPDF4-mCFcMy6JMGOQTUd367pcvL4w==',
    2019-01-26 01:04:01.449000 189dfc 'x-amzn-trace-id': 'Root=1-5c4bb201-b56313b28f6fdc1ce3892232',
    2019-01-26 01:04:01.449000 189dfc 'x-forwarded-for': '54.67.51.193, 54.239.134.14',
    2019-01-26 01:04:01.449000 189dfc 'x-forwarded-port': '443',
    2019-01-26 01:04:01.449000 189dfc 'x-forwarded-proto': 'https'},
    2019-01-26 01:04:01.450000 189dfc 'method': 'GET',
    2019-01-26 01:04:01.450000 189dfc 'query_params': None,
    2019-01-26 01:04:01.450000 189dfc 'stage_vars': None,
    2019-01-26 01:04:01.450000 189dfc 'uri_params': {'key': 'test'}}
    2019-01-26 01:04:01.450000 189dfc GET s3://mjbright-uploads/test
    2019-01-26 01:04:01.949000 189dfc END RequestId: 9788080c-6ed5-49bb-a096-0e869f307417
    2019-01-26 01:04:01.949000 189dfc REPORT RequestId: 9788080c-6ed5-49bb-a096-0e869f307417	Duration: 518.54 ms	Billed Duration: 600 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 01:04:02.435000 189dfc START RequestId: 56179a04-0ccc-4bc5-9ed2-988e4b03d897 Version: $LATEST
    2019-01-26 01:04:02.437000 189dfc s3json: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==', 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': '1ay49m', 'resourcePath': '/json/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAYGqtSK4Ff-A=', 'requestTime': '26/Jan/2019:01:04:02 +0000', 'path': '/api/json/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464642423, 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:02.437000 189dfc s3json: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==', 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': '1ay49m', 'resourcePath': '/json/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAYGqtSK4Ff-A=', 'requestTime': '26/Jan/2019:01:04:02 +0000', 'path': '/api/json/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464642423, 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:02.437000 189dfc s3json: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==', 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': '1ay49m', 'resourcePath': '/json/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAYGqtSK4Ff-A=', 'requestTime': '26/Jan/2019:01:04:02 +0000', 'path': '/api/json/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464642423, 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:02.437000 189dfc {   'context': {   'accountId': '568285458700',
    2019-01-26 01:04:02.437000 189dfc 'apiId': 'jlmq3ygdu1',
    2019-01-26 01:04:02.438000 189dfc 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:04:02.438000 189dfc 'domainPrefix': 'jlmq3ygdu1',
    2019-01-26 01:04:02.438000 189dfc 'extendedRequestId': 'UFjAYGqtSK4Ff-A=',
    2019-01-26 01:04:02.438000 189dfc 'httpMethod': 'GET',
    2019-01-26 01:04:02.438000 189dfc 'identity': {   'accessKey': None,
    2019-01-26 01:04:02.438000 189dfc 'accountId': None,
    2019-01-26 01:04:02.438000 189dfc 'caller': None,
    2019-01-26 01:04:02.438000 189dfc 'cognitoAuthenticationProvider': None,
    2019-01-26 01:04:02.438000 189dfc 'cognitoAuthenticationType': None,
    2019-01-26 01:04:02.438000 189dfc 'cognitoIdentityId': None,
    2019-01-26 01:04:02.438000 189dfc 'cognitoIdentityPoolId': None,
    2019-01-26 01:04:02.438000 189dfc 'sourceIp': '54.67.51.193',
    2019-01-26 01:04:02.449000 189dfc 'user': None,
    2019-01-26 01:04:02.449000 189dfc 'userAgent': 'HTTPie/0.9.8',
    2019-01-26 01:04:02.449000 189dfc 'userArn': None},
    2019-01-26 01:04:02.449000 189dfc 'path': '/api/json/test',
    2019-01-26 01:04:02.449000 189dfc 'protocol': 'HTTP/1.1',
    2019-01-26 01:04:02.449000 189dfc 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d',
    2019-01-26 01:04:02.449000 189dfc 'requestTime': '26/Jan/2019:01:04:02 +0000',
    2019-01-26 01:04:02.449000 189dfc 'requestTimeEpoch': 1548464642423,
    2019-01-26 01:04:02.449000 189dfc 'resourceId': '1ay49m',
    2019-01-26 01:04:02.449000 189dfc 'resourcePath': '/json/{key}',
    2019-01-26 01:04:02.449000 189dfc 'stage': 'api'},
    2019-01-26 01:04:02.449000 189dfc 'headers': {   'accept': '*/*',
    2019-01-26 01:04:02.449000 189dfc 'accept-encoding': 'gzip, deflate',
    2019-01-26 01:04:02.449000 189dfc 'cloudfront-forwarded-proto': 'https',
    2019-01-26 01:04:02.449000 189dfc 'cloudfront-is-desktop-viewer': 'true',
    2019-01-26 01:04:02.449000 189dfc 'cloudfront-is-mobile-viewer': 'false',
    2019-01-26 01:04:02.449000 189dfc 'cloudfront-is-smarttv-viewer': 'false',
    2019-01-26 01:04:02.449000 189dfc 'cloudfront-is-tablet-viewer': 'false',
    2019-01-26 01:04:02.449000 189dfc 'cloudfront-viewer-country': 'US',
    2019-01-26 01:04:02.449000 189dfc 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:04:02.449000 189dfc 'user-agent': 'HTTPie/0.9.8',
    2019-01-26 01:04:02.449000 189dfc 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net '
    2019-01-26 01:04:02.449000 189dfc '(CloudFront)',
    2019-01-26 01:04:02.449000 189dfc 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==',
    2019-01-26 01:04:02.449000 189dfc 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8',
    2019-01-26 01:04:02.449000 189dfc 'x-forwarded-for': '54.67.51.193, 54.239.134.14',
    2019-01-26 01:04:02.449000 189dfc 'x-forwarded-port': '443',
    2019-01-26 01:04:02.449000 189dfc 'x-forwarded-proto': 'https'},
    2019-01-26 01:04:02.449000 189dfc 'method': 'GET',
    2019-01-26 01:04:02.449000 189dfc 'query_params': None,
    2019-01-26 01:04:02.449000 189dfc 'stage_vars': None,
    2019-01-26 01:04:02.449000 189dfc 'uri_params': {'key': 'test'}}
    2019-01-26 01:04:02.449000 189dfc GET s3://mjbright-uploads/test
    2019-01-26 01:04:02.528000 189dfc s3 - ERROR - Internal Error for <function s3json at 0x7f3be49ebd90>
    2019-01-26 01:04:02.528000 189dfc Traceback (most recent call last):
    2019-01-26 01:04:02.528000 189dfc File "/var/task/chalice/app.py", line 731, in _get_view_function_response
    2019-01-26 01:04:02.528000 189dfc response = view_function(**function_args)
    2019-01-26 01:04:02.528000 189dfc File "/var/task/app.py", line 59, in s3json
    2019-01-26 01:04:02.528000 189dfc return json.loads(response['Body'].read())
    2019-01-26 01:04:02.528000 189dfc File "/var/lang/lib/python3.6/json/__init__.py", line 354, in loads
    2019-01-26 01:04:02.528000 189dfc return _default_decoder.decode(s)
    2019-01-26 01:04:02.528000 189dfc File "/var/lang/lib/python3.6/json/decoder.py", line 339, in decode
    2019-01-26 01:04:02.528000 189dfc obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    2019-01-26 01:04:02.528000 189dfc File "/var/lang/lib/python3.6/json/decoder.py", line 355, in raw_decode
    2019-01-26 01:04:02.528000 189dfc obj, end = self.scan_once(s, idx)
    2019-01-26 01:04:02.528000 189dfc json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
    2019-01-26 01:04:02.528000 189dfc END RequestId: 56179a04-0ccc-4bc5-9ed2-988e4b03d897
    2019-01-26 01:04:02.528000 189dfc REPORT RequestId: 56179a04-0ccc-4bc5-9ed2-988e4b03d897	Duration: 92.26 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 37 MB
    2019-01-26 01:05:14.426000 189dfc START RequestId: 13c4f37c-e11a-40d2-8f43-ef6fc1aec0e7 Version: $LATEST
    2019-01-26 01:05:14.429000 189dfc s3text: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': 'application/json, */*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'content-type': 'application/json', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'rV0fGUZdmJugOKPdZXy5IDemCwyrR8sp0M59XLnWZDnl2iUQGggeTg==', 'x-amzn-trace-id': 'Root=1-5c4bb24a-c4346c80ef290c006c5cab40', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'PUT', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'PUT', 'extendedRequestId': 'UFjLoHZfyK4FlIg=', 'requestTime': '26/Jan/2019:01:05:14 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464714410, 'requestId': '700050be-2106-11e9-9afc-0db0ce26a5a3', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:05:14.429000 189dfc s3text: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': 'application/json, */*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'content-type': 'application/json', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'rV0fGUZdmJugOKPdZXy5IDemCwyrR8sp0M59XLnWZDnl2iUQGggeTg==', 'x-amzn-trace-id': 'Root=1-5c4bb24a-c4346c80ef290c006c5cab40', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'PUT', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'PUT', 'extendedRequestId': 'UFjLoHZfyK4FlIg=', 'requestTime': '26/Jan/2019:01:05:14 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464714410, 'requestId': '700050be-2106-11e9-9afc-0db0ce26a5a3', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:05:14.449000 189dfc {   'context': {   'accountId': '568285458700',
    2019-01-26 01:05:14.449000 189dfc 'apiId': 'jlmq3ygdu1',
    2019-01-26 01:05:14.449000 189dfc 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:05:14.449000 189dfc 'domainPrefix': 'jlmq3ygdu1',
    2019-01-26 01:05:14.469000 189dfc 'extendedRequestId': 'UFjLoHZfyK4FlIg=',
    2019-01-26 01:05:14.469000 189dfc 'httpMethod': 'PUT',
    2019-01-26 01:05:14.469000 189dfc 'identity': {   'accessKey': None,
    2019-01-26 01:05:14.469000 189dfc 'accountId': None,
    2019-01-26 01:05:14.469000 189dfc 'caller': None,
    2019-01-26 01:05:14.469000 189dfc 'cognitoAuthenticationProvider': None,
    2019-01-26 01:05:14.469000 189dfc 'cognitoAuthenticationType': None,
    2019-01-26 01:05:14.469000 189dfc 'cognitoIdentityId': None,
    2019-01-26 01:05:14.469000 189dfc 'cognitoIdentityPoolId': None,
    2019-01-26 01:05:14.469000 189dfc 'sourceIp': '54.67.51.193',
    2019-01-26 01:05:14.469000 189dfc 'user': None,
    2019-01-26 01:05:14.469000 189dfc 'userAgent': 'HTTPie/0.9.8',
    2019-01-26 01:05:14.469000 189dfc 'userArn': None},
    2019-01-26 01:05:14.469000 189dfc 'path': '/api/text/test',
    2019-01-26 01:05:14.469000 189dfc 'protocol': 'HTTP/1.1',
    2019-01-26 01:05:14.469000 189dfc 'requestId': '700050be-2106-11e9-9afc-0db0ce26a5a3',
    2019-01-26 01:05:14.469000 189dfc 'requestTime': '26/Jan/2019:01:05:14 +0000',
    2019-01-26 01:05:14.469000 189dfc 'requestTimeEpoch': 1548464714410,
    2019-01-26 01:05:14.469000 189dfc 'resourceId': 'ezap0f',
    2019-01-26 01:05:14.469000 189dfc 'resourcePath': '/text/{key}',
    2019-01-26 01:05:14.469000 189dfc 'stage': 'api'},
    2019-01-26 01:05:14.469000 189dfc 'headers': {   'accept': 'application/json, */*',
    2019-01-26 01:05:14.469000 189dfc 'accept-encoding': 'gzip, deflate',
    2019-01-26 01:05:14.469000 189dfc 'cloudfront-forwarded-proto': 'https',
    2019-01-26 01:05:14.469000 189dfc 'cloudfront-is-desktop-viewer': 'true',
    2019-01-26 01:05:14.469000 189dfc 'cloudfront-is-mobile-viewer': 'false',
    2019-01-26 01:05:14.469000 189dfc 'cloudfront-is-smarttv-viewer': 'false',
    2019-01-26 01:05:14.469000 189dfc 'cloudfront-is-tablet-viewer': 'false',
    2019-01-26 01:05:14.469000 189dfc 'cloudfront-viewer-country': 'US',
    2019-01-26 01:05:14.469000 189dfc 'content-type': 'application/json',
    2019-01-26 01:05:14.469000 189dfc 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com',
    2019-01-26 01:05:14.469000 189dfc 'user-agent': 'HTTPie/0.9.8',
    2019-01-26 01:05:14.469000 189dfc 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net '
    2019-01-26 01:05:14.469000 189dfc '(CloudFront)',
    2019-01-26 01:05:14.469000 189dfc 'x-amz-cf-id': 'rV0fGUZdmJugOKPdZXy5IDemCwyrR8sp0M59XLnWZDnl2iUQGggeTg==',
    2019-01-26 01:05:14.469000 189dfc 'x-amzn-trace-id': 'Root=1-5c4bb24a-c4346c80ef290c006c5cab40',
    2019-01-26 01:05:14.469000 189dfc 'x-forwarded-for': '54.67.51.193, 54.239.134.7',
    2019-01-26 01:05:14.469000 189dfc 'x-forwarded-port': '443',
    2019-01-26 01:05:14.469000 189dfc 'x-forwarded-proto': 'https'},
    2019-01-26 01:05:14.469000 189dfc 'method': 'PUT',
    2019-01-26 01:05:14.469000 189dfc 'query_params': None,
    2019-01-26 01:05:14.469000 189dfc 'stage_vars': None,
    2019-01-26 01:05:14.469000 189dfc 'uri_params': {'key': 'test'}}
    2019-01-26 01:05:14.469000 189dfc END RequestId: 13c4f37c-e11a-40d2-8f43-ef6fc1aec0e7
    2019-01-26 01:05:14.469000 189dfc REPORT RequestId: 13c4f37c-e11a-40d2-8f43-ef6fc1aec0e7	Duration: 21.55 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 38 MB
    2019-01-26 02:51:35.820000 7fe24c START RequestId: f1eb20f2-c827-4dcd-9f3d-290bb7dc10c1 Version: $LATEST
    2019-01-26 02:51:35.821000 7fe24c END RequestId: f1eb20f2-c827-4dcd-9f3d-290bb7dc10c1
    2019-01-26 02:51:35.821000 7fe24c REPORT RequestId: f1eb20f2-c827-4dcd-9f3d-290bb7dc10c1	Duration: 0.87 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 02:51:54.024000 7fe24c START RequestId: 9145667d-ff2c-479d-9f72-4f7aca71bc71 Version: $LATEST
    2019-01-26 02:51:54.029000 7fe24c END RequestId: 9145667d-ff2c-479d-9f72-4f7aca71bc71
    2019-01-26 02:51:54.029000 7fe24c REPORT RequestId: 9145667d-ff2c-479d-9f72-4f7aca71bc71	Duration: 0.66 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 02:52:51.462000 ebd3d5 START RequestId: 7b854487-4b45-4d39-b519-8b2d7e7a1250 Version: $LATEST
    2019-01-26 02:52:51.463000 ebd3d5 Looks like we got a request!
    2019-01-26 02:52:51.464000 ebd3d5 END RequestId: 7b854487-4b45-4d39-b519-8b2d7e7a1250
    2019-01-26 02:52:51.464000 ebd3d5 REPORT RequestId: 7b854487-4b45-4d39-b519-8b2d7e7a1250	Duration: 0.97 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 03:19:12.067000 8ee5f3 START RequestId: a28f561c-b402-4662-bc81-5b6ea57a5b6a Version: $LATEST
    2019-01-26 03:19:12.067000 8ee5f3 END RequestId: a28f561c-b402-4662-bc81-5b6ea57a5b6a
    2019-01-26 03:19:12.067000 8ee5f3 REPORT RequestId: a28f561c-b402-4662-bc81-5b6ea57a5b6a	Duration: 10.26 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 03:20:40.747000 cec580 START RequestId: c0b0a7d3-5ab8-4a1d-ac63-fda3968dd02f Version: $LATEST
    2019-01-26 03:20:40.767000 cec580 END RequestId: c0b0a7d3-5ab8-4a1d-ac63-fda3968dd02f
    2019-01-26 03:20:40.767000 cec580 REPORT RequestId: c0b0a7d3-5ab8-4a1d-ac63-fda3968dd02f	Duration: 6.38 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 03:20:40.767000 cec580 Looks like we got a request!
    2019-01-26 03:29:56.227000 a7bf47 START RequestId: 565cbab2-9861-4d07-abba-4aca6daa275a Version: $LATEST
    2019-01-26 03:29:56.227000 a7bf47 END RequestId: 565cbab2-9861-4d07-abba-4aca6daa275a
    2019-01-26 03:29:56.227000 a7bf47 REPORT RequestId: 565cbab2-9861-4d07-abba-4aca6daa275a	Duration: 13.88 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB
    2019-01-26 03:30:43.347000 78416b START RequestId: f6a2ed3b-e5bd-48b4-ac44-ad416e388556 Version: $LATEST
    2019-01-26 03:30:43.347000 78416b Looks like we got a request!
    2019-01-26 03:30:43.347000 78416b END RequestId: f6a2ed3b-e5bd-48b4-ac44-ad416e388556
    2019-01-26 03:30:43.348000 78416b REPORT RequestId: f6a2ed3b-e5bd-48b4-ac44-ad416e388556	Duration: 10.22 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 24 MB


## Cleanup: deleting the function deployment

We can cleanup by deleting the function which we deployed


```bash
#aws lambda delete-function --function-name chalice-app-dev
#aws lambda list-functions
```

# Function capabilities

Let's now investigate how we can treat different routes, requests, responses with Chalice.

## Returning custom headers, status_code
Until now we returned directly a *json* structure but we can control the type of response we return e.g. text/plain instead of json, or other headers.  It is also possible to set an error status code.

In the below example we
- return a 200 OK status_code
- return a plaintext 'hello world!' body, whilst setting content-type to 'text/plain' in the headers
- we also add a custom 'X-Debug' header


```bash
cd ~/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda

cd chalice-app
pwd
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/chalice-app



```bash
cat > app.py << EOF
from chalice import Chalice, Response

app = Chalice(app_name='chalice-app')


@app.route('/')
def index():

    custom_headers = {
        'Content-Type': 'text/plain',
        'X-Debug': 'some debug information'
    }

    return Response(body='hello world!',
                  status_code=200,
                  headers=custom_headers)
EOF
```


```bash
http 127.0.0.1:8000
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m12[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/plain[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:38:50 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    [36mX-Debug[39;49;00m: [33msome debug information[39;49;00m
    
    hello world!
    


## Implementing a REST API

We can also use the decorators to specify parametrized url patterns to specify parameters to a request, and also specify GET, PUT, POST, DELETE requests allowing to implement a REST API.

In the below example we add new routes:
- GET /hello/{name} allowing to greet a specified named person
- POST /users       allowing to create a user (*)

**Note**: this is only notional creation of a user as we have no persistence across function calls.  We would need to add some persistent backend storage for that.


```bash
cat > app.py <<EOF
from chalice import Chalice

app = Chalice(app_name='helloworld')

@app.route('/')
def index():
    return {'hello': 'world'}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
@app.route('/hello/{name}')
def hello_name(name):
   # '/hello/james' -> {"hello": "james"}
   return {'hello': name}

@app.route('/users', methods=['POST'])
def create_user():
    # This is the JSON body the user sent in their POST request.
    user_as_json = app.current_request.json_body
    # We'll echo the json body back to the user in a 'user' key.
    return {'user': user_as_json}

EOF
```

We can make a **GET** request to **/hello/bob** to make a greeting to 'bob':


```bash
http :8000/hello/bob
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m15[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:03 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"hello"[39;49;00m: [33m"bob"[39;49;00m
    }
    


We can make a **POST** request to /users to create a new user - this function returns a json definition of this user although that definition is not persisted by the function itself.


```bash
echo '"testuser"' | http POST :8000/users
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m19[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:08 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"user"[39;49;00m: [33m"testuser"[39;49;00m
    }
    



```bash
echo '["testuser", {"fullname": "My full name"}]' | http POST :8000/users
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m49[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:09 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"user"[39;49;00m: [
            [33m"testuser"[39;49;00m,
            {
                [34;01m"fullname"[39;49;00m: [33m"My full name"[39;49;00m
            }
        ]
    }
    


## Accessing a datastore

For the moment we have no persistent datastore, for the moment we use a poor man's datastore, a hardcoded dictionary in our code !!

**Note**: This is not so ridiculous.  We could imagine some scenarii where the Serverless function is used with an immutable database, maybe even deployed as a Unikernel.  It could be an infrequently modified store such as a DNS database where a new appliction is created when DNS changes are to be made.

Let's implement something vaguely DNS-like ...


```bash
cat > app.py <<EOF
from chalice import Chalice

app = Chalice(app_name='bindservice')

'''
Note: Enabling app.debug gives much better error message for missing key than:
    { "Code": "ChaliceViewError",
      "Message": "ChaliceViewError: An internal server error occurred."
    }
'''
app.debug = True

HOST_IPv4_MAPPING = {
    'localhost': '127.0.0.1',
    'google.com': ['172.217.5.110', '216.58.195.68'],
}

# Yes this could be calcuated from HOST_IPv4_MAPPING but better to have an immutable static copy created when the applicaton is created.
IPv4_HOST_MAPPING = {
    '127.0.0.1': 'localhost',
    '216.58.195.68': 'google.com',
    '172.217.5.110': 'google.com',
}


'''
* Query database for the host with specified IPv4 address
'''
@app.route('/host/{ip}')
def get_host(ip):
    return {'host': IPv4_HOST_MAPPING[ip]}

'''
* Query database for the  IPv4 addresses for the specified host
'''
@app.route('/ips/{host}')
def get_host(host):
    return {'ips': HOST_IPv4_MAPPING[host]}

EOF
```

### Querying on IPv4 address


```bash
http 127.0.0.1:8000/host/127.0.0.1
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m20[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:27 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"host"[39;49;00m: [33m"localhost"[39;49;00m
    }
    



```bash
http 127.0.0.1:8000/host/172.217.5.110
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m21[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:29 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"host"[39;49;00m: [33m"google.com"[39;49;00m
    }
    


### Querying on hostname


```bash
http 127.0.0.1:8000/ips/google.com
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m41[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:32 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"ips"[39;49;00m: [
            [33m"172.217.5.110"[39;49;00m,
            [33m"216.58.195.68"[39;49;00m
        ]
    }
    


### But we need error handling

But our current implementation doesn't look very smart if we look up an unknown item


```bash
http 127.0.0.1:8000/ips/UNKNOWN.com
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m500[39;49;00m [36mInternal Server Error[39;49;00m
    [36mContent-Length[39;49;00m: [33m372[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/plain[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:39:36 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    Traceback (most recent call last):
      File "/usr/local/lib/python3.6/dist-packages/chalice/app.py", line 731, in _get_view_function_response
        response = view_function(**function_args)
      File "/home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/chalice-app/app.py", line 38, in get_host
        return {'ips': HOST_IPv4_MAPPING[host]}
    KeyError: 'UNKNOWN.com'
    


### Error handling

We can handle error cases such as catching an unknown ip address or hostname


```bash
cat > app.py <<EOF
from chalice import Chalice
from chalice import NotFoundError

app = Chalice(app_name='bindservice')

'''
  NOTE: Can use different error codes:
    * BadRequestError   - return a status code of 400
    * UnauthorizedError - return a status code of 401
    * ForbiddenError    - return a status code of 403
    * NotFoundError     - return a status code of 404
    * ConflictError     - return a status code of 409
    * UnprocessableEntityError - return a status code of 422
    * TooManyRequestsError - return a status code of 429
    * ChaliceViewError  - return a status code of 500
'''

app.debug = True

HOST_IPv4_MAPPING = {
    'localhost': '127.0.0.1',
    'google.com': ['172.217.5.110', '216.58.195.68']
}

# Yes this could be calcuated from HOST_IPv4_MAPPING but better to have an immutable static copy created when the applicaton is created.
IPv4_HOST_MAPPING = {
    '127.0.0.1': 'localhost',
    '216.58.195.68': 'google.com',
    '172.217.5.110': 'google.com'
}


'''
* Query database for the host with specified IPv4 address
'''
@app.route('/host/{ip}')
def get_host(ip):
    try:
        host = {'host':  IPv4_HOST_MAPPING[ip]} 
    except KeyError:
        raise NotFoundError("Unknown ip '%s'" % ( ip ))
        
    return host

'''
* Query database for the  IPv4 addresses for the specified host
'''
@app.route('/ips/{host}')
def get_host(host):
    try:
        ips = {'ips': HOST_IPv4_MAPPING[host]}
    except KeyError:
        raise NotFoundError("Unknown host '%s'" % ( host ))
        
    return ips

EOF
```

Now when we rerun some error cases we get a cleaner response:


```bash
#http 127.0.0.1:8000/host/127.0.0.1
#http 127.0.0.1:8000/host/172.217.5.110
http 127.0.0.1:8000/host/172.217.5.255 # UNKNOWN
#http 127.0.0.1:8000/ips/google.com
http 127.0.0.1:8000/ips/UNKNOWN.com  # UNKNOWN
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m404[39;49;00m [36mNot Found[39;49;00m
    [36mContent-Length[39;49;00m: [33m78[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:43:31 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"NotFoundError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"NotFoundError: Unknown ip '172.217.5.255'"[39;49;00m
    }
    
    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m404[39;49;00m [36mNot Found[39;49;00m
    [36mContent-Length[39;49;00m: [33m78[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 03:43:31 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"NotFoundError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"NotFoundError: Unknown host 'UNKNOWN.com'"[39;49;00m
    }
    


## Think of some scenarii

### Think about some use cases for this functionality.

### Is it clear why it is interesting to do this as a serverless function?

Remember that in this example we are not configuring a server to host our database and so we are very light on resource usage and we pay only for what we use.

If we use a persistent backing store, S3 file storage or a database, then we wil pay for that usage but likely we will be sharing an existing file storage or database server and so we stil have a low cost solution where our front end application doesn't require a server to itself.

We also get automatic scaling of our function if there is a lot of traffic from the network

### Think of some scenario where we use all http/REST methods GET, PUT, POST, DELETE

### So far we've used an embedded immutable database - what could we do with a persistent storage backend ?


# More Reading



# Cleanup




```bash
cleanup_functions
```


```bash
aws s3 rm s3://mjbright-static-site --recursive
aws s3 rb s3://mjbright-static-site
```

It's also possible to remoce the bucket directly using the ```--force``` option:
    ```aws s3 rb --force s3://mjbright-static-site```
