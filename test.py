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


import disco #functions for Content Discovery

print(disco.disco_url('basic',limit=1, rid='SEARCH1', fx='the simpsons', sfx='type:LINEAR', mlt=None))
