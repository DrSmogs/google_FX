#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from OpenSSL import SSL

import disco #functions for Content Discovery

# Flask app should start in global layout
app = Flask(__name__)

#setup a few deaults for using the Content Disco API


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "trending":

        queryurl = disco.disco_url('trending','1')

        result = urllib.request.urlopen(queryurl).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res

    if req.get("result").get("action") == "trendin_list":

        limit = req.get("result").get("parameters").get("limit")
        queryurl = disco.disco_url('trending',limit)

        result = urllib.request.urlopen(queryurl).read()
        data = json.loads(result)
        res = makeWebhookResult2(data)
        return res

    else:
        return {}




def makeWebhookResult(data):
    hits = data.get('hits')
    if hits is None:
        return {}

    title = hits[0]['metadata']['title']
    description= hits[0]['metadata']['description']

    # print(json.dumps(item, indent=4))

    speech = "The hot show at the moment is " + title + "...." + description

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


def makeWebhookResult2(data):
    hits = data.get('hits')
    if hits is None:
        return {}

    speech = "The hot shows are "

    for show in hits:

        speech = speech + show['metadata']['title']


    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)
    context = ('/etc/letsencrypt/live/iamshaw.net/fullchain.pem', '/etc/letsencrypt/live/iamshaw.net/privkey.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True)
