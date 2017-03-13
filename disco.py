#!/usr/bin/env python

#This is to hold functions for content disco to clean the main app nice and clean
# in particular it contains a fucntion for building the content disco query url and also for parsing
#the results from content disco into the google format

import datetime
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

def disco_url(searchtype, limit=None, rid=None, fx=None, sfx=None, mlt=None):
    #build the content disco url
    url_params = {}

    envurl = "https://foxtel-prod-admin-0.digitalsmiths.net/sd/temp-foxtel/"
    #this is the main url to use - i am using production one

    #below are parameters for the search which will be hard coded and not required to change with function
    #at least for now.....

    url_params['prod']="FOXTELIQ3"
    #Product Values:FOXTELIQ3, FOXTELTVGuide, FOXTELOnlineGuide, FOXTELGO, FOXTELGOKIDS, FOXTELPLAY
    #REQUIRED

    url_params['fxid']="00d41d8cd98f00b204e9800998ecf8427ed41d8cd98f00b204e9800998ecf8427e" #supplied by jason
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

    url_params['aid']="d41d8cd98f00b204e9800998ecf8427ecfcd208495d565ef66e7dff9f98764da" #supplied by Jason
    #This is a hashed value of the account Id (MD5)
    #REQUIRED

    url_params['hwid']="d41d8cd98f00b204e9800998ecf8427e" #Provided by Jason
    #This is a hashed value of the hardware Id. If not available per installation UUID is required
    #REQUIRED

    url_params['device']="GOOGLEHOME-JamesAPI"
    #This field is to have MANUFACTURER-MODEL IDENTIFIER
    #MODEL IDENTIFIER may also include a dash if this helps but must be consistent.
    #REQUIRED

    url_params['dclass']="TERMINAL"
    #An agreed generic name for the product grouping. IE. PHONE, TABLET, BROWSER etc..
    #REQUIRED

    url_params['swver']="0.1"
    #Version of the client side software
    #REQUIRED

    url_params['dpg']="R"
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

    url_params['utcOffset']="+1000" #hardcoded to +11.. but need to have this chage later from google device
    #This is a 4 character representation of the current offset. i.e.
    #1000 for +10 UTC zones. This needs to be based on the users time settings.
    #REQUIRED

    #url_params['fp']="" #no idea what this does
    #Specifies the fields of the result to be returned this specifies the exa

    if limit is not None:
        url_params['limit']=limit
    #Limits the number of results

    if fx is None:
        url_params['fx']= ("metadata.title,metadata.episodeTitle,metadata.seasonNumber,metadata.episodeNumber,metadata.classification,"
        "metadata.genreName,metadata.subGenreName,metadata.titleId,metadata.shortSynopsis,metadata.category,"
        "metadaa.publishDuration,relevantSchedules.eventTitle,relevantSchedules.type,"
        "relevantSchedules.startTime,relevantSchedules.endTime,relevantSchedules.sourceChannel")

    else:
        url_params['fx']=fx

    #Asset search parameter, this is used for the base levels of search

    if sfx is not None:
        url_params['sfx']=sfx
    #Schedule search parameter, this is used to filter/search forspecific schedules or

    if mlt is not None:
        url_params['mlt']=mlt
    #YMAL parameter, this needs to be sent the programId of the show/movie that is needing to create the YMAL for

    if rid is not None:
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
        baseurl= envurl + "taps/assets/yma?"
        #This controls all the YMAL(You May Also Like) functionality

    elif searchtype=="popular":
        baseurl=envurl + "taps/assets/popularity/popular?"
        #This controls all the popular searches

    elif searchtype=="related":
        baseurl=envurl + "taps/assets/metadata/related?"
        #This controls all the related functions. Currently this is the other episode functionality

    elif searchtype=="itemdetails":
        baseurl=envurl + "taps/assets/metadata/itemDetails?"
        #This controls all the item detail functionality. This will only return 1 asset per call

    elif searchtype=="channel":
        baseurl=envurl + "taps/assets/metadata/channel?"
        #This controls all the channel functionality. Based on sent channel tags will return all results that are within schedule

    elif searchtype=="detaillist":
        baseurl=envurl + "taps/assets/metadata/detailList?"
        #This is similar to the item details function but will return more that 1 asset per call

    elif searchtype=="images":
        baseurl=envurl + "taps/assets/metadata/images?"
        #This controls the image functionality. Will return images for all assets requested. This is not restricted by schedule

    elif searchtype=="trending":
        baseurl=envurl + "taps/assets/popularity/trending?"
        #This controls the trendingfunctionality. Will return the current trending data (over the entire platform) based on what is
        #available on the product

    elif searchtype=="suggested":
        baseurl=envurl + "taps/assets/personalised/suggested?"
        #This controls the suggested functionality. Will return suggested results based on the users sent privacy settings

    elif searchtype=="autosuggest":
        baseurl=envurl + "taps/assets/search/autosuggest?"
        #This controls the autosuggest results

    elif searchtype=="keyword":
        baseurl=envurl + "taps/assets/search/keyword?"
        #This controls the keyword search. This is search that specifies the field to match against

    elif searchtype=="fullsearch":
        baseurl=envurl + "taps/assets/search/prefix?"
        #This controls the Full search functionality. This is non-field based search

    elif searchtype=="basic":
        baseurl=envurl + "taps/assets/search/basic?"
        #This controls the Full search functionality. This is non-field based search

    elif searchtype=="events":
        baseurl=envurl + "implicitEvents?"
        #This is where all the TVGuide Events need to be POSTed

    else:
        baseurl=""

    url=baseurl + urlencode(url_params) #+"&fx="+fx

    return url

def disco_resp(action, data):

    #build the results need for the web query - returns speech and display text (more later) as a dictionary
    #uses the action to determine how to process results


    if action=="trending":
        hits = data.get('hits')
        if hits is None:
            return {}

        title = hits[0]['metadata']['title']
        description= hits[0]['metadata']['description']
	#starttime = datetime.datetime.fromtimestamp((hits[0]['relevantSchedules'][0]['startTime'])/1000).strftime('%I:%M %p')
        speech = "The hot show at the moment is " + title + "...." + description #+ ".. it started at " + starttime
        displayText = "The hot show at the moment is " + title + "...." + description


    elif action=="trending_list":
        hits = data.get('hits')
        if hits is None:
            return {}

        speech = "The hottest shows are "

        for show in hits:

            speech = speech + show['metadata']['title'] + ", "

        displayText = speech


    elif action=="search":
        hits = data.get('hits')
        if hits is None:
            return {}

        title = hits[0]['metadata']['title']
        description= hits[0]['metadata']['description']
        starttime = datetime.datetime.fromtimestamp((hits[0]['relevantSchedules'][0]['startTime'])/1000).strftime('%A %d %I:%M %p')
        endtime = datetime.datetime.fromtimestamp((hits[0]['relevantSchedules'][0]['endTime'])/1000).strftime('%I:%M %p')
        channel = hits[0]['relevantSchedules'][0]['sourceChannel']
        speech = title + " starts on " + starttime + " and ends at " + endtime + " on " + channel + ". This is the one where " + description
        displayText = speech


    else:
        speech="oh crap, something went wrong"
        displayText= "oh crap something went wrong"

    return {
        "speech": speech,
        "displayText": displayText,
        # "data": data,
        # "contextOut": [],
        "source": "Foxtel-Content-Disco-API"
    }
