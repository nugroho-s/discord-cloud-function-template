from flask import escape, jsonify
import functions_framework
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

def hello_world(name):
    return 'Hello {}!'.format(escape(name or "World"))

def handle_interaction(request):
    if request["type"] == 1:
        return jsonify({
            "type": 1
        })
    else:
        return jsonify({
            "type": 4,
            "data": {
                "content": "hello"
            }
        })

def verify_signature(body, signature, timestamp):
    # Your public key can be found on your application in the Developer Portal
    PUBLIC_KEY = '011205304185c8e8c7e01ea97ec5d48888aeb9f1b1e054615a067a67c14c8b2a'
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    print(request_json)

    print("path is {}-".format(request.path))
    print("request is : {}".format(request_json))

    if (request.path is '/'):
        return hello_world(request.args["name"] if "name" in request.args else None)
    elif ("/interaction" in request.path):
        if (not "X-Signature-Ed25519" in request.headers) or (not "X-Signature-Timestamp" in request.headers):
            return 'invalid request signature', 401
        try:
            verify_signature(request.data.decode("utf-8"), request.headers["X-Signature-Ed25519"], request.headers["X-Signature-Timestamp"])
        except BadSignatureError:
            return 'invalid request signature', 401
        return handle_interaction(request_json)