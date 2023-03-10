from flask import escape, jsonify
import functions_framework

def hello_world(name):
    return 'Hello {}!'.format(escape(name or "World"))

def handle_interaction(request):
     if request["type"] == 1:
        return jsonify({
            "type": 1
        })

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
        return handle_interaction(request_json)