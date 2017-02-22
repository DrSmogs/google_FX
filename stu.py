#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssl
import sys
import logging
import getpass
import socket
from sleekxmpp import Iq, ClientXMPP
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin, ET
from sleekxmpp.exceptions import IqError, IqTimeout

import sleekxmpp

import iq3 #custom stnza stuff for iQ3 unit

#This contains the iq3 xmpp class as well as the functions you can call. functions will return a dictionary of values




class iq3_cmd(sleekxmpp.ClientXMPP):

    """
    Class for setting up the scorpio login and shit
    this then defines all the functions which go to get spaWned for the mother fucking API
    """

    def __init__(self, jid, password, to, resource):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.to = to
        self.Resource = resource


    # return info about current viewing
    def get_current(self):
        resp= {}
        resp['cmd']='get_current'
        resp['error']= None
        try:
            out = self['iq3'].get_current(self.jid, self.to, self.Resource)

            resp['event_name'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text
            resp['start_time'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}start_time').text
            resp['event_length'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_length').text
            resp['synopsys'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}synopsys').text
            resp['genre'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}genre').text
            resp['parental_rating'] = out.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}parental_rating').text

        except IqError as e:
            resp['error'] = "iq error " + str(e)
        except IqTimeout:
            resp['error'] = "Timeout "


        return resp

    def set_chan(self,channel):
        resp= {}
        resp['cmd']='set_channel'
        resp['error']= None
        resp['channel']=channel
        try:
            out = self['iq3'].set_viewing(self.jid, self.to, self.Resource, channel)
            try:
                resp['error'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}error').text
            except:
                resp['error'] = None

            try:
                resp['response'] = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}response').text
            except:
                resp['error'] = 'Unknown error'

        except IqError as e:
            resp['error'] = "iq error " + str(e)
        except IqTimeout:
            resp['error'] = "Timeout "

        return resp





def iq3_resp(action, data):

    #build the results need for the web query - returns speech and display text (more later) as a dictionary
    #uses the action to determine how to process results


    if action=="current_viewing":


        if data['error'] is not None:
            speech = "Sorry, i got an error - " + str(data['error'])
            displayText = "Sorry, i got an error - " + str(data['error'])

        else:


            speech = "Looks like you are watching " + str(data['event_name']) + "...." + str(data['synopsys'])
            displayText = "Looks like you are watching " + str(data['event_name']) + "...." + str(data['synopsys'])
    # change the channel
    elif action=="change_channel":


        if data['error'] is not None:
            speech = "Sorry, i got an error - " + str(data['error'])
            displayText = "Sorry, i got an error - " + str(data['error'])

        else:


            speech = "I have changed the channel to " + str(data['channel'])
            displayText = "I have changed the channel to " + str(data['channel'])


    else:
        speech="oh crap, something went wrong"
        displayText= "oh crap something went wrong"

    return {
        "speech": speech,
        "displayText": displayText,
        # "data": data,
        # "contextOut": [],
        "source": "Foxtel-iQ3"
    }
