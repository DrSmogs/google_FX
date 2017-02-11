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

# Flask app should start in global layout
app = Flask(__name__)

#setup a few deaults for using the Content Disco API

trendingurl = 'https://foxtel-prod-elb.digitalsmiths.net/sd/foxtel/taps/assets/popularity/trending'
trendingrid = 'TRENDING1'
trendinglimit= '1'
trendingBLOCKED = 'YES'
utcOfsett = '%2B1100'
offsett = '0'
prod = 'FOXTELIQ3'

# class ContDisco:
#     baseurl = 'https://foxtel-prod-elb.digitalsmiths.net/sd/foxtel/'
#     ymal = 'taps/assets/ymal'
#     popular = 'taps/assets/popularity/popular'
#     related = 'taps/assets/metadata/related'
#     idemdetails = 'taps/assets/metadata/itemDetails'
#     channel='taps/assets/metadata/channel'
#     detailslist='taps/assets/metadata/detailList'
#     image='taps/assets/metadata/images'
#     trending='taps/assets/popularity/trending'
#     suggested='taps/assets/personalised/suggested'
#     autosuggest='taps/assets/search/autosugges'
#     keyword='taps/assets/search/keyword'
#     fullsearch='taps/assets/search/prefix'
#     events='implicitEvents'

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

        baseurl = trendingurl
        fullurl = baseurl + '?rid=TRENDING1&limit=1&BLOCKED=YES&utcOffset=%2B1100&offset=0&prod=FOXTELIQ3'

        result = urllib.request.urlopen(fullurl).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res

    else:
        return {}



# def makeYqlQuery(req):
#     result = req.get("result")
#     parameters = result.get("parameters")
#     city = parameters.get("geo-city")
#     if city is None:
#         return None
#
#     return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    hits = data.get('hits')
    if hits is None:
        return {}


    metadata = hits.get('metadata')
    if result is None:
        return {}


    title = metadata.get('title')
    description = metadata.get('description')

    if (title is None) or (description is None):
        return {}


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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)
    context = ('/etc/letsencrypt/live/iamshaw.net/fullchain.pem', '/etc/letsencrypt/live/iamshaw.net/privkey.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True)
