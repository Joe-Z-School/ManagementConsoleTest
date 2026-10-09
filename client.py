#!/usr/bin/env python3

from __future__ import print_function

import requests
import json
import time
import base64
import jsonpickle
import random
import argparse


def doListStories(addr, debug=False):

    # Headers for http request
    headers = {'content-type': 'application/json'}

    # Here is where the logic of what to pass to the server resides
    x = 0

    # send http request receive response
    storyUrl = addr + '/api/listStories'
    response = requests.post(storyUrl, data=x, headers=headers)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))


def doCountWords(addr, debug=False):

    headers = {'content-type': 'application/json'}

    # Data to be passed
    data = 0
  
    # send http request with image and receive response
    countUrl = addr + "/api/countWords"
    response = requests.post(countUrl, headers=headers)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))


def doWordSearch(addr, debug=False):
    headers = {'content-type': 'application/json'}
    searchUrl = addr + "/api/wordSearch"

    # Data to be passed
    data = 0
  
    response = requests.post(dot_url, data=data, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))



def doGetModifiedDate(addr, debug=False):
    # Prepare the headers
    headers = {'content-type': 'application/json'}

    # Data to be passed
    data = 0

    # send http request with image and receive response
    modifiedUrl = addr + '/api/getModifiedDate'
    response = requests.post(image_url, data=data, headers=headers)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))



# ---------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------

parser = argparse.ArgumentParser(
    description='REST client for testing a management console log detailing application'
)

parser.add_argument(
    'host',
    help='IP address or hostname of the REST server'
)

parser.add_argument(
    '-p', '--port',
    type=int,
    default=5000,
    help='Server port (default: 5000)'
)

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help='Print the response from the server'
)

args = parser.parse_args()


# ---------------------------------------------------------
# Build server address
# ---------------------------------------------------------

addr = f"http://{args.host}:{args.port}"

print(f"Running server {addr}")


# ---------------------------------------------------------
# Perform requested operation
# ---------------------------------------------------------

if x == '':
    doListStories(addr, debug=args.debug)


elif x == '':
    doCountWords(addr, debug=args.debug)


elif x == '':
    doWordSearch(addr, debug=args.debug)


elif x == '':
    doGetModifiedDate(addr, debug=args.debug)
