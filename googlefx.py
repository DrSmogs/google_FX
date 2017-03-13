#!/usr/bin/env python

from __future__ import print_function
from future import standard_library


standard_library.install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sys
import getpass
import socket

import logging
logging.basicConfig(level=logging.DEBUG)

#xmpp stuff
from sleekxmpp import Iq, ClientXMPP
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin, ET
from sleekxmpp.exceptions import IqError, IqTimeout

import sleekxmpp
import iq3 #custom stanza stuff for iQ3 unit
import stu #class and functions for sending iQ3 commands and processing responses

from flask import Flask, request, make_response, render_template #API stuff

from config import config # config file for app - make sure you rename config-blank.py and fill out values

import disco # functions for Content Discovery

# little big of stuff to make it work on both python versions
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

# Flask app should start in global layout
app = Flask(__name__)

# setup the xmpp connection for controlling the iQ3
xmpp = stu.iq3_cmd(config.loginjid, config.loginpw, config.tojid, config.resource)
xmpp.register_plugin('xep_0030') # Service Discovery
xmpp.register_plugin('xep_0004') # Data Forms
xmpp.register_plugin('xep_0060') # PubSub
xmpp.register_plugin('xep_0199') # XMPP Ping
xmpp.register_plugin('iq3', module=iq3) # custom iQ3 stanza plugin



#main API endpoint for google home
@app.route('/google', methods=['POST'])
def google():
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

    # Return the title and synopsys of top trending show
    if action == "trending":

        queryurl = disco.disco_url('trending','1')

        result = urlopen(queryurl).read().decode('utf8')
        data = json.loads(result)
        res = disco.disco_resp(action,data)
        return res

    # Return the titles of X trending shows in order
    elif action == "trending_list":

        limit = req.get("result").get("parameters").get("limit")
        queryurl = disco.disco_url('trending',limit)

        result = urlopen(queryurl).read().decode('utf8')
        data = json.loads(result)
        res = disco.disco_resp(action,data)
        return res

    # Return the current title and synopsys of what is being viewed
    elif action == "current_viewing":

        data = xmpp.get_current()
        res = stu.iq3_resp(action,data)
        return res
    # change to the channel number
    elif action == "change_channel":

        channel = req.get("result").get("parameters").get("channel")
        data = xmpp.set_chan(channel)
        res = stu.iq3_resp(action,data)
        return res

    elif action == "search":

        search = req.get("result").get("parameters").get("search")
        queryurl = disco.disco_url('basic',limit=1, rid='SEARCH1', fx=search, sfx='type:LINEAR', mlt=None)

        result = urlopen(queryurl).read().decode('utf8')
        data = json.loads(result)
        res = disco.disco_resp(action,data,search)
        return res




    else:
        return {}

# once xmpp client is connected - send presence and roster as expected
def session_start(e):
    xmpp.get_roster()
    xmpp.send_presence()


xmpp.add_event_handler('session_start', session_start) # xmpp session start handler

if __name__ == '__main__':
    xmpp.connect() # connect to xmpp server
    xmpp.process(block=False) #process xmpp stuff

    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(host='0.0.0.0',port=5000)
