#!/usr/bin/env python3

from __future__ import print_function

import requests
import json
import time
import random
import argparse


def doListStories(addr, debug=False):

    # send http request receive response
    storyUrl = addr + '/api/listStories'
    response = requests.post(storyUrl, json={}, timeout=10)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))

    return response.json()


def doCountWords(addr, filename, debug=False):
    countUrl = addr + '/api/countWords'

    # Filename to be requested count for
    data = {"filename": filename}

    response = requests.post(countUrl, json=data, timeout=10)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))

    return response.json()


def doWordSearch(addr, filename, word, debug=False):
    searchUrl = addr + "/api/wordSearch"

    # Data to be passed
    data = {"filename": filename, "word": word}

    response = requests.post(searchUrl, json=data, timeout=10)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))

    return response.json()



def doGetModifiedDate(addr, filename, debug=False):
    modifiedUrl = addr + '/api/getModifiedDate'

    data = {"filename": filename}
    response = requests.post(modifiedUrl, json=data, timeout=10)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))

    return response.json()

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

filename = ''
word = ''

if x == '':
    doListStories(addr, debug=args.debug)


elif x == '':
    doCountWords(addr, filename, debug=args.debug)


elif x == '':
    doWordSearch(addr, filename, word, debug=args.debug)


elif x == '':
    doGetModifiedDate(addr, filename, debug=args.debug)
