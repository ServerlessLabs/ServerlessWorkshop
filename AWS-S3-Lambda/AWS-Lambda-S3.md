
# AWS Lambda - S3


## Setup



If you have chosen to use an rc file, source it as ```source <your-aws-credentials-rc-file>```, e.g.


```bash
. ~/.aws/credentials.rc
```


```bash
cleanup_functions() {
    echo "-- Functions before:"
    aws lambda list-functions | grep FunctionName

    FNS=$(aws lambda list-functions | grep FunctionName |sed -e 's/.*: //'  -e 's/"//g' -e 's/,//')
    for FN in $FNS; do aws lambda delete-function --function-name $FN; done
    echo "-- Functions after cleanup:"
    aws lambda list-functions | grep FunctionName
}
```


```bash
cd ~/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda
```


```bash

```


```bash
cleanup_functions
```

    -- Functions before:
                "[01;31m[KFunctionName[m[K": "chalice-app-dev",
                "[01;31m[KFunctionName[m[K": "scheduled-app-dev-periodic_task",
                "[01;31m[KFunctionName[m[K": "s3-app-dev-handler",
    -- Functions after cleanup:





```bash
chalice new-project s3-app
cd s3-app
```


```bash
aws lambda list-functions
```

    {
        "Functions": []
    }


# From Lambda

Remove old bucket if present to avoid possible event configuration conflict


```bash
aws s3 rb --force s3://mjbright-uploads
```

    delete: s3://mjbright-uploads/testfile
    remove_bucket: mjbright-uploads



```bash
aws s3 mb s3://mjbright-uploads
aws s3 ls
```

    make_bucket: mjbright-uploads
    2019-01-25 21:41:22 mjbright-static-site
    2019-01-26 07:00:20 mjbright-uploads





```bash
BUCKET_NAME='mjbright-uploads'

cat > app.py <<EOF
from chalice import Chalice
#import sys

app = Chalice(app_name="s3-uploads")

# Whenever an object is uploaded to 'mybucket'
# this lambda function will be invoked.

@app.on_s3_event(bucket='$BUCKET_NAME')
def handler(event):
    # Output goes to CloudWatch logs - viewable via 'chalice logs'
    print("Object uploaded for bucket: %s, key: %s"
          % (event.bucket, event.key))
    #sys.exit(0)
EOF
```




```bash
pwd; cat app.py
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/s3-app
    from chalice import Chalice
    #import sys
    
    app = Chalice(app_name="s3-uploads")
    
    # Whenever an object is uploaded to 'mybucket'
    # this lambda function will be invoked.
    
    @app.on_s3_event(bucket='mjbright-uploads')
    def handler(event):
        # Output goes to CloudWatch logs - viewable via 'chalice logs'
        print("Object uploaded for bucket: %s, key: %s"
              % (event.bucket, event.key))
        #sys.exit(0)


Deploy a local chalice server in another window using ```chalice local```, then upload a file to our bucket


```bash
cat > requirements.txt <<EOF
boto3==1.3.1
EOF
```




```bash
# Only works when deployed - local server has no S3 access
chalice deploy
```

    /usr/share/python-wheels/requests-2.18.4-py2.py3-none-any.whl/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
    Creating deployment package.
    Updating policy for IAM role: s3-app-dev
    Updating lambda function: s3-app-dev-handler
    Configuring S3 events in bucket mjbright-uploads to function s3-app-dev-handler
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-1:568285458700:function:s3-app-dev-handler



```bash

```


```bash
aws s3 ls s3://mjbright-uploads
```


```bash
aws s3 cp app.py s3://mjbright-uploads/testfile
```

    upload: ./app.py to s3://mjbright-uploads/testfile                



```bash
aws s3 ls s3://mjbright-uploads
```

    2019-01-26 07:02:59        406 testfile



```bash
chalice logs --help
```

    Usage: chalice logs [OPTIONS]
    
    Options:
      --num-entries INTEGER           Max number of log entries to show.
      --include-lambda-messages / --no-include-lambda-messages
                                      Controls whether or not lambda log messages
                                      are included.
      --stage TEXT
      -n, --name TEXT                 The name of the lambda function to retrieve
                                      logs from.
      --profile TEXT                  The profile to use for fetching logs.
      --help                          Show this message and exit.



```bash
chalice logs --include-lambda-messages
```


```bash

```


```bash
pwd
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/s3-app



```bash
cat > app.py <<EOF

from chalice import Chalice
from chalice import NotFoundError
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

app = Chalice(app_name='s3')

import json
import boto3
from botocore.exceptions import ClientError

S3 = boto3.client('s3', region_name='us-west-1')
BUCKET = 'mjbright-uploads'

@app.route('/text/{key}', methods=['GET', 'PUT'])
def s3text(key):
    request = app.current_request
    
    # Log request information to CloudWatch
    print("s3text: -----------------------------------------------------------------"); pp.pprint(request.to_dict())
    
    # PUT a new S3 object:
    if request.method == 'PUT':
        print("s3text: PUT s3://{}/{}".format(BUCKET,key))
        #S3.put_object(Bucket=BUCKET, Key=key, Body=str(request.json_body))
        jb = request.json_body
        if jb == null:
            print("jb == null")
        else:
            print( str(jb))
        S3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(request.json_body))

    # GET an existing S3 object, if it exists:
    elif request.method == 'GET':
        try:
            print("s3text: GET s3://{}/{}".format(BUCKET,key))
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return str(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)

@app.route('/json/{key}', methods=['GET', 'PUT'])
def s3json(key):
    request = app.current_request
    
    # Log request information to CloudWatch
    print("s3json: -----------------------------------------------------------------"); pp.pprint(request.to_dict())
    print("json_body: -----------------------------------------------------------------"); pp.pprint(request.json_body)
    print("json_body: -----------------------------------------------------------------"); print(request.json_body)
    print("len(json_body): ", len(request.json_body))
    
    # PUT a new S3 object:
    if request.method == 'PUT':
        print("s3json: PUT s3://{}/{}".format(BUCKET,key))
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))

    # GET an existing S3 object, if it exists:
    elif request.method == 'GET':
        try:
            print("s3json: GET s3://{}/{}".format(BUCKET,key))
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)

EOF
```

