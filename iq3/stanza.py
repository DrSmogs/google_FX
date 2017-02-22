
from sleekxmpp.xmlstream import ElementBase, ET


class current_programme(ElementBase):

    namespace = "foxtel:iq"
    name = 'current_programme'
    plugin_attrib = 'current_programme'
    interfaces = set(('current_programme'))
    sub_interfaces = interfaces

class diagnostic_tuner(ElementBase):

    namespace = "foxtel:iq"
    name = 'diagnostic_tuner'
    plugin_attrib = 'diagnostic_tuner'
    interfaces = set(('diagnostic_tuner'))
    sub_interfaces = interfaces

class current_viewing(ElementBase):
    namespace = "foxtel:iq"
    name = 'current_viewing'
    plugin_attrib = 'current_viewing'
    interfaces = set(('current_viewing','current_channel'))
    sub_interfaces = set(['current_channel'])

class system_information(ElementBase):
    namespace = "foxtel:iq"
    name = "system_information"
    plugin_attrib = "system_information"
    interfaces = set(('system_information'))
    sub_interfaces = interfaces

class get_volume(ElementBase):
    namespace = "foxtel:iq"
    name = "volume"
    plugin_attrib = "volume"
    interfaces = set(('volume'))
    sub_interfaces = interfaces

class set_volume(ElementBase):
    namespace = "foxtel:iq"
    name = "volume"
    plugin_attrib = "volume"
    interfaces = set(('volume','current_volume','mute'))
    sub_interfaces = set(['current_volume','mute'])
