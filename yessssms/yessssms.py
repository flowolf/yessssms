#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:36:14 2017

@author: Florian Klien <flowolf@klienux.org>

Send SMS via yesss.at web interface with your yesss login and password
"""

#import sys
from __future__ import print_function
from builtins import input
import requests
import argparse
try:
    from BeautifulSoup import BeautifulSoup as bs
except ImportError:
    from bs4 import BeautifulSoup as bs

YESSS_NUMBER = "0681XXXXXXXXXX"
YESSS_PASSWD = "YOUR_SECRET_YESSS_WEBLOGIN"
to_number = ""
# alternatively import pass and number from external file
try:
    from secrets import *
except:
    pass

login_url="https://www.yesss.at/kontomanager.at/index.php"
logout_url="https://www.yesss.at/kontomanager.at/index.php?dologout=2"
kontomanager="https://www.yesss.at/kontomanager.at/kundendaten.php"
websms_url = "https://www.yesss.at/kontomanager.at/websms_send.php"
parser = argparse.ArgumentParser()
parser.add_argument("number", help="Send SMS to this number")
parser.add_argument("-m", "--message", default="", help="The text message for the SMS")
args = parser.parse_args()

#print(args.message)
logindata={'login_rufnummer': YESSS_NUMBER, 'login_passwort': YESSS_PASSWD}
message = args.message
to_number = args.number
if len(args.message) == 0:
    # read message from stdin
    print("message empty...")
    message = "test message 123"
    message = input("Please enter a message: ")[:160]

print("number: " + to_number)
print("message: " + message)


with requests.Session() as s:
    req = s.post(login_url, data=logindata)
    req = s.get(kontomanager)
#    print(req)
#    print(req.content)
    phtml = bs(req.content,"html.parser")
    balance = phtml.find('div',attrs={'class':'bar-label-right'}).text
    balance = balance[-len(balance)+balance.rfind(':')+2:].strip()
    print("Balance: {}".format(balance))

    sms_data = {'to_nummer': to_number, 'nachricht': message}
    #req = s.post(websms_url,data=sms_data)



    s.get(logout_url)
