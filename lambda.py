#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import urllib2

def getprice():
    response = urllib2.urlopen('https://blockchain.info/q/24hrprice')
    data = response.read()
    response.close()
    return data

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Bitcoinpreis",
            'content': "Bitcoin Fan - " + output
        },
        'shouldEndSession': True
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.01',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

def get_response():

    session_attributes = {}
    card_title = "Bitcoinpreis"
    speech_output = "Der aktuelle Bitcoinpreis ist "+getprice()+" US-Dollar"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output))

def get_help_response():

    session_attributes = {}
    card_title = "Bitcoinpreis Hilfe"
    speech_output = "Ich kann dir den aktuellen Bitcoinpreis nennen, wenn du mich danach fragst."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output))

# --------------- Events ------------------

def on_launch(launch_request, session):
    return get_response()

def on_intent(intent_request, session):

    intent_name = intent_request['intent']['name']

    if intent_name == "BitcoinIntent":
        return get_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    raise ValueError("Invalid intent")

# --------------- Main handler ------------------

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
