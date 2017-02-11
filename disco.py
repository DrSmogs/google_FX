#!/usr/bin/env python

#This is to hold functions for content disco to clean the main app nice and clean

from __future__ import print_function
#from future import standard_library
#standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os


def disco_url(searchtype, rid, fx, sfx, mlt):
    #build the content disco url
    url_params = {}

    envurl = "https://foxtel-prod-elb.digitalsmiths.net/sd/foxtel/"
    #this is the main url to use - i am using production one

    #below are parameters for the search which will be hard coded and not required to change with function
    #at least for now.....

    url_params['prod']="FOXTELIQ3"
    #Product Values:FOXTELIQ3, FOXTELTVGuide, FOXTELOnlineGuide, FOXTELGO, FOXTELGOKIDS, FOXTELPLAY
    #REQUIRED

    url_params['fxid']="00" #default value for no user
    #This is the user id which is a concatination of IDM + AID + LID
    #REQUIRE

    url_params['idm']="00" #default value for not logged in
    #This is a two character identifier Identifies which subscription
    # type ( IDM value) was used for sign-on or FOXTELSTB (02)
    # FOXTELPLAY(04). The value 00 will be used where sign-on has
    # not occurred for concatenated values(within fxid), NOLOGIN
    # where the value is used alone. IDM=00 is not expected,
    # FXID=00.. etc is expected.
    #REQUIRED

    url_params['aid']="cfcd208495d565ef66e7dff9f98764da" #md5 hash value of '0'
    #This is a hashed value of the account Id (MD5)
    #REQUIRED

    url_params['hwid']="cfcd208495d565ef66e7dff9f98764da" #md5 hash value of '0'
    #This is a hashed value of the hardware Id. If not available per installation UUID is required
    #REQUIRED

    url_params['device']="GOOGLEHOME-JamesAPI"
    #This field is to have MANUFACTURER-MODEL IDENTIFIER
    #MODEL IDENTIFIER may also include a dash if this helps but must be consistent.
    #REQUIRED

    url_params['dclass']=""
    #An agreed generic name for the product grouping. IE. PHONE, TABLET, BROWSER etc..
    #REQUIRED

    url_params['swver']="0.1"
    #Version of the client side software
    #REQUIRED

    url_params['dpg']="R18+"
    #Parental setting of the customer facing application or device.
    #Provided to allow results to be filtered against this value. The default sent needs to be the maximum value (R18+)
    #REQUIRED

    url_params['ao']="Y"
    #Default set to N. Separate to classification, indicates if adult
    #content should ever be returned. Implementation must allow
    #(not prohibit) this value to be changed by customer facing menu at a later date.
    #REQUIRED

    url_params['dopt']="0"
    #Default set to 0. See below for details. Implementation must
    #allow (not prohibit) this value to be changed by a customer facing menu.
    #REQUIRED

    url_params['BLOCKED']="YES"
    #Default set to YES. To support performing More Like this
    #Operations on a Program ID  for a channel tag provider
    #inaccessible to the customer at time of operation (other than parental blocking) by logged in users
    #REQUIRED

    url_params['REGION']="0" #would be noce to get DTT - need region ID tho
    #Default set to 0 for devices that dont support DTT. The Guide
    #app has a requirement to remember local terrestrial channels for not logged in users.
    #REQUIRED

    url_params['utcOffset']="+1100" #hardcoded to +11.. but need to have this chage later from google device
    #This is a 4 character representation of the current offset. i.e.
    #1000 for +10 UTC zones. This needs to be based on the users time settings.
    #REQUIRED

    url_params['fp']="" #no idea what this does
    #Specifies the fields of the result to be returned this specifies the exa


    url_params['fx']=fx
    #Asset search parameter, this is used for the base levels of search

    url_params['sfx']=sfx
     #Schedule search parameter, this is used to filter/search forspecific schedules or

    url_params['mlt']=mlt
    #YMAL parameter, this needs to be sent the programId of the show/movie that is needing to create the YMAL for

    url_params['rid']=rid
    # This contains the request identifier, this identifies the function
    # that is being called: AUTO1,AUTO2,AUTO3 - autosuggest RID's
    # SEARCH1 - Base search (no rollup)
    # SEARCH5 - Roll up search (roll up by show)
    # MLT1 - Base YMAL
    # MLT2 - Roll up YMAL
    # TRENDING1 - Trending results
    # SUGGEST1 - Base Suggested results
    # YESSUGGEST2 - Roll up Suggested results
    # POPULAR1 - Popular search results
    # POPULAR2 - Roll up popular search results
    #REQUIRED

    #construct the base url based on search type

    if searchtype=="YMAL":
        baseurl= envurl + "taps/assets/yma"
        #This controls all the YMAL(You May Also Like) functionality

    elif searchtype=="popular":
        baseurl=envurl + "taps/assets/popularity/popular"
        #This controls all the popular searches

    elif searchtype=="related":
        baseurl=envurl + "taps/assets/metadata/related"
        #This controls all the related functions. Currently this is the other episode functionality

    elif searchtype=="itemdetails":
        baseurl=envurl + "taps/assets/metadata/itemDetails"
        #This controls all the item detail functionality. This will only return 1 asset per call

    elif searchtype=="channel":
        baseurl=envurl + "taps/assets/metadata/channel"
        #This controls all the channel functionality. Based on sent channel tags will return all results that are within schedule

    elif searchtype=="detaillist":
        baseurl=envurl + "taps/assets/metadata/detailList"
        #This is similar to the item details function but will return more that 1 asset per call

    elif searchtype=="images":
        baseurl=envurl + "taps/assets/metadata/images"
        #This controls the image functionality. Will return images for all assets requested. This is not restricted by schedule

    elif searchtype=="trending":
        baseurl=envurl + "taps/assets/popularity/trending"
        #This controls the trendingfunctionality. Will return the current trending data (over the entire platform) based on what is
        #available on the product

    elif searchtype=="suggested":
        baseurl=envurl + "taps/assets/personalised/suggested"
        #This controls the suggested functionality. Will return suggested results based on the users sent privacy settings

    elif searchtype=="autosuggest":
        baseurl=envurl + "taps/assets/search/autosugges"
        #This controls the autosuggest results

    elif searchtype=="keyword":
        baseurl=envurl + "taps/assets/search/keyword"
        #This controls the keyword search. This is search that specifies the field to match against

    elif searchtype=="fullsearch":
        baseurl=envurl + "taps/assets/search/prefix"
        #This controls the Full search functionality. This is non-field based search

    elif searchtype=="events":
        baseurl=envurl + "implicitEvents"
        #This is where all the TVGuide Events need to be POSTed

    else:
        baseurl=""

    url=baseurl + urllib.urlencode(url_params)

    print(url)