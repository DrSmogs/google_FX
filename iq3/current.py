import logging

from sleekxmpp.stanza import StreamFeatures, Iq
from sleekxmpp.xmlstream import register_stanza_plugin, JID
from sleekxmpp.plugins import BasePlugin
from iq3 import stanza, current_programme, diagnostic_tuner, current_viewing, system_information, get_volume, set_volume
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher.id import MatcherId
import xml.etree.ElementTree as ET


class iq3(BasePlugin):

    name = 'iq3'
    description = 'my iq3'

    def plugin_init(self):
        register_stanza_plugin(Iq, current_programme)
        register_stanza_plugin(Iq, diagnostic_tuner)
        register_stanza_plugin(Iq, current_viewing)
        register_stanza_plugin(Iq, system_information)
        register_stanza_plugin(Iq, get_volume)
        register_stanza_plugin(Iq, set_volume)


        self.sessions = {};

    def get_current(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'get'
        iq.enable('current_programme')
        resp = iq.send(block=True);

        return resp

    def get_diag(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'get'
        iq.enable('diagnostic_tuner')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "diagnostic_tuner", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def set_viewing(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'set'
        iq.enable('current_viewing')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_viewing", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def set_viewing(self, jid=None, tjid=None, resource=None, chan=None):
        seqnr = "1234567"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'set'
        iq['xml:lang'] = 'en'
        iq['current_viewing']['current_channel'] = chan
        iq.enable('current_viewing')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_viewing", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def get_viewing(self, jid=None, tjid=None, resource=None):
        seqnr = "123"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'get'
        iq['xml:lang'] = 'en'
        iq.enable('current_viewing')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_viewing", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def get_info(self, jid=None, tjid=None, resource=None):
        seqnr = "1234567"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'get'
        iq['xml:lang'] = 'en'
        iq.enable('system_information')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "system_information", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def get_volume(self, jid=None, tjid=None, resource=None):
        seqnr = "1234567"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'get'
        iq['xml:lang'] = 'en'
        iq.enable('volume')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "volume", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def set_volume(self, jid=None, tjid=None, resource=None, mode=None):
        seqnr = "12345678"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'set'
        iq['xml:lang'] = 'en'
        if(mode=="on"):
            iq['volume']['mute'] = 'true'
        else:
            iq['volume']['mute'] = 'false'
        iq.enable('volume')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "volume", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def set_message(self, jid=None, tjid=None, resource=None):
        seqnr = "123456789"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['type'] = 'set'
        iq['xml:lang'] = 'en'
        iq['popup_message']['popup_name'] = 'default_foxtel_popup'
        iq['popup_message']['message'] = 'Test Message'
        iq['popup_message']['title'] = 'This is a titleMCtitle'
        iq['popup_message']['timeout'] = '5'
        iq.enable('popup_message')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "popup_message", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def get_chan(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'get'
        iq.enable('current_programme')
        resp = iq.send(block=True);

        return resp
