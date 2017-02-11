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

disco.disco_url('trending','rid', 'fx', 'sfx', 'mlt')
