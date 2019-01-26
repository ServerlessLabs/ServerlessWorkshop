
# AWS Lambda - Twilio


## Setup



If you have chosen to use an rc file, source it as ```source <your-aws-credentials-rc-file>```, e.g.


```bash
. ~/.aws/credentials.rc
```

# Interfacing with Twilio

For this functionality you will need to create a free account with Twilio at https://www.twilio.com/try-twilio and then validate the telephone numbers to which you wish to send SMS

You then need to export the following variables in your environment:

```
export TWILIO_ACCOUNT_SID='your-account-sid
export TWILIO_AUTH_TOKEN='your-auth-token
export TWILIO_FROM_NUMBER='twilio-provided-number'
export TWILIO_TO_NUMBER='the-number-to-send-SMS'
```

It is best to place them in a sourceable file such as ~/.twilio.rc


```bash
cd /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/

chalice new-project twilio-sms
```


```bash
cd twilio-sms

cat > app.py <<EOF

from os import environ as env

# 3rd party imports
from chalice import Chalice, Response
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio Config
ACCOUNT_SID = env.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = env.get('TWILIO_AUTH_TOKEN')
FROM_NUMBER = env.get('TWILIO_FROM_NUMBER')
TO_NUMBER = env.get('TWILIO_TO_NUMBER')

app = Chalice(app_name='sms-shooter')

# Create a Twilio client using account_sid and auth token
tw_client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/service/sms/send', methods=['POST'])
def send_sms():
    request_body = app.current_request.json_body
    if request_body:
        custom_headers={'X-myheader': 'cool', 'X-From': "'"+FROM_NUMBER+"'", 'X-To': "'"+TO_NUMBER+"'", 'Content-Type': 'application/json'}
        try:
            msg = tw_client.messages.create(
                from_=FROM_NUMBER,
                body=request_body['msg'],
                to=TO_NUMBER)

            if msg.sid:
                return Response(status_code=201,
                                headers=custom_headers,
                                body={'status': 'success',
                                      'data': msg.sid,
                                      'message': 'SMS <{}> successfully sent to {}'.format(request_body['msg'], TO_NUMBER)})
            else:
                return Response(status_code=200,
                                headers=custom_headers,
                                body={'status': 'failure',
                                      'message': 'Please try again!!!'})
        except TwilioRestException as exc:
            return Response(status_code=400,
                                headers=custom_headers,
                            body={'status': 'failure',
                                  'message': exc.msg})
                                  

EOF

cat > requirements.txt <<EOF
boto3==1.3.1
twilio==6.22.0
EOF
```

### Sending SMS from local server

Stop the local server ```ctrl-C```

Source ~/.twilio.rc
```.  ~/.twilio.rc```

Restart local server
```chalice local```



```bash
. ~/.twilio.rc
#http POST :8000/service/sms/send msg="MY MESSAGE" --debug
http POST :8000/service/sms/send msg="MY MESSAGE at $(date) from ${USER}@$(hostname)"
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m201[39;49;00m [36mCreated[39;49;00m
    [36mContent-Length[39;49;00m: [33m187[39;49;00m
    [36mContent-Type[39;49;00m: [33mapplication/json[39;49;00m
    [36mDate[39;49;00m: [33mSat, 26 Jan 2019 06:48:04 GMT[39;49;00m
    [36mServer[39;49;00m: [33mBaseHTTP/0.6 Python/3.6.7[39;49;00m
    [36mX-From[39;49;00m: [33m'+33644601324'[39;49;00m
    [36mX-To[39;49;00m: [33m'+33652891534'[39;49;00m
    [36mX-myheader[39;49;00m: [33mcool[39;49;00m
    
    {
        [34;01m"data"[39;49;00m: [33m"SM7db3a082946e411cb95eec2e44cc7149"[39;49;00m,
        [34;01m"message"[39;49;00m: [33m"SMS <MY MESSAGE at Sat Jan 26 06:48:04 UTC 2019 from user1@ip-172-31-21-116> successfully sent to +33652891534"[39;49;00m,
        [34;01m"status"[39;49;00m: [33m"success"[39;49;00m
    }
    


### Sending SMS to Twilio from deployed service

**INCOMPLETE**: Need to safely transfer credentials into version deployed onto AWS

For now this is a **WORST PRACTICE** ... but this VM will be deleted this morning so the risk is limited.


```bash
chalice deploy; chalice url
```




```bash
## BUT HOW TO PASS IN TWILIO SECRETS ?? !!

http POST $(chalice url)/service/sms/send msg="MY MESSAGE at $(date) from ${USER}@$(hostname)"
```



# More Reading


# Cleanup




```bash

```


