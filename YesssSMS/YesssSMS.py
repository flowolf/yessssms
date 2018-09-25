#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Send SMS via yesss.at web interface with your yesss login and password """
#from __future__ import print_function
#
# @author: Florian Klien <flowolf@klienux.org>
#
from YesssSMS.const import VERSION
import requests
# import sys
# from builtins import input
# import argparse
# try:
#     from BeautifulSoup import BeautifulSoup as bs
# except ImportError:
#     from bs4 import BeautifulSoup as bs

_LOGIN_URL = "https://www.yesss.at/kontomanager.at/index.php"
_LOGOUT_URL = "https://www.yesss.at/kontomanager.at/index.php?dologout=2"
_KONTOMANAGER_URL = "https://www.yesss.at/kontomanager.at/kundendaten.php"
_WEBSMS_URL = "https://www.yesss.at/kontomanager.at/websms_send.php"

# yesss.at responds with HTTP 200 on non successful login
_LOGIN_ERROR_STRING = "<strong>Login nicht erfolgreich"
_LOGIN_LOCKED_MESS = "Wegen 3 ungültigen Login-Versuchen ist Ihr Account für eine Stunde gesperrt."
_UNSUPPORTED_CHARS_STRING = "<strong>Achtung:</strong> Ihre SMS konnte nicht versendet werden, da sie folgende ungültige Zeichen enthält:"
YESSS_LOGIN = None # normally your phone number
YESSS_PASSWD = None # your password

# alternatively import pass and number from external file
try:
    from secrets import YESSS_LOGIN, YESSS_PASSWD
except:
    pass

class NoRecipientError(ValueError):
    pass

class EmptyMessageError(ValueError):
    pass

class LoginError(ValueError):
    pass

class SMSSendingError(RuntimeError):
    pass

class UnsupportedCharsError(ValueError):
    pass

class YesssSMS():
    def __init__( self, yesss_login=YESSS_LOGIN, yesss_pw=YESSS_PASSWD ):
        self._version = VERSION
        self._login_url = _LOGIN_URL
        self._logout_url = _LOGOUT_URL
        self._kontomanager = _KONTOMANAGER_URL
        self._websms_url = _WEBSMS_URL
        self._logindata = { 'login_rufnummer': yesss_login,
                            'login_passwort': yesss_pw}

    def _login(self, session, get_request=False):
        r = session.post(self._login_url, data=self._logindata)
        if _LOGIN_ERROR_STRING in r.text or \
                r.status_code == 403 or \
                r.url == _LOGIN_URL:
            err_mess = "YesssSMS: login failed, username or password wrong"
            if _LOGIN_LOCKED_MESS in r.text:
                err_mess += ", page says: " + _LOGIN_LOCKED_MESS
            raise LoginError(err_mess)
        if get_request:
            #s.get(self._logout_url)
            return (session, r)
        else:
            return session

    def send(self, to, message):
        if self._logindata['login_rufnummer'] == None or \
                self._logindata['login_passwort'] == None:
            err_mess = "YesssSMS: Login data required"
            raise LoginError(err_mess)
        if to == None or to == "":
            raise NoRecipientError("YesssSMS: recipient number missing")
        if type(to) != str:
            raise ValueError("YesssSMS: str expected as recipient number")
        if len(message) == 0:
            raise EmptyMessageError("YesssSMS: message is empty")

        with self._login(requests.Session()) as s:

            sms_data = {'to_nummer': to, 'nachricht': message}
            r = s.post(self._websms_url, data=sms_data)

            if r.status_code == 403 or r.status_code == 404:
                raise SMSSendingError("YesssSMS: error sending SMS")
            if _UNSUPPORTED_CHARS_STRING in r.text:
                raise UnsupportedCharsError("YesssSMS: message contains unsupported character(s)")

            s.get(self._logout_url)

# if __name__ == "__main__":
#     pass
