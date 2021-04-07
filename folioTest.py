
import requests
from crontab import CronTab
try:
    import configparser
except:
    import ConfigParser
import copy, json, os, sys
import argparse, datetime 



def getCredentials(section="DEFAULT"):
    """ 
        getCredentials- pull credentials from credential file.
    """
    home=os.path.expanduser('~')
    credentials="{0}/.folio-cron".format(home)
    try:
        config = configparser.ConfigParser()
    except:
        config = ConfigParser.ConfigParser()
    config.read(credentials)
    return  dict(config.items(section))

def getAuthToken(tenant,section="DEFAULT"):
    """ 
        getAuthToken- returns auth token.
    """
    headers = copy.copy(header_default)
    headers["x-okapi-tenant"]= tenant
    creds= getCredentials(section)
    req = requests.post("{0}/authn/login".format(okapi_url),data=json.dumps(creds),headers=headers)
    if req.status_code >= 400:
        raise Exception("Please check username and password in credential file ('~/.folio-cron').")
    # print(reg.headers['x-okapi-token'])
    return req.headers['x-okapi-token']



header_default={ "Content-type": "application/json", "cache-control": "no-cache", "accept": "application/json" }
okapi_url = "https://test-culibraries.colorado.edu"

def getHeaders(tenant,section="DEFAULT"):
    headers = copy.copy(header_default)
    headers["x-okapi-tenant"]= tenant
    headers["x-okapi-token"]=getAuthToken(tenant,section=section)
    return headers 
tenant="culibraries"
req = requests.get("{0}/codex-instances?active=true".format(okapi_url),headers=getHeaders(tenant))
print(req.json())
