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
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    action=req.get("result").get("action")

    if action == "trending":

        queryurl = disco.disco_url('trending','1')

        result = urllib.request.urlopen(queryurl).read()
        data = json.loads(result)
        res = disco.disco_resp(action,data)
        return res

    elif action == "trending_list":

        print("trending_list triggered")
        limit = req.get("result").get("parameters").get("limit")
        print(limit)
        queryurl = disco.disco_url('trending',limit)

        result = urllib.request.urlopen(queryurl).read()
        data = json.loads(result)
        res = disco.disco_resp(action,data)
        return res

    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)
    #context = ('/etc/letsencrypt/live/iamshaw.net/fullchain.pem', '/etc/letsencrypt/live/iamshaw.net/privkey.pem')
    #app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True)
    app.run(host='0.0.0.0',port=5000)
