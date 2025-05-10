# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask,request

app = Flask(__name__)

# Define a route that handles GET requests
@app.route('/createJIRA', methods=['POST'])
def createJira():

    data = request.get_json()

    # Get the body from the comment only
    comment_body = data.get("comment", {}).get("body", "")

    if "/jira" not in comment_body:
        return json.dumps({"message": "No /jira command in the comment. Skipping JIRA creation."}), 200

    url = "https://thirupathicob.atlassian.net/rest/api/3/issue"

    auth = HTTPBasicAuth("email", "APIKEY")

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = json.dumps( {
    "fields": {
        "description": {
        "content": [
            {
            "content": [
                {
                "text": "My first JIRA ticket.",
                "type": "text"
                }
            ],
            "type": "paragraph"
            }
        ],
        "type": "doc",
        "version": 1
        },
        "issuetype": {
        "id": "10009"
        },
        "project": {
        "key": "THIR"
        },
        "summary": "Creating first JIRA ticket",
    },
    "update": {}
    } )

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

app.run('0.0.0.0',port=5000)
