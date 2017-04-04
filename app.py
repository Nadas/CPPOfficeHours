#!/usr/bin/env python

import urllib
import json
import os
import csv

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if (req.get("result").get("action") != "office.hours") or (req.get("result").get("action") != "office.location"):
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("prof-name")


    reader = csv.reader(open('prof-office-hours.csv', 'r'))
    officeHours = {}
    for row in reader:
       k, v = row
       officeHours[k] = v

    reader = csv.reader(open('prof-office-locations.csv', 'r'))
    officeLocation = {}
    for row in reader:
       k, v = row
       officeLocation[k] = v

    if req.get("result").get("action") = "office.hours":
        speech = "Professor's " + name + " office hours are on" + str(officeHours[name]) + "."

    if req.get("result").get("action") = "office.location":
        speech = "Professor's " + name + " office location is" + str(officeLocation[name]) + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-cppofficehours"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
