# Importing general python modules
import logging, os

KID = os.environ['KID']
PSSH = os.environ['PSSH']
PROHEADER = os.environ['PROHEADER']
MYKEY = os.environ['MYKEY']
DEBUGMODE = os.environ['DEBUGMODE']
CONTENTID = os.environ['CONTENTID']

# Importing modules from Chalice
from chalice import Chalice, Response, IAMAuthorizer

# Enabling IAM as the default authorizer
authorizer = IAMAuthorizer()

app = Chalice(app_name='speke4hbbtv')

# Enabling debug logs
if DEBUGMODE == 'ENABLED':
    app.log.setLevel(logging.DEBUG)
    app.log.debug('Debug mode enabled')

# A simple lambda function to capture MediaPackage events. CW events from MP is piped to this Lambda function as event.
# @app.lambda_function()
# def mediapackage_logging(event, context):
#     print(event)

# Lambda function to generate SPEKE response with the WRMHEADER as environment variable.
@app.route('/get/keys', methods=['GET','POST'], content_types=['application/xml'], authorizer=authorizer)
def getkeys():

    # Sample SPEKE responses. This response was hardcoded. WRMHEADER was pre-created using an Elemental Live
    kresponse = '''
    <cpix:CPIX xmlns:cpix="urn:dashif:org:cpix" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:speke="urn:aws:amazon:com:speke" id="''' +CONTENTID+ '''">
        <cpix:ContentKeyList>
            <cpix:ContentKey explicitIV="OFj2IjCsPJFfMAxmQxLGPw==" kid="''' +KID+ '''">
                <cpix:Data>
                    <pskc:Secret>
                        <pskc:PlainValue>'''+MYKEY+'''</pskc:PlainValue>
                    </pskc:Secret>
                </cpix:Data>
            </cpix:ContentKey>
        </cpix:ContentKeyList>
        <cpix:DRMSystemList>
        <!-- Common encryption / MSS (Playready) -->
            <cpix:DRMSystem kid="'''+KID+'''" systemId="9a04f079-9840-4286-ab92-e65be0885f95">
                <cpix:PSSH>'''+PSSH+'''</cpix:PSSH>
                <speke:ProtectionHeader>'''+PROHEADER+'''</speke:ProtectionHeader>
            </cpix:DRMSystem>
        </cpix:DRMSystemList>
        <cpix:ContentKeyPeriodList>
            <cpix:ContentKeyPeriod id="keyPeriod_4ff2e55e-e3eb-4456-b3f8-e636be7f6747" index="0"/>
        </cpix:ContentKeyPeriodList>
        <cpix:ContentKeyUsageRuleList>
            <cpix:ContentKeyUsageRule kid="'''+KID+'''">
            <cpix:KeyPeriodFilter periodId="keyPeriod_4ff2e55e-e3eb-4456-b3f8-e636be7f6747"/>
        </cpix:ContentKeyUsageRule>
    </cpix:ContentKeyUsageRuleList>
    </cpix:CPIX>
    '''

    request = app.current_request

    if request.raw_body is not None:
        event = request.raw_body
        app.log.debug(event)
        myheaders = request.headers
        app.log.debug(myheaders) # header requests
        app.log.debug("Request-Method:" + request.method) # Method used by the requester
        app.log.debug("SPEKE-Serever-Response*************")
        app.log.debug(kresponse) # response created 
        app.log.debug("KID:" + KID)
        app.log.debug("Content-Key:" + MYKEY)
        app.log.debug("PSSH-Header:" + PSSH)
        app.log.debug("PRO-HEADER:" + PROHEADER)
        statuscode="200"

    else:
        app.log.error("No request body inside the client request.") # if the request doesn't contain a valid body, the lambda function throw an error
        kresponse = """
        <?xml version="1.0"?>
            <error>
                <message> No request body </message>
            </error>
        """
        statuscode="400"
    
    return Response(
        body=kresponse,
        status_code=statuscode,
        headers={
            'Speke-User-Agent': 'speke-demo',
            'Content-Type': 'application/xml'
        }
    )

# Lambda function to provide heartbeat status for SPEKE server
# @app.route('/get/heartbeat', methods=['GET'], authorizer=authorizer)
# def spekeheartbeat():
#     return {"Status": "OK"}