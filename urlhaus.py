#!/usr/bin/env python

"""
This Python code can be used to submit new malicious URLs to the URLhaus project by abuse.ch. Details about the API as well as you personal api_key can be found at
https://urlhaus.abuse.ch/api/#submit
For questions and feature requests about the code please contact the author.
"""

import json
import requests
import argparse
import re

__author__ = "Corsin Camichel"
__copyright__ = "Copyright 2018, Corsin Camichel"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0-20180326"
__email__ = "cocaman@gmail.com"

url = 'https://urlhaus.abuse.ch/api/'
api_key = 'YOUR_API_KEY'

# helper function to check that a tag has the right format [A-Za-z0-9.-]
def check_tag_regex(s):
    if s == "":
        return 
    p = re.compile(r'([a-zA-Z\.-]+)')
    m = p.match(s)
    if m == None or not m.group() == s:
        raise argparse.ArgumentTypeError("Invalid tag used '" + s + "'")
    return str(s)

parser = argparse.ArgumentParser(description='Submit a new malicious URL to URLhaus')
parser.add_argument('-u', '--url', help='URL you want to submit (required)', type=str, metavar="URL", required=True)
parser.add_argument('-t', '--tags', dest='tags', help='Tag, allowed characters: [A-Za-z0-9.-]', required=False, type=check_tag_regex, metavar="Tags", default='', nargs="*")
parser.add_argument('-a', '--anon', dest='anon', help='If set to "1", your submission will be anonymous (no Twitter username displayed)', required=False, type=str, metavar="Anonymous", choices=['0', '1'], default=0)
parser.add_argument('-d', '--threat', dest='threat', help='Threat type of the URL (must be "malware_download" for now)', required=False, type=str, choices=['malware_download'], metavar="Threat", default="malware_download")
args = parser.parse_args()

json_data = {
    'token' : api_key,
    'anonymous' : args.anon,
    'submission' : [
        {
            'url' : args.url,
            'threat' : args.threat,
            'tags' : args.tags
        }
    ]
}
headers = {
    'Content-Type'  :   'application/json',
    'user-agent' : 'URLhaus Python Submission Script'
}
        
r = requests.post(url, json=json_data, timeout=15, headers=headers)
print("Submission status: " + r.text)