## NOTE: local test

This will not work because local server hasn't S3 credentials, but at least we might learn something from error messages


```bash
#echo "{ 'hello': 'world'; }" | http PUT :8000/json/test
echo "{ 'a': 'b'; };" > test
echo "{ 'a': 'b' }" > test
cat test

#cat test | http PUT :8000/json/test
cat test | http PUT :8000/text/test
```

    { 'a': 'b' }
    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m400[39;49;00m [36mBad Request[39;49;00m
    [36mContent-Length[39;49;00m: [33m74[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:51:01 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"BadRequestError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"BadRequestError: Error Parsing JSON"[39;49;00m
    }
    



```bash
echo hello world | http PUT :8000/text/test
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m500[39;49;00m [36mInternal Server Error[39;49;00m
    [36mContent-Length[39;49;00m: [33m77[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:10:37 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"InternalServerError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"An internal server error occurred."[39;49;00m
    }
    



```bash
http :8000/json/test; http :8000/text/test;
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m500[39;49;00m [36mInternal Server Error[39;49;00m
    [36mContent-Length[39;49;00m: [33m77[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:03:06 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"InternalServerError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"An internal server error occurred."[39;49;00m
    }
    
    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m500[39;49;00m [36mInternal Server Error[39;49;00m
    [36mContent-Length[39;49;00m: [33m77[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:03:06 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"InternalServerError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"An internal server error occurred."[39;49;00m
    }
    



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
      - Rest API URL: https://jlmq3ygdu1.execute-api.us-west-1.amazonaws.com/api/



```bash
echo "{ 'a': 'b' }" > test
aws s3 cp test s3://mjbright-uploads/test
```

    upload: ./test to s3://mjbright-uploads/test                      



```bash
aws s3 ls s3://mjbright-uploads/
```

                               PRE objects/
    2019-01-26 00:19:14        900 app.py
    2019-01-26 00:18:18        221 hosts
    2019-01-26 01:03:32         13 test



```bash
cat test
```

    { 'a': 'b' }



```bash
http https://jlmq3ygdu1.execute-api.us-west-1.amazonaws.com/api/text/test
http https://jlmq3ygdu1.execute-api.us-west-1.amazonaws.com/api/json/test
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mConnection[39;49;00m: [33mkeep-alive[39;49;00m
    [36mContent-Length[39;49;00m: [33m17[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:04:01 GMT[39;49;00m
    [36mVia[39;49;00m: [33m1.1 49c80a47c1441dd194a8337982f1cd7e.cloudfront.net (CloudFront)[39;49;00m
    [36mX-Amz-Cf-Id[39;49;00m: [33mx5l6UO5ZAWQVuG_3tPQWMiZHcMuAD2DrC2PGoGYLvUlkS2Y6zaXXBg==[39;49;00m
    [36mX-Amzn-Trace-Id[39;49;00m: [33mRoot=1-5c4bb201-b56313b28f6fdc1ce3892232;Sampled=0[39;49;00m
    [36mX-Cache[39;49;00m: [33mMiss from cloudfront[39;49;00m
    [36mx-amz-apigw-id[39;49;00m: [33mUFjAOGudyK4FSUw=[39;49;00m
    [36mx-amzn-RequestId[39;49;00m: [33m447e02ca-2106-11e9-86ac-6596e4f7f276[39;49;00m
    
    [04m[31;01mb[39;49;00m[33m"{ 'a': 'b' }\n"[39;49;00m
    
    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m500[39;49;00m [36mInternal Server Error[39;49;00m
    [36mConnection[39;49;00m: [33mkeep-alive[39;49;00m
    [36mContent-Length[39;49;00m: [33m77[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:04:02 GMT[39;49;00m
    [36mVia[39;49;00m: [33m1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)[39;49;00m
    [36mX-Amz-Cf-Id[39;49;00m: [33mLzSezq7jYA317ADwo32HIrrvZ9KO-M31qe5370IYqdT6Q0ODUdq1LQ==[39;49;00m
    [36mX-Amzn-Trace-Id[39;49;00m: [33mRoot=1-5c4bb202-550f0d68a4b72c38b4559ae8;Sampled=0[39;49;00m
    [36mX-Cache[39;49;00m: [33mError from cloudfront[39;49;00m
    [36mx-amz-apigw-id[39;49;00m: [33mUFjAYGqtSK4Ff-A=[39;49;00m
    [36mx-amzn-RequestId[39;49;00m: [33m4517f8df-2106-11e9-813f-4b680ee1356d[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"InternalServerError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"An internal server error occurred."[39;49;00m
    }
    



```bash
chalice logs --include-lambda-messages | grep s3
```

    2019-01-26 00:22:26.050000 c313db [01;31m[Ks3[m[Kobjects: <<chalice.app.Request object at 0x7ffa1f2c6940>>
    2019-01-26 00:24:34.082000 a295f6 [01;31m[Ks3[m[Kobjects: <<chalice.app.Request object at 0x7fa8a7cd6940>>
    2019-01-26 00:27:26.818000 c569b0 [01;31m[Ks3[m[K - ERROR - Internal Error for <function [01;31m[Ks3[m[Kobjects at 0x7f22ac1fc730>
    2019-01-26 00:27:26.818000 c569b0 File "/var/task/app.py", line 20, in [01;31m[Ks3[m[Kobjects
    2019-01-26 00:32:18.695000 b6528d [01;31m[Ks3[m[Kobjects: <{"query_params": null, "headers": {"accept": "*/*", "accept-encoding": "gzip, deflate", "cloudfront-forwarded-proto": "https", "cloudfront-is-desktop-viewer": "true", "cloudfront-is-mobile-viewer": "false", "cloudfront-is-smarttv-viewer": "false", "cloudfront-is-tablet-viewer": "false", "cloudfront-viewer-country": "US", "host": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "user-agent": "HTTPie/0.9.8", "via": "1.1 f1a40337a32137e1c23ceffead6a50d5.cloudfront.net (CloudFront)", "x-amz-cf-id": "Bt_hdRpgoK_u8oGdWSuYLo42AEdGxKYmJEnJjOeLbZ7og4P1kyMFZw==", "x-amzn-trace-id": "Root=1-5c4baa92-b9b2765f8181eff9ffbc7e42", "x-forwarded-for": "54.67.51.193, 54.239.134.7", "x-forwarded-port": "443", "x-forwarded-proto": "https"}, "uri_params": {"key": "test"}, "method": "GET", "context": {"resourceId": "wvdbuo", "resourcePath": "/objects/{key}", "httpMethod": "GET", "extendedRequestId": "UFeW0GbkyK4Fitg=", "requestTime": "26/Jan/2019:00:32:18 +0000", "path": "/api/objects/test", "accountId": "568285458700", "protocol": "HTTP/1.1", "stage": "api", "domainPrefix": "jlmq3ygdu1", "requestTimeEpoch": 1548462738044, "requestId": "d5feccae-2101-11e9-900f-d5ae7e711214", "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "sourceIp": "54.67.51.193", "accessKey": null, "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "HTTPie/0.9.8", "user": null}, "domainName": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "apiId": "jlmq3ygdu1"}, "stage_vars": null}>
    2019-01-26 00:34:33.415000 a8ddcb [01;31m[Ks3[m[Kobjects: SO FAR SO GOOD
    2019-01-26 00:34:33.415000 a8ddcb [01;31m[Ks3[m[Kobjects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 5c2ff4ca1e447265402af29264e83497.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'mQCX2b5PHSGu4WVl-i1aUxzXHg9DnMHq5hUiAspg9Cqv_DL8c9Lw_w==', 'x-amzn-trace-id': 'Root=1-5c4bab18-5c7d601bd991bc898c6db78f', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFer3HhUSK4FghQ=', 'requestTime': '26/Jan/2019:00:34:32 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548462872776, 'requestId': '264d4499-2102-11e9-9ca2-032065ee22a7', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:34:33.415000 a8ddcb [01;31m[Ks3[m[Kobjects: <{"query_params": null, "headers": {"accept": "*/*", "accept-encoding": "gzip, deflate", "cloudfront-forwarded-proto": "https", "cloudfront-is-desktop-viewer": "true", "cloudfront-is-mobile-viewer": "false", "cloudfront-is-smarttv-viewer": "false", "cloudfront-is-tablet-viewer": "false", "cloudfront-viewer-country": "US", "host": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "user-agent": "HTTPie/0.9.8", "via": "1.1 5c2ff4ca1e447265402af29264e83497.cloudfront.net (CloudFront)", "x-amz-cf-id": "mQCX2b5PHSGu4WVl-i1aUxzXHg9DnMHq5hUiAspg9Cqv_DL8c9Lw_w==", "x-amzn-trace-id": "Root=1-5c4bab18-5c7d601bd991bc898c6db78f", "x-forwarded-for": "54.67.51.193, 54.239.134.7", "x-forwarded-port": "443", "x-forwarded-proto": "https"}, "uri_params": {"key": "test"}, "method": "GET", "context": {"resourceId": "wvdbuo", "resourcePath": "/objects/{key}", "httpMethod": "GET", "extendedRequestId": "UFer3HhUSK4FghQ=", "requestTime": "26/Jan/2019:00:34:32 +0000", "path": "/api/objects/test", "accountId": "568285458700", "protocol": "HTTP/1.1", "stage": "api", "domainPrefix": "jlmq3ygdu1", "requestTimeEpoch": 1548462872776, "requestId": "264d4499-2102-11e9-9ca2-032065ee22a7", "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "sourceIp": "54.67.51.193", "accessKey": null, "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "HTTPie/0.9.8", "user": null}, "domainName": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "apiId": "jlmq3ygdu1"}, "stage_vars": null}>
    2019-01-26 00:37:55.489000 a8ddcb [01;31m[Ks3[m[Kobjects: SO FAR SO GOOD
    2019-01-26 00:37:55.489000 a8ddcb [01;31m[Ks3[m[Kobjects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 20f1c35f343f4b271ae8dcacfd7ea0e9.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'ruqvfTXReomBotCmWepayfZnZVp5Nln6TThdjKf8xT1oPKVTAxJUbg==', 'x-amzn-trace-id': 'Root=1-5c4babe3-d12496852222efb0d911dfa2', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFfLiFlNSK4Fmrw=', 'requestTime': '26/Jan/2019:00:37:55 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463075419, 'requestId': '9f1622b9-2102-11e9-b14b-5551fb47ff1c', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:37:55.489000 a8ddcb [01;31m[Ks3[m[Kobjects: <{"query_params": null, "headers": {"accept": "*/*", "accept-encoding": "gzip, deflate", "cloudfront-forwarded-proto": "https", "cloudfront-is-desktop-viewer": "true", "cloudfront-is-mobile-viewer": "false", "cloudfront-is-smarttv-viewer": "false", "cloudfront-is-tablet-viewer": "false", "cloudfront-viewer-country": "US", "host": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "user-agent": "HTTPie/0.9.8", "via": "1.1 20f1c35f343f4b271ae8dcacfd7ea0e9.cloudfront.net (CloudFront)", "x-amz-cf-id": "ruqvfTXReomBotCmWepayfZnZVp5Nln6TThdjKf8xT1oPKVTAxJUbg==", "x-amzn-trace-id": "Root=1-5c4babe3-d12496852222efb0d911dfa2", "x-forwarded-for": "54.67.51.193, 54.239.134.14", "x-forwarded-port": "443", "x-forwarded-proto": "https"}, "uri_params": {"key": "test"}, "method": "GET", "context": {"resourceId": "wvdbuo", "resourcePath": "/objects/{key}", "httpMethod": "GET", "extendedRequestId": "UFfLiFlNSK4Fmrw=", "requestTime": "26/Jan/2019:00:37:55 +0000", "path": "/api/objects/test", "accountId": "568285458700", "protocol": "HTTP/1.1", "stage": "api", "domainPrefix": "jlmq3ygdu1", "requestTimeEpoch": 1548463075419, "requestId": "9f1622b9-2102-11e9-b14b-5551fb47ff1c", "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "sourceIp": "54.67.51.193", "accessKey": null, "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "HTTPie/0.9.8", "user": null}, "domainName": "jlmq3ygdu1.execute-api.us-west-1.amazonaws.com", "apiId": "jlmq3ygdu1"}, "stage_vars": null}>
    2019-01-26 00:37:56.009000 a8ddcb [01;31m[Ks3[m[K - ERROR - Internal Error for <function [01;31m[Ks3[m[Kobjects at 0x7f6689386730>
    2019-01-26 00:37:56.009000 a8ddcb File "/var/task/app.py", line 35, in [01;31m[Ks3[m[Kobjects
    2019-01-26 00:39:25.506000 882ee8 [01;31m[Ks3[m[Kobjects: SO FAR SO GOOD -----------------------------------------------------------------
    2019-01-26 00:39:25.506000 882ee8 [01;31m[Ks3[m[Kobjects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 24b0e5a3429d07ef12381da50e07f70f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'jJFLYx3gAXNkB8v5_zW3OgO7IYkbvDBktrUD8hZSt2qp20QVMpXIew==', 'x-amzn-trace-id': 'Root=1-5c4bac3c-2d30962cbacf1490cf4231f6', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFfZgGp6SK4Ff-A=', 'requestTime': '26/Jan/2019:00:39:24 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463164862, 'requestId': 'd4660ebb-2102-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:39:25.506000 882ee8 GET [01;31m[Ks3[m[K://mjbright-uploads/test
    2019-01-26 00:39:26.089000 882ee8 [01;31m[Ks3[m[K - ERROR - Internal Error for <function [01;31m[Ks3[m[Kobjects at 0x7f74add50730>
    2019-01-26 00:39:26.089000 882ee8 File "/var/task/app.py", line 36, in [01;31m[Ks3[m[Kobjects
    2019-01-26 00:42:38.817000 0d4318 [01;31m[Ks3[m[Kobjects: SO FAR SO GOOD -----------------------------------------------------------------
    2019-01-26 00:42:38.817000 0d4318 [01;31m[Ks3[m[Kobjects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 1b52a5dd431f9e3c81753e61dfdf467a.cloudfront.net (CloudFront)', 'x-amz-cf-id': '66biLrXpMrvpM4V03J1OvKfbPVXicEW22C7uQ6u9oItwQAHGgMDUCg==', 'x-amzn-trace-id': 'Root=1-5c4bacfe-36903ca282508f579135cda1', 'x-forwarded-for': '54.67.51.193, 54.239.134.7', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFf3tEdCyK4Fp6w=', 'requestTime': '26/Jan/2019:00:42:38 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463358168, 'requestId': '479e35bd-2103-11e9-b75a-8fe56bba7a8e', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:42:38.817000 0d4318 GET [01;31m[Ks3[m[K://mjbright-uploads/test
    2019-01-26 00:42:39.449000 0d4318 [01;31m[Ks3[m[K - ERROR - Internal Error for <function [01;31m[Ks3[m[Kobjects at 0x7fb703c83730>
    2019-01-26 00:42:39.449000 0d4318 File "/var/task/app.py", line 36, in [01;31m[Ks3[m[Kobjects
    2019-01-26 00:46:09.358000 830682 [01;31m[Ks3[m[Kobjects: SO FAR SO GOOD -----------------------------------------------------------------
    2019-01-26 00:46:09.358000 830682 [01;31m[Ks3[m[Kobjects: <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 24b0e5a3429d07ef12381da50e07f70f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'O2lh0HapYLq_0y5dVOfrUFBbkwRLoamPEqLGPzNn7rkgHm9z34tbJg==', 'x-amzn-trace-id': 'Root=1-5c4badd0-12c28bf8272ed3db0745db70', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'wvdbuo', 'resourcePath': '/objects/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFgYnGv6yK4Fitg=', 'requestTime': '26/Jan/2019:00:46:08 +0000', 'path': '/api/objects/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548463568702, 'requestId': 'c51b26d3-2103-11e9-900f-d5ae7e711214', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 00:46:09.358000 830682 GET [01;31m[Ks3[m[K://mjbright-uploads/test
    2019-01-26 01:03:44.809000 189dfc [01;31m[Ks3[m[Ktext: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 e2af8a85927835558866752f53562ecd.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'pc2_vVu5MLKAg72qL6zQ9Fj-Y9UHZS8R-gBq76TbPcrAIvrVKzhS6g==', 'x-amzn-trace-id': 'Root=1-5c4bb1f0-4a683a7b7d0b5cf1ac91e237', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFi9hGfnyK4FUUQ=', 'requestTime': '26/Jan/2019:01:03:44 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464624139, 'requestId': '3a320e6d-2106-11e9-b04b-6deecaeee351', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:03:44.809000 189dfc [01;31m[Ks3[m[Ktext: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 e2af8a85927835558866752f53562ecd.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'pc2_vVu5MLKAg72qL6zQ9Fj-Y9UHZS8R-gBq76TbPcrAIvrVKzhS6g==', 'x-amzn-trace-id': 'Root=1-5c4bb1f0-4a683a7b7d0b5cf1ac91e237', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFi9hGfnyK4FUUQ=', 'requestTime': '26/Jan/2019:01:03:44 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464624139, 'requestId': '3a320e6d-2106-11e9-b04b-6deecaeee351', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:03:44.869000 189dfc GET [01;31m[Ks3[m[K://mjbright-uploads/test
    2019-01-26 01:04:01.431000 189dfc [01;31m[Ks3[m[Ktext: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 49c80a47c1441dd194a8337982f1cd7e.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'THP5eRWQ4cEezLBbXU-2vT4VzPDF4-mCFcMy6JMGOQTUd367pcvL4w==', 'x-amzn-trace-id': 'Root=1-5c4bb201-b56313b28f6fdc1ce3892232', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAOGudyK4FSUw=', 'requestTime': '26/Jan/2019:01:04:01 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464641414, 'requestId': '447e02ca-2106-11e9-86ac-6596e4f7f276', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:01.431000 189dfc [01;31m[Ks3[m[Ktext: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 49c80a47c1441dd194a8337982f1cd7e.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'THP5eRWQ4cEezLBbXU-2vT4VzPDF4-mCFcMy6JMGOQTUd367pcvL4w==', 'x-amzn-trace-id': 'Root=1-5c4bb201-b56313b28f6fdc1ce3892232', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': 'ezap0f', 'resourcePath': '/text/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAOGudyK4FSUw=', 'requestTime': '26/Jan/2019:01:04:01 +0000', 'path': '/api/text/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464641414, 'requestId': '447e02ca-2106-11e9-86ac-6596e4f7f276', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:01.450000 189dfc GET [01;31m[Ks3[m[K://mjbright-uploads/test
    2019-01-26 01:04:02.437000 189dfc [01;31m[Ks3[m[Kjson: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==', 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': '1ay49m', 'resourcePath': '/json/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAYGqtSK4Ff-A=', 'requestTime': '26/Jan/2019:01:04:02 +0000', 'path': '/api/json/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464642423, 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:02.437000 189dfc [01;31m[Ks3[m[Kjson: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==', 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': '1ay49m', 'resourcePath': '/json/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAYGqtSK4Ff-A=', 'requestTime': '26/Jan/2019:01:04:02 +0000', 'path': '/api/json/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464642423, 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:02.437000 189dfc [01;31m[Ks3[m[Kjson: ----------------------------------------------------------------- <{'query_params': None, 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cloudfront-forwarded-proto': 'https', 'cloudfront-is-desktop-viewer': 'true', 'cloudfront-is-mobile-viewer': 'false', 'cloudfront-is-smarttv-viewer': 'false', 'cloudfront-is-tablet-viewer': 'false', 'cloudfront-viewer-country': 'US', 'host': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'user-agent': 'HTTPie/0.9.8', 'via': '1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)', 'x-amz-cf-id': 'Fl_4Y6lsAmuU7vr5sIZ7jXR0N3k0V6d2fnm9cb2FBowui4L_K5pqpQ==', 'x-amzn-trace-id': 'Root=1-5c4bb202-550f0d68a4b72c38b4559ae8', 'x-forwarded-for': '54.67.51.193, 54.239.134.14', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'uri_params': {'key': 'test'}, 'method': 'GET', 'context': {'resourceId': '1ay49m', 'resourcePath': '/json/{key}', 'httpMethod': 'GET', 'extendedRequestId': 'UFjAYGqtSK4Ff-A=', 'requestTime': '26/Jan/2019:01:04:02 +0000', 'path': '/api/json/test', 'accountId': '568285458700', 'protocol': 'HTTP/1.1', 'stage': 'api', 'domainPrefix': 'jlmq3ygdu1', 'requestTimeEpoch': 1548464642423, 'requestId': '4517f8df-2106-11e9-813f-4b680ee1356d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '54.67.51.193', 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'HTTPie/0.9.8', 'user': None}, 'domainName': 'jlmq3ygdu1.execute-api.us-west-1.amazonaws.com', 'apiId': 'jlmq3ygdu1'}, 'stage_vars': None}>
    2019-01-26 01:04:02.449000 189dfc GET [01;31m[Ks3[m[K://mjbright-uploads/test
    2019-01-26 01:04:02.528000 189dfc [01;31m[Ks3[m[K - ERROR - Internal Error for <function [01;31m[Ks3[m[Kjson at 0x7f3be49ebd90>
    2019-01-26 01:04:02.528000 189dfc File "/var/task/app.py", line 59, in [01;31m[Ks3[m[Kjson



```bash
echo hello world | http PUT :8000/text/test
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m400[39;49;00m [36mBad Request[39;49;00m
    [36mContent-Length[39;49;00m: [33m74[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:05:44 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"BadRequestError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"BadRequestError: Error Parsing JSON"[39;49;00m
    }
    



```bash
echo hello world | http PUT https://jlmq3ygdu1.execute-api.us-west-1.amazonaws.com/api/text/test
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m400[39;49;00m [36mBad Request[39;49;00m
    [36mConnection[39;49;00m: [33mkeep-alive[39;49;00m
    [36mContent-Length[39;49;00m: [33m74[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 01:05:14 GMT[39;49;00m
    [36mVia[39;49;00m: [33m1.1 8008015354a3ca72f56c382a1d1cfe9f.cloudfront.net (CloudFront)[39;49;00m
    [36mX-Amz-Cf-Id[39;49;00m: [33mhJ_mqOfA_pDSF8wBR5xVPFHwYsiTK9WKOfJ0SEPPIXQljIw__LA52w==[39;49;00m
    [36mX-Amzn-Trace-Id[39;49;00m: [33mRoot=1-5c4bb24a-c4346c80ef290c006c5cab40;Sampled=0[39;49;00m
    [36mX-Cache[39;49;00m: [33mError from cloudfront[39;49;00m
    [36mx-amz-apigw-id[39;49;00m: [33mUFjLoHZfyK4FlIg=[39;49;00m
    [36mx-amzn-RequestId[39;49;00m: [33m700050be-2106-11e9-9afc-0db0ce26a5a3[39;49;00m
    
    {
        [34;01m"Code"[39;49;00m: [33m"BadRequestError"[39;49;00m,
        [34;01m"Message"[39;49;00m: [33m"BadRequestError: Error Parsing JSON"[39;49;00m
    }
    



```bash
aws s3 help
```

    S3()                                                                      S3()
    
    
    
    NAME
           s3 -
    
    DESCRIPTION
           This  section  explains  prominent concepts and notations in the set of
           high-level S3 commands provided.
    
       Path Argument Type
           Whenever using a command, at least one path argument must be specified.
           There are two types of path arguments: LocalPath and S3Uri.
    
           LocalPath: represents the path of a local file or directory.  It can be
           written as an absolute path or relative path.
    
           S3Uri: represents the location of a S3 object, prefix, or bucket.  This
           must  be  written in the form s3://mybucket/mykey where mybucket is the
           specified S3 bucket, mykey is the specified S3 key.  The path  argument
           must  begin with s3:// in order to denote that the path argument refers
           to a S3 object. Note that prefixes are separated  by  forward  slashes.
           For  example, if the S3 object myobject had the prefix myprefix, the S3
           key would be myprefix/myobject, and if the object  was  in  the  bucket
           mybucket, the S3Uri would be s3://mybucket/myprefix/myobject.
    
       Order of Path Arguments
           Every  command  takes  one or two positional path arguments.  The first
           path argument represents the source, which is the local  file/directory
           or  S3  object/prefix/bucket  that  is being referenced.  If there is a
           second path argument, it represents the destination, which is the local
           file/directory  or  S3  object/prefix/bucket that is being operated on.
           Commands with only one path argument do not have a destination  because
           the operation is being performed only on the source.
    
       Single Local File and S3 Object Operations
           Some  commands  perform operations only on single files and S3 objects.
           The following commands are single file/object operations if no --recur-
           sive flag is provided.
    
              o cp
    
              o mv
    
              o rm
    
           For  this  type of operation, the first path argument, the source, must
           exist and be a local file or S3 object.  The second path argument,  the
           destination,  can  be  the  name  of  a local file, local directory, S3
           object, S3 prefix, or S3 bucket.
    
           The destination is indicated as a local directory,  S3  prefix,  or  S3
           bucket if it ends with a forward slash or back slash.  The use of slash
           depends on the path argument type.  If the path argument  is  a  Local-
           Path,  the type of slash is the separator used by the operating system.
           If the path is a S3Uri, the forward slash must always be  used.   If  a
           slash  is at the end of the destination, the destination file or object
           will adopt the name of the source file or object.  Otherwise, if  there
           is no slash at the end, the file or object will be saved under the name
           provided.  See examples in cp and mv to illustrate this description.
    
       Directory and S3 Prefix Operations
           Some commands only perform operations on the contents of a local direc-
           tory  or  S3 prefix/bucket.  Adding or omitting a forward slash or back
           slash to the end of any path argument, depending on its type, does  not
           affect  the  results  of  the  operation.   The following commands will
           always result in a directory or S3 prefix/bucket operation:
    
           o sync
    
           o mb
    
           o rb
    
           o ls
    
       Use of Exclude and Include Filters
           Currently, there is no support for the use of UNIX style wildcards in a
           command's  path  arguments.   However,  most  commands  have  --exclude
           "<value>" and --include  "<value>"  parameters  that  can  achieve  the
           desired  result.   These  parameters perform pattern matching to either
           exclude or include a particular file or object.  The following  pattern
           symbols are supported.
    
              o *: Matches everything
    
              o ?: Matches any single character
    
              o [sequence]: Matches any character in sequence
    
              o [!sequence]: Matches any character not in sequence
    
           Any  number of these parameters can be passed to a command.  You can do
           this by providing an --exclude or --include  argument  multiple  times,
           e.g.   --include  "*.txt"  --include  "*.png".  When there are multiple
           filters, the rule is the filters that appear later in the command  take
           precedence  over filters that appear earlier in the command.  For exam-
           ple, if the filter parameters passed to the command were
    
              --exclude "*" --include "*.txt"
    
           All files will be excluded from the command  except  for  files  ending
           with  .txt   However, if the order of the filter parameters was changed
           to
    
              --include "*.txt" --exclude "*"
    
           All files will be excluded from the command.
    
           Each filter is evaluated against the source directory.  If  the  source
           location is a file instead of a directory, the directory containing the
           file is used as the source directory.  For example, suppose you had the
           following directory structure:
    
              /tmp/foo/
                .git/
                |---config
                |---description
                foo.txt
                bar.txt
                baz.jpg
    
           In  the  command aws s3 sync /tmp/foo s3://bucket/ the source directory
           is /tmp/foo.  Any include/exclude filters will be  evaluated  with  the
           source  directory prepended.  Below are several examples to demonstrate
           this.
    
           Given the directory structure above and the command aws s3 cp  /tmp/foo
           s3://bucket/  --recursive --exclude ".git/*", the files .git/config and
           .git/description will be excluded from the files to upload because  the
           exclude  filter  .git/*  will  have the source prepended to the filter.
           This means that:
    
              /tmp/foo/.git/* -> /tmp/foo/.git/config       (matches, should exclude)
              /tmp/foo/.git/* -> /tmp/foo/.git/description  (matches, should exclude)
              /tmp/foo/.git/* -> /tmp/foo/foo.txt  (does not match, should include)
              /tmp/foo/.git/* -> /tmp/foo/bar.txt  (does not match, should include)
              /tmp/foo/.git/* -> /tmp/foo/baz.jpg  (does not match, should include)
    
           The command aws s3  cp  /tmp/foo/  s3://bucket/  --recursive  --exclude
           "ba*" will exclude /tmp/foo/bar.txt and /tmp/foo/baz.jpg:
    
              /tmp/foo/ba* -> /tmp/foo/.git/config      (does not match, should include)
              /tmp/foo/ba* -> /tmp/foo/.git/description (does not match, should include)
              /tmp/foo/ba* -> /tmp/foo/foo.txt          (does not match, should include)
              /tmp/foo/ba* -> /tmp/foo/bar.txt  (matches, should exclude)
              /tmp/foo/ba* -> /tmp/foo/baz.jpg  (matches, should exclude)
    
           Note that, by default, all files are included.  This means that provid-
           ing only an --include filter will not  change  what  files  are  trans-
           ferred.   --include  will only re-include files that have been excluded
           from an --exclude filter.  If you only want to upload files with a par-
           ticular extension, you need to first exclude all files, then re-include
           the files with the particular extension.  This command will upload only
           files ending with .jpg:
    
              aws s3 cp /tmp/foo/ s3://bucket/ --recursive --exclude "*" --include "*.jpg"
    
           If  you wanted to include both .jpg files as well as .txt files you can
           run:
    
              aws s3 cp /tmp/foo/ s3://bucket/ --recursive \
                  --exclude "*" --include "*.jpg" --include "*.txt"
    
           See 'aws help' for descriptions of global parameters.
    
    SYNOPSIS
              aws s3 <Command> [<Arg> ...]
    
    OPTIONS
           None
    
           See 'aws help' for descriptions of global parameters.
    
    AVAILABLE COMMANDS
           o cp
    
           o ls
    
           o mb
    
           o mv
    
           o presign
    
           o rb
    
           o rm
    
           o sync
    
           o website
    
    
    
                                                                              S3()



```bash
aws s3 ls s3://mjbright-uploads/objects/
```

    2019-01-26 00:19:55        900 test



```bash
aws s3 cp app.py s3://mjbright-uploads/test
```

    upload: ./app.py to s3://mjbright-uploads/test                 



```bash
chalice logs --include-lambda-messages
```


```bash
aws lambda list-functions
```

    {
        "Functions": [
            {
                "FunctionName": "chalice-app-dev-handler",
                "FunctionArn": "arn:aws:lambda:us-west-1:568285458700:function:chalice-app-dev-handler",
                "Runtime": "python3.6",
                "Role": "arn:aws:iam::568285458700:role/chalice-app-dev",
                "Handler": "app.handler",
                "CodeSize": 6116621,
                "Description": "",
                "Timeout": 60,
                "MemorySize": 128,
                "LastModified": "2019-01-26T02:26:42.254+0000",
                "CodeSha256": "WrtJGS2Xp8x7h2B/J869JIw9a7prGX20yCQXLKJzymo=",
                "Version": "$LATEST",
                "VpcConfig": {
                    "SubnetIds": [],
                    "SecurityGroupIds": [],
                    "VpcId": ""
                },
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": "82800b08-5f85-4e50-b501-dfe42805c38e"
            }
        ]
    }


# S3 Events


```bash
pwd
cat >app.py <<EOF

from chalice import Chalice

app = Chalice(app_name="s3events")
app.debug = True


# Whenever an object is uploaded to 'mybucket'
# this lambda function will be invoked.

@app.on_s3_event(bucket='mjbright-uploads')
def handler(event):
    print("S3Event: Object uploaded for bucket: %s, key: %s"
          % (event.bucket, event.key))

EOF
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/chalice-app



```bash
chalice deploy
```

    /usr/share/python-wheels/requests-2.18.4-py2.py3-none-any.whl/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
    Creating deployment package.
    Updating policy for IAM role: chalice-app-dev
    Updating lambda function: chalice-app-dev-handler
    Configuring S3 events in bucket mjbright-uploads to function chalice-app-dev-handler
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-1:568285458700:function:chalice-app-dev-handler



```bash
pwd
ls -al
aws s3 cp .gitignore s3://mjbright-uploads/g2314
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/chalice-app
    total 40
    drwxrwxr-x  6 user1 user1 4096 Jan 26 00:41 [0m[01;34m.[0m
    drwxrwxr-x 10 user1 user1 4096 Jan 26 02:21 [01;34m..[0m
    drwxrwxr-x  4 user1 user1 4096 Jan 25 00:00 [01;34m.chalice[0m
    -rw-rw-r--  1 user1 user1   37 Jan 24 22:33 .gitignore
    drwxrwxr-x  3 user1 user1 4096 Jan 25 01:32 [01;34m0[0m
    drwxrwxr-x  2 user1 user1 4096 Jan 26 02:26 [01;34m__pycache__[0m
    -rw-rw-r--  1 user1 user1  337 Jan 26 02:26 app.py
    drwxrwxr-x  4 user1 user1 4096 Jan 26 00:11 [01;34mchalice-app[0m
    -rw-rw-r--  1 user1 user1   28 Jan 25 02:41 requirements.txt
    -rw-rw-r--  1 user1 user1   13 Jan 26 01:51 test
    upload: ./.gitignore to s3://mjbright-uploads/g2314               



```bash
chalice logs --include-lambda-messages
```




```bash

```




```bash
cat > app.py <<EOF

from chalice import Chalice
from chalice import NotFoundError

app = Chalice(app_name='s3')

@app.route('/')
def index():
    return {'hello': 'world'}

import json
import boto3
from botocore.exceptions import ClientError

S3 = boto3.client('s3', region_name='us-west-2')
BUCKET = 'mjbright-uploads'

@app.route('/objects/{key}', methods=['GET', 'PUT'])
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT':
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)

EOF
```


```bash
aws s3 rb --force s3://mjbright-uploads/
aws s3 mb s3://mjbright-uploads/
```

Just for local testing - cannot work as cannot access S3 credentials.


```bash
aws s3 ls s3://mjbright-uploads
echo '["testuser", {"fullname": "My full name"}]' | http PUT :8000/objects/testfile
aws s3 ls s3://mjbright-uploads
```




```bash
chalice deploy
```




```bash
echo '["testuser", {"fullname": "My full name"}]' | http PUT $(chalice url)/objects/testfile
```




```bash
aws s3 ls s3://mjbright-uploads/
```


```bash
aws s3 cp s3://mjbright-uploads/testfile -
```






```bash
BUCKET_NAME='mjbright-uploads'

cat > app.py <<EOF
from chalice import Chalice
#import sys

app = Chalice(app_name="helloworld")

# Whenever an object is uploaded to 'mybucket'
# this lambda function will be invoked.

@app.on_s3_event(bucket='$BUCKET_NAME')
def handler(event):
    # BUT WHERE DOES THIS OUTPUT GO?
    print("Object uploaded for bucket: %s, key: %s"
          % (event.bucket, event.key))
    #sys.exit(0)
EOF
```




```bash
cat app.py
```

Deploy a local chalice server in another window using ```chalice local```, then upload a file to our bucket


```bash
cat > requirements.txt <<EOF
boto3==1.3.1
EOF
```




```bash
aws lambda delete-function --function-name chalice-app-dev-handler
```




```bash
cat app.py

```




```bash
cat requirements.txt
```




```bash
aws lambda list-functions
```




```bash
# Only works when deployed?
chalice deploy
```






```bash
aws s3 cp /etc/hosts s3://mjbright-uploads/1
aws s3 ls  s3://mjbright-uploads
```




```bash

```




```bash

```




```bash

```




```bash

```




```bash

```




```bash

```




```bash

```




```bash

```




```bash

```


```bash

```


```bash

```


```bash

```


```bash

```


```bash

```


```bash

```

# More Reading

You can find more details about S3 website hosting here: https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html

An article describing the use of S3 for static website hosting including use of https, DNS routing
https://medium.freecodecamp.org/how-to-host-a-static-website-with-s3-cloudfront-and-route53-7cbb11d4aeea

# Cleanup

Note that we can use the ```aws s3 rm``` command to remove files from the bucket and ```aws s3 rb``` command to remove a bucket.


```bash
aws s3 rm s3://mjbright-static-site --recursive
aws s3 rb s3://mjbright-static-site
```

It's also possible to remoce the bucket directly using the ```--force``` option:
    ```aws s3 rb --force s3://mjbright-static-site```
