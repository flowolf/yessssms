#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Send SMS via yesss.at web interface with your yesss login and password """
#
# @author: Florian Klien <flowolf@klienux.org>
#
# pylint not amused about package name
# pylint: disable-msg=C0103

from contextlib import suppress

import requests

from YesssSMS.const import VERSION

_LOGIN_URL = "https://www.yesss.at/kontomanager.at/index.php"
_LOGOUT_URL = "https://www.yesss.at/kontomanager.at/index.php?dologout=2"
_KONTOMANAGER_URL = "https://www.yesss.at/kontomanager.at/kundendaten.php"
_WEBSMS_URL = "https://www.yesss.at/kontomanager.at/websms_send.php"

# yesss.at responds with HTTP 200 on non successful login
_LOGIN_ERROR_STRING = "<strong>Login nicht erfolgreich"
_LOGIN_LOCKED_MESS = "Wegen 3 ungültigen Login-Versuchen ist Ihr Account für \
eine Stunde gesperrt."
_LOGIN_LOCKED_MESS_ENG = "because of 3 failed login-attempts, your account \
has been suspended for one hour"
_UNSUPPORTED_CHARS_STRING = "<strong>Achtung:</strong> Ihre SMS konnte nicht \
versendet werden, da sie folgende ungültige Zeichen enthält:"
_SMS_SENDING_SUCCESSFUL_STRING = ">Ihre SMS wurde erfolgreich verschickt!<"
YESSS_LOGIN = None  # normally your phone number
YESSS_PASSWD = None  # your password

# alternatively import passwd and number from external file
with suppress(ImportError):
    from secrets import YESSS_LOGIN, YESSS_PASSWD

class YesssSMS():
    """YesssSMS class for sending SMS via yesss.at website"""
    class NoRecipientError(ValueError):
        """empty recipient"""
        pass

    class EmptyMessageError(ValueError):
        """empty message"""
        pass

    class LoginError(ValueError):
        """login credentials not accepted"""
        pass

    class AccountSuspendedError(LoginError):
        """too many failed login tries, account suspended for one hour"""
        pass

    class SMSSendingError(RuntimeError):
        """error during sending"""
        pass

    class UnsupportedCharsError(ValueError):
        """yesss.at refused characters in message"""
        pass

    def __init__(self, yesss_login=YESSS_LOGIN, yesss_pw=YESSS_PASSWD):
        self._version = VERSION
        self._login_url = _LOGIN_URL
        self._logout_url = _LOGOUT_URL
        self._kontomanager = _KONTOMANAGER_URL
        self._websms_url = _WEBSMS_URL
        self._suspended = False
        self._logindata = {'login_rufnummer': yesss_login,
                           'login_passwort': yesss_pw}

    def _login(self, session, get_request=False):
        req = session.post(self._login_url, data=self._logindata)
        if _LOGIN_ERROR_STRING in req.text or \
                req.status_code == 403 or \
                req.url == _LOGIN_URL:
            err_mess = "YesssSMS: login failed, username or password wrong"

            if _LOGIN_LOCKED_MESS in req.text:
                err_mess += ", page says: " + _LOGIN_LOCKED_MESS_ENG
                self._suspended = True
                raise self.AccountSuspendedError(err_mess)
            raise self.LoginError(err_mess)

        self._suspended = False  # login worked

        return (session, req) if get_request else session

    def account_is_suspended(self):
        """return if account is suspended"""
        return self._suspended

    def login_data_valid(self):
        """check for working login data"""
        login_working = False
        try:
            with self._login(requests.Session()) as sess:
                sess.get(self._logout_url)
        except self.LoginError:
            pass
        else:
            login_working = True
        return login_working

    def send(self, recipient, message):
        """send a SMS"""
        if self._logindata['login_rufnummer'] is None or \
                self._logindata['login_passwort'] is None:
            err_mess = "YesssSMS: Login data required"
            raise self.LoginError(err_mess)
        if not recipient:
            raise self.NoRecipientError("YesssSMS: recipient number missing")
        if not isinstance(recipient, str):
            raise ValueError("YesssSMS: str expected as recipient number")
        if not message:
            raise self.EmptyMessageError("YesssSMS: message is empty")

        with self._login(requests.Session()) as sess:

            sms_data = {'to_nummer': recipient, 'nachricht': message}
            req = sess.post(self._websms_url, data=sms_data)

            if not (req.status_code == 200 or req.status_code == 302):
                raise self.SMSSendingError("YesssSMS: error sending SMS")

            if _UNSUPPORTED_CHARS_STRING in req.text:
                raise self.UnsupportedCharsError(
                    "YesssSMS: message contains unsupported character(s)")

            if not _SMS_SENDING_SUCCESSFUL_STRING in req.text:
                raise self.SMSSendingError("YesssSMS: error sending SMS")

            sess.get(self._logout_url)

    def version(self):
        """get version of YesssSMS package"""
        return self._version

# if __name__ == "__main__":
#     pass
