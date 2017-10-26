#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Send SMS via yesss.at web interface with your yesss login and password """


#
# @author: Florian Klien <flowolf@klienux.org>
#

import requests
#import sys
#from __future__ import print_function
#from builtins import input
#import argparse
# try:
#     from BeautifulSoup import BeautifulSoup as bs
# except ImportError:
#     from bs4 import BeautifulSoup as bs

_LOGIN_URL="https://www.yesss.at/kontomanager.at/index.php"
_LOGOUT_URL="https://www.yesss.at/kontomanager.at/index.php?dologout=2"
_KONTOMANAGER_URL="https://www.yesss.at/kontomanager.at/kundendaten.php"
_WEBSMS_URL = "https://www.yesss.at/kontomanager.at/websms_send.php"

YESSS_LOGIN = None # normally your phone number
YESSS_PASSWD = None # your password

# alternatively import pass and number from external file
try:
    from secrets import *
except:
    pass

class NoRecipientError(ValueError):
    pass

class EmptyMessageError(ValueError):
    pass

class YesssSMS():
    def __init__( self, yesss_login=YESSS_LOGIN, yesss_pw=YESSS_PASSWD ):
        self._login_url=_LOGIN_URL
        self._logout_url=_LOGOUT_URL
        self._kontomanager=_KONTOMANAGER_URL
        self._websms_url = _WEBSMS_URL
        self._logindata={ 'login_rufnummer': yesss_login,
                          'login_passwort': yesss_pw}

    def send_sms(self, to, message):
        if to == None or to == "":
            raise NoRecipientError("recipient number missing")
        if type(to) != str:
            raise ValueError("str expected as recipient number")
        if len(message) == 0:
            raise EmptyMessageError("message is empty")

        with requests.Session() as s:
            req = s.post(self._login_url, data=self._logindata)
            # TODO check for successful login
            sms_data = {'to_nummer': to, 'nachricht': message}
            req = s.post(self._websms_url, data=sms_data)
            s.get(self._logout_url)

# if __name__ == "__main__":
#     pass
